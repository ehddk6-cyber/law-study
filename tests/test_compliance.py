"""
Tests for Compliance Features - 컴플라이언스 캘린더 및 체크리스트
"""
import pytest
from datetime import datetime

# Import directly (not through packages)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from repositories.compliance_calendar import ComplianceCalendar, get_compliance_calendar
from repositories.compliance_checklists import ComplianceChecklists, get_compliance_checklists


class TestComplianceCalendar:
    """컴플라이언스 캘린더 테스트"""

    def test_calendar_initialization(self):
        """캘린더 초기화 테스트"""
        calendar = ComplianceCalendar()
        assert len(calendar.events) > 0

    def test_get_upcoming_events(self):
        """향후 이벤트 조회 테스트"""
        calendar = ComplianceCalendar()
        events = calendar.get_upcoming_events(days=30)
        assert isinstance(events, list)
        assert len(events) >= 3

    def test_get_events_by_month(self):
        """월별 이벤트 조회 테스트"""
        calendar = ComplianceCalendar()
        events = calendar.get_events_by_month(3)
        assert isinstance(events, list)
        assert len(events) >= 2

    def test_get_events_by_category(self):
        """카테고리별 이벤트 조회 테스트"""
        calendar = ComplianceCalendar()
        events = calendar.get_events_by_category("세무")
        assert isinstance(events, list)
        assert len(events) >= 4

    def test_get_all_categories(self):
        """모든 카테고리 조회 테스트"""
        calendar = ComplianceCalendar()
        categories = calendar.get_all_categories()
        assert isinstance(categories, list)
        assert "세무" in categories
        assert "근로" in categories

    def test_icalendar_export(self):
        """iCal 내보내기 테스트"""
        calendar = ComplianceCalendar()
        ical = calendar.get_icalendar()
        assert "BEGIN:VCALENDAR" in ical
        assert "END:VCALENDAR" in ical

    def test_event_structure(self):
        """이벤트 구조 테스트"""
        calendar = ComplianceCalendar()
        events = calendar.get_upcoming_events(days=365)
        
        for event in events:
            assert "name" in event
            assert "category" in event
            assert "deadline" in event
            assert "days_until" in event


class TestComplianceChecklists:
    """컴플라이언스 체크리스트 테스트"""

    def test_checklists_initialization(self):
        """체크리스트 초기화 테스트"""
        checklists = ComplianceChecklists()
        assert len(checklists.checklists) > 0

    def test_get_all_checklists(self):
        """모든 체크리스트 목록 조회 테스트"""
        checklists = ComplianceChecklists()
        result = checklists.get_all_checklists()
        assert isinstance(result, list)
        assert len(result) >= 5

    def test_get_checklist_startup(self):
        """창업 체크리스트 조회 테스트"""
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("startup")
        assert result is not None
        assert result["id"] == "startup"
        assert len(result["items"]) >= 5

    def test_get_checklist_privacy(self):
        """개인정보보호 체크리스트 조회 테스트"""
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("privacy")
        assert result is not None
        assert len(result["items"]) >= 5

    def test_get_checklist_labor(self):
        """근로기준법 체크리스트 조회 테스트"""
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("labor")
        assert result is not None
        assert len(result["items"]) >= 5

    def test_get_checklist_not_found(self):
        """존재하지 않는 체크리스트 조회 테스트"""
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("nonexistent")
        assert result is None

    def test_search_checklists(self):
        """체크리스트 검색 테스트"""
        checklists = ComplianceChecklists()
        results = checklists.search_checklists("개인정보")
        assert isinstance(results, list)
        assert len(results) >= 1

    def test_checklist_item_structure(self):
        """체크리스트 항목 구조 테스트"""
        checklists = ComplianceChecklists()
        result = checklists.get_checklist("startup")
        
        for item in result["items"]:
            assert "id" in item
            assert "question" in item
            assert "law_reference" in item

    def test_get_categories(self):
        """체크리스트 카테고리 조회 테스트"""
        checklists = ComplianceChecklists()
        categories = checklists.get_categories()
        assert isinstance(categories, list)
        assert len(categories) >= 5


class TestComplianceService:
    """컴플라이언스 서비스 테스트"""

    def test_get_upcoming_events_service(self):
        """향후 이벤트 조회 서비스 테스트"""
        calendar = get_compliance_calendar()
        result = calendar.get_upcoming_events(days=30)
        assert isinstance(result, list)

    def test_get_all_checklists_service(self):
        """모든 체크리스트 조회 서비스 테스트"""
        checklists = get_compliance_checklists()
        result = checklists.get_all_checklists()
        assert isinstance(result, list)
        assert len(result) >= 5

    def test_get_checklist_service(self):
        """체크리스트 조회 서비스 테스트"""
        checklists = get_compliance_checklists()
        result = checklists.get_checklist("startup")
        assert result is not None
        assert "id" in result


class TestComplianceIntegration:
    """컴플라이언스 통합 테스트"""

    def test_calendar_and_checklists_together(self):
        """캘린더와 체크리스트 통합 사용 테스트"""
        calendar = ComplianceCalendar()
        checklists = ComplianceChecklists()
        
        upcoming = calendar.get_upcoming_events(days=30)
        privacy = checklists.get_checklist("privacy")
        
        assert len(upcoming) > 0
        assert privacy is not None
