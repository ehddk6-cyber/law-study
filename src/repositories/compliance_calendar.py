"""
Compliance Calendar - 법령 컴플라이언스 캘린더
법정 기한, 신고기간, 납부기한 등을 관리
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ComplianceEvent:
    """컴플라이언스 이벤트"""
    name: str
    category: str
    deadline_type: str  # fixed, relative, monthly
    month: Optional[int] = None  # 고정 월 (1-12)
    day: Optional[int] = None  # 고정 일 (1-31)
    relative_days: Optional[int] = None  # 기준일로부터 일수
    description: str = ""
    penalty: str = ""  # 과태료/가산금


class ComplianceCalendar:
    """컴플라이언스 캘린더"""

    def __init__(self):
        self.events: List[ComplianceEvent] = []
        self._init_default_events()

    def _init_default_events(self):
        """기본 법정 기한 이벤트 초기화"""
        # 법인세 관련
        self.events.append(ComplianceEvent(
            name="법인세 중간신고",
            category="세무",
            deadline_type="fixed",
            month=8,
            day=31,
            description="사업연도 개시일로부터 6 월이 되는 날부터 2 월 이내",
            penalty="무신고가산세 20%"
        ))

        self.events.append(ComplianceEvent(
            name="법인세 확정신고",
            category="세무",
            deadline_type="fixed",
            month=3,
            day=31,
            description="사업연도 종료일부터 3 월 이내",
            penalty="무신고가산세 20%"
        ))

        # 부가가치세 관련
        self.events.append(ComplianceEvent(
            name="부가가치세 1 기 확정신고",
            category="세무",
            deadline_type="fixed",
            month=4,
            day=25,
            description="1 월 1 일 ~ 3 월 31 일",
            penalty="무신고가산세 20%"
        ))

        self.events.append(ComplianceEvent(
            name="부가가치세 2 기 확정신고",
            category="세무",
            deadline_type="fixed",
            month=10,
            day=25,
            description="7 월 1 일 ~ 9 월 30 일",
            penalty="무신고가산세 20%"
        ))

        # 원천징수 관련
        self.events.append(ComplianceEvent(
            name="원천징수신고 (전반기)",
            category="세무",
            deadline_type="fixed",
            month=7,
            day=10,
            description="1 월 ~ 6 월 급여 원천징수",
            penalty="가산세 10%"
        ))

        self.events.append(ComplianceEvent(
            name="원천징수신고 (후반기)",
            category="세무",
            deadline_type="fixed",
            month=1,
            day=10,
            description="7 월 ~ 12 월 급여 원천징수",
            penalty="가산세 10%"
        ))

        # 4 대 보험 관련
        self.events.append(ComplianceEvent(
            name="4 대 보험료 납부",
            category="보험",
            deadline_type="monthly",
            day=10,
            description="전월분 보험료 납부 (매월 10 일)",
            penalty="연 15% 가산금"
        ))

        # 근로기준법 관련
        self.events.append(ComplianceEvent(
            name="임금 지급일",
            category="근로",
            deadline_type="monthly",
            day=25,
            description="임금 지급일 (사규에 따름)",
            penalty="3 년 이하 징역 또는 3 천만원 이하 벌금"
        ))

        # 상법 관련
        self.events.append(ComplianceEvent(
            name="정기주주총회",
            category="상법",
            deadline_type="fixed",
            month=3,
            day=31,
            description="매 사업연도 종료 후 3 월 이내",
            penalty="결의 취소 사유"
        ))

        # 개인정보보호법 관련
        self.events.append(ComplianceEvent(
            name="개인정보 처리방침 공개",
            category="개인정보",
            deadline_type="relative",
            relative_days=0,
            description="서비스 개시 시점",
            penalty="5 천만원 이하 과태료"
        ))

        # 산업안전보건법 관련
        self.events.append(ComplianceEvent(
            name="안전보건교육",
            category="안전",
            deadline_type="monthly",
            description="분기 1 회 이상 정기교육",
            penalty="500 만원 이하 과태료"
        ))

    def get_upcoming_events(self, days: int = 30) -> List[Dict]:
        """향후 N 일 이내 이벤트 반환"""
        today = datetime.now()
        upcoming = []

        for event in self.events:
            deadline = self._calculate_next_deadline(event, today)
            if deadline:
                days_until = (deadline - today).days
                if 0 <= days_until <= days:
                    upcoming.append({
                        "name": event.name,
                        "category": event.category,
                        "deadline": deadline.strftime("%Y-%m-%d"),
                        "days_until": days_until,
                        "description": event.description,
                        "penalty": event.penalty
                    })

        # D-day 순으로 정렬
        upcoming.sort(key=lambda x: x["days_until"])
        return upcoming

    def get_events_by_month(self, month: int) -> List[Dict]:
        """특정 월의 이벤트 반환"""
        result = []
        for event in self.events:
            if event.month == month or event.deadline_type == "monthly":
                result.append({
                    "name": event.name,
                    "category": event.category,
                    "deadline_type": event.deadline_type,
                    "day": event.day,
                    "description": event.description,
                    "penalty": event.penalty
                })
        return result

    def get_events_by_category(self, category: str) -> List[Dict]:
        """특정 카테고리의 이벤트 반환"""
        result = []
        for event in self.events:
            if event.category == category:
                result.append({
                    "name": event.name,
                    "deadline_type": event.deadline_type,
                    "month": event.month,
                    "day": event.day,
                    "description": event.description,
                    "penalty": event.penalty
                })
        return result

    def _calculate_next_deadline(self, event: ComplianceEvent, base_date: datetime) -> Optional[datetime]:
        """다음 기한 계산"""
        if event.deadline_type == "fixed":
            if event.month and event.day:
                deadline = datetime(base_date.year, event.month, event.day)
                if deadline < base_date:
                    deadline = datetime(base_date.year + 1, event.month, event.day)
                return deadline

        elif event.deadline_type == "monthly":
            if event.day:
                deadline = datetime(base_date.year, base_date.month, event.day)
                if deadline < base_date:
                    # 다음 달로
                    if base_date.month == 12:
                        deadline = datetime(base_date.year + 1, 1, event.day)
                    else:
                        deadline = datetime(base_date.year, base_date.month + 1, event.day)
                return deadline

        elif event.deadline_type == "relative":
            if event.relative_days is not None:
                return base_date + timedelta(days=event.relative_days)

        return None

    def get_all_categories(self) -> List[str]:
        """모든 카테고리 반환"""
        categories = set(e.category for e in self.events)
        return sorted(list(categories))

    def add_event(self, event: ComplianceEvent):
        """이벤트 추가"""
        self.events.append(event)

    def get_icalendar(self) -> str:
        """iCal 형식 내보내기"""
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//LAW-STUDY//Compliance Calendar//KO",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:법령 컴플라이언스 캘린더",
            "X-WR-TIMEZONE:Asia/Seoul",
        ]

        for event in self.events:
            if event.deadline_type == "fixed" and event.month and event.day:
                lines.append("BEGIN:VEVENT")
                lines.append(f"SUMMARY:{event.name}")
                lines.append(f"DTSTART;VALUE=DATE:{datetime.now().year:04d}{event.month:02d}{event.day:02d}")
                lines.append(f"DTEND;VALUE=DATE:{datetime.now().year:04d}{event.month:02d}{event.day:02d}")
                lines.append(f"DESCRIPTION:{event.description}")
                lines.append(f"CATEGORIES:{event.category}")
                lines.append("RRULE:FREQ=YEARLY")
                lines.append("END:VEVENT")

            elif event.deadline_type == "monthly" and event.day:
                lines.append("BEGIN:VEVENT")
                lines.append(f"SUMMARY:{event.name}")
                lines.append(f"DTSTART;VALUE=DATE:{datetime.now().year:04d}{datetime.now().month:02d}{event.day:02d}")
                lines.append(f"DTEND;VALUE=DATE:{datetime.now().year:04d}{datetime.now().month:02d}{event.day:02d}")
                lines.append(f"DESCRIPTION:{event.description}")
                lines.append(f"CATEGORIES:{event.category}")
                lines.append("RRULE:FREQ=MONTHLY")
                lines.append("END:VEVENT")

        lines.append("END:VCALENDAR")
        return "\r\n".join(lines)


# 전역 인스턴스
_compliance_calendar: Optional[ComplianceCalendar] = None


def get_compliance_calendar() -> ComplianceCalendar:
    """컴플라이언스 캘린더 인스턴스 반환"""
    global _compliance_calendar
    if _compliance_calendar is None:
        _compliance_calendar = ComplianceCalendar()
    return _compliance_calendar
