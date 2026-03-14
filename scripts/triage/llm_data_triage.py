import argparse
import json
import os
import tempfile
import time
from collections import Counter
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "05_source" / "extracted_corpus" / "snapshot_20260309"
OUTPUT_DIR = ROOT / "09_app" / "public" / "data"
EXPANSION_DIR = ROOT / "08_expansion"
QUARANTINE_DIR = EXPANSION_DIR / "triage_quarantine"
RUN_REPORT_DIR = EXPANSION_DIR / "triage_reports"
CHECKPOINT_FILE = RUN_REPORT_DIR / "llm_data_triage_checkpoint.json"
LATEST_REPORT_FILE = RUN_REPORT_DIR / "llm_data_triage_latest_report.json"

MEANINGS_FILE = SOURCE_DIR / "Lemma_Meanings.jsonl"
CORE_PAYLOAD = OUTPUT_DIR / "APP_READY_CORE_PAYLOAD_V1.json"
SYSTEM_CANDIDATES = EXPANSION_DIR / "SYSTEM_CANDIDATES_V1.json"
CATEGORY_CANDIDATES = EXPANSION_DIR / "CATEGORY_CANDIDATES_V1.json"
EXCLUDED_WORDS = EXPANSION_DIR / "EXCLUDED_WORDS_V1.json"

DEFAULT_PROVIDER = "gemini"
DEFAULT_MODEL = "gemini-3-flash-preview"
DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"
DEFAULT_FALLBACK_PROVIDER = "openai"
DEFAULT_BATCH_SIZE = 60
DEFAULT_TIMEOUT = 300
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 5

VALID_STATUSES = {"CORE", "SYSTEM_CAND", "CAT_CAND", "EXCLUDED"}
PROPER_NOUN_EXCEPTIONS = {"서울", "부산"}

ROOTS_BY_SYSTEM = {
    "상황과 장소": [
        "사람과 관계",
        "식생활",
        "주거와 일상",
        "쇼핑",
        "교통",
        "학교와 공부",
        "직장과 업무",
        "여가와 취미",
        "여행",
        "보건과 의료",
        "날씨와 자연",
        "공공 서비스",
        "문화와 사회",
        "상황 지시/기타",
    ],
    "마음과 표현": [
        "내면과 감정",
        "성격과 태도",
        "감각과 묘사",
        "의견과 가치",
    ],
    "구조와 기초": [
        "수량과 단위",
        "시간과 흐름",
        "논리와 연결",
        "지시와 질문",
    ],
}
ALL_ROOTS = [root for roots in ROOTS_BY_SYSTEM.values() for root in roots]
ROOT_TO_SYSTEM = {
    root: system
    for system, roots in ROOTS_BY_SYSTEM.items()
    for root in roots
}

ROOT_NEGATIVE_GUIDE = {
    "식생활": ["배탈", "소화액", "치아", "제사상", "집안일", "거실"],
    "사람과 관계": ["가족부", "거실", "병실"],
    "보건과 의료": ["김치", "과자", "가마솥"],
    "감각과 묘사": ["맛", "식감", "입맛", "풍미", "싱겁다"],
    "문화와 사회": ["제사", "제사상", "연회", "파티"],
    "공공 서비스": ["가족부", "구청", "세금"],
}
META_LANGUAGE_TRAPS = ["세포", "문장", "방법", "물음", "표현", "내용"]
HIGH_RISK_BOUNDARY_TERMS = [
    "맛",
    "맛있다",
    "맛없다",
    "식감",
    "입맛",
    "식욕",
    "고프다",
    "배탈",
    "소화",
    "소화액",
    "치아",
    "침",
    "가족부",
    "거실",
    "제사상",
]
BOUNDARY_BODY_CUES = {
    "맛": ["음식", "먹", "혀", "미각", "짠", "달", "싱겁", "맵", "풍미", "식감", "조미"],
    "맛있다": ["음식", "먹", "혀", "미각", "요리", "식사"],
    "맛없다": ["음식", "먹", "혀", "미각", "요리", "식사"],
    "식감": ["음식", "먹", "씹", "혀", "질감", "요리"],
    "입맛": ["음식", "먹", "혀", "식욕", "미각"],
    "식욕": ["음식", "먹", "배고픔", "허기", "욕구"],
    "고프다": ["배", "허기", "배고픔", "식사", "음식"],
    "배탈": ["배", "복통", "설사", "위", "장", "아프"],
    "소화": ["음식", "먹", "위", "장", "흡수", "위장", "영양", "식후", "생리", "신체"],
    "소화액": ["위액", "침", "췌", "장", "위", "소장", "액체", "신체"],
    "치아": ["이", "치과", "잇몸", "입안", "씹"],
    "침": ["입안", "침샘", "타액", "신체", "입"],
    "가족부": ["행정", "부처", "정부", "부서", "기관"],
    "거실": ["집", "방", "주택", "생활 공간", "소파"],
    "제사상": ["제사", "의례", "차례", "전통", "상차림"],
}
BOUNDARY_SAFE_CORE_OVERRIDES = {
    "소화": ["불", "화재", "진화", "끄", "지식", "내용", "이해", "받아들여", "자기 것으로"],
}

STRUCTURAL_ISSUES = {
    "decisions가 리스트가 아님",
    "입력 순서와 출력 순서가 다름",
    "id 중복 존재",
    "입력 id와 출력 id 집합이 다름",
}


def high_risk_boundary_core_violation(item: dict, row: dict) -> bool:
    lemma = item.get("lemma")
    if lemma not in HIGH_RISK_BOUNDARY_TERMS:
        return False
    text = " ".join(
        part
        for part in [
            item.get("meaning_kr"),
            row.get("reason"),
            row.get("rationale_short"),
        ]
        if part
    )
    for safe_cue in BOUNDARY_SAFE_CORE_OVERRIDES.get(lemma, []):
        if safe_cue in text:
            return False
    body_cues = BOUNDARY_BODY_CUES.get(lemma, [])
    if body_cues:
        return any(cue in text for cue in body_cues)
    return True


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_json_atomic(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, dir=str(path.parent)
    ) as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def prefilter_exclusion(item: dict) -> dict | None:
    lemma = item["lemma"]
    pos = item["pos_ko"]
    if pos == "고유명사" and lemma not in PROPER_NOUN_EXCEPTIONS:
        return {
            "id": item["meaning_id"],
            "lemma": lemma,
            "status": "EXCLUDED",
            "system": None,
            "root": None,
            "reason": "고유명사 (인명/지명)",
            "confidence_band": "HIGH",
            "boundary_flags": [],
            "negative_rule_triggered": ["phase0_proper_noun_filter"],
        }
    if pos in {"대명사", "의존명사", "조사", "접속조사"}:
        return {
            "id": item["meaning_id"],
            "lemma": lemma,
            "status": "EXCLUDED",
            "system": None,
            "root": None,
            "reason": "기능적 요소 (대명사/의존명사)",
            "confidence_band": "HIGH",
            "boundary_flags": [],
            "negative_rule_triggered": ["phase0_functional_filter"],
        }
    return None


def build_system_prompt() -> str:
    return f"""너는 한국어 어휘 triage 엔진이다.
목표는 각 meaning inventory를 보수적으로 하나의 상태로 판정하는 것이다.

[상태 정의]
- CORE: system/root가 모두 100% 확실할 때만
- SYSTEM_CAND: 3대 축 자체가 모호할 때
- CAT_CAND: 축은 보이지만 root가 확실하지 않을 때
- EXCLUDED: 고유명사, 대명사, 의존명사, 조사/접속조사 같은 기능 요소

[핵심 규칙]
1. 조금이라도 불확실하면 CORE 금지
2. 문자열 일부 매칭만으로 root를 정하지 말 것
3. meta-language trap `{', '.join(META_LANGUAGE_TRAPS)}` 를 scene root에 자동 배치하지 말 것
4. 맛/감각/내면/신체 경계어 `{', '.join(HIGH_RISK_BOUNDARY_TERMS[:8])}` 는 candidate 우선

[우선순위 규칙]
- 식생활: 음식/식재료/조리도구/조리행위/식당 장면 중심일 때만
- 보건과 의료: 신체 부위/생리 기능/증상/진료 과정 중심이면 우선
- 주거와 일상: 생활 공간/가사 활동 중심이면 우선
- 문화와 사회: 의례/전통/사회 제도 중심이면 우선
- 공공 서비스: 행정 기관/민원/제도 운영 조직 중심이면 우선
- 사람과 관계: 가족/친구/생애 주기 인물 중심일 때만
- 감각과 묘사: 오감 질감/맛/색/상태 서술 중심일 때만
- 내면과 감정: 욕구/감정/심리 상태 중심일 때만
- 의견과 가치: 맞다/틀리다/중요하다 같은 판단 중심일 때만

[대표 금지/경계 예시]
- 식생활 자동 배치 금지: 배탈, 소화액, 치아, 제사상, 집안일
- 사람과 관계 자동 배치 금지: 가족부, 거실
- 감각/내면 경계 예시: 맛, 식감, 입맛, 식욕, 고프다

[반환 규칙]
- JSON object만 반환
- 최상위 키는 반드시 `decisions`만 사용
- 입력 순서 유지, 각 id 정확히 1회
- 모든 decision에 id, lemma, status, reason, confidence_band, boundary_flags, negative_rule_triggered, rationale_short 포함
- CORE는 system/root 필수
- CAT_CAND는 system 필수, root는 null
- SYSTEM_CAND/EXCLUDED는 system/root null 허용
- confidence_band는 HIGH|MEDIUM|LOW만 허용
- system은 `{', '.join(ROOTS_BY_SYSTEM.keys())}` 중 하나만 허용
- root는 `{', '.join(ALL_ROOTS)}` 중 하나만 허용
- `경제`, `상점`, `식생활/주거 일상` 같은 새 분류명을 만들지 말 것
- lemma 자체를 root로 쓰지 말 것
"""


def slim_item_for_llm(item: dict) -> dict:
    return {
        "id": item["meaning_id"],
        "lemma": item["lemma"],
        "pos_ko": item["pos_ko"],
        "meaning_kr": item["meaning_kr"],
    }


def build_user_prompt(batch: list[dict]) -> str:
    slim_batch = [slim_item_for_llm(item) for item in batch]
    return "아래 입력 항목을 순서 그대로 판정하라.\n\n" + json.dumps(
        slim_batch, ensure_ascii=False, indent=2
    )


def build_repair_prompt(
    batch: list[dict],
    previous_text: str,
    issues: list[str],
    failed_ids: list[str],
) -> str:
    subset = [item for item in batch if item["meaning_id"] in set(failed_ids)]
    slim_subset = [slim_item_for_llm(item) for item in subset]
    return f"""이전 응답 중 일부 항목만 로컬 검증에 실패했다.
실패한 항목만 다시 판정하라. JSON object만 반환하라.

[검증 실패 항목]
{json.dumps(issues, ensure_ascii=False, indent=2)}

[재판정 대상 id]
{json.dumps(failed_ids, ensure_ascii=False)}

[필수 수정]
- decisions 길이를 재판정 대상 개수와 정확히 맞출 것
- 각 id를 정확히 한 번만 반환할 것
- 누락 필드를 채울 것
- meta-language trap 단어를 scene root에 넣지 말 것
- 최상위 키는 반드시 `decisions`만 사용할 것
- system은 `{", ".join(ROOTS_BY_SYSTEM.keys())}` 중 하나만 사용할 것
- root는 `{", ".join(ALL_ROOTS)}` 중 하나만 사용할 것
- 새 분류명이나 lemma 기반 root를 만들지 말 것

[이전 응답]
{previous_text}

[재판정 입력]
{json.dumps(slim_subset, ensure_ascii=False, indent=2)}
"""


def call_gemini(
    system_prompt: str,
    user_prompt: str,
    model: str,
    timeout: int,
    max_retries: int,
    retry_backoff: int,
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.0,
            "responseMimeType": "application/json",
        },
    }
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.RequestException as exc:
            last_error = exc
            if attempt == max_retries:
                break
            time.sleep(retry_backoff * attempt)
    raise RuntimeError(f"Gemini 호출 실패: {last_error}")


def call_openai(
    system_prompt: str,
    user_prompt: str,
    model: str,
    timeout: int,
    max_retries: int,
    retry_backoff: int,
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다.")

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                url, headers=headers, json=payload, timeout=timeout
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as exc:
            last_error = exc
            if attempt == max_retries:
                break
            time.sleep(retry_backoff * attempt)
    raise RuntimeError(f"OpenAI 호출 실패: {last_error}")


def call_model(
    provider: str,
    system_prompt: str,
    user_prompt: str,
    model: str,
    timeout: int,
    max_retries: int,
    retry_backoff: int,
) -> str:
    if provider == "gemini":
        return call_gemini(
            system_prompt, user_prompt, model, timeout, max_retries, retry_backoff
        )
    if provider == "openai":
        return call_openai(
            system_prompt, user_prompt, model, timeout, max_retries, retry_backoff
        )
    raise RuntimeError(f"지원하지 않는 provider: {provider}")


def fallback_model_name(provider: str) -> str:
    if provider == "openai":
        return DEFAULT_OPENAI_MODEL
    if provider == "gemini":
        return DEFAULT_MODEL
    raise RuntimeError(f"지원하지 않는 fallback provider: {provider}")


def coerce_response_shape(parsed) -> dict:
    if isinstance(parsed, list):
        return {"decisions": parsed}
    if isinstance(parsed, dict):
        if "decisions" in parsed:
            return parsed
        if "results" in parsed:
            return {"decisions": parsed.get("results", [])}
        # tolerate direct object maps only if they already look like a decision wrapper
        return {"decisions": parsed.get("items", [])} if "items" in parsed else parsed
    return {"decisions": []}


def normalize_decision_fields(parsed) -> dict:
    parsed = coerce_response_shape(parsed)
    for row in parsed.get("decisions", []):
        if row.get("id") is None and row.get("meaning_id") is not None:
            row["id"] = row["meaning_id"]
        reason = row.get("reason")
        if not row.get("rationale_short"):
            row["rationale_short"] = reason or "근거 요약 누락"
        if row.get("status") in {"CORE", "SYSTEM_CAND", "CAT_CAND", "EXCLUDED"} and not row.get("reason"):
            row["reason"] = row["rationale_short"]
        if row.get("boundary_flags") is None or isinstance(
            row.get("boundary_flags"), bool
        ):
            row["boundary_flags"] = []
        if row.get("negative_rule_triggered") is None or isinstance(
            row.get("negative_rule_triggered"), bool
        ):
            row["negative_rule_triggered"] = []
        if isinstance(row.get("boundary_flags"), str):
            row["boundary_flags"] = [row["boundary_flags"]]
        if isinstance(row.get("negative_rule_triggered"), str):
            row["negative_rule_triggered"] = [row["negative_rule_triggered"]]

        status = row.get("status")
        system = row.get("system")
        root = row.get("root")
        reason_text = " ".join(
            part for part in [row.get("reason"), row.get("rationale_short")] if part
        )
        if status == "CORE" and root not in ALL_ROOTS:
            matched_roots = [candidate for candidate in ALL_ROOTS if candidate in reason_text]
            if len(matched_roots) == 1:
                row["root"] = matched_roots[0]
                row["system"] = ROOT_TO_SYSTEM[matched_roots[0]]
                system = row.get("system")
                root = row.get("root")
        if status in {"CORE", "CAT_CAND"} and system not in ROOTS_BY_SYSTEM:
            matched_systems = [
                candidate for candidate in ROOTS_BY_SYSTEM if candidate in reason_text
            ]
            if len(matched_systems) == 1:
                row["system"] = matched_systems[0]
                system = row.get("system")
        if status == "CORE":
            if root in ALL_ROOTS:
                row["system"] = ROOT_TO_SYSTEM[root]
            elif system in ALL_ROOTS:
                row["root"] = system
                row["system"] = ROOT_TO_SYSTEM[system]
            elif system in ROOTS_BY_SYSTEM and root in ROOTS_BY_SYSTEM:
                row["status"] = "CAT_CAND"
                row["system"] = system
                row["root"] = None
            elif system in ROOTS_BY_SYSTEM and root is None:
                row["status"] = "CAT_CAND"
                row["system"] = system
                row["root"] = None
        elif status == "CAT_CAND":
            if system in ALL_ROOTS:
                row["system"] = ROOT_TO_SYSTEM[system]
                row["root"] = None
    return parsed


def validate_response(batch: list[dict], parsed: dict) -> list[str]:
    issues = []
    parsed = normalize_decision_fields(parsed)
    decisions = parsed.get("decisions")
    if not isinstance(decisions, list):
        return ["decisions가 리스트가 아님"]

    input_ids = [item["meaning_id"] for item in batch]
    output_ids = [row.get("id") for row in decisions if isinstance(row, dict)]

    if len(decisions) != len(batch):
        issues.append(f"입력 {len(batch)}건 대비 decisions {len(decisions)}건")
    if output_ids != input_ids:
        issues.append("입력 순서와 출력 순서가 다름")
    if len(set(output_ids)) != len(output_ids):
        issues.append("id 중복 존재")
    if set(output_ids) != set(input_ids):
        issues.append("입력 id와 출력 id 집합이 다름")

    batch_map = {item["meaning_id"]: item for item in batch}
    for row in decisions:
        if not isinstance(row, dict):
            issues.append("dict가 아닌 decision 항목 존재")
            continue
        status = row.get("status")
        meaning_id = row.get("id")
        if status not in VALID_STATUSES:
            issues.append(f"{meaning_id}: invalid status `{status}`")
            continue
        if status == "CORE":
            if row.get("system") not in ROOTS_BY_SYSTEM:
                issues.append(f"{meaning_id}: CORE인데 system 누락/오류")
            if row.get("root") not in ALL_ROOTS:
                issues.append(f"{meaning_id}: CORE인데 root 누락/오류")
            elif row.get("system") and row["root"] not in ROOTS_BY_SYSTEM[row["system"]]:
                issues.append(f"{meaning_id}: root와 system 불일치")
        if status == "CAT_CAND":
            if row.get("system") not in ROOTS_BY_SYSTEM:
                issues.append(f"{meaning_id}: CAT_CAND인데 system 누락/오류")
        if status in {"SYSTEM_CAND", "CAT_CAND", "EXCLUDED", "CORE"} and not row.get("reason"):
            issues.append(f"{meaning_id}: reason 누락")
        if not row.get("rationale_short"):
            issues.append(f"{meaning_id}: rationale_short 누락")
        if row.get("confidence_band") not in {"HIGH", "MEDIUM", "LOW"}:
            issues.append(f"{meaning_id}: confidence_band 누락/오류")

        item = batch_map.get(meaning_id, {})
        pos = item.get("pos_ko")
        if pos in {"고유명사", "대명사", "의존명사", "조사", "접속조사"} and status == "CORE":
            issues.append(f"{meaning_id}: phase0 filter 대상이 CORE로 분류됨")
        if status == "CORE" and high_risk_boundary_core_violation(item, row):
            issues.append(f"{meaning_id}: 고위험 경계어가 CORE로 승격됨")
    return issues


def extract_failed_ids(batch: list[dict], parsed: dict) -> list[str]:
    failed = []
    parsed = normalize_decision_fields(parsed)
    decisions = parsed.get("decisions")
    if not isinstance(decisions, list):
        return [item["meaning_id"] for item in batch]

    decision_by_id = {row.get("id"): row for row in decisions if isinstance(row, dict)}
    for item in batch:
        mid = item["meaning_id"]
        row = decision_by_id.get(mid)
        if row is None:
            failed.append(mid)
            continue
        status = row.get("status")
        if status not in VALID_STATUSES:
            failed.append(mid)
            continue
        if not row.get("reason") or not row.get("rationale_short"):
            failed.append(mid)
            continue
        if row.get("confidence_band") not in {"HIGH", "MEDIUM", "LOW"}:
            failed.append(mid)
            continue
        if status == "CORE":
            if row.get("system") not in ROOTS_BY_SYSTEM:
                failed.append(mid)
                continue
            if row.get("root") not in ALL_ROOTS:
                failed.append(mid)
                continue
            if row["root"] not in ROOTS_BY_SYSTEM[row["system"]]:
                failed.append(mid)
                continue
        if status == "CAT_CAND" and row.get("system") not in ROOTS_BY_SYSTEM:
            failed.append(mid)
            continue
        if status == "EXCLUDED" and item.get("pos_ko") in {"고유명사", "대명사", "의존명사", "조사", "접속조사"}:
            continue
        if status == "CORE" and high_risk_boundary_core_violation(item, row):
            failed.append(mid)
            continue
    return sorted(set(failed), key=lambda x: [b["meaning_id"] for b in batch].index(x))


def split_decisions(parsed: dict) -> dict:
    parsed = normalize_decision_fields(parsed)
    buckets = {
        "CORE": {},
        "SYSTEM_CAND": [],
        "CAT_CAND": [],
        "EXCLUDED": [],
    }
    for row in parsed["decisions"]:
        status = row["status"]
        if status == "CORE":
            buckets["CORE"][row["id"]] = {
                "system": row["system"],
                "root": row["root"],
            }
        elif status == "SYSTEM_CAND":
            buckets["SYSTEM_CAND"].append({"id": row["id"], "reason": row["reason"]})
        elif status == "CAT_CAND":
            buckets["CAT_CAND"].append(
                {
                    "id": row["id"],
                    "system": row["system"],
                    "reason": row["reason"],
                }
            )
        else:
            buckets["EXCLUDED"].append({"id": row["id"], "reason": row["reason"]})
    return buckets


def quarantine_batch(
    batch_index: int,
    batch: list[dict],
    raw_texts: list[str],
    issues: list[str],
) -> None:
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "batch_index": batch_index,
        "input_count": len(batch),
        "issues": issues,
        "items": batch,
        "responses": raw_texts,
    }
    write_json_atomic(QUARANTINE_DIR / f"batch_{batch_index:04d}.json", payload)


def parse_model_response(
    raw_text: str,
    batch_index: int,
    batch: list[dict],
    raw_texts: list[str],
    stage: str,
) -> dict:
    try:
        return normalize_decision_fields(json.loads(raw_text))
    except json.JSONDecodeError as exc:
        issues = [f"{stage}: JSON decode failure: {exc.msg} at line {exc.lineno} col {exc.colno}"]
        quarantine_batch(batch_index, batch, raw_texts, issues)
        raise RuntimeError(
            f"batch_{batch_index:04d} {stage} 응답 JSON 파싱 실패: {exc.msg}"
        ) from exc


def process_batch(
    batch_index: int,
    batch: list[dict],
    provider: str,
    model: str,
    fallback_provider: str | None,
    timeout: int,
    max_retries: int,
    retry_backoff: int,
) -> tuple[dict, dict]:
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(batch)
    raw_texts = []
    provider_used = provider

    try:
        raw_text = call_model(
            provider,
            system_prompt,
            user_prompt,
            model,
            timeout,
            max_retries,
            retry_backoff,
        )
    except Exception as exc:
        if not fallback_provider:
            raise
        fallback_key = (
            os.getenv("OPENAI_API_KEY")
            if fallback_provider == "openai"
            else os.getenv("GEMINI_API_KEY")
        )
        if not fallback_key:
            raise RuntimeError(
                f"기본 provider `{provider}` 실패 후 fallback `{fallback_provider}` 키가 없어 재시도 불가: {exc}"
            ) from exc
        provider_used = fallback_provider
        raw_text = call_model(
            fallback_provider,
            system_prompt,
            user_prompt,
            fallback_model_name(fallback_provider),
            timeout,
            max_retries,
            retry_backoff,
        )
    raw_texts.append(raw_text)
    parsed = parse_model_response(raw_text, batch_index, batch, raw_texts, "initial")
    issues = validate_response(batch, parsed)

    if issues:
        structural = [
            issue
            for issue in issues
            if issue in STRUCTURAL_ISSUES or issue.startswith("입력 ")
        ]
        if structural:
            failed_ids = [item["meaning_id"] for item in batch]
        else:
            failed_ids = extract_failed_ids(batch, parsed)
            if not failed_ids:
                failed_ids = [item["meaning_id"] for item in batch]
        repair_prompt = build_repair_prompt(batch, raw_text, issues, failed_ids)
        repaired_provider = provider_used
        repaired_model = model if provider_used == provider else fallback_model_name(provider_used)
        try:
            repaired_text = call_model(
                repaired_provider,
                system_prompt,
                repair_prompt,
                repaired_model,
                timeout,
                max_retries,
                retry_backoff,
            )
        except Exception as exc:
            if not fallback_provider or repaired_provider == fallback_provider:
                raise
            fallback_key = (
                os.getenv("OPENAI_API_KEY")
                if fallback_provider == "openai"
                else os.getenv("GEMINI_API_KEY")
            )
            if not fallback_key:
                raise RuntimeError(
                    f"repair 단계 provider `{repaired_provider}` 실패 후 fallback `{fallback_provider}` 키가 없어 재시도 불가: {exc}"
                ) from exc
            repaired_provider = fallback_provider
            provider_used = fallback_provider
            repaired_text = call_model(
                fallback_provider,
                system_prompt,
                repair_prompt,
                fallback_model_name(fallback_provider),
                timeout,
                max_retries,
                retry_backoff,
            )
        raw_texts.append(repaired_text)
        repaired_parsed = parse_model_response(
            repaired_text, batch_index, batch, raw_texts, "repair"
        )
        if failed_ids and len(failed_ids) < len(batch):
            repaired_map = {
                row["id"]: row for row in repaired_parsed.get("decisions", []) if isinstance(row, dict)
            }
            merged = {"decisions": []}
            for row in parsed.get("decisions", []):
                if row.get("id") in repaired_map:
                    merged["decisions"].append(repaired_map[row["id"]])
                else:
                    merged["decisions"].append(row)
            parsed = normalize_decision_fields(merged)
        else:
            parsed = repaired_parsed
        issues = validate_response(batch, parsed)

    if issues:
        quarantine_batch(batch_index, batch, raw_texts, issues)
        raise RuntimeError(
            f"batch_{batch_index:04d} 검증 실패: {'; '.join(issues[:5])}"
        )

    split = split_decisions(parsed)
    report = {
        "batch_index": batch_index,
        "provider_used": provider_used,
        "input_count": len(batch),
        "core_count": len(split["CORE"]),
        "system_cand_count": len(split["SYSTEM_CAND"]),
        "cat_cand_count": len(split["CAT_CAND"]),
        "excluded_count": len(split["EXCLUDED"]),
        "distribution_warning": batch_distribution_warning(parsed),
    }
    return split, report


def batch_distribution_warning(parsed: dict) -> str | None:
    decisions = parsed.get("decisions", [])
    roots = [row.get("root") for row in decisions if row.get("status") == "CORE"]
    if not roots:
        return None
    counts = Counter(roots)
    root, value = counts.most_common(1)[0]
    if value / len(roots) >= 0.8:
        return f"CORE root 편중 경고: {root} {value}/{len(roots)}"
    return None


def merge_pools(pools: dict, split: dict) -> None:
    pools["CORE"].update(split["CORE"])
    pools["SYSTEM_CAND"].extend(split["SYSTEM_CAND"])
    pools["CAT_CAND"].extend(split["CAT_CAND"])
    pools["EXCLUDED"].extend(split["EXCLUDED"])


def write_outputs(pools: dict) -> None:
    write_json_atomic(CORE_PAYLOAD, pools["CORE"])
    write_json_atomic(SYSTEM_CANDIDATES, pools["SYSTEM_CAND"])
    write_json_atomic(CATEGORY_CANDIDATES, pools["CAT_CAND"])
    write_json_atomic(EXCLUDED_WORDS, pools["EXCLUDED"])


def load_checkpoint() -> dict | None:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
    return None


def write_checkpoint(
    pools: dict,
    batch_reports: list[dict],
    next_offset: int,
    llm_queue_count: int,
    total_input: int,
    batch_size: int,
    provider: str,
    fallback_provider: str | None,
    model: str,
) -> None:
    RUN_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "next_offset": next_offset,
        "llm_queue_count": llm_queue_count,
        "total_input": total_input,
        "batch_size": batch_size,
        "provider": provider,
        "fallback_provider": fallback_provider,
        "model": model,
        "pools": pools,
        "batch_reports": batch_reports,
    }
    write_json_atomic(CHECKPOINT_FILE, payload)
    write_json_atomic(
        LATEST_REPORT_FILE,
        {
            "model": model,
            "batch_size": batch_size,
            "total_input": total_input,
            "llm_queue": llm_queue_count,
            "next_offset": next_offset,
            "provider": provider,
            "fallback_provider": fallback_provider,
            "core": len(pools["CORE"]),
            "system_cand": len(pools["SYSTEM_CAND"]),
            "cat_cand": len(pools["CAT_CAND"]),
            "excluded": len(pools["EXCLUDED"]),
            "batch_reports": batch_reports,
        },
    )


def clear_checkpoint() -> None:
    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()


def run_triage(
    batch_size: int,
    limit: int | None,
    provider: str,
    fallback_provider: str | None,
    model: str,
    timeout: int,
    max_retries: int,
    retry_backoff: int,
) -> None:
    source_rows = load_jsonl(MEANINGS_FILE)
    source_total = len(source_rows)
    all_rows = source_rows
    if limit is not None:
        all_rows = all_rows[:limit]
    is_partial_run = len(all_rows) < source_total

    pools = {"CORE": {}, "SYSTEM_CAND": [], "CAT_CAND": [], "EXCLUDED": []}
    batch_reports = []
    llm_queue = []
    RUN_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    for row in all_rows:
        filtered = prefilter_exclusion(row)
        if filtered:
            split = split_decisions({"decisions": [filtered]})
            merge_pools(pools, split)
        else:
            llm_queue.append(row)

    checkpoint = load_checkpoint()
    start_offset = 0
    if (
        checkpoint
        and checkpoint.get("batch_size") == batch_size
        and checkpoint.get("model") == model
        and checkpoint.get("provider") == provider
        and checkpoint.get("fallback_provider") == fallback_provider
        and checkpoint.get("total_input") == len(all_rows)
        and checkpoint.get("llm_queue_count") == len(llm_queue)
    ):
        pools = checkpoint["pools"]
        batch_reports = checkpoint["batch_reports"]
        start_offset = checkpoint["next_offset"]

    for batch_index, start in enumerate(
        range(start_offset, len(llm_queue), batch_size),
        start=(start_offset // batch_size) + 1,
    ):
        batch = llm_queue[start : start + batch_size]
        split, report = process_batch(
            batch_index,
            batch,
            provider,
            model,
            fallback_provider,
            timeout,
            max_retries,
            retry_backoff,
        )
        merge_pools(pools, split)
        batch_reports.append(report)
        write_checkpoint(
            pools=pools,
            batch_reports=batch_reports,
            next_offset=start + len(batch),
            llm_queue_count=len(llm_queue),
            total_input=len(all_rows),
            batch_size=batch_size,
            provider=provider,
            fallback_provider=fallback_provider,
            model=model,
        )
        print(
            json.dumps(
                {
                    "batch_index": batch_index,
                    "input_count": report["input_count"],
                    "core": report["core_count"],
                    "system_cand": report["system_cand_count"],
                    "cat_cand": report["cat_cand_count"],
                    "excluded": report["excluded_count"],
                    "distribution_warning": report["distribution_warning"],
                },
                ensure_ascii=False,
            )
        )

    if any(QUARANTINE_DIR.glob("batch_*.json")):
        raise RuntimeError("격리된 실패 배치가 있어 최종 산출물 쓰기를 중단합니다.")

    if not is_partial_run:
        write_outputs(pools)
    write_json_atomic(
        LATEST_REPORT_FILE,
        {
            "model": model,
            "batch_size": batch_size,
            "total_input": len(all_rows),
            "source_total": source_total,
            "is_partial_run": is_partial_run,
            "llm_queue": len(llm_queue),
            "provider": provider,
            "fallback_provider": fallback_provider,
            "core": len(pools["CORE"]),
            "system_cand": len(pools["SYSTEM_CAND"]),
            "cat_cand": len(pools["CAT_CAND"]),
            "excluded": len(pools["EXCLUDED"]),
            "batch_reports": batch_reports,
        },
    )
    clear_checkpoint()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        choices=["gemini", "openai"],
    )
    parser.add_argument(
        "--fallback-provider",
        default=DEFAULT_FALLBACK_PROVIDER,
        choices=["none", "gemini", "openai"],
    )
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES)
    parser.add_argument("--retry-backoff", type=int, default=DEFAULT_RETRY_BACKOFF)
    args = parser.parse_args()
    fallback_provider = None if args.fallback_provider == "none" else args.fallback_provider
    if fallback_provider == args.provider:
        fallback_provider = None
    model = args.model or (
        DEFAULT_MODEL if args.provider == "gemini" else DEFAULT_OPENAI_MODEL
    )

    if not args.execute:
        print(
            json.dumps(
                {
                    "mode": "review_only",
                    "message": "--execute 없이 실제 API 호출과 파일 쓰기를 하지 않습니다.",
                    "batch_size": args.batch_size,
                    "provider": args.provider,
                    "fallback_provider": fallback_provider,
                    "model": model,
                    "meanings_file": str(MEANINGS_FILE),
                },
                ensure_ascii=False,
            )
        )
        return

    run_triage(
        batch_size=args.batch_size,
        limit=args.limit,
        provider=args.provider,
        fallback_provider=fallback_provider,
        model=model,
        timeout=args.timeout,
        max_retries=args.max_retries,
        retry_backoff=args.retry_backoff,
    )


if __name__ == "__main__":
    main()
