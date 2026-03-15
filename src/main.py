"""
LAW-STUDY MCP Server - Main Entry Point
"""
import os
from .config.settings import get_api, setup_logging
from .routes.http_routes import register_http_routes
from .routes.mcp_routes import register_mcp_routes
from .core.container import create_container, get_container

logger = setup_logging()
api = get_api()

# Create DI container
container = create_container()

# Get services from container
law_service = container.law_service()
precedent_service = container.precedent_service()
health_service = container.health_service()
legal_source_service = container.legal_source_service()
compliance_service = container.compliance_service()

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

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8099))
    uvicorn.run(
        "src.main:api", 
        host="0.0.0.0", 
        port=port, 
        reload=os.environ.get("RELOAD", "false").lower() == "true"
    )
