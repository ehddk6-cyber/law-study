# LAW-STUDY - AI Agent 연동 가이드

## 📖 프로젝트 개요

**LAW-STUDY**는 대한민국 헌법·행정법 객관식 시험 대비를 위한 MCP 서버입니다.

- **URL**: `https://law-open-data-dedicated-mcp.onrender.com/mcp`
- **프로토콜**: MCP (Model Context Protocol)
- **언어**: Python 3.10+
- **테스트**: 46 개 통과 (pytest)

---

## 🔌 연동 방법

### 1. MCP 프로토콜 지원 에이전트

#### Claude (Anthropic)
```json
{
  "mcpServers": {
    "kr-law-mcq": {
      "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
    }
  }
}
```

#### ChatGPT (OpenAI)
```json
{
  "mcpServers": {
    "kr-law-mcq": {
      "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
    }
  }
}
```

#### Codex (Qwen)
```toml
[mcp_servers.kr_law_mcq]
url = "https://law-open-data-dedicated-mcp.onrender.com/mcp"
```

### 2. HTTP API 직접 호출

```bash
# 헬스체크
curl https://law-open-data-dedicated-mcp.onrender.com/health

# 판례 검색
curl -X POST https://law-open-data-dedicated-mcp.onrender.com/tools/search_precedent_tool \
  -H "Content-Type: application/json" \
  -d '{"query":"행정행위 무효 명백성","per_page":5}'

# 조문 조회
curl -X POST https://law-open-data-dedicated-mcp.onrender.com/tools/get_law_article_tool \
  -H "Content-Type: application/json" \
  -d '{"law_name":"행정절차법","article_number":"제 21 조"}'
```

---

## 🛠️ 제공되는 API

### 법령 관련

| 엔드포인트 | 메서드 | 설명 |
|----------|------|------|
| `/tools/search_law_tool` | POST | 법령 검색 |
| `/tools/get_law_detail_tool` | POST | 법령 상세 조회 |
| `/tools/get_law_article_tool` | POST | 조문 단건 조회 |

### 판례 관련

| 엔드포인트 | 메서드 | 설명 |
|----------|------|------|
| `/tools/search_precedent_tool` | POST | 판례 검색 (fallback 포함) |
| `/tools/get_precedent_tool` | POST | 판례 상세 조회 |

### 헌법 관련

| 엔드포인트 | 메서드 | 설명 |
|----------|------|------|
| `/tools/search_constitutional_decision_tool` | POST | 헌재결정 검색 |
| `/tools/get_constitutional_decision_tool` | POST | 헌재결정 상세 조회 |

### 행정법 관련

| 엔드포인트 | 메서드 | 설명 |
|----------|------|------|
| `/tools/search_administrative_appeal_tool` | POST | 행정심판 검색 |
| `/tools/search_administrative_rule_tool` | POST | 행정규칙 검색 |
| `/tools/search_law_interpretation_tool` | POST | 법령해석 검색 |

---

## 📝 사용 예시

### 예시 1: 판례 검색

```python
import requests

response = requests.post(
    "https://law-open-data-dedicated-mcp.onrender.com/tools/search_precedent_tool",
    json={
        "query": "행정행위 무효 명백성",
        "per_page": 5
    }
)

result = response.json()
print(f"Total: {result['total']}")
print(f"Fallback used: {result.get('fallback_used')}")
for p in result.get('precedents', [])[:3]:
    print(f"  - {p.get('사건명')}")
```

### 예시 2: 조문 조회

```python
import requests

response = requests.post(
    "https://law-open-data-dedicated-mcp.onrender.com/tools/get_law_article_tool",
    json={
        "law_name": "행정절차법",
        "article_number": "제 21 조"
    }
)

result = response.json()
print(result.get('content'))
```

### 예시 3: MCP 프로토콜 사용

```python
# MCP initialize
requests.post(
    "https://law-open-data-dedicated-mcp.onrender.com/mcp",
    json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "my-agent", "version": "1.0"}
        }
    }
)

# tools/list
requests.post(
    "https://law-open-data-dedicated-mcp.onrender.com/mcp",
    json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
)

# tools/call
requests.post(
    "https://law-open-data-dedicated-mcp.onrender.com/mcp",
    json={
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "search_precedent_tool",
            "arguments": {"query": "행정행위 무효 명백성"}
        }
    }
)
```

---

## 🧪 테스트

```bash
# 단위 테스트 실행
pytest tests/ -v -m "not integration"

# 통합 테스트 실행 (API 키 필요)
pytest tests/ -m integration

# 커버리지 리포트
pytest tests/ --cov=src --cov-report=html
```

---

## 🔧 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `LAW_API_KEY` | 국가법령정보센터 API 키 | `da` |
| `PORT` | 서버 포트 | `8099` |
| `LOG_LEVEL` | 로그 레벨 | `INFO` |

---

## 📚 추가 리소스

- [GitHub 저장소](https://github.com/ehddk6-cyber/law-study)
- [Render 배포](https://law-open-data-dedicated-mcp.onrender.com)
- [CLAUDE.md](CLAUDE.md) - Claude 연동 가이드
- [README.md](README.md) - 프로젝트 개요

---

## ⚠️ 주의사항

- **Free Plan 슬립**: 15 분 유휴 시 슬립 (첫 요청 시 약 30 초 웨이킹)
- **API 키**: 현재 `LAW_API_KEY=da` 설정됨 (실사용 시 유효한 키로 교체 권장)
- **한국어 전용**: 한국어 법률 용어에 최적화되어 있습니다
