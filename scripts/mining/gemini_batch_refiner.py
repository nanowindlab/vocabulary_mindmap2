import argparse
import json
import os
import urllib.request
from collections import Counter
from pathlib import Path


DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_PROFILE = "general_inventory"
ALLOWED_ROOTS = [
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
    "내면과 감정",
    "성격과 태도",
    "감각과 묘사",
    "의견과 가치",
    "수량과 단위",
    "시간과 흐름",
    "논리와 연결",
    "지시와 질문",
]
VALID_BUCKETS = {"core", "candidate", "exclusion"}
SUSPICIOUS_EXCLUSION_PHRASES = [
    "너무 일반적인",
    "학습에 부적합",
    "특정 재료",
    "사람은 학습에 부적합",
]


def call_gemini(prompt: str, api_key: str, model: str) -> dict:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json",
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def build_initial_prompt(items: list[dict], profile: str) -> str:
    common_header = f"""너는 한국어 어휘 마인드맵 프로젝트의 데이터 전략가다.
반드시 SDCP V1과 IA V4를 따른다.

핵심 규칙:
1. 100% 확실한 것만 core로 보낸다.
2. 모호하면 candidate로 보낸다.
3. negative examples: 세포, 문장, 가축, 박선호 같은 오분류를 절대 반복하지 마라.

허용 root 목록:
{json.dumps(ALLOWED_ROOTS, ensure_ascii=False)}

반환 규칙:
- JSON만 반환한다. 코드펜스 금지.
- `decisions` 길이는 반드시 입력 개수와 같아야 한다.
- 각 `meaning_id`는 정확히 한 번만 등장해야 한다.
- 입력 순서를 유지한다.
- bucket이 `candidate`이면 `root`를 반드시 채운다. 이 root는 `임시 제안 root`다.
- root는 bucket이 core/candidate일 때만 쓴다.
- category_label_ko는 bucket이 core일 때만 쓰고, root 이름을 반복하지 않는 2~4어절 한국어 라벨로 쓴다.

반환 형식:
{{
  "decisions": [
    {{
      "meaning_id": "...",
      "bucket": "core|candidate|exclusion",
      "root": "...",
      "category_label_ko": "...",
      "candidate_reason": "...",
      "exclusion_reason": "...",
      "rationale_short": "..."
    }}
  ],
  "insights": {{
    "hard_patterns": ["..."],
    "ia_suggestions": ["..."]
  }}
}}

검토 대상 JSON:
{json.dumps(items, ensure_ascii=False)}
"""
    if profile == "payload_audit":
        profile_rules = """

추가 프로필 규칙: payload_audit
- exclusion은 고유명사, 대명사, 의존명사, 조사/접사, 욕설/비속어, 학습 비적합 파편어에만 사용한다.
- 아래 이유로 exclusion 하지 마라:
  - 너무 일반적이다
  - 음식 재료다
  - 직업/역할이다
  - 신체 부위다
  - 조리 행위다
- 특별 보정:
  - `메밀`, `조미료`, `소금`, `요리`, `요리법`, `조리`, `조리법`, `익히다`, `요리사`, `치아`는 exclusion 후보가 아니다.
  - 직업 역할어는 exclusion이 아니라 관련 scene root 또는 candidate로 보낸다.
  - 신체 부위/의료 증상은 exclusion이 아니라 `보건과 의료` 또는 candidate다.
  - 음식 재료/식기/조리도구/식당/조리행위는 exclusion이 아니라 `식생활` core 또는 candidate다.
  - 맛/감각/신체 경계가 겹치면 candidate를 우선한다.
"""
    else:
        profile_rules = """

추가 프로필 규칙: general_inventory
- exclusion은 아래 경우에만 허용한다:
  - 고유명사
  - 대명사
  - 의존명사
  - 조사/접사
  - 욕설/비속어
  - 시각화가 거의 불가능한 학습 비적합 파편어
- 직업/역할어는 exclusion 하지 말고 관련 scene root를 우선 검토한다.
- 신체 부위/의료 증상은 exclusion 하지 말고 `보건과 의료` 또는 candidate를 검토한다.
- 음식 재료/식기/조리도구/식당/조리행위는 exclusion 하지 말고 `식생활` 또는 candidate를 검토한다.
- 장소/장면/제도/직업/행위가 명확하면 core를 우선한다.
- 감각/평가/내면/신체와 경계가 겹치면 candidate를 우선한다.
"""
    return common_header.replace("허용 root 목록:", profile_rules + "\n허용 root 목록:")


def build_repair_prompt(
    items: list[dict], previous_text: str, issues: list[str], attempt: int
) -> str:
    return f"""이전 응답은 로컬 검증에서 실패했다. 이전 응답을 버리고 아래 오류를 모두 수정해서 JSON만 다시 반환하라.

검증 오류:
{json.dumps(issues, ensure_ascii=False, indent=2)}

수정 규칙:
- `decisions`는 입력 {len(items)}건과 정확히 1:1이어야 한다.
- 각 `meaning_id`는 정확히 한 번만 등장한다.
- candidate는 모두 `root`를 반드시 가져야 한다.
- exclusion은 SDCP 필터 기준에만 사용한다.
- 아래 표현은 exclusion 사유로 금지한다:
  - 너무 일반적인 명사/동사
  - 특정 재료라서 부적합
  - 사람이라서 부적합
  - 신체 부위라서 exclusion
- 의심되면 candidate로 이동한다.
- root는 다음 목록에서만 선택한다:
{json.dumps(ALLOWED_ROOTS, ensure_ascii=False)}

이전 응답:
{previous_text}

원본 입력:
{json.dumps(items, ensure_ascii=False)}
"""


def suspicious_exclusion(item: dict, decision: dict) -> bool:
    reason = str(decision.get("exclusion_reason", ""))
    if any(phrase in reason for phrase in SUSPICIOUS_EXCLUSION_PHRASES):
        return True
    pos = item.get("pos_ko", "")
    if pos in {"고유명사", "대명사", "의존명사"}:
        return False
    return False


def ensure_rationale_short(parsed: dict) -> dict:
    for row in parsed.get("decisions", []):
        if row.get("rationale_short"):
            continue
        row["rationale_short"] = (
            row.get("candidate_reason")
            or row.get("exclusion_reason")
            or row.get("category_label_ko")
            or "근거 요약 누락"
        )
    return parsed


def normalize_decision_fields(parsed: dict) -> dict:
    parsed = ensure_rationale_short(parsed)
    for row in parsed.get("decisions", []):
        bucket = row.get("bucket")
        rationale = row.get("rationale_short") or "근거 요약 누락"
        if bucket == "candidate" and not row.get("candidate_reason"):
            row["candidate_reason"] = rationale
        if bucket == "exclusion" and not row.get("exclusion_reason"):
            row["exclusion_reason"] = rationale
        if bucket == "core" and not row.get("category_label_ko"):
            row["category_label_ko"] = rationale
    return parsed


def validate_response(items: list[dict], parsed: dict) -> list[str]:
    issues = []
    parsed = normalize_decision_fields(parsed)
    decisions = parsed.get("decisions")
    if not isinstance(decisions, list):
        return ["`decisions`가 리스트가 아님"]

    input_ids = [item["meaning_id"] for item in items]
    output_ids = [row.get("meaning_id") for row in decisions if isinstance(row, dict)]
    if len(decisions) != len(items):
        issues.append(
            f"입력 {len(items)}건 대비 decisions {len(decisions)}건으로 길이가 다름"
        )

    counts = Counter(output_ids)
    dups = sorted([mid for mid, count in counts.items() if count > 1 and mid is not None])
    missing = [mid for mid in input_ids if counts.get(mid, 0) == 0]
    extra = [mid for mid in output_ids if mid not in set(input_ids)]
    if dups:
        issues.append(f"중복 meaning_id: {dups}")
    if missing:
        issues.append(f"누락 meaning_id: {missing}")
    if extra:
        issues.append(f"입력에 없는 meaning_id: {extra}")
    if output_ids != input_ids:
        issues.append("입력 순서와 출력 순서가 다름")

    item_map = {item["meaning_id"]: item for item in items}
    for row in decisions:
        if not isinstance(row, dict):
            issues.append("dict가 아닌 decision 항목 존재")
            continue
        bucket = row.get("bucket")
        mid = row.get("meaning_id")
        if bucket not in VALID_BUCKETS:
            issues.append(f"{mid}: invalid bucket `{bucket}`")
        if bucket in {"core", "candidate"}:
            root = row.get("root")
            if root not in ALLOWED_ROOTS:
                issues.append(f"{mid}: invalid root `{root}`")
        if bucket == "core" and not row.get("category_label_ko"):
            issues.append(f"{mid}: core인데 category_label_ko 누락")
        if bucket == "candidate" and not row.get("candidate_reason"):
            issues.append(f"{mid}: candidate인데 candidate_reason 누락")
        if bucket == "exclusion" and not row.get("exclusion_reason"):
            issues.append(f"{mid}: exclusion인데 exclusion_reason 누락")
        if not row.get("rationale_short"):
            issues.append(f"{mid}: rationale_short 누락")
        if bucket == "exclusion" and mid in item_map:
            if suspicious_exclusion(item_map[mid], row):
                issues.append(f"{mid}: exclusion 사유가 과도하거나 SDCP 필터와 불일치")
    return issues


def split_decisions(parsed: dict) -> dict:
    parsed = normalize_decision_fields(parsed)
    buckets = {"core": [], "candidate": [], "exclusion": []}
    for row in parsed["decisions"]:
        bucket = row["bucket"]
        clean = {"meaning_id": row["meaning_id"], "rationale_short": row["rationale_short"]}
        if bucket == "core":
            clean["root"] = row["root"]
            clean["category_label_ko"] = row["category_label_ko"]
        elif bucket == "candidate":
            clean["root"] = row.get("root")
            clean["candidate_reason"] = row["candidate_reason"]
        else:
            clean["exclusion_reason"] = row["exclusion_reason"]
        buckets[bucket].append(clean)
    buckets["insights"] = parsed.get("insights", {})
    return buckets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    args = parser.parse_args()

    api_key = os.environ["GEMINI_API_KEY"]
    model = args.model
    profile = args.profile
    input_path = Path(args.input)
    output_prefix = Path(args.output_prefix)
    output_prefix.parent.mkdir(parents=True, exist_ok=True)

    items = json.loads(input_path.read_text(encoding="utf-8"))
    prompt = build_initial_prompt(items, profile)
    output_prefix.with_name(output_prefix.name + "_prompt_attempt1.txt").write_text(
        prompt, encoding="utf-8"
    )

    raw = call_gemini(prompt, api_key, model)
    raw_text = raw["candidates"][0]["content"]["parts"][0]["text"]
    output_prefix.with_name(output_prefix.name + "_raw_attempt1.json").write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    output_prefix.with_name(output_prefix.name + "_response_attempt1.json").write_text(
        raw_text, encoding="utf-8"
    )
    parsed = normalize_decision_fields(json.loads(raw_text))
    issues = validate_response(items, parsed)

    if issues:
        repair_prompt = build_repair_prompt(items, raw_text, issues, 2)
        output_prefix.with_name(output_prefix.name + "_prompt_attempt2.txt").write_text(
            repair_prompt, encoding="utf-8"
        )
        repair_raw = call_gemini(repair_prompt, api_key, model)
        repair_text = repair_raw["candidates"][0]["content"]["parts"][0]["text"]
        output_prefix.with_name(output_prefix.name + "_raw_attempt2.json").write_text(
            json.dumps(repair_raw, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        output_prefix.with_name(
            output_prefix.name + "_response_attempt2.json"
        ).write_text(repair_text, encoding="utf-8")
        parsed = normalize_decision_fields(json.loads(repair_text))
        issues = validate_response(items, parsed)

    split = split_decisions(parsed)
    output_prefix.with_name(output_prefix.name + "_validated.json").write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    output_prefix.with_name(output_prefix.name + "_buckets.json").write_text(
        json.dumps(split, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    report = {
        "model": model,
        "profile": profile,
        "input_count": len(items),
        "core_count": len(split["core"]),
        "candidate_count": len(split["candidate"]),
        "exclusion_count": len(split["exclusion"]),
        "validation_issues": issues,
    }
    output_prefix.with_name(output_prefix.name + "_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
