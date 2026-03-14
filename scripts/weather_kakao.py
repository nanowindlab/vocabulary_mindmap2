#!/usr/bin/env python3
"""Fetch today's weather summary and send it to KakaoTalk."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


SEOUL_TZ = ZoneInfo("Asia/Seoul")
DEFAULT_LINK = "https://www.weather.go.kr/w/index.do"

WEATHER_CODE_LABELS = {
    0: "맑음",
    1: "대체로 맑음",
    2: "부분적으로 흐림",
    3: "흐림",
    45: "안개",
    48: "서리 안개",
    51: "약한 이슬비",
    53: "이슬비",
    55: "강한 이슬비",
    56: "약한 어는 이슬비",
    57: "강한 어는 이슬비",
    61: "약한 비",
    63: "비",
    65: "강한 비",
    66: "약한 어는 비",
    67: "강한 어는 비",
    71: "약한 눈",
    73: "눈",
    75: "강한 눈",
    77: "진눈깨비",
    80: "약한 소나기",
    81: "소나기",
    82: "강한 소나기",
    85: "약한 눈 소나기",
    86: "강한 눈 소나기",
    95: "뇌우",
    96: "약한 우박 동반 뇌우",
    99: "강한 우박 동반 뇌우",
}


@dataclass
class Config:
    latitude: float
    longitude: float
    location_name: str
    kakao_rest_api_key: str
    kakao_refresh_token: str
    kakao_client_secret: str | None
    weather_link: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch today's weather and send it to KakaoTalk."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the weather summary without calling Kakao APIs.",
    )
    return parser.parse_args()


def load_config() -> Config:
    missing = []

    def getenv(name: str, default: str | None = None) -> str | None:
        value = os.getenv(name, default)
        if value is None or value == "":
            if default is None:
                missing.append(name)
            return None
        return value

    latitude_raw = getenv("OPEN_METEO_LAT")
    longitude_raw = getenv("OPEN_METEO_LON")
    kakao_rest_api_key = getenv("KAKAO_REST_API_KEY")
    kakao_refresh_token = getenv("KAKAO_REFRESH_TOKEN")

    if missing:
        raise SystemExit(
            "Missing required environment variables: " + ", ".join(sorted(missing))
        )

    try:
        latitude = float(latitude_raw)  # type: ignore[arg-type]
        longitude = float(longitude_raw)  # type: ignore[arg-type]
    except ValueError as exc:
        raise SystemExit("OPEN_METEO_LAT and OPEN_METEO_LON must be valid numbers.") from exc

    return Config(
        latitude=latitude,
        longitude=longitude,
        location_name=os.getenv("WEATHER_LOCATION_NAME", "서울"),
        kakao_rest_api_key=kakao_rest_api_key or "",
        kakao_refresh_token=kakao_refresh_token or "",
        kakao_client_secret=os.getenv("KAKAO_CLIENT_SECRET"),
        weather_link=os.getenv("WEATHER_LINK", DEFAULT_LINK),
    )


def http_json(
    url: str,
    *,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> dict:
    request = urllib.request.Request(url, data=data, method=method)
    for key, value in (headers or {}).items():
        request.add_header(key, value)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} calling {url}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error calling {url}: {exc}") from exc


def fetch_weather(config: Config) -> dict:
    params = {
        "latitude": config.latitude,
        "longitude": config.longitude,
        "timezone": "Asia/Seoul",
        "current": "temperature_2m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)
    return http_json(url)


def weather_label(code: int | None) -> str:
    if code is None:
        return "정보 없음"
    return WEATHER_CODE_LABELS.get(code, f"코드 {code}")


def build_message(config: Config, weather: dict) -> str:
    current = weather.get("current", {})
    daily = weather.get("daily", {})

    today = datetime.now(SEOUL_TZ).strftime("%Y-%m-%d (%a)")
    current_temp = current.get("temperature_2m")
    current_code = current.get("weather_code")

    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    daily_codes = daily.get("weather_code", [])
    precip_probs = daily.get("precipitation_probability_max", [])

    max_temp = max_temps[0] if max_temps else None
    min_temp = min_temps[0] if min_temps else None
    daily_code = daily_codes[0] if daily_codes else None
    precip = precip_probs[0] if precip_probs else None

    lines = [
        f"[{config.location_name} 날씨] {today}",
        f"현재: {current_temp}°C, {weather_label(current_code)}",
        f"오늘: 최저 {min_temp}°C / 최고 {max_temp}°C, {weather_label(daily_code)}",
        f"강수확률: {precip}%",
        "",
        f"상세 보기: {config.weather_link}",
    ]
    return "\n".join(lines)


def refresh_access_token(config: Config) -> tuple[str, str | None]:
    form = {
        "grant_type": "refresh_token",
        "client_id": config.kakao_rest_api_key,
        "refresh_token": config.kakao_refresh_token,
    }
    if config.kakao_client_secret:
        form["client_secret"] = config.kakao_client_secret

    payload = urllib.parse.urlencode(form).encode("utf-8")
    data = http_json(
        "https://kauth.kakao.com/oauth/token",
        method="POST",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    access_token = data.get("access_token")
    if not access_token:
        raise RuntimeError("Kakao token refresh response did not include access_token.")
    return access_token, data.get("refresh_token")


def send_kakao_message(access_token: str, text: str, weather_link: str) -> dict:
    template_object = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": weather_link,
            "mobile_web_url": weather_link,
        },
        "button_title": "날씨 보기",
    }
    payload = urllib.parse.urlencode(
        {"template_object": json.dumps(template_object, ensure_ascii=False)}
    ).encode("utf-8")
    return http_json(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        method="POST",
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )


def main() -> int:
    args = parse_args()
    config = load_config()
    weather = fetch_weather(config)
    message = build_message(config, weather)

    if args.dry_run:
        print(message)
        return 0

    access_token, new_refresh_token = refresh_access_token(config)
    response = send_kakao_message(access_token, message, config.weather_link)

    print("Kakao response:", json.dumps(response, ensure_ascii=False))
    if new_refresh_token:
        print(
            "Kakao issued a new refresh token. Replace KAKAO_REFRESH_TOKEN in your environment."
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
