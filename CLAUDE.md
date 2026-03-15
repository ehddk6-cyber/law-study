# LAW-STUDY - Claude 연동 가이드

## 📖 프로젝트 개요

**LAW-STUDY**는 대한민국 헌법·행정법 객관식 시험 대비를 위한 MCP 서버입니다.

- **주요 기능**: 법령 검색, 판례 검색, 헌재결정 검색, 행정심판 검색
- **검색 엔진**: 4 단계 fallback, 동의어 확장, 행정법 특화 쿼리 생성
- **배포**: Render 에서 실제 구동 중
- **테스트**: pytest 기반 46 개 테스트 통과

---

## 🚀 빠른 시작

### 1. MCP 서버 설정

Claude Desktop 설정 파일에 다음을 추가하세요:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kr-law-mcq": {
      "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
    }
  }
}
```

### 2. 사용 예시

#### 판례 검색

```
"행정행위 무효 명백성"에 대한 대법원 판례를 search_precedent_tool 로 검색해줘
TOOL=true, SearchPolicy=yes 로
```

#### 조문 조회

```
행정절차법 제 21 조를 get_law_article_tool 로 조회해줘
```

#### 헌재결정 검색

```
헌법 제 11 조 평등권 관련 헌재결정을 search_constitutional_decision_tool 로 찾아줘
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
| `search_administrative_rule_tool` | 행정규칙 검색 |
| `search_law_interpretation_tool` | 법령해석 검색 |

---

## 📝 KR-LAW MCQ 프롬프트와 함께 사용하기

LAW-STUDY 는 다음과 같은 객관식 학습 프롬프트와 함께 사용하도록 설계되었습니다:

```
<instructions>
# MISSION
너는 대한민국 헌법·행정법 객관식 학습 코치이다.

# RULES
- TOOL=true 일 때 MCP 도구를 사용하여 법령·판례 검증
- 조문 번호, 판례 번호는 반드시 도구로 확인
- 불확실하면 [NEEDS_VERIFICATION] 표시
</instructions>

Query: {{문제/선지}}
TOOL: true
SearchPolicy: yes
```

---

## 🧪 테스트 실행

```bash
# 전체 테스트
pytest tests/ -v

# 특정 테스트
pytest tests/test_query_planner.py -v

# 통합 테스트 (API 키 필요)
pytest tests/ -m integration
```

---

## 📚 추가 문서

- [DEPLOY.md](DEPLOY.md) - Render 배포 가이드
- [MCP-SETUP.md](MCP-SETUP.md) - MCP 클라이언트 설정
- [README.md](README.md) - 프로젝트 개요

---

## ⚠️ 주의사항

- **Free Plan 슬립**: 15 분 유휴 시 슬립 (첫 요청 시 약 30 초 웨이킹)
- **API 키**: 현재 `LAW_API_KEY=da` 설정됨 (실사용 시 유효한 키로 교체 권장)
- **한국어 전용**: 한국어 법률 용어에 최적화되어 있습니다
