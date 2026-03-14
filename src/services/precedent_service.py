"""
Precedent Service - 판례 관련 비즈니스 로직
"""
import asyncio
from typing import Optional, List
from ..repositories.precedent_repository import PrecedentRepository
from ..models import SearchPrecedentRequest, GetPrecedentRequest


class PrecedentService:
    """판례 관련 비즈니스 로직을 처리하는 Service"""
    
    def __init__(self):
        self.repository = PrecedentRepository()

    @staticmethod
    def _infer_issue_type(query: Optional[str]) -> Optional[str]:
        if not query:
            return None
        if any(keyword in query for keyword in ["근로자성", "프리랜서", "사용종속관계", "지휘감독"]):
            return "근로자성"
        if any(keyword in query for keyword in ["부당해고", "해고", "계약해지"]):
            return "부당해고"
        if any(keyword in query for keyword in ["임금체불", "퇴직금", "임금"]):
            return "임금체불"
        if any(keyword in query for keyword in ["재산분할", "이혼"]):
            return "재산분할"
        return None
    
    async def search_precedent(self, req: SearchPrecedentRequest, arguments: Optional[dict] = None) -> dict:
        """판례 검색 (use_fallback 옵션 지원)"""
        try:
            if arguments is None:
                arguments = {}
            
            # use_fallback이 True이거나 issue_type/must_include가 있으면 fallback 사용
            if req.use_fallback or req.issue_type or req.must_include:
                issue_type = req.issue_type or self._infer_issue_type(req.query)
                result = await self.search_precedent_with_fallback(
                    req, arguments, issue_type, req.must_include
                )
                if (not result.get("precedents")) and issue_type:
                    direct_issue_req = SearchPrecedentRequest(
                        query=issue_type,
                        page=req.page,
                        per_page=req.per_page,
                        court=req.court,
                        date_from=req.date_from,
                        date_to=req.date_to,
                        use_fallback=False,
                    )
                    direct_issue_result = await asyncio.to_thread(
                        self.repository.search_precedent,
                        direct_issue_req.query,
                        direct_issue_req.page,
                        direct_issue_req.per_page,
                        direct_issue_req.court,
                        direct_issue_req.date_from,
                        direct_issue_req.date_to,
                        arguments
                    )
                    if direct_issue_result.get("precedents"):
                        return direct_issue_result
                return result
            
            # 기존 방식 (호환성 유지)
            return await asyncio.to_thread(
                self.repository.search_precedent,
                req.query,
                req.page,
                req.per_page,
                req.court,
                req.date_from,
                req.date_to,
                arguments
            )
        except Exception as e:
            return {
                "error": f"판례 검색 중 오류 발생: {str(e)}",
                "recovery_guide": "시스템 오류가 발생했습니다. 서버 로그를 확인하거나 관리자에게 문의하세요."
            }
    
    async def search_precedent_with_fallback(
        self,
        req: SearchPrecedentRequest,
        arguments: Optional[dict] = None,
        issue_type: Optional[str] = None,
        must_include: Optional[List[str]] = None
    ) -> dict:
        """판례 검색 (다단계 fallback 전략 사용)"""
        try:
            if arguments is None:
                arguments = {}
            return await asyncio.to_thread(
                self.repository.search_precedent_with_fallback,
                req.query,
                req.page,
                req.per_page,
                req.court,
                req.date_from,
                req.date_to,
                arguments,
                issue_type,
                must_include
            )
        except Exception as e:
            return {
                "error": f"판례 검색 중 오류 발생: {str(e)}",
                "recovery_guide": "시스템 오류가 발생했습니다. 서버 로그를 확인하거나 관리자에게 문의하세요."
            }
    
    async def get_precedent(self, req: GetPrecedentRequest, arguments: Optional[dict] = None) -> dict:
        """판례 조회"""
        try:
            if arguments is None:
                arguments = {}
            if not req.precedent_id and not req.case_number:
                return {
                    "error": "precedent_id 또는 case_number 중 하나는 필수입니다.",
                    "recovery_guide": "판례 일련번호(precedent_id) 또는 사건번호(case_number) 중 하나를 입력해주세요."
                }
            return await asyncio.to_thread(
                self.repository.get_precedent,
                req.precedent_id,
                req.case_number,
                arguments
            )
        except Exception as e:
            return {
                "error": f"판례 조회 중 오류 발생: {str(e)}",
                "recovery_guide": "시스템 오류가 발생했습니다. 서버 로그를 확인하거나 관리자에게 문의하세요."
            }
