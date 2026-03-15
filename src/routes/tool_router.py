"""
Tool Router - 통합 도구 라우팅
MCP 와 HTTP 에서 공통으로 사용하는 도구 라우팅 로직
"""
import json
from typing import Dict, Any, Optional
from ..services.law_service import LawService
from ..services.precedent_service import PrecedentService
from ..services.legal_source_service import LegalSourceService
from ..services.health_service import HealthService
from ..services.compliance_service import ComplianceService
from ..models.schemas import (
    SearchLawRequest,
    GetLawDetailRequest,
    GetLawArticleRequest,
    SearchPrecedentRequest,
    GetPrecedentRequest,
    SearchConstitutionalDecisionRequest,
    GetConstitutionalDecisionRequest,
    SearchAdministrativeAppealRequest,
    GetAdministrativeAppealRequest,
    SearchAdministrativeRuleRequest,
    SearchLawInterpretationRequest,
    GetLawInterpretationRequest,
)


class ToolRouter:
    """도구 라우팅을 담당하는 클래스"""

    def __init__(
        self,
        law_service: LawService,
        precedent_service: PrecedentService,
        health_service: HealthService,
        legal_source_service: LegalSourceService,
        compliance_service: ComplianceService,
    ):
        self.law_service = law_service
        self.precedent_service = precedent_service
        self.health_service = health_service
        self.legal_source_service = legal_source_service
        self.compliance_service = compliance_service
        
        # 도구 메타데이터 정의
        self.tool_definitions = self._build_tool_definitions()

    def _build_tool_definitions(self) -> list:
        """도구 정의 메타데이터 구축"""
        return [
            {
                "name": "health",
                "description": "서버 상태 확인",
                "inputSchema": {"type": "object", "additionalProperties": False}
            },
            {
                "name": "search_law_tool",
                "description": "법령 검색",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "검색어"},
                        "page": {"type": "integer", "minimum": 1, "default": 1},
                        "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 10},
                    },
                    "required": ["query"],
                }
            },
            {
                "name": "get_law_detail_tool",
                "description": "법령 상세 조회",
                "inputSchema": {
                    "type": "object",
                    "properties": {"law_name": {"type": "string", "description": "법령명"}},
                    "required": ["law_name"],
                }
            },
            {
                "name": "get_law_article_tool",
                "description": "조문 단건 조회",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "law_name": {"type": "string", "description": "법령명"},
                        "law_id": {"type": "string", "description": "법령일련번호"},
                        "article_number": {"type": "string", "description": "조 번호"},
                        "hang": {"type": "string", "description": "항 번호"},
                        "ho": {"type": "string", "description": "호 번호"},
                        "mok": {"type": "string", "description": "목"},
                    },
                    "required": ["article_number"],
                }
            },
            {
                "name": "search_precedent_tool",
                "description": "판례 검색 (fallback 포함)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "검색어"},
                        "page": {"type": "integer", "minimum": 1, "default": 1},
                        "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
                        "court": {"type": "string", "description": "법원 코드"},
                        "date_from": {"type": "string", "description": "시작일자 (YYYYMMDD)"},
                        "date_to": {"type": "string", "description": "종료일자 (YYYYMMDD)"},
                        "use_fallback": {"type": "boolean", "default": True},
                        "issue_type": {"type": "string", "description": "쟁점 유형"},
                        "must_include": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["query"],
                }
            },
            {
                "name": "get_precedent_tool",
                "description": "판례 상세 조회",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "precedent_id": {"type": "string", "description": "판례 일련번호"},
                        "case_number": {"type": "string", "description": "사건번호"},
                    },
                    "anyOf": [
                        {"required": ["precedent_id"]},
                        {"required": ["case_number"]},
                    ],
                }
            },
            {
                "name": "search_constitutional_decision_tool",
                "description": "헌재결정 검색",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "검색어"},
                        "page": {"type": "integer", "minimum": 1, "default": 1},
                        "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
                        "date_from": {"type": "string", "description": "시작일자 (YYYYMMDD)"},
                        "date_to": {"type": "string", "description": "종료일자 (YYYYMMDD)"},
                    },
                }
            },
            {
                "name": "get_constitutional_decision_tool",
                "description": "헌재결정 상세 조회",
                "inputSchema": {
                    "type": "object",
                    "properties": {"decision_id": {"type": "string", "description": "헌재결정 일련번호"}},
                    "required": ["decision_id"],
                }
            },
            {
                "name": "search_administrative_appeal_tool",
                "description": "행정심판 검색",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "검색어"},
                        "page": {"type": "integer", "minimum": 1, "default": 1},
                        "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
                        "date_from": {"type": "string", "description": "시작일자 (YYYYMMDD)"},
                        "date_to": {"type": "string", "description": "종료일자 (YYYYMMDD)"},
                    },
                }
            },
            {
                "name": "get_administrative_appeal_tool",
                "description": "행정심판 상세 조회",
                "inputSchema": {
                    "type": "object",
                    "properties": {"appeal_id": {"type": "string", "description": "행정심판 일련번호"}},
                    "required": ["appeal_id"],
                }
            },
            {
                "name": "search_administrative_rule_tool",
                "description": "행정규칙 검색",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "검색어"},
                        "agency": {"type": "string", "description": "소관 부처명"},
                        "page": {"type": "integer", "minimum": 1, "default": 1},
                        "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
                    },
                }
            },
            {
                "name": "search_law_interpretation_tool",
                "description": "법령해석 검색",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "검색어"},
                        "agency": {"type": "string", "description": "질의기관 또는 부처명"},
                        "page": {"type": "integer", "minimum": 1, "default": 1},
                        "per_page": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
                    },
                }
            },
            {
                "name": "get_law_interpretation_tool",
                "description": "법령해석 상세 조회",
                "inputSchema": {
                    "type": "object",
                    "properties": {"interpretation_id": {"type": "string", "description": "법령해석 일련번호"}},
                    "required": ["interpretation_id"],
                }
            },
            {
                "name": "get_compliance_calendar_tool",
                "description": "컴플라이언스 캘린더",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "days": {"type": "integer", "minimum": 1, "maximum": 365, "description": "향후 N 일 이내"},
                        "month": {"type": "integer", "minimum": 1, "maximum": 12, "description": "특정 월"},
                        "category": {"type": "string", "description": "카테고리 (세무, 근로, 등)"},
                    },
                }
            },
            {
                "name": "get_compliance_checklist_tool",
                "description": "컴플라이언스 체크리스트",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "checklist_id": {"type": "string", "description": "체크리스트 ID (startup, privacy, labor, 등)"},
                        "keyword": {"type": "string", "description": "검색 키워드"},
                    },
                }
            },
        ]

    def get_tool_definitions(self) -> list:
        """도구 정의 반환"""
        return self.tool_definitions

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        도구 호출
        
        Args:
            name: 도구 이름
            arguments: 도구 인자
            
        Returns:
            도구 실행 결과
        """
        try:
            if name == "health":
                return await self.health_service.check_health()
            
            elif name == "search_law_tool":
                req = SearchLawRequest(**arguments)
                return await self.law_service.search_law(req, arguments=arguments)
            
            elif name == "get_law_detail_tool":
                req = GetLawDetailRequest(**arguments)
                return await self.law_service.get_law_detail(req, arguments=arguments)
            
            elif name == "get_law_article_tool":
                req = GetLawArticleRequest(**arguments)
                return await self.legal_source_service.get_law_article(req, arguments=arguments)
            
            elif name == "search_precedent_tool":
                req = SearchPrecedentRequest(**arguments)
                return await self.precedent_service.search_precedent(req, arguments=arguments)
            
            elif name == "get_precedent_tool":
                req = GetPrecedentRequest(**arguments)
                return await self.precedent_service.get_precedent(req, arguments=arguments)
            
            elif name == "search_constitutional_decision_tool":
                req = SearchConstitutionalDecisionRequest(**arguments)
                return await self.legal_source_service.search_constitutional_decision(req, arguments=arguments)
            
            elif name == "get_constitutional_decision_tool":
                req = GetConstitutionalDecisionRequest(**arguments)
                return await self.legal_source_service.get_constitutional_decision(req, arguments=arguments)
            
            elif name == "search_administrative_appeal_tool":
                req = SearchAdministrativeAppealRequest(**arguments)
                return await self.legal_source_service.search_administrative_appeal(req, arguments=arguments)
            
            elif name == "get_administrative_appeal_tool":
                req = GetAdministrativeAppealRequest(**arguments)
                return await self.legal_source_service.get_administrative_appeal(req, arguments=arguments)
            
            elif name == "search_administrative_rule_tool":
                req = SearchAdministrativeRuleRequest(**arguments)
                return await self.legal_source_service.search_administrative_rule(req, arguments=arguments)
            
            elif name == "search_law_interpretation_tool":
                req = SearchLawInterpretationRequest(**arguments)
                return await self.legal_source_service.search_law_interpretation(req, arguments=arguments)
            
            elif name == "get_law_interpretation_tool":
                req = GetLawInterpretationRequest(**arguments)
                return await self.legal_source_service.get_law_interpretation(req, arguments=arguments)
            
            elif name == "get_compliance_calendar_tool":
                days = arguments.get("days")
                month = arguments.get("month")
                category = arguments.get("category")
                if days:
                    return self.compliance_service.get_upcoming_events(days)
                elif month:
                    return self.compliance_service.get_events_by_month(month)
                elif category:
                    return self.compliance_service.get_events_by_category(category)
                else:
                    return self.compliance_service.get_all_categories()
            
            elif name == "get_compliance_checklist_tool":
                checklist_id = arguments.get("checklist_id")
                keyword = arguments.get("keyword")
                if checklist_id:
                    return self.compliance_service.get_checklist(checklist_id)
                elif keyword:
                    return self.compliance_service.search_checklists(keyword)
                else:
                    return self.compliance_service.get_all_checklists()
            
            else:
                return {"error": f"Unknown tool: {name}", "error_code": "UNKNOWN_TOOL"}
        
        except Exception as e:
            return {
                "error": f"도구 호출 중 오류 발생: {str(e)}",
                "error_code": "TOOL_EXECUTION_ERROR",
                "tool_name": name,
            }
