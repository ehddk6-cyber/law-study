# LAW-STUDY 프로젝트 분석 가이드 (Codex 용)

## 📋 프로젝트 개요

**LAW-STUDY**는 대한민국 헌법·행정법 객관식 시험 대비를 위한 MCP 서버입니다.

- **저장소**: https://github.com/ehddk6-cyber/law-study
- **배포 URL**: https://law-open-data-dedicated-mcp.onrender.com
- **MCP 엔드포인트**: `https://law-open-data-dedicated-mcp.onrender.com/mcp`
- **언어**: Python 3.10+
- **테스트**: 70 개 통과 (pytest)

---

## 🎯 Codex 에게 분석시킬 작업

### 1 단계: 프로젝트 구조 이해

```markdown
다음 파일을 순서대로 읽어주세요:

1. README.md - 프로젝트 개요 및 기능
2. src/main.py - 앱 진입점
3. src/routes/mcp_routes.py - MCP 프로토콜 구현
4. src/services/ - 비즈니스 로직
5. src/repositories/ - 데이터 액세스 계층
6. tests/ - 테스트 코드
```

### 2 단계: 기능 분석

```markdown
다음 기능을 분석해주세요:

1. **법령 검색 기능**
   - search_law_tool, get_law_detail_tool, get_law_article_tool
   - 국가법령정보센터 API 연동 구조

2. **판례 검색 기능**
   - search_precedent_tool (4 단계 fallback)
   - get_precedent_tool
   - 검색어 최적화 로직 (utils/query_planner.py)

3. **컴플라이언스 기능** (NEW)
   - get_compliance_calendar_tool
   - get_compliance_checklist_tool
   - compliance_calendar.py, compliance_checklists.py

4. **기타 법률 기능**
   - 헌재결정, 행정심판, 행정규칙, 법령해석
```

### 3 단계: 코드 품질 평가

```markdown
다음 항목을 평가해주세요:

1. **테스트 커버리지**
   - 현재 70 개 테스트 통과
   - 누락된 테스트 영역 식별

2. **코드 구조**
   - 계층화 (routes → services → repositories)
   - 의존성 주입 패턴

3. **에러 처리**
   - API 에러 처리
   - 유효성 검사

4. **성능**
   - 캐싱 사용 (cachetools)
   - 비동기 처리
```

### 4 단계: 개선 제안

```markdown
다음 관점에서 개선을 제안해주세요:

1. **기능적 개선**
   - 추가하면 좋은 법률 도구
   - UI/UX 개선사항

2. **기술적 개선**
   - 리팩토링이 필요한 부분
   - 성능 최적화 방안

3. **테스트 개선**
   - 추가해야 할 테스트 케이스
   - 통합 테스트 방안

4. **문서화 개선**
   - 보완할 문서
   - 사용 예시 추가
```

---

## 📁 주요 파일 목록

### 핵심 파일

| 파일 | 역할 | 라인수 |
|------|------|--------|
| `src/main.py` | 앱 진입점 | ~30 |
| `src/routes/mcp_routes.py` | MCP 프로토콜 | ~300 |
| `src/routes/http_routes.py` | HTTP API | ~150 |
| `src/services/compliance_service.py` | 컴플라이언스 로직 | ~140 |
| `src/repositories/compliance_calendar.py` | 캘린더 데이터 | ~250 |
| `src/repositories/compliance_checklists.py` | 체크리스트 데이터 | ~400 |
| `src/utils/query_planner.py` | 검색어 최적화 | ~400 |

### 테스트 파일

| 파일 | 테스트수 | 내용 |
|------|---------|------|
| `tests/test_query_planner.py` | 28 | 키워드 추출, 행정법 쿼리 |
| `tests/test_fallback.py` | 10 | fallback 전략 |
| `tests/test_search_precedent.py` | 8 | 판례 검색 스키마 |
| `tests/test_compliance.py` | 24 | 캘린더, 체크리스트 |

---

## 🔧 MCP 도구 목록

### 법률 검색 도구 (13 개)

1. `search_law_tool` - 법령 검색
2. `get_law_detail_tool` - 법령 상세
3. `get_law_article_tool` - 조문 조회
4. `search_precedent_tool` - 판례 검색
5. `get_precedent_tool` - 판례 상세
6. `search_constitutional_decision_tool` - 헌재결정
7. `get_constitutional_decision_tool` - 헌재결정 상세
8. `search_administrative_appeal_tool` - 행정심판
9. `get_administrative_appeal_tool` - 행정심판 상세
10. `search_administrative_rule_tool` - 행정규칙
11. `search_law_interpretation_tool` - 법령해석
12. `get_law_interpretation_tool` - 법령해석 상세

### 컴플라이언스 도구 (2 개)

13. `get_compliance_calendar_tool` - 캘린더
14. `get_compliance_checklist_tool` - 체크리스트

---

## 🧪 테스트 실행 방법

```bash
# 전체 테스트
pytest tests/ -v

# 특정 테스트
pytest tests/test_compliance.py -v

# 커버리지
pytest tests/ --cov=src --cov-report=html

# 통합 테스트 제외
pytest tests/ -v -m "not integration"
```

---

## 📊 프로젝트 통계

| 항목 | 수치 |
|------|------|
| **Python 파일** | 39 개 |
| **테스트 파일** | 4 개 |
| **테스트 케이스** | 70 개 |
| **MCP 도구** | 15 개 |
| **컴플라이언스 체크리스트** | 7 종류 |
| **컴플라이언스 이벤트** | 10+ 개 |
| **코드 라인** | ~3,000+ |

---

## 🎯 Codex 분석 후 기대 효과

1. **객관적 코드 품질 평가**
2. **발견하지 못한 버그 식별**
3. **성능 병목 지점 발견**
4. **테스트 커버리지 향상 방안**
5. **리팩토링 우선순위 설정**
6. **새로운 기능 아이디어**

---

## 📝 Codex 에게 줄 프롬프트 예시

### 예시 1: 전체 분석

```
이 프로젝트의 전체 구조를 분석해주세요.

1. 폴더 구조와 각 역할
2. 주요 컴포넌트 간 의존성
3. 데이터 흐름 (API 요청 → 응답)
4. 현재 아키텍처의 장단점

파일을 차근차근 읽어보고 상세히 보고해주세요.
```

### 예시 2: 특정 기능 분석

```
컴플라이언스 기능을 집중 분석해주세요.

1. compliance_calendar.py 의 이벤트 관리 로직
2. compliance_checklists.py 의 체크리스트 구조
3. MCP 도구 연동 방식
4. 테스트 커버리지 충분성

개선할 점이 있으면 구체적으로 제안해주세요.
```

### 예시 3: 성능 최적화

```
이 프로젝트의 성능 병목 지점을 찾아주세요.

1. API 호출 최적화 방안
2. 캐싱 전략 개선
3. 데이터베이스/저장소 최적화
4. 비동기 처리 확대 방안

구체적인 코드 수정 예시까지 제안해주세요.
```

---

## 🔗 참고 문서

- [README.md](README.md) - 프로젝트 개요
- [DEPLOY.md](DEPLOY.md) - 배포 가이드
- [MCP-SETUP.md](MCP-SETUP.md) - MCP 설정
- [CLAUDE.md](CLAUDE.md) - Claude 연동
- [AGENTS.md](AGENTS.md) - AI Agent 연동

---

## ✅ 분석 완료 후 다음 단계

1. **개선 작업 우선순위 설정**
2. **이슈 트래커 등록**
3. **단계적 구현 계획**
4. **테스트 추가/보완**
