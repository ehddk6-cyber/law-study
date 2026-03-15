"""
Dependency Injection Container for LAW-STUDY MCP
"""
from dependency_injector import containers, providers

from ..repositories.law_repository import LawRepository
from ..repositories.law_search import LawSearchRepository
from ..repositories.law_detail import LawDetailRepository
from ..repositories.precedent_repository import PrecedentRepository
from ..repositories.constitutional_decision_repository import ConstitutionalDecisionRepository
from ..repositories.administrative_appeal_repository import AdministrativeAppealRepository
from ..repositories.administrative_rule_repository import AdministrativeRuleRepository
from ..repositories.law_interpretation_repository import LawInterpretationRepository
from ..repositories.compliance_calendar import get_compliance_calendar
from ..repositories.compliance_checklists import get_compliance_checklists

from ..services.law_service import LawService
from ..services.precedent_service import PrecedentService
from ..services.legal_source_service import LegalSourceService
from ..services.health_service import HealthService
from ..services.compliance_service import ComplianceService


class Container(containers.DeclarativeContainer):
    """DI Container for LAW-STUDY MCP"""

    # Configuration
    config = providers.Configuration()

    # Wire configuration
    wiring_config = containers.WiringConfiguration()

    # Repositories
    law_repository = providers.Singleton(LawRepository)
    law_search_repository = providers.Singleton(LawSearchRepository)
    law_detail_repository = providers.Singleton(LawDetailRepository)
    precedent_repository = providers.Singleton(PrecedentRepository)
    constitutional_decision_repository = providers.Singleton(ConstitutionalDecisionRepository)
    administrative_appeal_repository = providers.Singleton(AdministrativeAppealRepository)
    administrative_rule_repository = providers.Singleton(AdministrativeRuleRepository)
    law_interpretation_repository = providers.Singleton(LawInterpretationRepository)

    # Compliance (singleton instances)
    compliance_calendar = providers.Callable(get_compliance_calendar)
    compliance_checklists = providers.Callable(get_compliance_checklists)

    # Services
    law_service = providers.Factory(
        LawService,
        repository=law_repository,
        search_repository=law_search_repository,
        detail_repository=law_detail_repository
    )

    precedent_service = providers.Factory(
        PrecedentService,
        repository=precedent_repository
    )

    legal_source_service = providers.Factory(
        LegalSourceService,
        constitutional_repository=constitutional_decision_repository,
        administrative_appeal_repository=administrative_appeal_repository,
        administrative_rule_repository=administrative_rule_repository,
        law_interpretation_repository=law_interpretation_repository
    )

    health_service = providers.Singleton(HealthService)

    compliance_service = providers.Factory(
        ComplianceService,
        calendar=compliance_calendar,
        checklists=compliance_checklists
    )


# Global container instance
_container: Container = None


def create_container() -> Container:
    """Create and configure DI container"""
    global _container
    _container = Container()
    
    # Wire configuration from environment
    _container.config.LAW_API_KEY.from_env("LAW_API_KEY", default="da")
    _container.config.PORT.from_env("PORT", default=8099)
    _container.config.LOG_LEVEL.from_env("LOG_LEVEL", default="INFO")
    
    return _container


def get_container() -> Container:
    """Get global container instance"""
    global _container
    if _container is None:
        _container = create_container()
    return _container


def reset_container():
    """Reset container (for testing)"""
    global _container
    _container = None
