from fastapi import FastAPI

from ..services.health_service import HealthService
from ..services.legal_source_service import LegalSourceService
from ..services.law_service import LawService
from ..services.precedent_service import PrecedentService
from ..services.compliance_service import ComplianceService
from .tool_router import ToolRouter


def register_http_routes(
    api: FastAPI,
    law_service: LawService,
    precedent_service: PrecedentService,
    health_service: HealthService,
    legal_source_service: LegalSourceService,
    compliance_service: ComplianceService,
):
    # Create ToolRouter for unified tool handling
    tool_router = ToolRouter(
        law_service=law_service,
        precedent_service=precedent_service,
        health_service=health_service,
        legal_source_service=legal_source_service,
        compliance_service=compliance_service,
    )
    
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
        # Use ToolRouter for tool definitions
        return tool_router.get_tool_definitions()

    @api.post("/tools/search_law_tool")
    async def search_law(data: dict):
        return await tool_router.call_tool("search_law_tool", data)

    @api.post("/tools/get_law_detail_tool")
    async def get_law_detail(data: dict):
        return await tool_router.call_tool("get_law_detail_tool", data)

    @api.post("/tools/get_law_article_tool")
    async def get_law_article(data: dict):
        return await tool_router.call_tool("get_law_article_tool", data)

    @api.post("/tools/search_precedent_tool")
    async def search_precedent(data: dict):
        return await tool_router.call_tool("search_precedent_tool", data)

    @api.post("/tools/get_precedent_tool")
    async def get_precedent(data: dict):
        return await tool_router.call_tool("get_precedent_tool", data)

    @api.post("/tools/search_constitutional_decision_tool")
    async def search_constitutional_decision(data: dict):
        return await tool_router.call_tool("search_constitutional_decision_tool", data)

    @api.post("/tools/get_constitutional_decision_tool")
    async def get_constitutional_decision(data: dict):
        return await tool_router.call_tool("get_constitutional_decision_tool", data)

    @api.post("/tools/search_administrative_appeal_tool")
    async def search_administrative_appeal(data: dict):
        return await tool_router.call_tool("search_administrative_appeal_tool", data)

    @api.post("/tools/get_administrative_appeal_tool")
    async def get_administrative_appeal(data: dict):
        return await tool_router.call_tool("get_administrative_appeal_tool", data)

    @api.post("/tools/search_administrative_rule_tool")
    async def search_administrative_rule(data: dict):
        return await tool_router.call_tool("search_administrative_rule_tool", data)

    @api.post("/tools/search_law_interpretation_tool")
    async def search_law_interpretation(data: dict):
        return await tool_router.call_tool("search_law_interpretation_tool", data)

    @api.post("/tools/get_law_interpretation_tool")
    async def get_law_interpretation(data: dict):
        return await tool_router.call_tool("get_law_interpretation_tool", data)

    @api.post("/tools/get_compliance_calendar_tool")
    async def get_compliance_calendar(data: dict):
        return await tool_router.call_tool("get_compliance_calendar_tool", data)

    @api.post("/tools/get_compliance_checklist_tool")
    async def get_compliance_checklist(data: dict):
        return await tool_router.call_tool("get_compliance_checklist_tool", data)
