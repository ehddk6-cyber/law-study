"""
Logging Configuration - structlog 기반 로깅 설정
"""
import logging
import os
import sys
from typing import Any

import structlog


def setup_logging(level: str = None) -> None:
    """
    structlog 기반 로깅 설정
    
    Args:
        level: 로그 레벨 (기본값: 환경변수 LOG_LEVEL 또는 INFO)
    """
    if level is None:
        level = os.environ.get("LOG_LEVEL", "INFO").upper()
    
    log_level = getattr(logging, level, logging.INFO)
    
    # Shared processors
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    
    # Console renderer for development
    if os.environ.get("RELOAD", "false").lower() == "true":
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    else:
        # JSON formatter for production
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(sys.stderr),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """
    로거 인스턴스 반환
    
    Args:
        name: 로거 이름 (모듈명 권장)
    
    Returns:
        structlog logger 인스턴스
    """
    return structlog.get_logger(name)
