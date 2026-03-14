# ChatGPT MCP 설정

## ChatGPT Developer Mode 에서 MCP 추가

1. ChatGPT Settings → Developer Mode → MCP Servers

2. **Add New MCP Server** 클릭

3. 아래 설정 입력:
   - **Name**: `kr-law-mcq`
   - **URL**: `https://law-open-data-dedicated-mcp.onrender.com/mcp`

4. **Save** 클릭

## 수동 설정 (config.json)

설정 파일 위치:
- **Windows**: `%APPDATA%\ChatGPT\config.json`
- **macOS**: `~/Library/Application Support/ChatGPT/config.json`
- **Linux**: `~/.config/ChatGPT/config.json`

```json
{
  "mcpServers": {
    "kr-law-mcq": {
      "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
    }
  }
}
```

## 사용 예시

ChatGPT 에게 다음과 같이 요청:

```
KR-LAW MCQ 프롬프트로 헌법 제 11 조 평등권 판례 분석해줘
TOOL=true, SearchPolicy=yes 로
```

## 제공 도구

- `search_law_tool`: 법령 검색
- `get_law_detail_tool`: 법령 상세 조회
- `get_law_article_tool`: 조문 단건 조회
- `search_precedent_tool`: 판례 검색
- `get_precedent_tool`: 판례 상세 조회
- `search_constitutional_decision_tool`: 헌재결정 검색
- `get_constitutional_decision_tool`: 헌재결정 상세 조회
- `search_administrative_appeal_tool`: 행정심판 검색
- `get_administrative_appeal_tool`: 행정심판 상세 조회
- `search_administrative_rule_tool`: 행정규칙 검색
- `search_law_interpretation_tool`: 법령해석 검색
- `get_law_interpretation_tool`: 법령해석 상세 조회
