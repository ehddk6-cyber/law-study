"""
Tests for Query Planner - 검색 쿼리 생성 및 최적화
"""
import pytest
from utils.query_planner import (
    extract_keywords,
    expand_synonyms,
    build_query_set,
    _build_admin_law_queries,
    remove_stopwords,
    LEGAL_CORE_KEYWORDS,
    LEGAL_SYNONYMS,
)


class TestRemoveStopwords:
    """불용어 제거 테스트"""

    def test_remove_basic_stopwords(self):
        # 불용어는 공백으로 구분된 단어만 제거됨
        result = remove_stopwords("검색 해줘")
        assert "해줘" not in result

    def test_remove_separated_stopwords(self):
        result = remove_stopwords("것 입니다")
        assert "것" not in result

    def test_remove_legal_stopwords(self):
        result = remove_stopwords("행정행위가 무효인지 확인해줘")
        assert "행정행위" in result
        assert "무효" in result
        assert "확인해줘" not in result


class TestExtractKeywords:
    """키워드 추출 테스트"""

    def test_extract_admin_keywords(self, sample_keyword_tests):
        """행정법 키워드 추출 테스트"""
        for input_text, expected in sample_keyword_tests:
            result = extract_keywords(input_text)
            # 최소한 하나의 핵심 키워드는 포함되어야 함
            assert len(result) > 0, f"Input: {input_text}"
            # 핵심 키워드가 우선적으로 추출됨
            for exp in expected:
                if exp in LEGAL_CORE_KEYWORDS or any(c in exp for c in LEGAL_CORE_KEYWORDS):
                    assert exp in result or any(exp in r for r in result), \
                        f"Expected {exp} in {result} for input: {input_text}"

    def test_extract_priority_order(self):
        """핵심 키워드가 우선 추출되는지 테스트"""
        result = extract_keywords("행정행위의 무효사유는 중대하고 명백해야 한다")
        # 핵심 키워드가 먼저 나와야 함
        core_found = [k for k in result if any(c in k for c in LEGAL_CORE_KEYWORDS)]
        assert len(core_found) > 0

    def test_min_length_filter(self):
        """최소 길이 미만 키워드 필터링"""
        result = extract_keywords("이 가 을")
        assert len(result) == 0


class TestBuildAdminLawQueries:
    """행정법 특화 쿼리 생성 테스트"""

    def test_generate_from_long_query(self):
        """긴 문장에서 핵심 법리 추출"""
        queries = _build_admin_law_queries("행정행위 무효사유 명백성 보충적으로 요구된다")
        assert len(queries) > 0
        # "무효 명백성" 또는 "무효 중대 명백" 같은 조합이 포함되어야 함
        combined = " ".join(queries)
        assert "무효" in combined and ("명백" in combined or "중대" in combined)

    def test_juhaenghaengwi_muhyo(self):
        """행정행위 무효 관련 쿼리 생성"""
        queries = _build_admin_law_queries("행정행위 무효 하자 중대 명백")
        assert any("무효" in q for q in queries)
        assert any("명백" in q or "중대" in q for q in queries)

    def test_wongojeokgyeok(self):
        """원고적격 관련 쿼리 생성"""
        queries = _build_admin_law_queries("원고적격 피고적격 소송요건")
        assert any("원고적격" in q for q in queries)
        assert any("소송요건" in q for q in queries)

    def test_jaeryangwon(self):
        """재량권 관련 쿼리 생성"""
        # 재량권은 핵심 키워드로 인식되어야 함
        queries = _build_admin_law_queries("재량권 남용 일탈 한계")
        # 재량권이 감지되면 쿼리가 생성됨
        assert len(queries) > 0

    def test_jeongbogonggae(self):
        """정보공개 관련 쿼리 생성"""
        queries = _build_admin_law_queries("정보공개청구 비공개 사유")
        # 정보공개가 감지되면 쿼리가 생성됨
        assert len(queries) > 0

    def test_no_admin_keywords(self):
        """행정법 키워드 없으면 빈 리스트 반환"""
        queries = _build_admin_law_queries("오늘 날씨 어때")
        assert len(queries) == 0


class TestExpandSynonyms:
    """동의어 확장 테스트"""

    def test_expand_muhyo(self):
        """무효 동의어 확장"""
        result = expand_synonyms("행정행위 무효")
        # 무효 → 당연무효, 무효등확인, 무효확인
        assert any("당연무효" in r for r in result) or "행정행위 무효" in result

    def test_expand_myeongbakseong(self):
        """명백성 동의어 확장"""
        result = expand_synonyms("무효 명백성")
        # 명백성 → 중대성, 중대명백, 중대하고명백
        assert any("중대" in r for r in result) or "무효 명백성" in result

    def test_expand_cheobun(self):
        """처분 동의어 확장"""
        result = expand_synonyms("행정처분")
        assert any("공권력" in r or "행정결정" in r for r in result) or "행정처분" in result


class TestBuildQuerySet:
    """쿼리 세트 생성 테스트"""

    def test_build_complete_set(self):
        """완전한 쿼리 세트 생성"""
        query_set = build_query_set("행정행위 무효 명백성")
        assert len(query_set) > 0

        # 전략별 쿼리 포함
        strategies = [q["strategy"] for q in query_set]
        assert "keyword_extraction" in strategies
        assert "admin_law_specialized" in strategies

    def test_priority_order(self):
        """우선순위 순 정렬"""
        query_set = build_query_set("행정행위 무효 명백성")
        priorities = [q["priority"] for q in query_set]
        assert priorities == sorted(priorities)

    def test_must_include_combination(self):
        """must_include 와 결합"""
        query_set = build_query_set("행정행위 무효", must_include=["대법원"])
        combined_queries = [
            q for q in query_set if q["strategy"] == "must_include_combined"
        ]
        assert len(combined_queries) > 0
        assert any("대법원" in q["query"] for q in combined_queries)

    def test_exclude_filter(self):
        """exclude 필터 적용"""
        query_set = build_query_set("행정행위 무효", exclude=["민사"])
        for q in query_set:
            assert "민사" not in q["query"]


class TestAdminLawSpecialized:
    """행정법 특화 쿼리 심층 테스트"""

    def test_muhyo_myeongbak_combined(self):
        """무효 + 명백 조합"""
        queries = _build_admin_law_queries("무효 명백성")
        assert "무효 명백성" in queries or "무효 중대 명백" in queries

    def test_jungdaeseong_myeongbakseong(self):
        """중대성 + 명백성 조합"""
        queries = _build_admin_law_queries("중대성 명백성")
        assert "중대성 명백성" in queries or "중대 명백 하자" in queries

    def test_cheobunseong_gonggwonlyeokseong(self):
        """처분성 + 공권력성"""
        queries = _build_admin_law_queries("처분성 공권력성")
        assert "처분성 공권력성" in queries or "행정처분 소송대상" in queries

    def test_songsonyogeon(self):
        """소송요건 관련"""
        queries = _build_admin_law_queries("원고적격 피고적격")
        assert "원고적격 피고적격" in queries or "소송요건 당사자적격" in queries

    def test_jaeryangwon_namyong(self):
        """재량권 남용"""
        queries = _build_admin_law_queries("재량권 남용 일탈")
        # 재량권이 감지되면 쿼리가 생성되어야 함
        assert len(queries) > 0
        # 재량권 관련 쿼리가 포함되어야 함
        assert any("재량" in q for q in queries)


class TestEdgeCases:
    """에지 케이스 테스트"""

    def test_empty_input(self):
        """빈 입력"""
        assert extract_keywords("") == []
        assert _build_admin_law_queries("") == []

    def test_single_keyword(self):
        """단일 키워드"""
        result = extract_keywords("무효")
        assert "무효" in result

    def test_only_stopwords(self):
        """불용어만 입력"""
        result = extract_keywords("이 가 을")
        assert len(result) == 0

    def test_mixed_languages(self):
        """한영 혼합"""
        result = extract_keywords("행정행위 administrative act")
        assert "행정행위" in result
