from ..models import (
    GetAdministrativeAppealRequest,
    GetConstitutionalDecisionRequest,
    GetLawArticleRequest,
    GetLawInterpretationRequest,
    SearchAdministrativeAppealRequest,
    SearchAdministrativeRuleRequest,
    SearchConstitutionalDecisionRequest,
    SearchLawInterpretationRequest,
)
from ..repositories.administrative_appeal_repository import AdministrativeAppealRepository
from ..repositories.administrative_rule_repository import AdministrativeRuleRepository
from ..repositories.constitutional_decision_repository import ConstitutionalDecisionRepository
from ..repositories.law_detail import LawDetailRepository
from ..repositories.law_interpretation_repository import LawInterpretationRepository
from ..core.error_handler import convert_to_error_dict, handle_api_errors


class LegalSourceService:
    def __init__(
        self,
        law_detail_repository=None,
        constitutional_repository=None,
        administrative_appeal_repository=None,
        administrative_rule_repository=None,
        law_interpretation_repository=None,
    ):
        self.law_detail_repository = law_detail_repository or LawDetailRepository()
        self.constitutional_decision_repository = constitutional_repository or ConstitutionalDecisionRepository()
        self.administrative_appeal_repository = administrative_appeal_repository or AdministrativeAppealRepository()
        self.administrative_rule_repository = administrative_rule_repository or AdministrativeRuleRepository()
        self.law_interpretation_repository = law_interpretation_repository or LawInterpretationRepository()

    @convert_to_error_dict
    @handle_api_errors
    async def get_law_article(self, req: GetLawArticleRequest, arguments=None):
        return self.law_detail_repository.get_law(
            law_id=req.law_id,
            law_name=req.law_name,
            mode="single",
            article_number=req.article_number,
            hang=req.hang,
            ho=req.ho,
            mok=req.mok,
            arguments=arguments,
        )

    @convert_to_error_dict
    @handle_api_errors
    async def search_constitutional_decision(self, req: SearchConstitutionalDecisionRequest, arguments=None):
        return self.constitutional_decision_repository.search_constitutional_decision(
            query=req.query,
            page=req.page,
            per_page=req.per_page,
            date_from=req.date_from,
            date_to=req.date_to,
            arguments=arguments,
        )

    @convert_to_error_dict
    @handle_api_errors
    async def get_constitutional_decision(self, req: GetConstitutionalDecisionRequest, arguments=None):
        return self.constitutional_decision_repository.get_constitutional_decision(
            decision_id=req.decision_id,
            arguments=arguments,
        )

    @convert_to_error_dict
    @handle_api_errors
    async def search_administrative_appeal(self, req: SearchAdministrativeAppealRequest, arguments=None):
        return self.administrative_appeal_repository.search_administrative_appeal(
            query=req.query,
            page=req.page,
            per_page=req.per_page,
            date_from=req.date_from,
            date_to=req.date_to,
            arguments=arguments,
        )

    @convert_to_error_dict
    @handle_api_errors
    async def get_administrative_appeal(self, req: GetAdministrativeAppealRequest, arguments=None):
        return self.administrative_appeal_repository.get_administrative_appeal(
            appeal_id=req.appeal_id,
            arguments=arguments,
        )

    @convert_to_error_dict
    @handle_api_errors
    async def search_administrative_rule(self, req: SearchAdministrativeRuleRequest, arguments=None):
        return self.administrative_rule_repository.search_administrative_rule(
            query=req.query,
            agency=req.agency,
            page=req.page,
            per_page=req.per_page,
            arguments=arguments,
        )

    @convert_to_error_dict
    @handle_api_errors
    async def search_law_interpretation(self, req: SearchLawInterpretationRequest, arguments=None):
        return self.law_interpretation_repository.search_law_interpretation(
            query=req.query,
            agency=req.agency,
            page=req.page,
            per_page=req.per_page,
            arguments=arguments,
        )

    @convert_to_error_dict
    @handle_api_errors
    async def get_law_interpretation(self, req: GetLawInterpretationRequest, arguments=None):
        return self.law_interpretation_repository.get_law_interpretation(
            interpretation_id=req.interpretation_id,
            arguments=arguments,
        )
