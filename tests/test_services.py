"""
Tests for Services - 서비스 계층 테스트
"""
import pytest

# Check if DI container is available
try:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    from core.container import create_container, reset_container
    CONTAINER_AVAILABLE = True
except (ImportError, Exception):
    CONTAINER_AVAILABLE = False


class TestPrecedentService:
    """PrecedentService 테스트"""

    def test_service_initialization(self, container):
        """서비스 초기화 테스트"""
        if not hasattr(container, 'precedent_service'):
            pytest.skip("DI container not fully configured")
        service = container.precedent_service()
        assert service is not None
        assert service.repository is not None

    def test_infer_issue_type_admin_law(self):
        """행정법 issue_type 추론"""
        import sys
        sys.path.insert(0, 'src')
        from services.precedent_service import PrecedentService
        issue = PrecedentService._infer_issue_type("행정행위 무효 명백성")
        assert issue == "행정행위무효"

    def test_infer_issue_type_songsonyogeon(self):
        """소송요건 issue_type 추론"""
        import sys
        sys.path.insert(0, 'src')
        from services.precedent_service import PrecedentService
        issue = PrecedentService._infer_issue_type("원고적격 피고적격")
        assert issue == "소송요건"

    def test_infer_issue_type_jaeryangwon(self):
        """재량권 issue_type 추론"""
        import sys
        sys.path.insert(0, 'src')
        from services.precedent_service import PrecedentService
        issue = PrecedentService._infer_issue_type("재량권 남용 일탈")
        assert issue == "재량권남용"

    def test_infer_issue_type_geunroja(self):
        """근로자성 issue_type 추론"""
        import sys
        sys.path.insert(0, 'src')
        from services.precedent_service import PrecedentService
        issue = PrecedentService._infer_issue_type("근로자성 프리랜서 지휘감독")
        assert issue == "근로자성"

    def test_infer_issue_type_unknown(self):
        """알 수 없는 쿼리"""
        import sys
        sys.path.insert(0, 'src')
        from services.precedent_service import PrecedentService
        issue = PrecedentService._infer_issue_type("오늘 날씨")
        assert issue is None

    def test_search_precedent_request_structure(self):
        """SearchPrecedentRequest 스키마 확인"""
        from models.schemas import SearchPrecedentRequest
        req = SearchPrecedentRequest(query="행정행위 무효")
        assert req.query == "행정행위 무효"
        assert req.page == 1
        assert req.per_page == 20
        assert req.use_fallback == True


class TestLawService:
    """LawService 테스트"""

    def test_service_initialization(self, container):
        """서비스 초기화 테스트"""
        service = container.law_service()
        assert service is not None

    def test_search_law_request_structure(self):
        """SearchLawRequest 스키마 확인"""
        from models.schemas import SearchLawRequest
        req = SearchLawRequest(query="민법")
        assert req.query == "민법"
        assert req.page == 1
        assert req.per_page == 10


class TestComplianceService:
    """ComplianceService 테스트"""

    def test_service_initialization(self, container):
        """서비스 초기화 테스트"""
        service = container.compliance_service()
        assert service is not None
        assert service.calendar is not None
        assert service.checklists is not None

    def test_get_upcoming_events(self, compliance_service):
        """향후 이벤트 조회 테스트"""
        result = compliance_service.get_upcoming_events(days=30)
        assert "total" in result
        assert "events" in result
        assert "period_days" in result

    def test_get_events_by_month(self, compliance_service):
        """월별 이벤트 조회 테스트"""
        result = compliance_service.get_events_by_month(month=3)
        assert "month" in result
        assert "events" in result

    def test_get_events_by_month_invalid(self, compliance_service):
        """유효하지 않은 월 조회 테스트"""
        result = compliance_service.get_events_by_month(month=13)
        assert "error" in result

    def test_get_all_categories(self, compliance_service):
        """카테고리 조회 테스트"""
        result = compliance_service.get_all_categories()
        assert "total" in result
        assert "categories" in result
        assert len(result["categories"]) > 0

    def test_get_all_checklists(self, compliance_service):
        """모든 체크리스트 조회 테스트"""
        result = compliance_service.get_all_checklists()
        assert "total" in result
        assert "checklists" in result
        assert len(result["checklists"]) >= 5

    def test_get_checklist_startup(self, compliance_service):
        """창업 체크리스트 조회 테스트"""
        result = compliance_service.get_checklist("startup")
        assert result is not None
        assert "id" in result
        assert "name" in result
        assert "items" in result
        assert len(result["items"]) >= 5

    def test_get_checklist_not_found(self, compliance_service):
        """존재하지 않는 체크리스트 조회 테스트"""
        result = compliance_service.get_checklist("nonexistent")
        assert "error" in result

    def test_search_checklists(self, compliance_service):
        """체크리스트 검색 테스트"""
        result = compliance_service.search_checklists(keyword="개인정보")
        assert "keyword" in result
        assert "results" in result
        assert len(result["results"]) >= 1


class TestLegalSourceService:
    """LegalSourceService 테스트"""

    def test_service_initialization(self, container):
        """서비스 초기화 테스트"""
        service = container.legal_source_service()
        assert service is not None

    def test_search_constitutional_request_structure(self):
        """SearchConstitutionalDecisionRequest 스키마 확인"""
        from models.schemas import SearchConstitutionalDecisionRequest
        req = SearchConstitutionalDecisionRequest(query="헌법 제 1 조")
        assert req.query == "헌법 제 1 조"
        assert req.page == 1
        assert req.per_page == 20


class TestHealthService:
    """HealthService 테스트"""

    def test_service_initialization(self, container):
        """서비스 초기화 테스트"""
        service = container.health_service()
        assert service is not None

    def test_check_health(self, health_service):
        """헬스체크 테스트"""
        import asyncio
        result = asyncio.run(health_service.check_health())
        assert "status" in result
        assert result["status"] == "ok"
        assert "environment" in result


class TestDIContainer:
    """DI 컨테이너 테스트"""

    def test_container_creation(self, test_config):
        """컨테이너 생성 테스트"""
        if not CONTAINER_AVAILABLE:
            pytest.skip("DI container not available")
        
        from core.container import create_container, reset_container
        
        reset_container()
        container = create_container()
        container.config.LAW_API_KEY.from_value(test_config["LAW_API_KEY"])
        
        assert container is not None
        assert container.config.LAW_API_KEY() == test_config["LAW_API_KEY"]
        
        reset_container()

    def test_container_singleton_services(self, container):
        """싱글톤 서비스 테스트"""
        if not CONTAINER_AVAILABLE:
            pytest.skip("DI container not available")
        
        health1 = container.health_service()
        health2 = container.health_service()
        # HealthService 는 Singleton
        assert health1 is health2

    def test_container_factory_services(self, container):
        """팩토리 서비스 테스트"""
        if not CONTAINER_AVAILABLE:
            pytest.skip("DI container not available")
        
        service1 = container.precedent_service()
        service2 = container.precedent_service()
        # Factory 는 인스턴스마다 새로 생성
        assert service1 is not service2
        assert type(service1) == type(service2)

    def test_container_reset(self, test_config):
        """컨테이너 리셋 테스트"""
        if not CONTAINER_AVAILABLE:
            pytest.skip("DI container not available")
        
        from core.container import create_container, reset_container, get_container
        
        # 컨테이너 생성
        reset_container()
        container1 = create_container()
        container1.config.LAW_API_KEY.from_value(test_config["LAW_API_KEY"])
        assert get_container() is container1
        
        # 리셋
        reset_container()
        
        # 새 컨테이너 생성
        container2 = create_container()
        assert get_container() is container2
        assert container1 is not container2
        
        # 정리
        reset_container()
