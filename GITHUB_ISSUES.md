# 📋 LAW-STUDY GitHub Issues 목록

ANALYSIS_REPORT.md 에서 도출된 18 개 개선 작업입니다.

---

## 🔥 Priority 1 (1-2 주)

### Issue #1: [REFACTOR] 의존성 주입 (DI) 컨테이너 도입

**우선순위**: 높음  
**소요시간**: 6 시간  
**레이블**: `refactoring`, `priority-high`, `architecture`

**현재 문제**:
- `src/main.py` 에서 전역 단일 인스턴스 직접 생성
- 테스트에서 서비스 대체 불가
- 설정 관리가 분산됨

**제안**:
- `dependency-injector` 라이브러리 도입
- Container 클래스로 의존성 관리
- 테스트에서는 mock 주입 가능하게

**관련 파일**:
- `src/main.py`
- `src/core/container.py` (신규)
- `tests/conftest.py`

**체크리스트**:
- [ ] `dependency-injector` 설치
- [ ] Container 클래스 설계
- [ ] 서비스 팩토리 정의
- [ ] main.py 리팩토링
- [ ] 테스트 fixture 업데이트

---

### Issue #2: [REFACTOR] MCP/HTTP 라우트 통합

**우선순위**: 높음  
**소요시간**: 8 시간  
**레이블**: `refactoring`, `priority-high`, `code-duplication`

**현재 문제**:
- `mcp_routes.py` 와 `http_routes.py` 에 동일한 도구 분기 로직 중복
- 약 200 줄 중복 코드
- 새 도구 추가 시 두 파일 수정 필요

**제안**:
- `ToolRouter` 클래스로 통합
- MCP/HTTP 는 인터페이스만 다르게

**관련 파일**:
- `src/routes/mcp_routes.py`
- `src/routes/http_routes.py`
- `src/routes/tool_router.py` (신규)

**체크리스트**:
- [ ] ToolRouter 클래스 설계
- [ ] 도구 정의 메타데이터 추출
- [ ] MCP 라우트 리팩토링
- [ ] HTTP 라우트 리팩토링
- [ ] 기존 테스트 통과 확인

---

### Issue #3: [REFACTOR] 죽은 코드 제거

**우선순위**: 높음  
**소요시간**: 1 시간  
**레이블**: `refactoring`, `cleanup`, `good-first-issue`

**현재 문제**:
- `src/repositories/generic_api_repository.py` 에서 존재하지 않는 모듈 import
- `from ..tools.api_metadata_loader import load_api_metadata`
- `src/tools/` 디렉토리 없음

**조치**:
1. `generic_api_repository.py` 사용 여부 확인
2. 사용되지 않으면 파일 삭제
3. 사용되면 `api_metadata_loader.py` 생성 또는 import 수정

**관련 파일**:
- `src/repositories/generic_api_repository.py`

**체크리스트**:
- [ ] 파일 사용처 검색
- [ ] 사용 안 하면 삭제
- [ ] 사용하면 의존성 추가

---

## 📊 Priority 2 (2-4 주)

### Issue #4: [REFACTOR] 에러 처리 일원화

**우선순위**: 중간  
**소요시간**: 5 시간  
**레이블**: `refactoring`, `error-handling`, `priority-medium`

**현재 문제**:
- 서비스마다 다른 에러 처리
- 일관성 없는 에러 응답
- 에러 코드 체계 없음

**제안**:
- `LawMCPError` 기본 예외 클래스
- `@handle_error` 데코레이터
- 에러 코드 체계 (API_ERROR_TIMEOUT, API_ERROR_AUTH, 등)

**관련 파일**:
- `src/core/exceptions.py` (신규)
- `src/core/error_handler.py` (신규)
- `src/services/*.py`

**체크리스트**:
- [ ] 예외 클래스 계층 정의
- [ ] 에러 핸들러 데코레이터
- [ ] 서비스 에러 처리 통합
- [ ] 에러 코드 문서화

---

### Issue #5: [FEATURE] 로깅 및 모니터링 강화

**우선순위**: 중간  
**소요시간**: 4 시간  
**레이블**: `enhancement`, `logging`, `monitoring`

**현재 문제**:
- 도구 호출 이력 추적 불가
- 성능 메트릭 없음
- 에러 패턴 분석 어려움

**제안**:
- `structlog` 도입 (구조화 로깅)
- 요청/응답 미들웨어
- 도구 호출 로깅

**관련 파일**:
- `src/core/logging_config.py` (신규)
- `src/middleware/request_logging.py` (신규)
- `src/services/*.py`

**체크리스트**:
- [ ] structlog 설정
- [ ] 요청 로깅 미들웨어
- [ ] 서비스 로깅 추가
- [ ] 로그 레벨 설정

---

### Issue #6: [TEST] 서비스 계층 테스트 추가

**우선순위**: 중간  
**소요시간**: 8 시간  
**레이블**: `testing`, `priority-medium`, `services`

**현재 상태**:
- 서비스 계층 테스트 전무
- 간접 테스트만 존재

**추가할 테스트**:
- `PrecedentService` - 15 개 테스트
- `LawService` - 10 개 테스트
- `ComplianceService` - 10 개 테스트
- `LegalSourceService` - 10 개 테스트

**관련 파일**:
- `tests/test_services.py` (신규)
- `tests/conftest.py` (업데이트)

**체크리스트**:
- [ ] DI 컨테이너 기반 test fixture
- [ ] 서비스별 테스트 클래스
- [ ] mock repository 구현
- [ ] 에러 케이스 테스트

---

### Issue #7: [TEST] 라우트 계층 테스트 추가

**우선순위**: 중간  
**소요시간**: 6 시간  
**레이블**: `testing`, `priority-medium`, `routes`

**현재 상태**:
- 라우트 테스트 전무
- 통합 테스트 없음

**추가할 테스트**:
- MCP 프로토콜 테스트 (initialize, tools/list, tools/call)
- HTTP 엔드포인트 테스트
- 에러 응답 테스트

**관련 파일**:
- `tests/test_routes.py` (신규)
- `tests/test_mcp_protocol.py` (신규)

**체크리스트**:
- [ ] TestClient 설정
- [ ] MCP 프로토콜 테스트
- [ ] HTTP 엔드포인트 테스트
- [ ] 통합 시나리오 테스트

---

## 🌱 Priority 3 (1-2 개월)

### Issue #8: [FIX] Python 버전 통일

**우선순위**: 낮음  
**소요시간**: 10 분  
**레이블**: `bug`, `documentation`, `good-first-issue`

**현재 문제**:
- README: "Python 3.10+"
- `pyproject.toml`: `requires-python = ">=3.11"`

**조치**:
- `pyproject.toml` 수정: `requires-python = ">=3.10"`

**관련 파일**:
- `pyproject.toml`

**체크리스트**:
- [ ] pyproject.toml 수정
- [ ] README 확인

---

### Issue #9: [REFACTOR] 테스트 import 방식 개선

**우선순위**: 낮음  
**소요시간**: 3 시간  
**레이블**: `refactoring`, `testing`, `low-priority`

**현재 문제**:
- `sys.path.insert` 로 import
- 배포 런타임과 구조 차이

**제안**:
- `pytest.ini` 에 `pythonpath` 설정
- 명시적 패키지 import 사용

**관련 파일**:
- `tests/conftest.py`
- `pytest.ini`
- `tests/*.py`

**체크리스트**:
- [ ] pytest.ini 설정
- [ ] 테스트 import 수정
- [ ] 전체 테스트 통과 확인

---

### Issue #10: [FEATURE] 캐싱 전략 개선

**우선순위**: 낮음  
**소요시간**: 3 시간  
**레이블**: `enhancement`, `performance`, `caching`

**현재 문제**:
- 단일 캐시 전략 (TTL 5 분)
- 데이터 특성 반영 안 됨

**제안**:
- 조문: 24 시간 (변경 적음)
- 판례: 1 시간 (자주 추가됨)
- 검색 결과: 10 분 (쿼리 다양)
- 컴플라이언스: 1 시간

**관련 파일**:
- `src/repositories/base.py`
- `src/repositories/*.py`

**체크리스트**:
- [ ] 캐시 매니저 클래스
- [ ] 계층별 TTL 설정
- [ ] 캐시 무효화 전략
- [ ] 성능 테스트

---

### Issue #11: [TEST] 통합 테스트 추가

**우선순위**: 낮음  
**소요시간**: 8 시간  
**레이블**: `testing`, `integration`, `api`

**추가할 테스트**:
- 실제 API 호출 테스트
- MCP 클라이언트 연동 테스트
- 엔드투엔드 플로우 테스트

**관련 파일**:
- `tests/test_integration.py` (신규)

**체크리스트**:
- [ ] API 키 설정 (CI secret)
- [ ] 통합 테스트 스킵 로직
- [ ] E2E 시나리오
- [ ] 플러시 테스트

---

## 📈 추가 개선 이슈

### Issue #12: [FEATURE] 판례 결과 재랭킹 개선

**우선순위**: 중간  
**레이블**: `enhancement`, `search`, `algorithm`

**내용**: BM25 외에 도메인 특화 가중치 추가

---

### Issue #13: [FEATURE] 이슈 타입 자동 분류 확장

**우선순위**: 중간  
**레이블**: `enhancement`, `ml`, `search`

**내용**: 현재 8 개 → 20 개로 확장

---

### Issue #14: [FEATURE] 컴플라이언스 사용자 정의 이벤트

**우선순위**: 낮음  
**레이블**: `enhancement`, `compliance`

**내용**: 사용자가 직접 이벤트 추가 기능

---

### Issue #15: [FEATURE] 컴플라이언스 알림 기능

**우선순위**: 낮음  
**레이블**: `enhancement`, `compliance`, `notification`

**내용**: 기한 임박 알림 (이메일, 웹훅)

---

### Issue #16: [FEATURE] 컴플라이언스 체크리스트 채점

**우선순위**: 낮음  
**레이블**: `enhancement`, `compliance`

**내용**: 진행 상황 추적 기능

---

### Issue #17: [DOCS] API 문서 개선

**우선순위**: 낮음  
**레이블**: `documentation`

**내용**: OpenAPI/Swagger 문서 추가

---

### Issue #18: [CI/CD] GitHub Actions 테스트 자동화

**우선순위**: 중간  
**레이블**: `ci/cd`, `testing`

**내용**: PR 시 자동 테스트 실행

---

## 📊 마일스톤

### Milestone 1: 구조 개선 (1-2 주)
- Issue #1, #2, #3

### Milestone 2: 테스트 강화 (2-4 주)
- Issue #4, #5, #6, #7

### Milestone 3: 품질 향상 (1-2 개월)
- Issue #8, #9, #10, #11

### Milestone 4: 기능 확장 (2-3 개월)
- Issue #12 ~ #18

---

## 🎯 다음 액션

1. 이 파일을 GitHub 에 업로드
2. 각 이슈를 GitHub Issues 로 생성
3. 마일스톤 설정
4. 우선순위 높은 이슈부터 할당
