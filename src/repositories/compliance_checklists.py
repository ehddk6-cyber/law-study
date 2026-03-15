"""
Compliance Checklists - 법령별 컴플라이언스 체크리스트
창업, 개인정보, 근로, 안전 등 분야별 체크리스트 제공
"""
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ChecklistItem:
    """체크리스트 항목"""
    id: str
    question: str
    category: str
    required: bool = True
    law_reference: str = ""  # 관련 법령
    penalty: str = ""  # 위반 시 제재
    tips: str = ""  # 체크 포인트


@dataclass
class Checklist:
    """체크리스트"""
    id: str
    name: str
    description: str
    category: str
    items: List[ChecklistItem] = field(default_factory=list)


class ComplianceChecklists:
    """컴플라이언스 체크리스트 모음"""

    def __init__(self):
        self.checklists: Dict[str, Checklist] = {}
        self._init_default_checklists()

    def _init_default_checklists(self):
        """기본 체크리스트 초기화"""

        # 1. 창업 체크리스트
        startup = Checklist(
            id="startup",
            name="창업 필수 체크리스트",
            description="사업 시작 전 필수 확인사항",
            category="창업"
        )
        startup.items = [
            ChecklistItem(
                id="startup_001",
                question="사업자등록증을 발급받았는가?",
                category="세무",
                required=True,
                law_reference="부가가치세법 제 8 조",
                penalty="무등록 가산세 20%",
                tips="관할 세무서에 사업 개시일로부터 20 일 이내 신청"
            ),
            ChecklistItem(
                id="startup_002",
                question="통신판매업 신고를 완료했는가? (온라인 판매 시)",
                category="인허가",
                required=True,
                law_reference="전자상거래법 제 11 조",
                penalty="2 천만원 이하 과태료",
                tips="정부 24 에서 온라인 신고 가능"
            ),
            ChecklistItem(
                id="startup_003",
                question="고용보험 피보험자격 취득신고를 했는가?",
                category="근로",
                required=True,
                law_reference="고용보험법 제 10 조",
                penalty="500 만원 이하 과태료",
                tips="근로자 채용일로부터 14 일 이내"
            ),
            ChecklistItem(
                id="startup_004",
                question="4 대 보험 가입을 완료했는가?",
                category="근로",
                required=True,
                law_reference="근로기준법 제 4 조",
                penalty="3 년 이하 징역 또는 3 천만원 이하 벌금",
                tips="국민연금, 건강보험, 고용보험, 산재보험"
            ),
            ChecklistItem(
                id="startup_005",
                question="개인정보 처리방침을 수립·공개했는가?",
                category="개인정보",
                required=True,
                law_reference="개인정보보호법 제 30 조",
                penalty="5 천만원 이하 과태료",
                tips="회원가입 시 필수 동의 절차 필요"
            ),
            ChecklistItem(
                id="startup_006",
                question="상표권 출원을 완료했는가?",
                category="지재권",
                required=False,
                law_reference="상표법 제 7 조",
                penalty="권리 보호 불가",
                tips="브랜드명, 로고 등 조기 출원 권장"
            ),
        ]
        self.checklists["startup"] = startup

        # 2. 개인정보보호 체크리스트
        privacy = Checklist(
            id="privacy",
            name="개인정보보호 체크리스트",
            description="개인정보보호법 준수사항",
            category="개인정보"
        )
        privacy.items = [
            ChecklistItem(
                id="privacy_001",
                question="개인정보 처리방침을 수립·공개했는가?",
                category="개인정보",
                required=True,
                law_reference="개인정보보호법 제 30 조",
                penalty="5 천만원 이하 과태료",
                tips="홈페이지 초기화면에서 쉽게 접근 가능해야 함"
            ),
            ChecklistItem(
                id="privacy_002",
                question="정보주체 동의 절차를 갖추고 있는가?",
                category="개인정보",
                required=True,
                law_reference="개인정보보호법 제 15 조",
                penalty="5 천만원 이하 과태료",
                tips="필수/선택 항목 구분, 별도 동의란 설치"
            ),
            ChecklistItem(
                id="privacy_003",
                question="개인정보 취급자를 지정·관리하는가?",
                category="개인정보",
                required=True,
                law_reference="개인정보보호법 제 31 조",
                penalty="5 천만원 이하 과태료",
                tips="최소한의 인원만 접근 권한 부여"
            ),
            ChecklistItem(
                id="privacy_004",
                question="안전성 확보조치를 이행하는가?",
                category="개인정보",
                required=True,
                law_reference="개인정보보호법 제 29 조",
                penalty="5 천만원 이하 과태료",
                tips="암호화, 접근통제, 보안프로그램 설치"
            ),
            ChecklistItem(
                id="privacy_005",
                question="개인정보 유출 사고 대응계획을 수립했는가?",
                category="개인정보",
                required=True,
                law_reference="개인정보보호법 제 34 조",
                penalty="5 천만원 이하 과태료",
                tips="유출 시 72 시간 이내 신고 의무"
            ),
            ChecklistItem(
                id="privacy_006",
                question="보유기간 경과 시 파기 절차를 갖추었는가?",
                category="개인정보",
                required=True,
                law_reference="개인정보보호법 제 21 조",
                penalty="5 천만원 이하 과태료",
                tips="파기방법: 복구불가능하게 기술적 조치"
            ),
        ]
        self.checklists["privacy"] = privacy

        # 3. 근로기준법 체크리스트
        labor = Checklist(
            id="labor",
            name="근로기준법 준수 체크리스트",
            description="근로자 고용 시 필수 확인사항",
            category="근로"
        )
        labor.items = [
            ChecklistItem(
                id="labor_001",
                question="근로계약서를 작성·교부했는가?",
                category="근로",
                required=True,
                law_reference="근로기준법 제 17 조",
                penalty="500 만원 이하 과태료",
                tips="임금, 소정근로시간, 휴일 등 필수기재사항"
            ),
            ChecklistItem(
                id="labor_002",
                question="주휴일을 부여하는가?",
                category="근로",
                required=True,
                law_reference="근로기준법 제 55 조",
                penalty="3 년 이하 징역 또는 3 천만원 이하 벌금",
                tips="1 주 개근 시 1 일 이상 유급휴일"
            ),
            ChecklistItem(
                id="labor_003",
                question="연차유급휴가를 부여하는가?",
                category="근로",
                required=True,
                law_reference="근로기준법 제 60 조",
                penalty="3 년 이하 징역 또는 3 천만원 이하 벌금",
                tips="1 년 80% 이상 출근 시 15 개"
            ),
            ChecklistItem(
                id="labor_004",
                question="퇴직금을 적립·관리하는가?",
                category="근로",
                required=True,
                law_reference="근로자퇴직급여보장법 제 8 조",
                penalty="3 년 이하 징역 또는 3 천만원 이하 벌금",
                tips="퇴직연금제도 가입 권장"
            ),
            ChecklistItem(
                id="labor_005",
                question="임금을 체불 없이 지급하는가?",
                category="근로",
                required=True,
                law_reference="근로기준법 제 43 조",
                penalty="3 년 이하 징역 또는 3 천만원 이하 벌금",
                tips="지정일, 통화, 직접, 전액, 정기 지급"
            ),
            ChecklistItem(
                id="labor_006",
                question="취업규칙을 작성·신고했는가? (상시 10 인 이상)",
                category="근로",
                required=True,
                law_reference="근로기준법 제 93 조",
                penalty="500 만원 이하 과태료",
                tips="관할 노동청에 신고, 근로자 의견 청취"
            ),
        ]
        self.checklists["labor"] = labor

        # 4. 산업안전보건법 체크리스트
        safety = Checklist(
            id="safety",
            name="산업안전보건법 체크리스트",
            description="사업장 안전관리 필수사항",
            category="안전"
        )
        safety.items = [
            ChecklistItem(
                id="safety_001",
                question="안전보건관리책임자를 지정했는가?",
                category="안전",
                required=True,
                law_reference="산업안전보건법 제 16 조",
                penalty="500 만원 이하 과태료",
                tips="사업주 또는 관리자 중 지정"
            ),
            ChecklistItem(
                id="safety_002",
                question="정기 안전보건교육을 실시하는가?",
                category="안전",
                required=True,
                law_reference="산업안전보건법 제 36 조",
                penalty="500 만원 이하 과태료",
                tips="분기 1 회 이상, 교육기록 3 년 보관"
            ),
            ChecklistItem(
                id="safety_003",
                question="유해·위험 작업환경 측정을 실시했는가?",
                category="안전",
                required=True,
                law_reference="산업안전보건법 제 42 조",
                penalty="1 천만원 이하 과태료",
                tips="3 년 1 회 이상, 측정결과 게시"
            ),
            ChecklistItem(
                id="safety_004",
                question="건강진단을 실시했는가?",
                category="안전",
                required=True,
                law_reference="산업안전보건법 제 43 조",
                penalty="500 만원 이하 과태료",
                tips="연 1 회 이상, 특수건강진단 별도"
            ),
            ChecklistItem(
                id="safety_005",
                question="재해발생 시 보고·조치했는가?",
                category="안전",
                required=True,
                law_reference="산업안전보건법 제 10 조",
                penalty="1 천만원 이하 과태료",
                tips="사망재해: 즉시, 부상재해: 3 일 이내"
            ),
        ]
        self.checklists["safety"] = safety

        # 5. 부패방지법 체크리스트 (공공기관)
        anticorruption = Checklist(
            id="anticorruption",
            name="부패방지법 체크리스트",
            description="공공기관 청렴 준수사항",
            category="청렴"
        )
        anticorruption.items = [
            ChecklistItem(
                id="ac_001",
                question="청렴교육을 실시했는가?",
                category="청렴",
                required=True,
                law_reference="부패방지법 제 5 조",
                penalty="시정권고",
                tips="연 1 회 이상, 임직원 대상"
            ),
            ChecklistItem(
                id="ac_002",
                question="공익신고자 보호조치를 마련했는가?",
                category="청렴",
                required=True,
                law_reference="부패방지법 제 10 조",
                penalty="2 천만원 이하 과태료",
                tips="신고접수창구, 비밀보장, 불이익금지"
            ),
        ]
        self.checklists["anticorruption"] = anticorruption

        # 6. 전자상거래법 체크리스트
        ecommerce = Checklist(
            id="ecommerce",
            name="전자상거래법 체크리스트",
            description="온라인 쇼핑몰 운영자 준수사항",
            category="전자상거래"
        )
        ecommerce.items = [
            ChecklistItem(
                id="ec_001",
                question="사업자정보를 표시했는가?",
                category="전자상거래",
                required=True,
                law_reference="전자상거래법 제 11 조",
                penalty="2 천만원 이하 과태료",
                tips="상호, 대표자, 주소, 연락처, 사업자번호"
            ),
            ChecklistItem(
                id="ec_002",
                question="청약철회권을 보장하는가?",
                category="전자상거래",
                required=True,
                law_reference="전자상거래법 제 17 조",
                penalty="2 천만원 이하 과태료",
                tips="배송일로부터 7 일 이내, 예외사항 명시"
            ),
            ChecklistItem(
                id="ec_003",
                question="이용약관을 명시·고시했는가?",
                category="전자상거래",
                required=True,
                law_reference="전자상거래법 제 12 조",
                penalty="2 천만원 이하 과태료",
                tips="회원가입 전 열람기회 제공"
            ),
        ]
        self.checklists["ecommerce"] = ecommerce

        # 7. 표시광고법 체크리스트
        advertising = Checklist(
            id="advertising",
            name="표시광고법 체크리스트",
            description="광고 표시 준수사항",
            category="광고"
        )
        advertising.items = [
            ChecklistItem(
                id="ad_001",
                question="과장·허위광고를 하지 않는가?",
                category="광고",
                required=True,
                law_reference="표시광고법 제 3 조",
                penalty="시정권고, 과징금",
                tips="객관적 근거 없는 표현 자제"
            ),
            ChecklistItem(
                id="ad_002",
                question="소비자주의환기문구를 표시했는가?",
                category="광고",
                required=True,
                law_reference="표시광고법 제 5 조",
                penalty="시정권고",
                tips="건강기능식품, 화장품 등"
            ),
        ]
        self.checklists["advertising"] = advertising

    def get_checklist(self, checklist_id: str) -> Optional[Dict]:
        """체크리스트 반환"""
        checklist = self.checklists.get(checklist_id)
        if not checklist:
            return None

        return {
            "id": checklist.id,
            "name": checklist.name,
            "description": checklist.description,
            "category": checklist.category,
            "items": [
                {
                    "id": item.id,
                    "question": item.question,
                    "category": item.category,
                    "required": item.required,
                    "law_reference": item.law_reference,
                    "penalty": item.penalty,
                    "tips": item.tips
                }
                for item in checklist.items
            ]
        }

    def get_all_checklists(self) -> List[Dict]:
        """모든 체크리스트 목록 반환"""
        return [
            {
                "id": cl.id,
                "name": cl.name,
                "description": cl.description,
                "category": cl.category,
                "item_count": len(cl.items)
            }
            for cl in self.checklists.values()
        ]

    def get_categories(self) -> List[str]:
        """모든 카테고리 반환"""
        categories = set(cl.category for cl in self.checklists.values())
        return sorted(list(categories))

    def search_checklists(self, keyword: str) -> List[Dict]:
        """키워드로 체크리스트 검색"""
        results = []
        for checklist in self.checklists.values():
            if keyword.lower() in checklist.name.lower() or \
               keyword.lower() in checklist.description.lower() or \
               any(keyword.lower() in item.question.lower() for item in checklist.items):
                results.append(self.get_checklist(checklist.id))
        return results


# 전역 인스턴스
_checklists: Optional[ComplianceChecklists] = None


def get_compliance_checklists() -> ComplianceChecklists:
    """컴플라이언스 체크리스트 인스턴스 반환"""
    global _checklists
    if _checklists is None:
        _checklists = ComplianceChecklists()
    return _checklists
