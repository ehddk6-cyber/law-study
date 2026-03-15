"""
Tests for Fallback Strategy - 다단계 fallback 전략
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.query_planner import build_query_set, expand_date_range_stepwise


class TestFallbackStrategy:
    """Fallback 전략 테스트"""

    def test_query_plan_generation(self):
        """쿼리 플랜 생성 테스트"""
        query = "행정행위 무효 명백성"
        query_set = build_query_set(query)

        # 최소 2 개 이상의 전략이 포함되어야 함
        assert len(query_set) >= 2

        # 원본 쿼리가 포함되어야 함
        original_queries = [q for q in query_set if q["strategy"] == "keyword_extraction"]
        assert len(original_queries) > 0

        # 행정법 특화 쿼리가 포함되어야 함
        admin_queries = [q for q in query_set if q["strategy"] == "admin_law_specialized"]
        assert len(admin_queries) > 0

    def test_fallback_steps(self):
        """Fallback 단계 테스트"""
        # Step A: 원본
        # Step B: 키워드 추출 + 동의어 확장
        # Step C: 날짜 범위 확장
        # Step D: 단일 키워드

        query_set = build_query_set("행정행위 무효 명백성")
        strategies = [q["strategy"] for q in query_set]

        # 다양한 전략이 포함되어야 함
        assert "keyword_extraction" in strategies
        assert "admin_law_specialized" in strategies


class TestDateRangeExpansion:
    """날짜 범위 확장 테스트"""

    def test_expand_to_10_years(self):
        """10 년으로 확장"""
        date_from, date_to = expand_date_range_stepwise("20210101", "20260101", step=1)
        assert date_from is not None
        assert date_to is not None

    def test_expand_to_all(self):
        """전체 기간으로 확장"""
        date_from, date_to = expand_date_range_stepwise("20210101", "20260101", step=2)
        assert date_from is None
        assert date_to is None


class TestQuerySetStrategies:
    """쿼리 세트 전략 테스트"""

    def test_synonym_expansion_count(self):
        """동의어 확장 수 테스트"""
        query_set = build_query_set("무효 명백성")

        # 동의어 확장이 여러 개 생성되어야 함
        synonym_queries = [q for q in query_set if "synonym" in q["strategy"]]
        assert len(synonym_queries) > 0

    def test_admin_law_specialized_queries(self):
        """행정법 특화 쿼리 테스트"""
        query_set = build_query_set("행정행위 무효 하자")

        admin_queries = [q for q in query_set if q["strategy"] == "admin_law_specialized"]

        # 행정법 특화 쿼리가 생성되어야 함
        assert len(admin_queries) > 0

        # "무효 중대 명백" 같은 조합이 포함되어야 함
        all_admin_text = " ".join([q["query"] for q in admin_queries])
        assert "무효" in all_admin_text


class TestPrecedentRepositoryFallback:
    """판례 저장소 fallback 테스트 (모의)"""

    def test_fallback_function_exists(self):
        """fallback 함수 존재 확인"""
        from utils.query_planner import build_query_set

        # build_query_set 함수가 존재해야 함
        assert build_query_set is not None

    def test_fallback_parameters(self):
        """fallback 파라미터 확인"""
        # build_query_set 이 issue_type, must_include 를 받아야 함
        import inspect
        sig = inspect.signature(build_query_set)
        params = list(sig.parameters.keys())

        assert "issue_type" in params
        assert "must_include" in params


class TestFallbackIntegration:
    """Fallback 통합 테스트 (API 키 필요)"""

    @pytest.mark.integration
    def test_real_fallback_search(self):
        """실제 fallback 검색 테스트"""
        # 이 테스트는 실제 API 호출이 필요하므로 integration 마커로 구분
        # 실행하려면: pytest -m integration
        pytest.skip("Integration test requires API key")


class TestQueryPlanPriority:
    """쿼리 플랜 우선순위 테스트"""

    def test_priority_sorting(self):
        """우선순위 정렬 테스트"""
        query_set = build_query_set("행정행위 무효 명백성")

        priorities = [q["priority"] for q in query_set]
        assert priorities == sorted(priorities), "우선순위 순으로 정렬되어야 함"

    def test_priority_1_queries(self):
        """우선순위 1 쿼리 테스트"""
        query_set = build_query_set("행정행위 무효 명백성")

        priority_1 = [q for q in query_set if q["priority"] == 1]
        assert len(priority_1) > 0

        # 키워드 추출과 행정법 특화 쿼리가 포함되어야 함
        strategies = [q["strategy"] for q in priority_1]
        assert "keyword_extraction" in strategies
        assert "admin_law_specialized" in strategies
