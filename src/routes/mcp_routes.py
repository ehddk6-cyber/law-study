import json

from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse

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
from .tool_router import ToolRouter


def _tool_definitions():
    return [
        {"name": "health", "inputSchema": {"type": "object", "additionalProperties": False}},
        {
            "name": "search_law_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "page": {"type": "integer", "minimum": 1},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100},
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_law_detail_tool",
            "inputSchema": {
                "type": "object",
                "properties": {"law_name": {"type": "string"}},
                "required": ["law_name"],
            },
        },
        {
            "name": "get_law_article_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "law_name": {"type": "string"},
                    "law_id": {"type": "string"},
                    "article_number": {"type": "string"},
                    "hang": {"type": "string"},
                    "ho": {"type": "string"},
                    "mok": {"type": "string"},
                },
                "required": ["article_number"],
            },
        },
        {
            "name": "search_precedent_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "page": {"type": "integer", "minimum": 1},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100},
                    "court": {"type": "string"},
                    "date_from": {"type": "string"},
                    "date_to": {"type": "string"},
                    "use_fallback": {"type": "boolean"},
                    "issue_type": {"type": "string"},
                    "must_include": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["query"],
            },
        },
        {
            "name": "get_precedent_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "precedent_id": {"type": "string"},
                    "case_number": {"type": "string"},
                },
                "anyOf": [
                    {"required": ["precedent_id"]},
                    {"required": ["case_number"]},
                ],
            },
        },
        {
            "name": "search_constitutional_decision_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "page": {"type": "integer", "minimum": 1},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100},
                    "date_from": {"type": "string"},
                    "date_to": {"type": "string"},
                },
            },
        },
        {
            "name": "get_constitutional_decision_tool",
            "inputSchema": {
                "type": "object",
                "properties": {"decision_id": {"type": "string"}},
                "required": ["decision_id"],
            },
        },
        {
            "name": "search_administrative_appeal_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "page": {"type": "integer", "minimum": 1},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100},
                    "date_from": {"type": "string"},
                    "date_to": {"type": "string"},
                },
            },
        },
        {
            "name": "get_administrative_appeal_tool",
            "inputSchema": {
                "type": "object",
                "properties": {"appeal_id": {"type": "string"}},
                "required": ["appeal_id"],
            },
        },
        {
            "name": "search_administrative_rule_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "agency": {"type": "string"},
                    "page": {"type": "integer", "minimum": 1},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100},
                },
            },
        },
        {
            "name": "search_law_interpretation_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "agency": {"type": "string"},
                    "page": {"type": "integer", "minimum": 1},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 100},
                },
            },
        },
        {
            "name": "get_law_interpretation_tool",
            "inputSchema": {
                "type": "object",
                "properties": {"interpretation_id": {"type": "string"}},
                "required": ["interpretation_id"],
            },
        },
        {
            "name": "get_compliance_calendar_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "minimum": 1, "maximum": 365},
                    "month": {"type": "integer", "minimum": 1, "maximum": 12},
                    "category": {"type": "string"},
                },
            },
        },
        {
            "name": "get_compliance_checklist_tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "checklist_id": {"type": "string"},
                    "keyword": {"type": "string"},
                },
            },
        },
    ]


def register_mcp_routes(
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
    
    @api.post("/mcp")
    async def mcp(request: Request):
        body = await request.body()
        data = json.loads(body.decode("utf-8"))
        request_id = data.get("id")
        method = data.get("method")
        params = data.get("params", {})

        if method == "notifications/initialized":
            return Response(status_code=202)

        async def generate():
            if method == "initialize":
                yield f"data: {json.dumps({'jsonrpc':'2.0','id':request_id,'result':{'protocolVersion':'2025-06-18','capabilities':{'tools':{},'resources':{'subscribe':False,'listChanged':False}},'serverInfo':{'name':'law-open-data-dedicated-mcp','version':'0.1.0'}}}, ensure_ascii=False)}\n\n"
                return

            if method == "resources/list":
                yield f"data: {json.dumps({'jsonrpc':'2.0','id':request_id,'result':{'resources':[]}}, ensure_ascii=False)}\n\n"
                return

            if method == "resources/templates/list":
                yield f"data: {json.dumps({'jsonrpc':'2.0','id':request_id,'result':{'resourceTemplates':[]}}, ensure_ascii=False)}\n\n"
                return

            if method == "tools/list":
                # Use ToolRouter for tool definitions
                tools = tool_router.get_tool_definitions()
                yield f"data: {json.dumps({'jsonrpc':'2.0','id':request_id,'result':{'tools':tools}}, ensure_ascii=False)}\n\n"
                return

            if method == "tools/call":
                name = params.get("name")
                arguments = params.get("arguments", {})
                
                # Use ToolRouter for tool execution
                result = await tool_router.call_tool(name, arguments)

                payload = {"jsonrpc": "2.0", "id": request_id, "result": {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}], "structuredContent": result, "isError": "error" in result}}
                yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
                return

            yield f"data: {json.dumps({'jsonrpc':'2.0','id':request_id,'error':{'code':-32601,'message':f'Unknown method: {method}'}}, ensure_ascii=False)}\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
