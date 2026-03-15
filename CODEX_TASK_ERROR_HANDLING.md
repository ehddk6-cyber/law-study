# Codex 작업 지시서: 에러 처리 일원화 (Issue #4)

## 📋 작업 개요

**작업명**: 에러 처리 일원화  
**우선순위**: 중간 (Priority 2)  
**예상 소요시간**: 5-6 시간  
**관련 이슈**: GITHUB_ISSUES.md Issue #4

---

## 🎯 목표

현재 서비스마다 다른 에러 처리 방식을 일원화하여:
1. 일관된 에러 응답 형식
2. 에러 코드 체계 도입
3. 복구 가이드 자동화
4. 디버깅 용이성 향상

---

## 📁 분석할 파일

### 1. 현재 에러 처리 현황

```bash
# 서비스 계층 에러 처리 확인
grep -n "except" src/services/*.py

# 저장소 계층 에러 처리 확인
grep -n "except" src/repositories/*.py
```

### 2. 주요 파일

| 파일 | 내용 | 라인수 |
|------|------|--------|
| `src/services/precedent_service.py` | 판례 서비스 에러 처리 | ~130 |
| `src/services/law_service.py` | 법령 서비스 에러 처리 | ~80 |
| `src/services/compliance_service.py` | 컴플라이언스 에러 처리 | ~140 |
| `src/repositories/base.py` | 기본 API 에러 처리 | ~200 |
| `src/repositories/precedent_repository.py` | 판례 저장소 에러 처리 | ~780 |

---

## 🔍 현재 문제점

### 1. 일관성 없는 에러 메시지

```python
# precedent_service.py
return {
    "error": f"판례 검색 중 오류 발생: {str(e)}",
    "recovery_guide": "시스템 오류가 발생했습니다. 서버 로그를 확인하거나 관리자에게 문의하세요."
}

# law_service.py
return {
    "error": f"법령 검색 중 오류 발생: {str(e)}",
    "recovery_guide": "시스템 오류가 발생했습니다."
}

# compliance_service.py
return {
    "error": f"이벤트 조회 중 오류 발생: {str(e)}"
}
```

### 2. 에러 코드 체계 부재

- 에러를 식별할 코드가 없음
- 클라이언트에서 에러 타입을 구분할 수 없음

### 3. 복구 가이드 부족

- 일부 서비스는 recovery_guide 없음
- 일관된 형식이 아님

---

## ✅ 작업 내용

### 단계 1: 에러 클래스 계층 설계 (1 시간)

**파일**: `src/core/exceptions.py` (신규)

```python
"""
LAW-STUDY MCP 예외 계층
"""


class LawMCPError(Exception):
    """기본 예외 클래스"""
    
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.code = code
        self.recovery_guide = self._get_recovery_guide(code)
        super().__init__(self.message)
    
    def _get_recovery_guide(self, code: str) -> str:
        """에러 코드별 복구 가이드"""
        guides = {
            "API_ERROR_TIMEOUT": "네트워크 응답 시간이 초과되었습니다. 잠시 후 다시 시도하거나, 인터넷 연결을 확인하세요.",
            "API_ERROR_AUTH": "API 키가 설정되지 않았거나 유효하지 않습니다. LAW_API_KEY 환경변수를 확인하세요.",
            "API_ERROR_NOT_FOUND": "요청한 리소스를 찾을 수 없습니다. 파라미터를 확인하세요.",
            "API_ERROR_INVALID_RESPONSE": "API 응답이 유효하지 않습니다. API 서버 상태를 확인하세요.",
            "TOOL_EXECUTION_ERROR": "도구 실행 중 오류가 발생했습니다. 입력 파라미터를 확인하세요.",
            "UNKNOWN_ERROR": "시스템 오류가 발생했습니다. 서버 로그를 확인하거나 관리자에게 문의하세요.",
        }
        return guides.get(code, guides["UNKNOWN_ERROR"])
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "error": self.message,
            "error_code": self.code,
            "recovery_guide": self.recovery_guide,
        }


class APITimeoutError(LawMCPError):
    """API 호출 타임아웃"""
    
    def __init__(self, message: str = "API 호출 타임아웃"):
        super().__init__(message, "API_ERROR_TIMEOUT")


class APIAuthError(LawMCPError):
    """API 인증 오류"""
    
    def __init__(self, message: str = "API 인증 오류"):
        super().__init__(message, "API_ERROR_AUTH")


class APINotFoundError(LawMCPError):
    """API 리소스 없음"""
    
    def __init__(self, message: str = "리소스를 찾을 수 없음"):
        super().__init__(message, "API_ERROR_NOT_FOUND")


class APIInvalidResponseError(LawMCPError):
    """API 응답 형식 오류"""
    
    def __init__(self, message: str = "응답 형식 오류"):
        super().__init__(message, "API_ERROR_INVALID_RESPONSE")


class ToolExecutionError(LawMCPError):
    """도구 실행 오류"""
    
    def __init__(self, message: str, tool_name: str = None):
        full_message = f"{tool_name}: {message}" if tool_name else message
        super().__init__(full_message, "TOOL_EXECUTION_ERROR")
```

---

### 단계 2: 에러 핸들러 데코레이터 (1 시간)

**파일**: `src/core/error_handler.py` (신규)

```python
"""
에러 핸들러 데코레이터
"""
import functools
import logging
from typing import Callable, Any
from .exceptions import LawMCPError

logger = logging.getLogger(__name__)


def handle_api_errors(func: Callable) -> Callable:
    """
    API 관련 에러를 처리하는 데코레이터
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except LawMCPError:
            # 이미 처리된 LawMCPError 는 그대로 반환
            raise
        except requests.exceptions.Timeout:
            from .exceptions import APITimeoutError
            raise APITimeoutError(f"{func.__name__} 타임아웃")
        except requests.exceptions.RequestException as e:
            from .exceptions import APIAuthError
            # API 키 오류 등
            if "401" in str(e) or "403" in str(e):
                raise APIAuthError(f"API 인증 실패: {str(e)}")
            raise
        except Exception as e:
            # 예상치 못한 에러는 로깅 후 재발생
            logger.exception(f"{func.__name__} 에서 예외 발생: {str(e)}")
            raise
    
    return async_wrapper


def handle_errors(func: Callable) -> Callable:
    """
    일반 에러를 처리하는 데코레이터 (동기 함수용)
    """
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except LawMCPError:
            raise
        except Exception as e:
            logger.exception(f"{func.__name__} 에서 예외 발생: {str(e)}")
            raise
    
    return sync_wrapper


def convert_to_error_dict(func: Callable) -> Callable:
    """
    예외를 딕셔너리로 변환하는 데코레이터
    루트 레벨 (라우트) 에서 사용
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> dict:
        try:
            return await func(*args, **kwargs)
        except LawMCPError as e:
            logger.error(f"{e.code}: {e.message}")
            return e.to_dict()
        except Exception as e:
            logger.exception(f"예상치 못한 오류: {str(e)}")
            from .exceptions import LawMCPError
            return LawMCPError(f"예상치 못한 오류: {str(e)}").to_dict()
    
    return wrapper
```

---

### 단계 3: 서비스 계층 에러 처리 통합 (2 시간)

**적용 파일**:
- `src/services/precedent_service.py`
- `src/services/law_service.py`
- `src/services/compliance_service.py`
- `src/services/legal_source_service.py`

**적용 방법**:

```python
# Before (precedent_service.py)
async def search_precedent(self, req: SearchPrecedentRequest, arguments: Optional[dict] = None) -> dict:
    try:
        if arguments is None:
            arguments = {}
        
        if req.use_fallback or req.issue_type or req.must_include:
            issue_type = req.issue_type or self._infer_issue_type(req.query)
            result = await self.search_precedent_with_fallback(...)
            return result
        
        return await asyncio.to_thread(...)
    
    except Exception as e:
        return {
            "error": f"판례 검색 중 오류 발생: {str(e)}",
            "recovery_guide": "시스템 오류가 발생했습니다. 서버 로그를 확인하거나 관리자에게 문의하세요."
        }


# After
from ..core.error_handler import handle_api_errors, convert_to_error_dict
from ..core.exceptions import ToolExecutionError

@handle_api_errors
@convert_to_error_dict
async def search_precedent(self, req: SearchPrecedentRequest, arguments: Optional[dict] = None) -> dict:
    if arguments is None:
        arguments = {}
    
    if req.use_fallback or req.issue_type or req.must_include:
        issue_type = req.issue_type or self._infer_issue_type(req.query)
        result = await self.search_precedent_with_fallback(...)
        return result
    
    return await asyncio.to_thread(...)
```

---

### 단계 4: 저장소 계층 에러 처리 개선 (1 시간)

**적용 파일**:
- `src/repositories/base.py`
- `src/repositories/precedent_repository.py`

**적용 예시**:

```python
# Before (base.py)
try:
    response = requests.get(LAW_API_SEARCH_URL, params=params, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    return {"error": "API 호출 타임아웃", ...}
except requests.exceptions.RequestException as e:
    return {"error": f"API 요청 실패: {str(e)}", ...}


# After
from ..core.exceptions import APITimeoutError, APIAuthError, APINotFoundError

try:
    response = requests.get(LAW_API_SEARCH_URL, params=params, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    raise APITimeoutError("법령 검색 API 타임아웃")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        raise APIAuthError("API 키 인증 실패")
    elif e.response.status_code == 404:
        raise APINotFoundError("법령 검색 API 엔드포인트 없음")
    raise
```

---

### 단계 5: ToolRouter 에러 처리 통합 (30 분)

**파일**: `src/routes/tool_router.py`

```python
# 현재 코드
async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if name == "health":
            return await self.health_service.check_health()
        # ... 다른 도구들
        else:
            return {"error": f"Unknown tool: {name}", "error_code": "UNKNOWN_TOOL"}
    
    except Exception as e:
        return {
            "error": f"도구 호출 중 오류 발생: {str(e)}",
            "error_code": "TOOL_EXECUTION_ERROR",
            "tool_name": name,
        }


# 개선 후
from ..core.error_handler import convert_to_error_dict
from ..core.exceptions import ToolExecutionError

@convert_to_error_dict
async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name not in [t["name"] for t in self.tool_definitions]:
        raise ToolExecutionError(f"알 수 없는 도구: {name}", name)
    
    # 도구 호출 로직...
```

---

### 단계 6: 테스트 작성 (30 분)

**파일**: `tests/test_exceptions.py` (신규)

```python
"""
Tests for Exception Handling
"""
import pytest
from src.core.exceptions import (
    LawMCPError,
    APITimeoutError,
    APIAuthError,
    APINotFoundError,
    ToolExecutionError,
)
from src.core.error_handler import handle_api_errors, convert_to_error_dict


class TestExceptions:
    """예외 클래스 테스트"""
    
    def test_law_mcp_error_basic(self):
        """기본 예외 테스트"""
        error = LawMCPError("테스트 오류", "TEST_ERROR")
        assert error.message == "테스트 오류"
        assert error.code == "TEST_ERROR"
        assert error.recovery_guide is not None
    
    def test_law_mcp_error_to_dict(self):
        """딕셔너리 변환 테스트"""
        error = LawMCPError("테스트", "TEST_ERROR")
        result = error.to_dict()
        assert "error" in result
        assert "error_code" in result
        assert "recovery_guide" in result
    
    def test_api_timeout_error(self):
        """타임아웃 에러 테스트"""
        error = APITimeoutError()
        assert error.code == "API_ERROR_TIMEOUT"
        assert "타임아웃" in error.message
    
    def test_api_auth_error(self):
        """인증 에러 테스트"""
        error = APIAuthError()
        assert error.code == "API_ERROR_AUTH"
    
    def test_tool_execution_error(self):
        """도구 실행 에러 테스트"""
        error = ToolExecutionError("오류 발생", "test_tool")
        assert error.code == "TOOL_EXECUTION_ERROR"
        assert "test_tool" in error.message


class TestErrorHandler:
    """에러 핸들러 테스트"""
    
    @pytest.mark.asyncio
    async def test_handle_api_errors_timeout(self):
        """API 타임아웃 에러 처리"""
        import requests
        
        @handle_api_errors
        async def test_func():
            raise requests.exceptions.Timeout()
        
        with pytest.raises(APITimeoutError):
            await test_func()
    
    @pytest.mark.asyncio
    async def test_convert_to_error_dict(self):
        """에러 딕셔너리 변환"""
        
        @convert_to_error_dict
        async def test_func():
            raise LawMCPError("테스트", "TEST_ERROR")
        
        result = await test_func()
        assert "error" in result
        assert result["error_code"] == "TEST_ERROR"
```

---

## 📋 체크리스트

작업 완료 후 다음 항목을 확인하세요:

### 코드 품질
- [ ] 모든 예외 클래스가 `LawMCPError` 를 상속받는가?
- [ ] 에러 핸들러 데코레이터가 모든 서비스에 적용되었는가?
- [ ] ToolRouter 에서 일관된 에러 처리가 되는가?

### 테스트
- [ ] 예외 클래스 테스트가 통과하는가?
- [ ] 에러 핸들러 테스트가 통과하는가?
- [ ] 기존 테스트가 여전히 통과하는가?

### 문서화
- [ ] 에러 코드 목록이 문서화되었는가?
- [ ] 복구 가이드가 모든 에러에 있는가?

---

## 🎯 완료 기준

다음 조건을 모두 만족하면 작업 완료입니다:

1. ✅ `src/core/exceptions.py` 에 예외 계층 구현
2. ✅ `src/core/error_handler.py` 에 데코레이터 구현
3. ✅ 모든 서비스에 에러 핸들러 적용
4. ✅ ToolRouter 에서 일관된 에러 처리
5. ✅ 테스트 10 개 이상 작성 및 통과
6. ✅ 기존 테스트 모두 통과

---

## 📚 참고 자료

- **이슈**: GITHUB_ISSUES.md Issue #4
- **분석 보고서**: ANALYSIS_REPORT.md 섹션 3.2
- **관련 파일**: `src/services/*.py`, `src/repositories/*.py`

---

## 💡 Codex 에게 추가 요청할 작업

작업 완료 후 다음을 요청하세요:

1. **코드 리뷰**: "생성된 exceptions.py 와 error_handler.py 를 리뷰해주세요"
2. **테스트 실행**: "pytest tests/test_exceptions.py -v 를 실행해주세요"
3. **적용 검증**: "모든 서비스에 데코레이터가 적용되었는지 확인해주세요"

---

**작업 시작!** 🚀
