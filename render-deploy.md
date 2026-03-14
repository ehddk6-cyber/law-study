# Render 배포 가이드

## GitHub 저장소
https://github.com/ehddk6-cyber/law-study

## Render 배포 절차

1. https://render.com 접속 → 로그인

2. **New +** → **Web Service** 클릭

3. **Connect a repository** → GitHub 선택

4. `ehddk6-cyber/law-study` 저장소 선택

5. 설정 입력:
   - **Name**: `law-open-data-dedicated-mcp`
   - **Region**: `Singapore` (권장) 또는 `Tokyo`
   - **Branch**: `main`
   - **Root Directory**: (비워둠)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m src.main`
   - **Instance Type**: `Free`

6. **Environment Variables** 추가:
   ```
   PORT=8099
   LAW_API_KEY=da
   LOG_LEVEL=INFO
   RELOAD=false
   ```

7. **Create Web Service** 클릭

## 배포 후

1. 배포 완료되면 URL 발급 (예: `https://law-open-data-dedicated-mcp.onrender.com`)

2. MCP 엔드포인트: `https://law-open-data-dedicated-mcp.onrender.com/mcp`

3. ChatGPT MCP 설정:
   ```json
   {
     "mcpServers": {
       "kr-law-mcq": {
         "url": "https://law-open-data-dedicated-mcp.onrender.com/mcp"
       }
     }
   }
   ```

## 주의사항

- Free Plan 은 15 분 유휴 시 슬립 (첫 요청 시 웨이킹)
- LAW_API_KEY 는 실제 국가법령정보센터 API 키 사용 권장
