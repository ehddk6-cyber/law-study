"""
Core module for LAW-STUDY MCP
"""
from .error_handler import convert_to_error_dict, handle_api_errors, handle_errors
from .exceptions import (
    APIAuthError,
    APIInvalidResponseError,
    APINotFoundError,
    APIRequestError,
    APITimeoutError,
    LawMCPError,
    ToolExecutionError,
    UnknownToolError,
    ValidationError,
)

__all__ = [
    "handle_api_errors",
    "handle_errors",
    "convert_to_error_dict",
    "LawMCPError",
    "APITimeoutError",
    "APIAuthError",
    "APINotFoundError",
    "APIInvalidResponseError",
    "APIRequestError",
    "ValidationError",
    "ToolExecutionError",
    "UnknownToolError",
]
