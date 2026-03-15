from fastapi import FastAPI

from ..models.schemas import (
    GetAdministrativeAppealRequest,
    GetConstitutionalDecisionRequest,
    GetLawArticleRequest,
    GetLawDetailRequest,
    GetLawInterpretationRequest,
    GetPrecedentRequest,
    SearchAdministrativeAppealRequest,
    SearchAdministrativeRuleRequest,
    SearchConstitutionalDecisionRequest,
    SearchLawInterpretationRequest,
    SearchLawRequest,
    SearchPrecedentRequest,
)
from ..services.health_service import HealthService
from ..services.legal_source_service import LegalSourceService
from ..services.law_service import LawService
from ..services.precedent_service import PrecedentService
from ..services.compliance_service import ComplianceService


def register_http_routes(
    api: FastAPI,
    law_service: LawService,
    precedent_service: PrecedentService,
    health_service: HealthService,
    legal_source_service: LegalSourceService,
    compliance_service: ComplianceService,
):
    @api.get("/")
    async def root():
        return {
            "service": "Law Open Data Dedicated MCP",
            "status": "running",
            "endpoints": {"health": "/health", "mcp": "/mcp", "tools": "/tools"},
        }

    @api.get("/health")
    async def health():
        return await health_service.check_health()

    @api.get("/tools")
    async def tools():
        return [
            {"name": "health"},
            {"name": "search_law_tool"},
            {"name": "get_law_detail_tool"},
            {"name": "get_law_article_tool"},
            {"name": "search_precedent_tool"},
            {"name": "get_precedent_tool"},
            {"name": "search_constitutional_decision_tool"},
            {"name": "get_constitutional_decision_tool"},
            {"name": "search_administrative_appeal_tool"},
            {"name": "get_administrative_appeal_tool"},
            {"name": "search_administrative_rule_tool"},
            {"name": "search_law_interpretation_tool"},
            {"name": "get_law_interpretation_tool"},
            {"name": "get_compliance_calendar_tool"},
            {"name": "get_compliance_checklist_tool"},
        ]

    @api.post("/tools/search_law_tool")
    async def search_law(data: dict):
        req = SearchLawRequest(**data)
        return await law_service.search_law(req, arguments=data)

    @api.post("/tools/get_law_detail_tool")
    async def get_law_detail(data: dict):
        req = GetLawDetailRequest(**data)
        return await law_service.get_law_detail(req, arguments=data)

    @api.post("/tools/get_law_article_tool")
    async def get_law_article(data: dict):
        req = GetLawArticleRequest(**data)
        return await legal_source_service.get_law_article(req, arguments=data)

    @api.post("/tools/search_precedent_tool")
    async def search_precedent(data: dict):
        req = SearchPrecedentRequest(**data)
        return await precedent_service.search_precedent(req, arguments=data)

    @api.post("/tools/get_precedent_tool")
    async def get_precedent(data: dict):
        req = GetPrecedentRequest(**data)
        return await precedent_service.get_precedent(req, arguments=data)

    @api.post("/tools/search_constitutional_decision_tool")
    async def search_constitutional_decision(data: dict):
        req = SearchConstitutionalDecisionRequest(**data)
        return await legal_source_service.search_constitutional_decision(req, arguments=data)

    @api.post("/tools/get_constitutional_decision_tool")
    async def get_constitutional_decision(data: dict):
        req = GetConstitutionalDecisionRequest(**data)
        return await legal_source_service.get_constitutional_decision(req, arguments=data)

    @api.post("/tools/search_administrative_appeal_tool")
    async def search_administrative_appeal(data: dict):
        req = SearchAdministrativeAppealRequest(**data)
        return await legal_source_service.search_administrative_appeal(req, arguments=data)

    @api.post("/tools/get_administrative_appeal_tool")
    async def get_administrative_appeal(data: dict):
        req = GetAdministrativeAppealRequest(**data)
        return await legal_source_service.get_administrative_appeal(req, arguments=data)

    @api.post("/tools/search_administrative_rule_tool")
    async def search_administrative_rule(data: dict):
        req = SearchAdministrativeRuleRequest(**data)
        return await legal_source_service.search_administrative_rule(req, arguments=data)

    @api.post("/tools/search_law_interpretation_tool")
    async def search_law_interpretation(data: dict):
        req = SearchLawInterpretationRequest(**data)
        return await legal_source_service.search_law_interpretation(req, arguments=data)

    @api.post("/tools/get_law_interpretation_tool")
    async def get_law_interpretation(data: dict):
        req = GetLawInterpretationRequest(**data)
        return await legal_source_service.get_law_interpretation(req, arguments=data)

    @api.post("/tools/get_compliance_calendar_tool")
    async def get_compliance_calendar(data: dict):
        days = data.get("days")
        month = data.get("month")
        category = data.get("category")
        if days:
            return compliance_service.get_upcoming_events(days)
        elif month:
            return compliance_service.get_events_by_month(month)
        elif category:
            return compliance_service.get_events_by_category(category)
        else:
            return compliance_service.get_all_categories()

    @api.post("/tools/get_compliance_checklist_tool")
    async def get_compliance_checklist(data: dict):
        checklist_id = data.get("checklist_id")
        keyword = data.get("keyword")
        if checklist_id:
            return compliance_service.get_checklist(checklist_id)
        elif keyword:
            return compliance_service.search_checklists(keyword)
        else:
            return compliance_service.get_all_checklists()
