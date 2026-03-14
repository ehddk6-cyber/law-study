# Render 배포 가이드

## 📋 사전 준비

- ✅ GitHub 저장소: https://github.com/ehddk6-cyber/law-study
- ✅ render.yaml 설정 완료
- ✅ LAW_API_KEY: `da`

---

## 🚀 Render 배포 절차

### 1. Render 로그인 및 대시보드 접속

1. https://render.com 접속
2. GitHub 계정으로 로그인 (권장) 또는 이메일 로그인

### 2. Web Service 생성

1. **New +** 버튼 클릭
2. **Web Service** 선택

### 3. 저장소 연결

1. **Connect a repository** 섹션에서 GitHub 선택
2. `ehddk6-cyber/law-study` 저장소 검색 및 선택
3. **Connect selected repository** 클릭

### 4. 설정 입력

| 항목 | 값 |
|------|-----|
| **Name** | `law-open-data-dedicated-mcp` |
| **Region** | `Singapore` (한국과 가장 가까움) |
| **Branch** | `main` |
| **Root Directory** | (비워둠) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python -m src.main` |
| **Instance Type** | `Free` |

### 5. 환경변수 설정

**Environment Variables** 섹션에서 다음 추가:

| Key | Value |
|-----|-------|
| `PORT` | `8099` |
| `LAW_API_KEY` | `da` |
| `LOG_LEVEL` | `INFO` |
| `RELOAD` | `false` |

### 6. 배포 시작

1. **Create Web Service** 클릭
2. 배포 진행 (약 3~5 분 소요)

---

## ✅ 배포 완료 후

### 1. URL 확인

배포 완료되면 다음과 같은 URL 이 발급됩니다:

```
https://law-open-data-dedicated-mcp.onrender.com
```

### 2. MCP 엔드포인트

```
https://law-open-data-dedicated-mcp.onrender.com/mcp
```

### 3. 헬스체크

```bash
curl https://law-open-data-dedicated-mcp.onrender.com/health
```

---

## 🔧 MCP 클라이언트 설정

### ChatGPT

`chatgpt-mcp-settings.json` 수정:

```json
{
  "mcpServers": {
    "kr-law-mcq": {
      "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
    }
  }
}
```

### Claude

`.mcp.json` 수정:

```json
{
  "mcpServers": {
    "kr-law-mcq": {
      "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
    }
  }
}
```

### Codex

`.qwen/config.toml` 수정:

```toml
[mcp_servers.kr_law_mcq]
url = "https://law-open-data-dedicated-mcp.onrender.com/mcp"
```

---

## ⚠️ Free Plan 주의사항

- **15 분 유휴 시 슬립**: 첫 요청 시 웨이킹 (약 30 초 소요)
- **월 750 시간 무료**: 하루 24 시간 × 31 일 = 744 시간 (충분함)
- **자동 슬립 방지**: Uptime Robot 등으로 5 분마다 헬스체크 요청 가능

---

## 🐛 문제 해결

### 빌드 실패

- `requirements.txt` 확인
- Python 버전 호환성 확인 (3.8+)

### 런타임 오류

- Render 대시보드 → **Logs** 탭 확인
- 환경변수 설정 확인

### API 키 오류

- `LAW_API_KEY` 환경변수 재설정
- 국가법령정보센터 API 키 유효성 확인

---

## 📝 참고 파일

- `render.yaml`: 배포 설정
- `requirements.txt`: Python 의존성
- `.env`: 로컬 환경변수 (업로드 금지)
