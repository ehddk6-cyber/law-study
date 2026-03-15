"""
Request Logging Middleware - HTTP 요청/응답 로깅
"""
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .logging_config import get_logger

logger = get_logger("middleware.request_logging")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """HTTP 요청/응답 로깅 미들웨어"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # 요청 정보 로깅
        logger.info(
            "request_started",
            method=request.method,
            path=str(request.url.path),
            query=str(request.url.query) if request.url.query else None,
            client=request.client.host if request.client else None,
        )
        
        try:
            response = await call_next(request)
            
            # 응답 정보 로깅
            duration = time.time() - start_time
            logger.info(
                "request_completed",
                method=request.method,
                path=str(request.url.path),
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "request_failed",
                method=request.method,
                path=str(request.url.path),
                error=str(e),
                duration_ms=round(duration * 1000, 2),
                exc_info=True,
            )
            raise


def setup_middleware(app: FastAPI) -> None:
    """FastAPI 앱에 미들웨어 등록"""
    app.add_middleware(RequestLoggingMiddleware)
