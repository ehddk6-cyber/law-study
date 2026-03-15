"""
Error handling decorators for LAW-STUDY MCP.
"""

from __future__ import annotations

import functools
import inspect
import logging
from typing import Any, Callable, TypeVar

import requests

from .exceptions import (
    APIAuthError,
    APIRequestError,
    APITimeoutError,
    LawMCPError,
)

logger = logging.getLogger("law-open-data-dedicated-mcp")

F = TypeVar("F", bound=Callable[..., Any])


def handle_api_errors(func: F) -> F:
    """Translate common requests exceptions into LawMCPError."""

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except LawMCPError:
            raise
        except requests.exceptions.Timeout as exc:
            raise APITimeoutError(f"{func.__name__} 타임아웃") from exc
        except requests.exceptions.HTTPError as exc:
            status_code = getattr(getattr(exc, "response", None), "status_code", None)
            if status_code in (401, 403):
                raise APIAuthError(f"API 인증 실패: {status_code}") from exc
            raise APIRequestError(f"API 요청 실패: {exc}") from exc
        except requests.exceptions.RequestException as exc:
            raise APIRequestError(f"API 요청 실패: {exc}") from exc
        except Exception:
            logger.exception("%s 에서 예외 발생", func.__name__)
            raise

    return async_wrapper  # type: ignore[return-value]


def handle_errors(func: F) -> F:
    """Log unexpected sync exceptions while preserving LawMCPError."""

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except LawMCPError:
            raise
        except Exception:
            logger.exception("%s 에서 예외 발생", func.__name__)
            raise

    return sync_wrapper  # type: ignore[return-value]


def convert_to_error_dict(func: F) -> F:
    """Convert raised LawMCPError into a standardized error dict."""

    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> dict:
            try:
                return await func(*args, **kwargs)
            except LawMCPError as exc:
                logger.error("%s: %s", exc.code, exc.message)
                return exc.to_dict()
            except Exception as exc:
                logger.exception("예상치 못한 오류")
                return LawMCPError(f"예상치 못한 오류: {exc}").to_dict()

        return async_wrapper  # type: ignore[return-value]

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> dict:
        try:
            return func(*args, **kwargs)
        except LawMCPError as exc:
            logger.error("%s: %s", exc.code, exc.message)
            return exc.to_dict()
        except Exception as exc:
            logger.exception("예상치 못한 오류")
            return LawMCPError(f"예상치 못한 오류: {exc}").to_dict()

    return sync_wrapper  # type: ignore[return-value]
