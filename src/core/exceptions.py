"""
LAW-STUDY MCP exception hierarchy.
"""

from __future__ import annotations

from typing import Any, Dict, Optional


RECOVERY_GUIDES = {
    "API_ERROR_TIMEOUT": "네트워크 응답 시간이 초과되었습니다. 잠시 후 다시 시도하거나, 인터넷 연결을 확인하세요.",
    "API_ERROR_AUTH": "API 키가 설정되지 않았거나 유효하지 않습니다. LAW_API_KEY 환경변수를 확인하세요.",
    "API_ERROR_NOT_FOUND": "요청한 리소스를 찾을 수 없습니다. 파라미터를 확인하세요.",
    "API_ERROR_INVALID_RESPONSE": "API 응답이 유효하지 않습니다. API 서버 상태를 확인하세요.",
    "API_ERROR_REQUEST": "API 요청 처리 중 오류가 발생했습니다. 입력값과 네트워크 상태를 확인하세요.",
    "VALIDATION_ERROR": "입력 파라미터를 확인하세요.",
    "TOOL_EXECUTION_ERROR": "도구 실행 중 오류가 발생했습니다. 입력 파라미터를 확인하세요.",
    "UNKNOWN_TOOL": "지원하지 않는 도구입니다. tools/list 응답을 확인하세요.",
    "UNKNOWN_ERROR": "시스템 오류가 발생했습니다. 서버 로그를 확인하거나 관리자에게 문의하세요.",
}


class LawMCPError(Exception):
    """Base exception for standardized MCP errors."""

    def __init__(
        self,
        message: str,
        code: str = "UNKNOWN_ERROR",
        *,
        recovery_guide: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code
        self.recovery_guide = recovery_guide or RECOVERY_GUIDES.get(code, RECOVERY_GUIDES["UNKNOWN_ERROR"])
        self.extra = extra or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "error": self.message,
            "error_code": self.code,
            "recovery_guide": self.recovery_guide,
        }
        payload.update(self.extra)
        if "missing_reason" not in payload:
            payload["missing_reason"] = self.code
        return payload


class APITimeoutError(LawMCPError):
    def __init__(self, message: str = "API 호출 타임아웃", **kwargs: Any):
        super().__init__(message, "API_ERROR_TIMEOUT", **kwargs)


class APIAuthError(LawMCPError):
    def __init__(self, message: str = "API 인증 오류", **kwargs: Any):
        super().__init__(message, "API_ERROR_AUTH", **kwargs)


class APINotFoundError(LawMCPError):
    def __init__(self, message: str = "리소스를 찾을 수 없습니다.", **kwargs: Any):
        super().__init__(message, "API_ERROR_NOT_FOUND", **kwargs)


class APIInvalidResponseError(LawMCPError):
    def __init__(self, message: str = "API 응답 형식 오류", **kwargs: Any):
        super().__init__(message, "API_ERROR_INVALID_RESPONSE", **kwargs)


class APIRequestError(LawMCPError):
    def __init__(self, message: str = "API 요청 처리 중 오류 발생", **kwargs: Any):
        super().__init__(message, "API_ERROR_REQUEST", **kwargs)


class ValidationError(LawMCPError):
    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message, "VALIDATION_ERROR", **kwargs)


class ToolExecutionError(LawMCPError):
    def __init__(self, message: str, tool_name: Optional[str] = None, **kwargs: Any):
        full_message = f"{tool_name}: {message}" if tool_name else message
        extra = kwargs.pop("extra", {}) or {}
        if tool_name:
            extra.setdefault("tool_name", tool_name)
        super().__init__(full_message, "TOOL_EXECUTION_ERROR", extra=extra, **kwargs)


class UnknownToolError(LawMCPError):
    def __init__(self, tool_name: str):
        super().__init__(
            f"Unknown tool: {tool_name}",
            "UNKNOWN_TOOL",
            extra={"tool_name": tool_name, "missing_reason": "UNKNOWN_TOOL"},
        )
