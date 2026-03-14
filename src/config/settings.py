import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("law-open-data-dedicated-mcp")
    level = getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper(), logging.INFO)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
    logger.propagate = True
    return logger


def get_api() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger = logging.getLogger("law-open-data-dedicated-mcp")
        logger.info("Dedicated law MCP starting")
        yield
        logger.info("Dedicated law MCP stopping")

    api = FastAPI(lifespan=lifespan)
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return api
