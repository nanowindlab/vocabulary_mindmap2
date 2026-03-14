# Weather To Kakao Automation

주중 오전 6시 30분에 날씨를 카카오톡으로 보내려면 아래 순서로 설정하면 된다.

## 1. 환경변수 준비

`.env.weather.example` 값을 참고해서 아래 환경변수를 준비한다.

- `OPEN_METEO_LAT`
- `OPEN_METEO_LON`
- `WEATHER_LOCATION_NAME`
- `WEATHER_LINK` (선택)
- `KAKAO_REST_API_KEY`
- `KAKAO_REFRESH_TOKEN`
- `KAKAO_CLIENT_SECRET` (선택)

카카오 메시지 전송은 Kakao Developers에서 `나에게 보내기` 권한이 포함된 OAuth 토큰이 필요하다.

## 2. 로컬 확인

```bash
cd /Users/nanowind/Library/CloudStorage/SynologyDrive-Work/Project/AI/antigravity/vocabulary_mindmap2
export $(grep -v '^#' .env.weather | xargs)
python3 scripts/weather_kakao.py --dry-run
python3 scripts/weather_kakao.py
```

첫 번째 명령은 메시지 내용을 콘솔에서만 확인하고, 두 번째 명령이 실제 카카오톡 전송이다.

## 3. Codex 예약 실행

Codex 자동화에서 아래 작업을 주중 오전 6시 30분으로 걸면 된다.

- 작업: `python3 scripts/weather_kakao.py` 실행
- 주기: 월요일~금요일, 06:30
- 작업 폴더: `/Users/nanowind/Library/CloudStorage/SynologyDrive-Work/Project/AI/antigravity/vocabulary_mindmap2`

## 4. 주의

- Kakao access token은 짧게 만료되므로 refresh token 기반으로 매 실행마다 재발급한다.
- refresh token이 새로 내려오면 스크립트가 콘솔에 교체 안내를 출력한다.
- Open-Meteo는 위도/경도 기반이라 도시명을 직접 검색하지 않는다.
