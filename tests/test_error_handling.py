"""
Tests for unified error handling.
"""

import asyncio


def test_law_mcp_error_to_dict():
    from src.core.exceptions import LawMCPError

    error = LawMCPError("boom", "UNKNOWN_ERROR", extra={"foo": "bar"})
    result = error.to_dict()

    assert result["error"] == "boom"
    assert result["error_code"] == "UNKNOWN_ERROR"
    assert result["missing_reason"] == "UNKNOWN_ERROR"
    assert result["foo"] == "bar"


def test_compliance_service_invalid_month_returns_standard_error():
    from src.services.compliance_service import ComplianceService

    service = ComplianceService()
    result = service.get_events_by_month(13)

    assert result["error_code"] == "VALIDATION_ERROR"
    assert result["missing_reason"] == "VALIDATION_ERROR"
    assert "recovery_guide" in result


def test_precedent_service_missing_identifier_returns_standard_error():
    from src.services.precedent_service import PrecedentService
    from src.models.schemas import GetPrecedentRequest

    service = PrecedentService()
    result = asyncio.run(service.get_precedent(GetPrecedentRequest()))

    assert result["error_code"] == "VALIDATION_ERROR"
    assert result["missing_reason"] == "VALIDATION_ERROR"
    assert "precedent_id 또는 case_number" in result["error"]


def test_tool_router_unknown_tool_returns_standard_error():
    from src.routes.tool_router import ToolRouter
    from src.services.health_service import HealthService
    from src.services.law_service import LawService
    from src.services.precedent_service import PrecedentService
    from src.services.legal_source_service import LegalSourceService
    from src.services.compliance_service import ComplianceService

    router = ToolRouter(
        law_service=LawService(),
        precedent_service=PrecedentService(),
        health_service=HealthService(),
        legal_source_service=LegalSourceService(),
        compliance_service=ComplianceService(),
    )

    result = asyncio.run(router.call_tool("missing_tool", {}))

    assert result["error_code"] == "UNKNOWN_TOOL"
    assert result["missing_reason"] == "UNKNOWN_TOOL"
    assert result["tool_name"] == "missing_tool"


def test_tool_router_pydantic_validation_returns_standard_error():
    from src.routes.tool_router import ToolRouter
    from src.services.health_service import HealthService
    from src.services.law_service import LawService
    from src.services.precedent_service import PrecedentService
    from src.services.legal_source_service import LegalSourceService
    from src.services.compliance_service import ComplianceService

    router = ToolRouter(
        law_service=LawService(),
        precedent_service=PrecedentService(),
        health_service=HealthService(),
        legal_source_service=LegalSourceService(),
        compliance_service=ComplianceService(),
    )

    result = asyncio.run(router.call_tool("search_law_tool", {}))

    assert result["error_code"] == "VALIDATION_ERROR"
    assert result["missing_reason"] == "VALIDATION_ERROR"
    assert result["tool_name"] == "search_law_tool"
    assert "details" in result
