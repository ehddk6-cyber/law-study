"""
Middleware module for LAW-STUDY MCP
"""
from .request_logging import RequestLoggingMiddleware, setup_middleware

__all__ = [
    "RequestLoggingMiddleware",
    "setup_middleware",
]
