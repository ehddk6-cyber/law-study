"""
Compliance Service - 컴플라이언스 서비스
"""
import asyncio
from typing import Optional, List
from ..repositories.compliance_calendar import get_compliance_calendar, ComplianceEvent
from ..repositories.compliance_checklists import get_compliance_checklists


class ComplianceService:
    """컴플라이언스 서비스"""

    def __init__(self):
        self.calendar = get_compliance_calendar()
        self.checklists = get_compliance_checklists()

    def get_upcoming_events(self, days: int = 30) -> dict:
        """향후 N 일 이내 컴플라이언스 이벤트 반환"""
        try:
            events = self.calendar.get_upcoming_events(days)
            return {
                "period_days": days,
                "total": len(events),
                "events": events
            }
        except Exception as e:
            return {
                "error": f"이벤트 조회 중 오류 발생: {str(e)}"
            }

    def get_events_by_month(self, month: int) -> dict:
        """특정 월의 이벤트 반환"""
        try:
            if not 1 <= month <= 12:
                return {"error": "월 (month) 은 1-12 사이여야 합니다."}

            events = self.calendar.get_events_by_month(month)
            return {
                "month": month,
                "total": len(events),
                "events": events
            }
        except Exception as e:
            return {
                "error": f"이벤트 조회 중 오류 발생: {str(e)}"
            }

    def get_events_by_category(self, category: str) -> dict:
        """특정 카테고리의 이벤트 반환"""
        try:
            events = self.calendar.get_events_by_category(category)
            return {
                "category": category,
                "total": len(events),
                "events": events
            }
        except Exception as e:
            return {
                "error": f"이벤트 조회 중 오류 발생: {str(e)}"
            }

    def get_all_categories(self) -> dict:
        """모든 카테고리 반환"""
        try:
            categories = self.calendar.get_all_categories()
            return {
                "total": len(categories),
                "categories": categories
            }
        except Exception as e:
            return {
                "error": f"카테고리 조회 중 오류 발생: {str(e)}"
            }

    def export_icalendar(self) -> dict:
        """iCal 형식 내보내기"""
        try:
            ical_content = self.calendar.get_icalendar()
            return {
                "format": "iCalendar",
                "content": ical_content
            }
        except Exception as e:
            return {
                "error": f"iCal 내보내기 중 오류 발생: {str(e)}"
            }

    def get_checklist(self, checklist_id: str) -> dict:
        """체크리스트 반환"""
        try:
            checklist = self.checklists.get_checklist(checklist_id)
            if not checklist:
                return {
                    "error": f"체크리스트 '{checklist_id}' 를 찾을 수 없습니다."
                }
            return checklist
        except Exception as e:
            return {
                "error": f"체크리스트 조회 중 오류 발생: {str(e)}"
            }

    def get_all_checklists(self) -> dict:
        """모든 체크리스트 목록 반환"""
        try:
            checklists = self.checklists.get_all_checklists()
            return {
                "total": len(checklists),
                "checklists": checklists
            }
        except Exception as e:
            return {
                "error": f"체크리스트 목록 조회 중 오류 발생: {str(e)}"
            }

    def search_checklists(self, keyword: str) -> dict:
        """체크리스트 검색"""
        try:
            results = self.checklists.search_checklists(keyword)
            return {
                "keyword": keyword,
                "total": len(results),
                "results": results
            }
        except Exception as e:
            return {
                "error": f"체크리스트 검색 중 오류 발생: {str(e)}"
            }

    def get_checklist_categories(self) -> dict:
        """체크리스트 카테고리 반환"""
        try:
            categories = self.checklists.get_categories()
            return {
                "total": len(categories),
                "categories": categories
            }
        except Exception as e:
            return {
                "error": f"카테고리 조회 중 오류 발생: {str(e)}"
            }
