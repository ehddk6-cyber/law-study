"""
LAW-STUDY MCP Server - Main Entry Point
"""
import os
from .config.settings import get_api
from .core.logging_config import setup_logging
from .core.container import create_container, get_container
from .middleware import setup_middleware
from .routes.http_routes import register_http_routes
from .routes.mcp_routes import register_mcp_routes

# Setup structlog logging
setup_logging()

logger = get_container()  # Will be initialized after container creation
api = get_api()

# Create DI container
container = create_container()

# Get services from container
law_service = container.law_service()
precedent_service = container.precedent_service()
health_service = container.health_service()
legal_source_service = container.legal_source_service()
compliance_service = container.compliance_service()

# Setup middleware (request logging)
setup_middleware(api)

# Register routes with services
register_mcp_routes(
    api,
    law_service,
    precedent_service,
    health_service,
    legal_source_service,
    compliance_service
)
register_http_routes(
    api,
    law_service,
    precedent_service,
    health_service,
    legal_source_service,
    compliance_service
)

# Get logger after container is ready
from .core.logging_config import get_logger
logger = get_logger("main")
logger.info("server_started", port=os.environ.get("PORT", 8099))

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8099))
    reload = os.environ.get("RELOAD", "false").lower() == "true"
    
    logger.info("server_initializing", port=port, reload=reload)
    
    uvicorn.run(
        "src.main:api",
        host="0.0.0.0",
        port=port,
        reload=reload
    )
