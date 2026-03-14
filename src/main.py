import os

from .config.settings import get_api, setup_logging
from .routes.http_routes import register_http_routes
from .routes.mcp_routes import register_mcp_routes
from .services.health_service import HealthService
from .services.legal_source_service import LegalSourceService
from .services.law_service import LawService
from .services.precedent_service import PrecedentService

logger = setup_logging()
api = get_api()

law_service = LawService()
precedent_service = PrecedentService()
health_service = HealthService()
legal_source_service = LegalSourceService()

register_mcp_routes(api, law_service, precedent_service, health_service, legal_source_service)
register_http_routes(api, law_service, precedent_service, health_service, legal_source_service)

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8099))
    uvicorn.run("src.main:api", host="0.0.0.0", port=port, reload=os.environ.get("RELOAD", "false").lower() == "true")
