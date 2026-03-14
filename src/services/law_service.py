from ..models.schemas import SearchLawRequest, GetLawDetailRequest
from ..repositories.law_repository import LawRepository


class LawService:
    def __init__(self):
        self.repository = LawRepository()

    async def search_law(self, req: SearchLawRequest, arguments=None):
        return self.repository.search_law(req.query, req.page, req.per_page, arguments)

    async def get_law_detail(self, req: GetLawDetailRequest, arguments=None):
        return self.repository.get_law_detail(req.law_name, arguments)
