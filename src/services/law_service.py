from ..models.schemas import SearchLawRequest, GetLawDetailRequest
from ..repositories.law_repository import LawRepository
from ..core.error_handler import convert_to_error_dict, handle_api_errors


class LawService:
    def __init__(self, repository=None, search_repository=None, detail_repository=None):
        self.repository = repository or LawRepository()
        self.search_repository = search_repository or self.repository
        self.detail_repository = detail_repository or self.repository

    @convert_to_error_dict
    @handle_api_errors
    async def search_law(self, req: SearchLawRequest, arguments=None):
        return self.search_repository.search_law(req.query, req.page, req.per_page, arguments)

    @convert_to_error_dict
    @handle_api_errors
    async def get_law_detail(self, req: GetLawDetailRequest, arguments=None):
        return self.detail_repository.get_law_detail(req.law_name, arguments)
