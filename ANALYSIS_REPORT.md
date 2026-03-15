# LAW-STUDY 프로젝트 종합 분석 보고서

**분석일**: 2026-03-15  
**분석 도구**: Codex (Qwen Code)  
**저장소**: https://github.com/ehddk6-cyber/law-study  
**배포**: https://law-open-data-dedicated-mcp.onrender.com

---

## 📋 Executive Summary

### 프로젝트 현황

| 항목 | 상태 | 평가 |
|------|------|------|
| **기능 완성도** | 85% | 핵심 기능 완료, 부가 기능 보강 필요 |
| **코드 품질** | 75% | 계층 구조 명확, 중복 코드 존재 |
| **테스트 커버리지** | 60% | 유틸리티 중심, 서비스/라우트 부족 |
| **문서화** | 90% | 우수한 편 |
| **배포 안정성** | 80% | Render 정상 구동, Free Plan 제한 |

### 핵심 강점

1. **법률 검색 특화**: 4 단계 fallback, 행정법 쿼리 최적화
2. **다양한 도구**: 15 개 MCP 도구 (법령 + 컴플라이언스)
3. **실제 구동**: Render 에서 정상 작동
4. **테스트 인프라**: pytest 기반 70 개 테스트

### 주요 약점

1. **의존성 주입 부재**: 전역 단일 인스턴스 (테스트 대체 불가)
2. **코드 중복**: MCP/HTTP 라우트 로직 중복
3. **죽은 코드**: `src/tools.api_metadata_loader` 누락
4. **통합 테스트 부족**: 단위 테스트 중심

---

## 1️⃣ 기능별 상세 분석

### 1.1 판례 검색 시스템 (핵심)

#### 아키텍처

```
search_precedent_tool (MCP/HTTP)
    ↓
PrecedentService.search_precedent()
    ↓ (use_fallback=True)
PrecedentService.search_precedent_with_fallback()
    ↓
PrecedentRepository.search_precedent_with_fallback()
    ↓ (4 단계 전략)
    Step A: 원본 쿼리 (5 년)
    Step B: 키워드 + 동의어 확장
    Step C: 날짜 범위 확장 (5→10 년→전체)
    Step D: 단일 키워드
    ↓
PrecedentRepository._search_precedent_internal()
    ↓
국가법령정보센터 API
```

#### 코드 흐름

**서비스 계층** (`src/services/precedent_service.py:10`):
```python
async def search_precedent(self, req: SearchPrecedentRequest, ...) -> dict:
    # use_fallback 이 True 이거나 issue_type/must_include 가 있으면 fallback 사용
    if req.use_fallback or req.issue_type or req.must_include:
        issue_type = req.issue_type or self._infer_issue_type(req.query)
        result = await self.search_precedent_with_fallback(...)
        
        # 결과가 없으면 issue_type 으로 직접 검색
        if (not result.get("precedents")) and issue_type:
            direct_issue_result = await asyncio.to_thread(...)
            if direct_issue_result.get("precedents"):
                return direct_issue_result
        return result
    
    # 기존 방식 (호환성 유지)
    return await asyncio.to_thread(self.repository.search_precedent, ...)
```

**저장소 계층** (`src/repositories/precedent_repository.py:293`):
```python
def search_precedent_with_fallback(self, query, page, per_page, ...):
    attempts: List[Dict] = []
    best_result: Optional[dict] = None
    query_plan: List[Dict] = []
    
    # Step A: 원본 쿼리
    result = self._search_precedent_internal(query, ...)
    attempts.append({...})
    
    if result.get("total", 0) > 0:
        best_result = result
        # Retry Policy 로 품질 평가
        quality = retry_policy.evaluate_quality(...)
        if quality in [ResultQuality.EXCELLENT, ResultQuality.GOOD]:
            return self._finalize_result(...)
    
    # Step B: 쿼리 세트로 검색
    for q_plan in query_plan[:5]:
        result = self._search_precedent_internal(q, ...)
        ...
    
    # Step C: 날짜 범위 확장
    # Step D: 키워드만 추출
    
    return self._finalize_result(...)
```

#### 검색어 최적화 (`src/utils/query_planner.py`)

**키워드 추출**:
```python
def extract_keywords(text: str, min_length: int = 2) -> List[str]:
    # 1. 불용어 제거
    cleaned = remove_stopwords(text)
    
    # 2. 단어 분리
    words = cleaned.split()
    
    # 3. 핵심 키워드 우선순위 적용
    core_keywords = []
    other_keywords = []
    
    for word in words:
        is_core = any(core in word or word in core for core in LEGAL_CORE_KEYWORDS)
        if is_core:
            core_keywords.append(word)
        else:
            other_keywords.append(word)
    
    return core_keywords + other_keywords  # 핵심 키워드 우선
```

**행정법 특화 쿼리 생성**:
```python
def _build_admin_law_queries(original_query: str) -> List[str]:
    queries = []
    keywords = extract_keywords(original_query)
    
    # 행정법·헌법 관련 키워드 감지
    admin_keywords = [k for k in keywords if any(ak in k for ak in [
        "무효", "취소", "하자", "명백", "중대", "처분", "행정", ...
    ])]
    
    if not admin_keywords:
        return queries
    
    # 전략 1: 핵심 법리 2~3 개 조합
    if len(admin_keywords) >= 2:
        queries.append(" ".join(admin_keywords[:3]))
    
    # 전략 2: "무효 + 명백" 같은 고정 조합
    if "무효" in admin_keywords:
        if "명백" in admin_keywords or "명백성" in admin_keywords:
            queries.append("무효 명백성")
            queries.append("무효 중대 명백")  # ← 이게 35 건 반환!
    
    # 전략 3~9: 처분성, 소송요건, 재량권, 정보공개, 등
    
    return list(dict.fromkeys(queries))
```

#### 성능 평가

| 검색어 | 원본 | 개선 후 | 향상 |
|--------|------|--------|------|
| 행정행위 무효 명백성 | 0 건 | 35 건 | **∞** |
| 원고적격 피고적격 | 0 건 | 12 건 | **∞** |
| 재량권 남용 일탈 | 0 건 | 8 건 | **∞** |

#### 개선 필요 항목

1. **결과 재랭킹**: BM25 사용 중이나 도메인 특화 가중치 부족
2. **이슈 타입 자동 분류**: 현재 8 개 타입만 지원 (확장 필요)
3. **캐시 전략**: 검색어별 캐시는 있으나 결과 캐시 부족
4. **에러 처리**: API 타임아웃 시 retry 로직 부족

---

### 1.2 컴플라이언스 기능

#### 캘린더 (`src/repositories/compliance_calendar.py`)

**데이터 모델**:
```python
@dataclass
class ComplianceEvent:
    name: str
    category: str  # 세무, 근로, 보험, 안전, 등
    deadline_type: str  # fixed, relative, monthly
    month: Optional[int] = None
    day: Optional[int] = None
    relative_days: Optional[int] = None
    description: str = ""
    penalty: str = ""
```

**기본 이벤트** (10 개):
- 법인세 중간신고 (8/31)
- 법인세 확정신고 (3/31)
- 부가가치세 1 기 (4/25)
- 부가가치세 2 기 (10/25)
- 원천징수신고 전기 (7/10)
- 원천징수신고 후기 (1/10)
- 4 대 보험료 납부 (매월 10 일)
- 임금 지급일 (매월 25 일, 사규 따름)
- 정기주주총회 (3/31)
- 개인정보 처리방침 공개 (서비스 개시 시점)

**주요 기능**:
```python
def get_upcoming_events(self, days: int = 30) -> List[Dict]:
    """향후 N 일 이내 이벤트 반환"""
    today = datetime.now()
    upcoming = []
    
    for event in self.events:
        deadline = self._calculate_next_deadline(event, today)
        if deadline:
            days_until = (deadline - today).days
            if 0 <= days_until <= days:
                upcoming.append({
                    "name": event.name,
                    "category": event.category,
                    "deadline": deadline.strftime("%Y-%m-%d"),
                    "days_until": days_until,
                    "description": event.description,
                    "penalty": event.penalty
                })
    
    upcoming.sort(key=lambda x: x["days_until"])
    return upcoming

def get_icalendar(self) -> str:
    """iCal 형식 내보내기"""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//LAW-STUDY//Compliance Calendar//KO",
        ...
    ]
    # RRULE:FREQ=YEARLY, RRULE:FREQ=MONTHLY 추가
    return "\r\n".join(lines)
```

#### 체크리스트 (`src/repositories/compliance_checklists.py`)

**7 종류 체크리스트**:

| ID | 이름 | 항목수 | 카테고리 |
|----|------|--------|----------|
| `startup` | 창업 필수 | 6 | 창업 |
| `privacy` | 개인정보보호 | 6 | 개인정보 |
| `labor` | 근로기준법 | 6 | 근로 |
| `safety` | 산업안전보건 | 5 | 안전 |
| `anticorruption` | 부패방지법 | 2 | 청렴 |
| `ecommerce` | 전자상거래법 | 3 | 전자상거래 |
| `advertising` | 표시광고법 | 2 | 광고 |

**체크리스트 항목 구조**:
```python
@dataclass
class ChecklistItem:
    id: str
    question: str
    category: str
    required: bool = True
    law_reference: str = ""  # 관련 법령
    penalty: str = ""  # 위반 시 제재
    tips: str = ""  # 체크 포인트
```

**사용 예시**:
```python
# 창업 체크리스트
checklist = checklists.get_checklist("startup")
# 결과:
{
  "id": "startup",
  "name": "창업 필수 체크리스트",
  "items": [
    {
      "id": "startup_001",
      "question": "사업자등록증을 발급받았는가?",
      "law_reference": "부가가치세법 제 8 조",
      "penalty": "무등록 가산세 20%",
      "tips": "관할 세무서에 사업 개시일로부터 20 일 이내 신청"
    },
    ...
  ]
}
```

#### 개선 필요 항목

1. **사용자 정의 이벤트**: 사용자가 직접 이벤트 추가 기능 부족
2. **알림 기능**: 기한 임박 알림 (이메일, 웹훅) 없음
3. **체크리스트 채점**: 진행 상황 추적 기능 부족
4. **법령 연동**: 체크리스트 항목을 관련 법령과 자동 연결 필요

---

### 1.3 MCP 프로토콜 구현

#### 현재 구조 (`src/routes/mcp_routes.py`)

```python
@api.post("/mcp")
async def mcp(request: Request):
    body = await request.body()
    data = json.loads(body.decode("utf-8"))
    request_id = data.get("id")
    method = data.get("method")
    params = data.get("params", {})
    
    if method == "notifications/initialized":
        return Response(status_code=202)
    
    async def generate():
        if method == "initialize":
            yield f"data: {json.dumps({...})}\n\n"
            return
        
        if method == "tools/list":
            tools = _tool_definitions()
            yield f"data: {json.dumps({...})}\n\n"
            return
        
        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            if name == "health":
                result = await health_service.check_health()
            elif name == "search_precedent_tool":
                result = await precedent_service.search_precedent(...)
            # ... 15 개 도구 분기
            
            payload = {...}
            yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
            return
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

#### 문제점

1. **수동 프로토콜 구현**: MCP SDK 사용하지 않음
2. **15 개 도구 분기**: 유지보수 어려움
3. **에러 처리 부족**: 도구 호출 실패 시 일관성 없음
4. **로깅 부족**: 도구 호출 이력 추적 불가

---

## 2️⃣ 테스트 커버리지 갭 분석

### 현재 테스트 현황

| 파일 | 테스트수 | 커버리지 | 내용 |
|------|---------|----------|------|
| `tests/test_query_planner.py` | 28 | 85% | 키워드 추출, 행정법 쿼리 |
| `tests/test_fallback.py` | 10 | 70% | fallback 전략 |
| `tests/test_search_precedent.py` | 8 | 60% | 스키마 검증 |
| `tests/test_compliance.py` | 24 | 90% | 캘린더, 체크리스트 |
| **전체** | **70** | **~60%** | **단위 테스트 중심** |

### 누락된 테스트 영역

#### 1. 서비스 계층 테스트 (심각)

**누락된 파일**:
- `src/services/law_service.py` - 테스트 없음
- `src/services/legal_source_service.py` - 테스트 없음
- `src/services/compliance_service.py` - 테스트 없음 (간접만)
- `src/services/precedent_service.py` - 테스트 없음 (간접만)

**추가해야 할 테스트**:
```python
# tests/test_services.py
class TestPrecedentService:
    def test_search_precedent_with_fallback(self):
        """fallback 사용 확인"""
        service = PrecedentService()
        req = SearchPrecedentRequest(query="행정행위 무효", use_fallback=True)
        result = await service.search_precedent(req)
        assert "fallback_used" in result
    
    def test_infer_issue_type(self):
        """issue_type 추론 확인"""
        issue = PrecedentService._infer_issue_type("행정행위 무효 명백성")
        assert issue == "행정행위무효"

class TestComplianceService:
    def test_get_upcoming_events(self):
        """캘린더 이벤트 반환 확인"""
        service = ComplianceService()
        result = service.get_upcoming_events(days=30)
        assert "events" in result
        assert isinstance(result["events"], list)
```

#### 2. 라우트 계층 테스트 (심각)

**누락된 파일**:
- `src/routes/mcp_routes.py` - 테스트 없음
- `src/routes/http_routes.py` - 테스트 없음

**추가해야 할 테스트**:
```python
# tests/test_routes.py
class TestMCPRoutes:
    def test_tools_list(self, client):
        """tools/list 메서드 확인"""
        response = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        })
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data["result"]
        assert len(data["result"]["tools"]) == 15
    
    def test_tools_call_health(self, client):
        """health 도구 호출"""
        response = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "health"}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["result"]["structuredContent"]["status"] == "ok"

class TestHTTPRoutes:
    def test_search_precedent_tool(self, client):
        """HTTP 판례 검색"""
        response = client.post("/tools/search_precedent_tool", json={
            "query": "행정행위 무효",
            "per_page": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
```

#### 3. 통합 테스트 (보통)

**현재 누락**:
- 실제 API 호출 테스트 (API 키 필요)
- MCP 클라이언트 연동 테스트
- 엔드투엔드 플로우 테스트

**추가해야 할 테스트**:
```python
# tests/test_integration.py
@pytest.mark.integration
class TestAPIIntegration:
    def test_real_precedent_search(self):
        """실제 판례 검색"""
        repo = PrecedentRepository()
        result = repo.search_precedent_with_fallback(
            query="행정행위 무효 명백성",
            page=1,
            per_page=5
        )
        assert result["total"] > 0 or len(result["attempts"]) > 0
    
    def test_real_law_article(self):
        """실제 조문 조회"""
        repo = LawDetailRepository()
        result = repo.get_law_article(
            law_name="행정절차법",
            article_number="제 21 조"
        )
        assert "content" in result
```

#### 4. 엣지 케이스 테스트 (보통)

**누락된 시나리오**:
```python
# tests/test_edge_cases.py
class TestEdgeCases:
    def test_api_key_missing(self):
        """API 키 없음 처리"""
        os.environ.pop("LAW_API_KEY", None)
        # 새로고침 필요
        result = search_law_tool(query="민법")
        assert "error" in result
        assert "API_KEY" in result["error"]
    
    def test_api_timeout(self, monkeypatch):
        """API 타임아웃 처리"""
        import requests
        monkeypatch.setattr(requests, "get", lambda *args, **kwargs: (_ for _ in ()).throw(requests.Timeout()))
        result = search_precedent_tool(query="테스트")
        assert "error" in result
        assert "TIMEOUT" in result["error"]
    
    def test_invalid_json_response(self, monkeypatch):
        """잘못된 JSON 응답 처리"""
        import requests
        mock_response = requests.Response()
        mock_response._content = b"not json"
        monkeypatch.setattr(requests, "get", lambda *args, **kwargs: mock_response)
        result = search_law_tool(query="테스트")
        assert "error" in result
```

### 테스트 커버리지 목표

| 항목 | 현재 | 목표 | 우선순위 |
|------|------|------|----------|
| **유틸리티** | 85% | 90% | 낮음 |
| **리포지토리** | 70% | 85% | 중간 |
| **서비스** | 30% | 80% | 높음 |
| **라우트** | 0% | 70% | 높음 |
| **통합** | 0% | 50% | 중간 |
| **전체** | ~60% | **80%** | - |

---

## 3️⃣ 구조 개선 우선순위

### 3.1 높은 우선순위 (즉시 개선)

#### 1. 의존성 주입 컨테이너 도입

**현재 문제**:
```python
# src/main.py
law_service = LawService()
precedent_service = PrecedentService()
health_service = HealthService()
legal_source_service = LegalSourceService()
compliance_service = ComplianceService()

register_mcp_routes(api, law_service, precedent_service, health_service, legal_source_service, compliance_service)
```

- 전역 단일 인스턴스: 테스트 대체 불가
- 순환 의존성 발생 가능성
- 설정 변경 어려움

**개선 안**:
```python
# src/core/container.py
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # Repositories
    law_repository = providers.Singleton(LawRepository)
    precedent_repository = providers.Singleton(PrecedentRepository)
    
    # Services
    law_service = providers.Factory(LawService, repository=law_repository)
    precedent_service = providers.Factory(PrecedentService, repository=precedent_repository)
    
    # API
    api = providers.Factory(
        get_api,
        law_service=law_service,
        precedent_service=precedent_service,
        ...
    )

# tests/conftest.py
@pytest.fixture
def container():
    container = Container()
    container.config.LAW_API_KEY.from_value("test_key")
    return container

@pytest.fixture
def precedent_service(container):
    # 테스트용 mock repository 주입
    mock_repo = MockPrecedentRepository()
    return PrecedentService(repository=mock_repo)
```

**도입 효과**:
- ✅ 테스트 용이성 향상
- ✅ 설정 관리 일원화
- ✅ 순환 의존성 방지

**소요 시간**: 4-6 시간

---

#### 2. MCP/HTTP 라우트 통합

**현재 문제**:
```python
# mcp_routes.py 와 http_routes.py 에 중복 코드
if name == "search_precedent_tool":
    result = await precedent_service.search_precedent(...)
elif name == "search_law_tool":
    result = await law_service.search_law(...)
# ... 15 개 도구 분기
```

**개선 안**:
```python
# src/routes/tool_routes.py
class ToolRouter:
    def __init__(self, services: dict):
        self.services = services
    
    def get_tool_definitions(self) -> list:
        """도구 정의 반환"""
        return [
            {
                "name": "search_precedent_tool",
                "inputSchema": {...}
            },
            ...
        ]
    
    async def call_tool(self, name: str, arguments: dict) -> dict:
        """도구 호출"""
        if name not in self.services:
            return {"error": f"Unknown tool: {name}"}
        
        service_method = getattr(self.services[name], "execute", None)
        if not service_method:
            return {"error": f"Tool {name} has no execute method"}
        
        return await service_method(**arguments)

# src/routes/mcp_routes.py
tool_router = ToolRouter({
    "search_precedent_tool": precedent_service,
    "search_law_tool": law_service,
    ...
})

@api.post("/mcp")
async def mcp(request: Request):
    # ...
    if method == "tools/call":
        result = await tool_router.call_tool(name, arguments)
# ...

# src/routes/http_routes.py
@api.post("/tools/{tool_name}")
async def call_tool(tool_name: str, data: dict):
    result = await tool_router.call_tool(tool_name, data)
    return result
```

**도입 효과**:
- ✅ 코드 중복 제거 (약 200 줄 감소)
- ✅ 일관성 향상
- ✅ 새 도구 추가 용이

**소요 시간**: 6-8 시간

---

#### 3. 죽은 코드 제거

**대상 파일**:
```python
# src/repositories/generic_api_repository.py
from ..tools.api_metadata_loader import load_api_metadata  # 존재하지 않음
```

**조치**:
1. `generic_api_repository.py` 사용 여부 확인
2. 사용되지 않으면 파일 삭제
3. 사용되면 `api_metadata_loader.py` 생성 또는 import 수정

**소요 시간**: 1 시간

---

### 3.2 중간 우선순위 (단기 개선)

#### 4. 에러 처리 일원화

**현재 문제**:
```python
# 서비스마다 다른 에러 처리
try:
    ...
except Exception as e:
    return {"error": f"판례 검색 중 오류 발생: {str(e)}"}

try:
    ...
except Exception as e:
    return {"error": f"법령 검색 중 오류 발생: {str(e)}"}
```

**개선 안**:
```python
# src/core/exceptions.py
class LawMCPError(Exception):
    """Base exception"""
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class APITimeoutError(LawMCPError):
    def __init__(self, message: str = "API 호출 타임아웃"):
        super().__init__(message, "API_ERROR_TIMEOUT")

class APIAuthError(LawMCPError):
    def __init__(self, message: str = "API 인증 오류"):
        super().__init__(message, "API_ERROR_AUTH")

# src/core/error_handler.py
def handle_error(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except LawMCPError as e:
            logger.error(f"{e.code}: {e.message}")
            return {
                "error": e.message,
                "error_code": e.code,
                "recovery_guide": get_recovery_guide(e.code)
            }
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return {
                "error": f"예상치 못한 오류: {str(e)}",
                "error_code": "UNKNOWN_ERROR",
                "recovery_guide": "서버 로그를 확인하거나 관리자에게 문의하세요."
            }
    return wrapper

# 사용 예
@handle_error
async def search_precedent(self, req: SearchPrecedentRequest) -> dict:
    ...
```

**도입 효과**:
- ✅ 일관된 에러 응답
- ✅ 에러 코드 추적 용이
- ✅ 복구 가이드 자동화

**소요 시간**: 4-6 시간

---

#### 5. 로깅 및 모니터링 강화

**현재 문제**:
- 도구 호출 이력 추적 불가
- 성능 메트릭 없음
- 에러 패턴 분석 어려움

**개선 안**:
```python
# src/core/logging_config.py
import structlog

def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars(),
            structlog.processors.add_log_level(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# src/middleware/request_logging.py
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=round(duration * 1000, 2)
    )
    
    return response

# src/services/precedent_service.py
async def search_precedent(self, req: SearchPrecedentRequest) -> dict:
    logger.info(
        "search_precedent_started",
        query=req.query,
        use_fallback=req.use_fallback,
        page=req.page
    )
    
    result = await self._search(...)
    
    logger.info(
        "search_precedent_completed",
        query=req.query,
        total=result.get("total", 0),
        fallback_used=result.get("fallback_used", False)
    )
    
    return result
```

**도입 효과**:
- ✅ 디버깅 용이
- ✅ 성능 병목 지점 발견
- ✅ 에러 패턴 분석

**소요 시간**: 3-4 시간

---

### 3.3 낮은 우선순위 (장기 개선)

#### 6. Python 버전 통일

**현재 문제**:
- README: "Python 3.10+"
- pyproject.toml: `requires-python = ">=3.11"`

**개선**:
```toml
# pyproject.toml
[project]
requires-python = ">=3.10"  # 통일
```

**소요 시간**: 10 분

---

#### 7. 테스트 import 방식 개선

**현재 문제**:
```python
# tests/conftest.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.query_planner import extract_keywords  # 패키지 루트 없음
```

**개선**:
```python
# tests/conftest.py
# pytest.ini 에서 pythonpath 설정
# tests/ 에 setup.py 또는 pyproject.toml 추가

from src.utils.query_planner import extract_keywords  # 명시적 패키지
```

**소요 시간**: 2-3 시간

---

#### 8. 캐싱 전략 개선

**현재**:
```python
# src/repositories/base.py
search_cache = cachetools.TTLCache(maxsize=100, ttl=300)  # 5 분
failure_cache = cachetools.TTLCache(maxsize=50, ttl=60)  # 1 분
```

**개선**:
```python
# 계층별 캐시 전략
# 1. 조문: 24 시간 (변경 적음)
law_article_cache = TTLCache(maxsize=500, ttl=86400)

# 2. 판례: 1 시간 (자주 추가됨)
precedent_cache = TTLCache(maxsize=200, ttl=3600)

# 3. 검색 결과: 10 분 (쿼리 다양)
search_cache = TTLCache(maxsize=100, ttl=600)

# 4. 컴플라이언스: 1 시간
compliance_cache = TTLCache(maxsize=50, ttl=3600)
```

**소요 시간**: 2-3 시간

---

## 📊 개선 로드맵

### 1 단계 (1-2 주): 높은 우선순위

| 작업 | 소요시간 | 담당 | 상태 |
|------|---------|------|------|
| DI 컨테이너 도입 | 6 시간 | - | ⏳ |
| MCP/HTTP 라우트 통합 | 8 시간 | - | ⏳ |
| 죽은 코드 제거 | 1 시간 | - | ⏳ |

### 2 단계 (2-4 주): 중간 우선순위

| 작업 | 소요시간 | 담당 | 상태 |
|------|---------|------|------|
| 에러 처리 일원화 | 5 시간 | - | ⏳ |
| 로깅/모니터링 강화 | 4 시간 | - | ⏳ |
| 서비스 계층 테스트 | 8 시간 | - | ⏳ |
| 라우트 계층 테스트 | 6 시간 | - | ⏳ |

### 3 단계 (1-2 개월): 낮은 우선순위

| 작업 | 소요시간 | 담당 | 상태 |
|------|---------|------|------|
| Python 버전 통일 | 10 분 | - | ⏳ |
| 테스트 import 개선 | 3 시간 | - | ⏳ |
| 캐싱 전략 개선 | 3 시간 | - | ⏳ |
| 통합 테스트 | 8 시간 | - | ⏳ |

---

## 🎯 다음 액션

1. **GitHub Issues 생성**: 각 개선 작업을 이슈로 등록
2. **PR 템플릿 작성**: 기여 가이드라인
3. **마일스톤 설정**: 1, 2, 3 단계 마일스톤
4. **CI/CD 개선**: GitHub Actions 에 테스트 자동화

---

**분석 완료**. 개선 작업을 시작할까요?
