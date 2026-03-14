from pydantic import BaseModel, Field
from typing import List, Optional


class SearchLawRequest(BaseModel):
    query: str = Field(..., description="법령 검색어")
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)


class GetLawDetailRequest(BaseModel):
    law_name: str = Field(..., description="법령명")


class GetLawArticleRequest(BaseModel):
    law_name: Optional[str] = Field(None, description="법령명")
    law_id: Optional[str] = Field(None, description="법령일련번호")
    article_number: str = Field(..., description="조 번호")
    hang: Optional[str] = Field(None, description="항 번호")
    ho: Optional[str] = Field(None, description="호 번호")
    mok: Optional[str] = Field(None, description="목")


class SearchPrecedentRequest(BaseModel):
    query: str = Field(..., description="판례 검색어")
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)
    court: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    use_fallback: bool = True
    issue_type: Optional[str] = None
    must_include: Optional[List[str]] = None


class GetPrecedentRequest(BaseModel):
    precedent_id: Optional[str] = None
    case_number: Optional[str] = None


class SearchConstitutionalDecisionRequest(BaseModel):
    query: Optional[str] = Field(None, description="헌재결정 검색어")
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)
    date_from: Optional[str] = None
    date_to: Optional[str] = None


class GetConstitutionalDecisionRequest(BaseModel):
    decision_id: str = Field(..., description="헌재결정 일련번호")


class SearchAdministrativeAppealRequest(BaseModel):
    query: Optional[str] = Field(None, description="행정심판 검색어")
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)
    date_from: Optional[str] = None
    date_to: Optional[str] = None


class GetAdministrativeAppealRequest(BaseModel):
    appeal_id: str = Field(..., description="행정심판 일련번호")


class SearchAdministrativeRuleRequest(BaseModel):
    query: Optional[str] = Field(None, description="행정규칙 검색어")
    agency: Optional[str] = Field(None, description="소관 부처명")
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class SearchLawInterpretationRequest(BaseModel):
    query: Optional[str] = Field(None, description="법령해석 검색어")
    agency: Optional[str] = Field(None, description="질의기관 또는 부처명")
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1, le=100)


class GetLawInterpretationRequest(BaseModel):
    interpretation_id: str = Field(..., description="법령해석 일련번호")
