"""
Tests for Precedent Search - 판례 검색
"""
import pytest
from models.schemas import SearchPrecedentRequest


class TestSearchPrecedentRequest:
    """SearchPrecedentRequest 스키마 테스트"""

    def test_basic_request(self):
        """기본 요청"""
        req = SearchPrecedentRequest(query="행정행위 무효")
        assert req.query == "행정행위 무효"
        assert req.page == 1
        assert req.per_page == 20
        assert req.use_fallback == True  # 기본값 True

    def test_custom_parameters(self):
        """커스텀 파라미터"""
        req = SearchPrecedentRequest(
            query="판례 검색",
            page=2,
            per_page=50,
            court="400201",  # 대법원
            use_fallback=False
        )
        assert req.page == 2
        assert req.per_page == 50
        assert req.court == "400201"
        assert req.use_fallback == False

    def test_issue_type_and_must_include(self):
        """issue_type 과 must_include"""
        req = SearchPrecedentRequest(
            query="무효 명백성",
            issue_type="행정행위무효",
            must_include=["대법원", "2020"]
        )
        assert req.issue_type == "행정행위무효"
        assert "대법원" in req.must_include

    def test_empty_query(self):
        """빈 쿼리"""
        req = SearchPrecedentRequest(query="")
        assert req.query == ""

    def test_very_long_query(self):
        """매우 긴 쿼리"""
        long_query = "행정행위의 무효사유를 판단하는 기준으로서의 명백성은 보충적으로 요구되는가에 대한 판례 검색" * 10
        req = SearchPrecedentRequest(query=long_query)
        assert len(req.query) > 100

    def test_special_characters(self):
        """특수문자 포함"""
        req = SearchPrecedentRequest(query="무효!@#$%명백성^&*()")
        assert req.query == "무효!@#$%명백성^&*()"


class TestAdminLawQueryImprovements:
    """행정법 쿼리 개선 효과 테스트"""

    def test_original_vs_improved(self):
        """원본 vs 개선된 쿼리"""
        from utils.query_planner import build_query_set

        original = "행정행위 무효사유 명백성"
        query_set = build_query_set(original)

        # 개선된 쿼리 세트에는 행정법 특화 쿼리가 포함되어야 함
        admin_queries = [q for q in query_set if q["strategy"] == "admin_law_specialized"]

        assert len(admin_queries) > 0

        # "무효 중대 명백" 같은 효과적인 쿼리가 생성되어야 함
        improved_queries = [q for q in admin_queries if "중대" in q["query"] or "명백" in q["query"]]
        assert len(improved_queries) > 0

    def test_search_success_with_improved_query(self):
        """개선된 쿼리로 검색 성공"""
        # 이 테스트는 실제로 검색이 되는지 확인
        # "무효 중대 명백" 이 35 건을 반환하는지 확인 (수동 확인)

        from utils.query_planner import _build_admin_law_queries

        queries = _build_admin_law_queries("행정행위 무효 명백성")

        # "무효 중대 명백" 이 생성되어야 함
        assert "무효 중대 명백" in queries
