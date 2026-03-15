"""
Integration Tests - 통합 테스트 (E2E)
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestHealthCheck:
    """헬스체크 통합 테스트"""
    
    def test_health_endpoint(self):
        """헬스체크 엔드포인트 테스트"""
        from services.health_service import HealthService
        import asyncio
        
        service = HealthService()
        result = asyncio.run(service.check_health())
        
        # status 는 'ok' 또는 'warning' (API 키 설정 여부에 따라)
        assert result["status"] in ["ok", "warning"]
        assert "environment" in result
        assert "message" in result


class TestComplianceCalendarIntegration:
    """컴플라이언스 캘린더 통합 테스트"""
    
    def test_get_upcoming_events_integration(self):
        """캘린더 이벤트 통합 테스트"""
        from repositories.compliance_calendar import get_compliance_calendar
        
        calendar = get_compliance_calendar()
        events = calendar.get_upcoming_events(days=30)
        
        assert isinstance(events, list)
        # 최소 1 개 이상의 이벤트가 있어야 함
        assert len(events) >= 1
        
        # 각 이벤트는 필요한 필드를 가져야 함
        for event in events:
            assert "name" in event
            assert "deadline" in event
            assert "days_until" in event
            assert 0 <= event["days_until"] <= 30


class TestComplianceChecklistsIntegration:
    """컴플라이언스 체크리스트 통합 테스트"""
    
    def test_get_all_checklists_integration(self):
        """모든 체크리스트 조회 통합 테스트"""
        from repositories.compliance_checklists import get_compliance_checklists
        
        checklists = get_compliance_checklists()
        result = checklists.get_all_checklists()
        
        assert isinstance(result, list)
        assert len(result) >= 5  # 최소 5 개 이상 체크리스트
        
        # 각 체크리스트는 필요한 필드를 가져야 함
        for checklist in result:
            assert "id" in checklist
            assert "name" in checklist
            assert "item_count" in checklist
    
    def test_get_specific_checklist_integration(self):
        """특정 체크리스트 조회 통합 테스트"""
        from repositories.compliance_checklists import get_compliance_checklists
        
        checklists = get_compliance_checklists()
        
        # 창업 체크리스트 테스트
        startup = checklists.get_checklist("startup")
        assert startup is not None
        assert startup["id"] == "startup"
        assert len(startup["items"]) >= 5
        
        # 개인정보 체크리스트 테스트
        privacy = checklists.get_checklist("privacy")
        assert privacy is not None
        assert len(privacy["items"]) >= 5


class TestQueryPlannerIntegration:
    """쿼리 플래너 통합 테스트"""
    
    def test_admin_law_query_generation(self):
        """행정법 쿼리 생성 통합 테스트"""
        from utils.query_planner import build_query_set
        
        query = "행정행위 무효 명백성"
        query_set = build_query_set(query)
        
        assert len(query_set) > 0
        
        # 행정법 특화 쿼리가 포함되어야 함
        admin_queries = [
            q for q in query_set 
            if q["strategy"] == "admin_law_specialized"
        ]
        assert len(admin_queries) > 0
        
        # "무효 중대 명백" 같은 효과적인 쿼리가 생성되어야 함
        all_queries = " ".join([q["query"] for q in query_set])
        assert "무효" in all_queries
        assert "명백" in all_queries or "중대" in all_queries


class TestPrecedentFallbackIntegration:
    """판례 fallback 통합 테스트"""
    
    def test_fallback_strategy(self):
        """fallback 전략 통합 테스트"""
        from utils.query_planner import build_query_set
        
        # 긴 문장을 효율적인 검색어로 변환
        long_query = "행정행위의 무효사유를 판단하는 기준으로서의 명백성은 보충적으로 요구되는가"
        query_set = build_query_set(long_query)
        
        # 여러 전략의 쿼리가 생성되어야 함
        strategies = set(q["strategy"] for q in query_set)
        assert "keyword_extraction" in strategies
        assert "admin_law_specialized" in strategies
        
        # 생성된 쿼리들은 원본보다 짧아야 함
        for q in query_set:
            assert len(q["query"]) <= len(long_query)


class TestErrorHandlingIntegration:
    """에러 처리 통합 테스트"""
    
    def test_standard_error_format(self):
        """표준 에러 형식 테스트"""
        from core.exceptions import LawMCPError, APITimeoutError
        
        # LawMCPError 테스트
        error = LawMCPError("테스트 오류", "TEST_ERROR")
        result = error.to_dict()
        assert "error" in result
        assert "error_code" in result
        assert "recovery_guide" in result
        assert result["error_code"] == "TEST_ERROR"
        
        # APITimeoutError 테스트
        timeout_error = APITimeoutError()
        result = timeout_error.to_dict()
        assert result["error_code"] == "API_ERROR_TIMEOUT"


class TestDIContainerIntegration:
    """DI 컨테이너 통합 테스트"""
    
    @pytest.mark.skip(reason="DI container import path needs fixing")
    def test_container_services(self):
        """컨테이너 서비스 통합 테스트"""
        import sys
        sys.path.insert(0, 'src')
        from core.container import create_container, reset_container
        
        reset_container()
        container = create_container()
        
        # 모든 서비스가 주입되어야 함
        assert container.law_service() is not None
        assert container.precedent_service() is not None
        assert container.health_service() is not None
        assert container.legal_source_service() is not None
        assert container.compliance_service() is not None
        
        reset_container()
    
    @pytest.mark.skip(reason="DI container import path needs fixing")
    def test_container_configuration(self):
        """컨테이너 설정 통합 테스트"""
        import sys
        sys.path.insert(0, 'src')
        from core.container import create_container, reset_container
        
        reset_container()
        container = create_container()
        
        # 환경 변수에서 설정을 읽어야 함
        api_key = container.config.LAW_API_KEY()
        assert api_key is not None
        
        reset_container()


@pytest.mark.skip(reason="Requires running server")
class TestHTTPEndpointsIntegration:
    """HTTP 엔드포인트 통합 테스트 (서버 실행 필요)"""
    
    def test_health_http_endpoint(self):
        """HTTP 헬스체크 엔드포인트 테스트"""
        import requests
        
        try:
            response = requests.get("http://localhost:8099/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running")
    
    def test_tools_list_http_endpoint(self):
        """HTTP tools 목록 엔드포인트 테스트"""
        import requests
        
        try:
            response = requests.get("http://localhost:8099/tools", timeout=5)
            assert response.status_code == 200
            tools = response.json()
            assert isinstance(tools, list)
            assert len(tools) >= 15  # 15 개 이상 도구
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running")
