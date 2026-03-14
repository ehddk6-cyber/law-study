# MCP 클라이언트 설정 가이드

## ✅ 배포 완료된 서버

**URL**: `https://law-open-data-dedicated-mcp.onrender.com/mcp`

**상태**: 정상 작동 중 ✅
- 헬스체크: `/health` → OK
- 판례 검색: `search_precedent_tool` → 35 건 반환
- Fallback 로직: 활성화됨

---

## 1. ChatGPT 설정

### 설정 파일 위치
- **Windows**: `%APPDATA%\ChatGPT\config.json`
- **macOS**: `~/Library/Application Support/ChatGPT/config.json`
- **Linux**: `~/.config/ChatGPT/config.json`

### 설정 내용
```json
{
  "mcpServers": {
    "kr-law-mcq": {
      "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
    }
  }
}
```

### 사용 예시
```
KR-LAW MCQ 프롬프트로 헌법 제 11 조 평등권 판례 분석해줘
TOOL=true, SearchPolicy=yes 로
```

---

## 2. Claude 설정

### 설정 파일 위치
- 프로젝트 루트의 `.mcp.json`

### 설정 내용
```json
{
  "mcpServers": {
    "kr-law-mcq": {
      "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
    }
  }
}
```

### 사용 예시
```
행정행위 무효사유 명백성에 대해 search_precedent_tool 로 판례 검색해줘
```

---

## 3. Codex 설정

### 설정 파일 위치
- `.qwen/config.toml`

### 설정 내용
```toml
[mcp_servers.kr_law_mcq]
url = "https://law-open-data-dedicated-mcp.onrender.com/mcp"
```

---

## 🛠️ 제공되는 도구

| 도구명 | 설명 |
|--------|------|
| `search_law_tool` | 법령 검색 |
| `get_law_detail_tool` | 법령 상세 조회 |
| `get_law_article_tool` | 조문 단건 조회 |
| `search_precedent_tool` | 판례 검색 (fallback 포함) |
| `get_precedent_tool` | 판례 상세 조회 |
| `search_constitutional_decision_tool` | 헌재결정 검색 |
| `get_constitutional_decision_tool` | 헌재결정 상세 조회 |
| `search_administrative_appeal_tool` | 행정심판 검색 |
| `get_administrative_appeal_tool` | 행정심판 상세 조회 |
| `search_administrative_rule_tool` | 행정규칙 검색 |
| `search_law_interpretation_tool` | 법령해석 검색 |
| `get_law_interpretation_tool` | 법령해석 상세 조회 |

---

## ⚠️ 주의사항

### Free Plan 슬립
- 15 분 유휴 시 슬립 (첫 요청 시 약 30 초 웨이킹)
- Uptime Robot 등으로 5 분마다 헬스체크 가능

### API 키
- `LAW_API_KEY=da` 설정됨
- 국가법령정보센터 실사용 시 유효한 키로 교체 권장

---

## 🧪 검증 방법

### 헬스체크
```bash
curl https://law-open-data-dedicated-mcp.onrender.com/health
```

### 판례 검색 테스트
```bash
curl -X POST https://law-open-data-dedicated-mcp.onrender.com/tools/search_precedent_tool \
  -H "Content-Type: application/json" \
  -d '{"query":"행정행위 무효 명백성","per_page":3}'
```

### MCP tools/list
```bash
curl -X POST https://law-open-data-dedicated-mcp.onrender.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```
