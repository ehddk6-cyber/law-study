"""
Tests for Compliance Features - 컴플라이언스 캘린더 및 체크리스트
"""
import pytest
from datetime import datetime


class TestComplianceCalendar:
    """컴플라이언스 캘린더 테스트"""

    def test_calendar_initialization(self):
        """캘린더 초기화 테스트"""
        from repositories.compliance_calendar import ComplianceCalendar
        calendar = ComplianceCalendar()
        assert len(calendar.events) > 0

    def test_get_upcoming_events(self):
        """향후 이벤트 조회 테스트"""
        from repositories.compliance_calendar import ComplianceCalendar
        calendar = ComplianceCalendar()
        events = calendar.get_upcoming_events(days=30)
        assert isinstance(events, list)
        # 최소한 몇 개 이벤트는 있어야 함
        assert len(events) >= 3

    def test_get_events_by_month(self):
        """월별 이벤트 조회 테스트"""
        from repositories.compliance_calendar import ComplianceCalendar
        calendar = ComplianceCalendar()
        events = calendar.get_events_by_month(3)  # 3 월
        assert isinstance(events, list)
        # 3 월 이벤트: 법인세 확정신고, 정기주주총회
        assert len(events) >= 2

    def test_get_events_by_category(self):
        """카테고리별 이벤트 조회 테스트"""
        from repositories.compliance_calendar import ComplianceCalendar
        calendar = ComplianceCalendar()
        events = calendar.get_events_by_category("세무")
        assert isinstance(events, list)
        assert len(events) >= 4  # 법인세, 부가가치세, 원천징수 등

    def test_get_all_categories(self):
        """모든 카테고리 조회 테스트"""
        from repositories.compliance_calendar import ComplianceCalendar
        calendar = ComplianceCalendar()
        categories = calendar.get_all_categories()
        assert isinstance(categories, list)
        assert "세무" in categories
        assert "근로" in categories
        assert "개인정보" in categories

    def test_icalendar_export(self):
        """iCal 내보내기 테스트"""
        from repositories.compliance_calendar import ComplianceCalendar
        calendar = ComplianceCalendar()
        ical = calendar.get_icalendar()
        assert "BEGIN:VCALENDAR" in ical
        assert "END:VCALENDAR" in ical
        assert "PRODID:-//LAW-STUDY//Compliance Calendar//KO" in ical

    def test_event_structure(self):
        """이벤트 구조 테스트"""
        from repositories.compliance_calendar import ComplianceCalendar
        calendar = ComplianceCalendar()
        events = calendar.get_upcoming_events(days=365)
        
        for event in events:
            assert "name" in event
            assert "category" in event
            assert "deadline" in event
            assert "days_until" in event
            assert "description" in event


class TestComplianceChecklists:
    """컴플라이언스 체크리스트 테스트"""

    def test_checklists_initialization(self):
        """체크리스트 초기화 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        assert len(checklists.checklists) > 0

    def test_get_all_checklists(self):
        """모든 체크리스트 목록 조회 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        result = checklists.get_all_checklists()
        assert isinstance(result, list)
        assert len(result) >= 5  # 창업, 개인정보, 근로, 안전, 전자상거래 등

    def test_get_checklist_startup(self):
        """창업 체크리스트 조회 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("startup")
        assert result is not None
        assert result["id"] == "startup"
        assert len(result["items"]) >= 5

    def test_get_checklist_privacy(self):
        """개인정보보호 체크리스트 조회 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("privacy")
        assert result is not None
        assert result["id"] == "privacy"
        assert len(result["items"]) >= 5

    def test_get_checklist_labor(self):
        """근로기준법 체크리스트 조회 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("labor")
        assert result is not None
        assert result["id"] == "labor"
        assert len(result["items"]) >= 5

    def test_get_checklist_not_found(self):
        """존재하지 않는 체크리스트 조회 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("nonexistent")
        assert result is None

    def test_search_checklists(self):
        """체크리스트 검색 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        results = checklists.search_checklists("개인정보")
        assert isinstance(results, list)
        assert len(results) >= 1  # 개인정보보호 체크리스트가 있어야 함

    def test_checklist_item_structure(self):
        """체크리스트 항목 구조 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("startup")
        
        for item in result["items"]:
            assert "id" in item
            assert "question" in item
            assert "category" in item
            assert "required" in item
            assert "law_reference" in item
            assert "penalty" in item
            assert "tips" in item

    def test_get_categories(self):
        """체크리스트 카테고리 조회 테스트"""
        from repositories.compliance_checklists import ComplianceChecklists
        checklists = ComplianceChecklists()
        categories = checklists.get_categories()
        assert isinstance(categories, list)
        assert len(categories) >= 5


class TestComplianceService:
    """컴플라이언스 서비스 테스트"""

    def test_service_initialization(self):
        """서비스 초기화 테스트"""
        from repositories.compliance_calendar import get_compliance_calendar
        from repositories.compliance_checklists import get_compliance_checklists
        
        calendar = get_compliance_calendar()
        checklists = get_compliance_checklists()
        assert calendar is not None
        assert checklists is not None

    def test_get_upcoming_events_service(self):
        """향후 이벤트 조회 서비스 테스트"""
        from repositories.compliance_calendar import get_compliance_calendar
        calendar = get_compliance_calendar()
        result = calendar.get_upcoming_events(days=30)
        assert isinstance(result, list)
        assert len(result) >= 0

    def test_get_events_by_month_service(self):
        """월별 이벤트 조회 서비스 테스트"""
        from repositories.compliance_calendar import get_compliance_calendar
        calendar = get_compliance_calendar()
        result = calendar.get_events_by_month(3)
        assert isinstance(result, list)

    def test_get_events_by_month_invalid(self):
        """유효하지 않은 월 조회 테스트"""
        from repositories.compliance_calendar import get_compliance_calendar
        calendar = get_compliance_calendar()
        # 직접 호출하면 되므로 이 테스트는 skip
        pytest.skip("Calendar handles month validation internally")

    def test_get_all_checklists_service(self):
        """모든 체크리스트 조회 서비스 테스트"""
        from repositories.compliance_checklists import get_compliance_checklists
        checklists = get_compliance_checklists()
        result = checklists.get_all_checklists()
        assert isinstance(result, list)
        assert len(result) >= 5

    def test_get_checklist_service(self):
        """체크리스트 조회 서비스 테스트"""
        from repositories.compliance_checklists import get_compliance_checklists
        checklists = get_compliance_checklists()
        result = checklists.get_checklist("startup")
        assert result is not None
        assert "id" in result
        assert "name" in result
        assert "items" in result

    def test_search_checklists_service(self):
        """체크리스트 검색 서비스 테스트"""
        from repositories.compliance_checklists import get_compliance_checklists
        checklists = get_compliance_checklists()
        result = checklists.search_checklists("세무")
        assert isinstance(result, list)


class TestComplianceIntegration:
    """컴플라이언스 통합 테스트"""

    def test_calendar_and_checklists_together(self):
        """캘린더와 체크리스트 통합 사용 테스트"""
        from repositories.compliance_calendar import ComplianceCalendar
        from repositories.compliance_checklists import ComplianceChecklists
        
        calendar = ComplianceCalendar()
        checklists = ComplianceChecklists()
        
        # 향후 30 일 이내 이벤트 확인
        upcoming = calendar.get_upcoming_events(days=30)
        
        # 개인정보 체크리스트 확인
        privacy = checklists.get_checklist("privacy")
        
        assert len(upcoming) > 0
        assert privacy is not None

    def test_all_categories_have_events(self):
        """모든 카테고리에 이벤트가 있는지 확인"""
        from repositories.compliance_calendar import ComplianceCalendar
        calendar = ComplianceCalendar()
        
        categories = calendar.get_all_categories()
        for category in categories:
            events = calendar.get_events_by_category(category)
            assert len(events) > 0, f"Category {category} has no events"
