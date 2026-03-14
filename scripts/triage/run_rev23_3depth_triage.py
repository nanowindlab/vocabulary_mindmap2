import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import llm_data_triage as base


ROOT = Path(__file__).resolve().parents[2]
MASTER_POOL = ROOT / "08_expansion" / "master_pool" / "MASTER_POOL_V1.jsonl"
CATEGORY_DICT_JSON = ROOT / "08_expansion" / "IA_V4_3DEPTH_CATEGORY_DICTIONARY_V1.json"
REV23_DIR = ROOT / "08_expansion" / "rev23"
RUN_REPORT_DIR = REV23_DIR / "triage_reports"
QUARANTINE_DIR = REV23_DIR / "triage_quarantine"
CHECKPOINT_FILE = RUN_REPORT_DIR / "rev23_3depth_checkpoint.json"
LATEST_REPORT_FILE = RUN_REPORT_DIR / "rev23_3depth_latest_report.json"

REV23_CORE = REV23_DIR / "REV23_CORE_WITH_CATEGORY_V1.json"
REV23_SYSTEM = REV23_DIR / "REV23_SYSTEM_CANDIDATES_V1.json"
REV23_CATEGORY = REV23_DIR / "REV23_CATEGORY_CANDIDATES_V1.json"
REV23_EXCLUDED = REV23_DIR / "REV23_EXCLUDED_V1.json"

APP_SITUATIONS = ROOT / "09_app" / "public" / "data" / "APP_READY_SITUATIONS_TREE.json"
APP_EXPRESSIONS = ROOT / "09_app" / "public" / "data" / "APP_READY_EXPRESSIONS_TREE.json"
APP_BASICS = ROOT / "09_app" / "public" / "data" / "APP_READY_BASICS_TREE.json"
APP_SEARCH = ROOT / "09_app" / "public" / "data" / "APP_READY_SEARCH_INDEX.json"
LIVE_DIR = ROOT / "09_app" / "public" / "data" / "live"
APP_SITUATIONS = LIVE_DIR / "APP_READY_SITUATIONS_TREE.json"
APP_EXPRESSIONS = LIVE_DIR / "APP_READY_EXPRESSIONS_TREE.json"
APP_BASICS = LIVE_DIR / "APP_READY_BASICS_TREE.json"
APP_SEARCH = LIVE_DIR / "APP_READY_SEARCH_INDEX.json"
RAW_DICT = ROOT / "05_source" / "raw_dictionary" / "한국어 어휘사전(영어판)_사전.json"
STATS_FILE = ROOT / "05_source" / "extracted_corpus" / "snapshot_20260309" / "MY_Lemma_Stats.jsonl"

VALID_STATUSES = {"CORE", "SYSTEM_CAND", "CAT_CAND", "EXCLUDED"}
RAW_POS_MAP = {
    "명": "일반명사",
    "동": "동사",
    "형": "형용사",
    "부": "일반부사",
    "감": "감탄사",
    "관": "관형사",
    "대": "대명사",
    "수": "수사",
    "조": "조사",
    "명|의존": "의존명사",
}
GRADE_RE = re.compile(r"\[(초|중|고)\]")


def live_quarantine_files() -> list[Path]:
    return [
        path
        for path in QUARANTINE_DIR.glob("batch_*.json")
        if "archive" not in path.name
    ]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"[.。,，·ㆍ:;!?]+$", "", text)
    text = re.sub(r"\s+", "", text)
    return text


def load_category_dict() -> dict:
    return json.loads(CATEGORY_DICT_JSON.read_text(encoding="utf-8"))


def build_category_maps(category_dict: dict) -> tuple[dict[str, list[str]], dict[str, str]]:
    categories_by_root = {}
    root_to_system = {}
    for system, roots in category_dict.items():
        for root, data in roots.items():
            categories_by_root[root] = [row["label"] for row in data.get("categories", [])]
            root_to_system[root] = system
    return categories_by_root, root_to_system


def load_stats_map() -> tuple[dict[str, dict], int, int, dict[str, int]]:
    stats_map = {}
    stats_rows = load_jsonl(STATS_FILE)
    max_frequency = max((row.get("total_frequency", 0) for row in stats_rows), default=0)
    max_round = max((row.get("round_count", 0) for row in stats_rows), default=0)
    sorted_rows = sorted(
        stats_rows,
        key=lambda row: (-row.get("total_frequency", 0), row.get("meaning_id") or row.get("lemma") or ""),
    )
    rank_map = {}
    for idx, row in enumerate(sorted_rows, start=1):
        if row.get("meaning_id"):
            rank_map[row["meaning_id"]] = idx
        stats_map[row.get("meaning_id")] = row
    return stats_map, max_frequency, max_round, rank_map


def load_raw_grade_index() -> dict[tuple[str, str], list[dict]]:
    raw = json.loads(RAW_DICT.read_text(encoding="utf-8"))
    index = defaultdict(list)
    for row in raw:
        lemma = row["entry"]["headword_ko"]
        pos_ko = RAW_POS_MAP.get(row["entry"].get("pos"), row["entry"].get("pos"))
        for sense in row.get("senses", []):
            index[(lemma, pos_ko)].append(
                {
                    "sense_no": sense.get("sense_no"),
                    "definition": normalize_text(sense.get("definition_ko")),
                    "grade": row["entry"].get("grade"),
                    "notation": row["entry"].get("level_pos_notation"),
                }
            )
    return index


def infer_grade_ko(src: dict, raw_grade_index: dict[tuple[str, str], list[dict]]) -> str | None:
    notation = src.get("level_pos_notation") or ""
    match = GRADE_RE.search(notation)
    if match:
        return match.group(1)

    candidates = raw_grade_index.get((src.get("lemma"), src.get("pos_ko")), [])
    if not candidates:
        return None

    exact = [cand for cand in candidates if cand["sense_no"] == src.get("sense_number") and cand.get("grade")]
    if len(exact) == 1:
        return exact[0]["grade"]

    grades = {cand["grade"] for cand in candidates if cand.get("grade")}
    if len(grades) == 1:
        return next(iter(grades))

    norm_def = normalize_text(src.get("meaning_kr"))
    fuzzy = [
        cand
        for cand in candidates
        if cand.get("definition") and norm_def and (norm_def in cand["definition"] or cand["definition"] in norm_def)
    ]
    fuzzy_grades = {cand["grade"] for cand in fuzzy if cand.get("grade")}
    if len(fuzzy_grades) == 1:
        return next(iter(fuzzy_grades))

    return None


def compute_band(stats_row: dict | None, max_frequency: int, max_round: int) -> int | None:
    if not stats_row:
        return None
    frequency = stats_row.get("total_frequency")
    round_count = stats_row.get("round_count")
    if frequency is None or round_count is None or max_frequency <= 0 or max_round <= 0:
        return None
    norm_freq = math.log10(frequency + 1) / math.log10(max_frequency + 1)
    norm_round = round_count / max_round
    score = (norm_freq * 0.4) + (norm_round * 0.6)
    if score >= 0.75:
        return 1
    if score >= 0.55:
        return 2
    if score >= 0.35:
        return 3
    if score >= 0.15:
        return 4
    return 5


def compute_level(grade_ko: str | None, band: int | None) -> str:
    if grade_ko == "초":
        return "Beginner"
    if grade_ko == "중":
        return "Beginner" if band == 1 else "Intermediate"
    if grade_ko == "고":
        return "Intermediate" if band == 1 else "Advanced"
    return "Unrated"


def build_dictionary_prompt(category_dict: dict) -> str:
    lines = []
    for system, roots in category_dict.items():
        lines.append(f"[{system}]")
        for root, data in roots.items():
            cats = ", ".join(row["label"] for row in data.get("categories", []))
            lines.append(f"- {root}: {cats}")
    return "\n".join(lines)


def build_system_prompt(category_dict: dict) -> str:
    dictionary_text = build_dictionary_prompt(category_dict)
    return f"""너는 한국어 어휘 3 Depth triage 엔진이다.
목표는 각 meaning inventory를 보수적으로 하나의 상태로 판정하는 것이다.

[상태 정의]
- CORE: system/root/category가 모두 확실할 때만
- CAT_CAND: system/root는 보이지만 category가 확실하지 않을 때
- SYSTEM_CAND: system 또는 root 자체가 모호할 때
- EXCLUDED: 고유명사, 대명사, 의존명사, 조사/접속조사 같은 기능 요소

[핵심 규칙]
1. 조금이라도 불확실하면 CORE 금지
2. category는 반드시 아래 사전의 허용 라벨 중 하나만 사용
3. root는 반드시 허용된 22개 루트 중 하나만 사용
4. system은 반드시 3대 축 중 하나만 사용
5. 이전 current_status/current_system/current_root는 참고만 하고, 틀리면 버릴 것
6. 고위험 경계어는 의미 문맥이 body cue면 candidate 우선

[3 Depth 카테고리 사전]
{dictionary_text}

[반환 규칙]
- JSON object만 반환
- 최상위 키는 반드시 `decisions`
- 입력 순서 유지, 각 id 정확히 1회
- 모든 decision에 id, lemma, status, reason, confidence_band, boundary_flags, negative_rule_triggered, rationale_short 포함
- CORE는 system/root/category 필수
- CAT_CAND는 system/root 필수, category는 null
- SYSTEM_CAND/EXCLUDED는 system/root/category null 허용
- confidence_band는 HIGH|MEDIUM|LOW만 허용
"""


def slim_item_for_llm(item: dict) -> dict:
    return {
        "id": item["meaning_id"],
        "lemma": item["lemma"],
        "pos_ko": item["pos_ko"],
        "meaning_kr": item["meaning_kr"],
        "current_status": item.get("current_status"),
        "current_system": item.get("current_system"),
        "current_root": item.get("current_root"),
    }


def build_user_prompt(batch: list[dict]) -> str:
    slim_batch = [slim_item_for_llm(item) for item in batch]
    return "아래 입력 항목을 순서 그대로 3 Depth 분류하라.\n\n" + json.dumps(
        slim_batch, ensure_ascii=False, indent=2
    )


def build_repair_prompt(batch: list[dict], previous_text: str, issues: list[str], failed_ids: list[str], category_dict: dict) -> str:
    subset = [item for item in batch if item["meaning_id"] in set(failed_ids)]
    slim_subset = [slim_item_for_llm(item) for item in subset]
    return f"""이전 응답 중 일부 항목만 로컬 검증에 실패했다.
실패한 항목만 다시 판정하라. JSON object만 반환하라.

[검증 실패 항목]
{json.dumps(issues, ensure_ascii=False, indent=2)}

[재판정 대상 id]
{json.dumps(failed_ids, ensure_ascii=False)}

[허용 3 Depth 사전]
{build_dictionary_prompt(category_dict)}

[필수 수정]
- decisions 길이를 재판정 대상 개수와 정확히 맞출 것
- 각 id를 정확히 한 번만 반환할 것
- category는 허용 라벨 중 하나만 쓰거나, 불확실하면 null로 둘 것
- 새 분류명이나 lemma 기반 category를 만들지 말 것
- system/root/category 누락 필드를 채울 것

[이전 응답]
{previous_text}

[재판정 입력]
{json.dumps(slim_subset, ensure_ascii=False, indent=2)}
"""


def normalize_decision_fields(parsed: dict, categories_by_root: dict, root_to_system: dict) -> dict:
    parsed = base.coerce_response_shape(parsed)
    for row in parsed.get("decisions", []):
        if row.get("id") is None and row.get("meaning_id") is not None:
            row["id"] = row["meaning_id"]
        reason = row.get("reason")
        if not row.get("rationale_short"):
            row["rationale_short"] = reason or "근거 요약 누락"
        if row.get("status") in VALID_STATUSES and not row.get("reason"):
            row["reason"] = row["rationale_short"]
        if row.get("boundary_flags") is None or isinstance(row.get("boundary_flags"), bool):
            row["boundary_flags"] = []
        if row.get("negative_rule_triggered") is None or isinstance(row.get("negative_rule_triggered"), bool):
            row["negative_rule_triggered"] = []
        if isinstance(row.get("boundary_flags"), str):
            row["boundary_flags"] = [row["boundary_flags"]]
        if isinstance(row.get("negative_rule_triggered"), str):
            row["negative_rule_triggered"] = [row["negative_rule_triggered"]]

        status = row.get("status")
        system = row.get("system")
        root = row.get("root")
        category = row.get("category")
        reason_text = " ".join(part for part in [row.get("reason"), row.get("rationale_short")] if part)

        exact_triplet = None
        for candidate_root, valid_categories in categories_by_root.items():
            candidate_system = root_to_system[candidate_root]
            for candidate_category in valid_categories:
                path_token = f"{candidate_system} > {candidate_root} > {candidate_category}"
                if path_token in reason_text:
                    exact_triplet = (candidate_system, candidate_root, candidate_category)
                    break
            if exact_triplet:
                break
        if exact_triplet:
            row["system"], row["root"], row["category"] = exact_triplet
            system, root, category = exact_triplet

        if root in categories_by_root:
            row["system"] = root_to_system[root]
            system = row["system"]
        else:
            matched_roots = [candidate for candidate in categories_by_root if candidate in reason_text]
            if system in root_to_system.values():
                filtered_roots = [candidate for candidate in matched_roots if root_to_system[candidate] == system]
                if len(filtered_roots) == 1:
                    matched_roots = filtered_roots
            if len(matched_roots) == 1:
                row["root"] = matched_roots[0]
                row["system"] = root_to_system[matched_roots[0]]
                root = row["root"]
                system = row["system"]

        if status in {"CORE", "CAT_CAND"} and system not in root_to_system.values():
            matched_systems = [candidate for candidate in root_to_system.values() if candidate in reason_text]
            if len(set(matched_systems)) == 1:
                row["system"] = matched_systems[0]
                system = row["system"]

        if status == "CORE" and root in categories_by_root:
            valid_categories = categories_by_root[root]
            if category not in valid_categories:
                matched_categories = [candidate for candidate in valid_categories if candidate in reason_text]
                if len(matched_categories) == 1:
                    row["category"] = matched_categories[0]
                else:
                    row["status"] = "CAT_CAND"
                    row["category"] = None
        elif status == "CAT_CAND":
            row["category"] = None
    return parsed


def validate_response(batch: list[dict], parsed: dict, categories_by_root: dict, root_to_system: dict) -> list[str]:
    issues = []
    parsed = normalize_decision_fields(parsed, categories_by_root, root_to_system)
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
            if row.get("system") not in root_to_system.values():
                issues.append(f"{meaning_id}: CORE인데 system 누락/오류")
            if row.get("root") not in categories_by_root:
                issues.append(f"{meaning_id}: CORE인데 root 누락/오류")
            elif row["root"] and row.get("system") != root_to_system[row["root"]]:
                issues.append(f"{meaning_id}: root와 system 불일치")
            if row.get("category") not in categories_by_root.get(row.get("root"), []):
                issues.append(f"{meaning_id}: CORE인데 category 누락/오류")
        if status == "CAT_CAND":
            if row.get("system") not in root_to_system.values():
                issues.append(f"{meaning_id}: CAT_CAND인데 system 누락/오류")
            if row.get("root") not in categories_by_root:
                issues.append(f"{meaning_id}: CAT_CAND인데 root 누락/오류")
        if not row.get("reason"):
            issues.append(f"{meaning_id}: reason 누락")
        if not row.get("rationale_short"):
            issues.append(f"{meaning_id}: rationale_short 누락")
        if row.get("confidence_band") not in {"HIGH", "MEDIUM", "LOW"}:
            issues.append(f"{meaning_id}: confidence_band 누락/오류")

        item = batch_map.get(meaning_id, {})
        pos = item.get("pos_ko")
        if pos in {"고유명사", "대명사", "의존명사", "조사", "접속조사"} and status == "CORE":
            issues.append(f"{meaning_id}: phase0 filter 대상이 CORE로 분류됨")
        if status == "CORE" and base.high_risk_boundary_core_violation(item, row):
            issues.append(f"{meaning_id}: 고위험 경계어가 CORE로 승격됨")
    return issues


def extract_failed_ids(batch: list[dict], parsed: dict, categories_by_root: dict, root_to_system: dict) -> list[str]:
    failed = []
    parsed = normalize_decision_fields(parsed, categories_by_root, root_to_system)
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
            if row.get("system") not in root_to_system.values():
                failed.append(mid)
                continue
            if row.get("root") not in categories_by_root:
                failed.append(mid)
                continue
            if row["root"] and row.get("system") != root_to_system[row["root"]]:
                failed.append(mid)
                continue
            if row.get("category") not in categories_by_root.get(row.get("root"), []):
                failed.append(mid)
                continue
        if status == "CAT_CAND":
            if row.get("system") not in root_to_system.values():
                failed.append(mid)
                continue
            if row.get("root") not in categories_by_root:
                failed.append(mid)
                continue
        if status == "CORE" and base.high_risk_boundary_core_violation(item, row):
            failed.append(mid)
            continue
    return sorted(set(failed), key=lambda x: [b["meaning_id"] for b in batch].index(x))


def split_decisions(parsed: dict, categories_by_root: dict, root_to_system: dict) -> dict:
    parsed = normalize_decision_fields(parsed, categories_by_root, root_to_system)
    buckets = {"CORE": {}, "SYSTEM_CAND": [], "CAT_CAND": [], "EXCLUDED": []}
    for row in parsed["decisions"]:
        status = row["status"]
        if status == "CORE":
            buckets["CORE"][row["id"]] = {
                "system": row["system"],
                "root": row["root"],
                "category": row["category"],
            }
        elif status == "SYSTEM_CAND":
            buckets["SYSTEM_CAND"].append({"id": row["id"], "reason": row["reason"]})
        elif status == "CAT_CAND":
            buckets["CAT_CAND"].append(
                {
                    "id": row["id"],
                    "system": row["system"],
                    "root": row["root"],
                    "reason": row["reason"],
                }
            )
        else:
            buckets["EXCLUDED"].append({"id": row["id"], "reason": row["reason"]})
    return buckets


def quarantine_batch(batch_index: int, batch: list[dict], raw_texts: list[str], issues: list[str]) -> None:
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "batch_index": batch_index,
        "input_count": len(batch),
        "issues": issues,
        "items": batch,
        "responses": raw_texts,
    }
    base.write_json_atomic(QUARANTINE_DIR / f"batch_{batch_index:04d}.json", payload)


def parse_model_response(raw_text: str, batch_index: int, batch: list[dict], raw_texts: list[str], stage: str, categories_by_root: dict, root_to_system: dict) -> dict:
    try:
        return normalize_decision_fields(json.loads(raw_text), categories_by_root, root_to_system)
    except json.JSONDecodeError as exc:
        issues = [f"{stage}: JSON decode failure: {exc.msg} at line {exc.lineno} col {exc.colno}"]
        quarantine_batch(batch_index, batch, raw_texts, issues)
        raise RuntimeError(f"batch_{batch_index:04d} {stage} 응답 JSON 파싱 실패: {exc.msg}") from exc


def apply_current_assignment_fallback(parsed: dict, batch: list[dict], categories_by_root: dict, root_to_system: dict) -> dict:
    batch_map = {item["meaning_id"]: item for item in batch}
    for row in parsed.get("decisions", []):
        if not isinstance(row, dict):
            continue
        item = batch_map.get(row.get("id"))
        if not item:
            continue
        current_system = item.get("current_system")
        current_root = item.get("current_root")
        if row.get("status") == "CORE":
            if current_root in categories_by_root and current_system == root_to_system[current_root]:
                if row.get("root") not in categories_by_root or row.get("system") not in root_to_system.values():
                    row["status"] = "CAT_CAND"
                    row["system"] = current_system
                    row["root"] = current_root
                    row["category"] = None
                elif row.get("category") not in categories_by_root.get(row.get("root"), []):
                    row["status"] = "CAT_CAND"
                    row["system"] = row.get("system") or current_system
                    row["root"] = row.get("root") or current_root
                    row["category"] = None
            if base.high_risk_boundary_core_violation(item, row):
                row["status"] = "CAT_CAND"
                if row.get("root") not in categories_by_root and current_root in categories_by_root:
                    row["root"] = current_root
                if row.get("system") not in root_to_system.values():
                    if row.get("root") in categories_by_root:
                        row["system"] = root_to_system[row["root"]]
                    elif current_system in root_to_system.values():
                        row["system"] = current_system
                row["category"] = None
        elif row.get("status") == "CAT_CAND" and row.get("root") is None:
            row["status"] = "SYSTEM_CAND"
            row["category"] = None
    return normalize_decision_fields(parsed, categories_by_root, root_to_system)


def process_batch(batch_index: int, batch: list[dict], provider: str, model: str, fallback_provider: str | None, timeout: int, max_retries: int, retry_backoff: int, category_dict: dict, categories_by_root: dict, root_to_system: dict) -> tuple[dict, dict]:
    system_prompt = build_system_prompt(category_dict)
    user_prompt = build_user_prompt(batch)
    raw_texts = []
    provider_used = provider

    try:
        raw_text = base.call_model(provider, system_prompt, user_prompt, model, timeout, max_retries, retry_backoff)
    except Exception as exc:
        if not fallback_provider:
            raise
        fallback_key = os.getenv("OPENAI_API_KEY") if fallback_provider == "openai" else os.getenv("GEMINI_API_KEY")
        if not fallback_key:
            raise RuntimeError(f"기본 provider `{provider}` 실패 후 fallback `{fallback_provider}` 키가 없어 재시도 불가: {exc}") from exc
        provider_used = fallback_provider
        raw_text = base.call_model(
            fallback_provider,
            system_prompt,
            user_prompt,
            base.fallback_model_name(fallback_provider),
            timeout,
            max_retries,
            retry_backoff,
        )
    raw_texts.append(raw_text)
    parsed = parse_model_response(raw_text, batch_index, batch, raw_texts, "initial", categories_by_root, root_to_system)
    parsed = apply_current_assignment_fallback(parsed, batch, categories_by_root, root_to_system)
    issues = validate_response(batch, parsed, categories_by_root, root_to_system)

    if issues:
        structural = [issue for issue in issues if issue in base.STRUCTURAL_ISSUES or issue.startswith("입력 ")]
        if structural:
            failed_ids = [item["meaning_id"] for item in batch]
        else:
            failed_ids = extract_failed_ids(batch, parsed, categories_by_root, root_to_system)
            if not failed_ids:
                failed_ids = [item["meaning_id"] for item in batch]
        repair_prompt = build_repair_prompt(batch, raw_text, issues, failed_ids, category_dict)
        repaired_provider = provider_used
        repaired_model = model if provider_used == provider else base.fallback_model_name(provider_used)
        try:
            repaired_text = base.call_model(repaired_provider, system_prompt, repair_prompt, repaired_model, timeout, max_retries, retry_backoff)
        except Exception as exc:
            if not fallback_provider or repaired_provider == fallback_provider:
                raise
            fallback_key = os.getenv("OPENAI_API_KEY") if fallback_provider == "openai" else os.getenv("GEMINI_API_KEY")
            if not fallback_key:
                raise RuntimeError(f"repair 단계 provider `{repaired_provider}` 실패 후 fallback `{fallback_provider}` 키가 없어 재시도 불가: {exc}") from exc
            repaired_provider = fallback_provider
            provider_used = fallback_provider
            repaired_text = base.call_model(
                fallback_provider,
                system_prompt,
                repair_prompt,
                base.fallback_model_name(fallback_provider),
                timeout,
                max_retries,
                retry_backoff,
            )
        raw_texts.append(repaired_text)
        repaired_parsed = parse_model_response(repaired_text, batch_index, batch, raw_texts, "repair", categories_by_root, root_to_system)
        if failed_ids and len(failed_ids) < len(batch):
            repaired_map = {row["id"]: row for row in repaired_parsed.get("decisions", []) if isinstance(row, dict)}
            merged = {"decisions": []}
            for row in parsed.get("decisions", []):
                if row.get("id") in repaired_map:
                    merged["decisions"].append(repaired_map[row["id"]])
                else:
                    merged["decisions"].append(row)
            parsed = normalize_decision_fields(merged, categories_by_root, root_to_system)
        else:
            parsed = repaired_parsed
        parsed = apply_current_assignment_fallback(parsed, batch, categories_by_root, root_to_system)
        issues = validate_response(batch, parsed, categories_by_root, root_to_system)

    if issues:
        quarantine_batch(batch_index, batch, raw_texts, issues)
        raise RuntimeError(f"batch_{batch_index:04d} 검증 실패: {'; '.join(issues[:5])}")

    split = split_decisions(parsed, categories_by_root, root_to_system)
    report = {
        "batch_index": batch_index,
        "provider_used": provider_used,
        "input_count": len(batch),
        "core_count": len(split["CORE"]),
        "system_cand_count": len(split["SYSTEM_CAND"]),
        "cat_cand_count": len(split["CAT_CAND"]),
        "excluded_count": len(split["EXCLUDED"]),
    }
    return split, report


def merge_pools(pools: dict, split: dict) -> None:
    pools["CORE"].update(split["CORE"])
    pools["SYSTEM_CAND"].extend(split["SYSTEM_CAND"])
    pools["CAT_CAND"].extend(split["CAT_CAND"])
    pools["EXCLUDED"].extend(split["EXCLUDED"])


def write_checkpoint(pools: dict, batch_reports: list[dict], next_offset: int, llm_queue_count: int, total_input: int, batch_size: int, provider: str, fallback_provider: str | None, model: str) -> None:
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
    base.write_json_atomic(CHECKPOINT_FILE, payload)
    base.write_json_atomic(
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


def load_checkpoint() -> dict | None:
    if CHECKPOINT_FILE.exists():
        return json.loads(CHECKPOINT_FILE.read_text(encoding="utf-8"))
    return None


def build_core_node(meaning_id: str, cls_info: dict, src: dict, stats_map: dict[str, dict], max_frequency: int, max_round: int, rank_map: dict[str, int], raw_grade_index: dict[tuple[str, str], list[dict]]) -> dict:
    stats_row = stats_map.get(meaning_id)
    grade_ko = infer_grade_ko(src, raw_grade_index)
    band = compute_band(stats_row, max_frequency, max_round)
    frequency = stats_row.get("total_frequency") if stats_row else None
    rank = rank_map.get(meaning_id) if stats_row else None
    round_count = stats_row.get("round_count") if stats_row else None
    return {
        "id": meaning_id,
        "word": src.get("lemma", ""),
        "pos": src.get("pos_ko", ""),
        "roman": src.get("phonetic_romanization") or "",
        "def_ko": src.get("meaning_kr", ""),
        "def_en": src.get("e_word") or src.get("meaning_en") or "",
        "surface": "mindmap_core",
        "routing": "mindmap_core",
        "hierarchy": {
            "system": cls_info["system"],
            "root": cls_info["root"],
            "category": cls_info["category"],
            "path_ko": f"{cls_info['system']} > {cls_info['root']} > {cls_info['category']}",
            "root_id": cls_info["system"],
            "root_label": cls_info["system"],
            "root_en": "",
            "scene": cls_info["root"],
        },
        "stats": {
            "frequency": frequency,
            "rank": rank,
            "round_count": round_count,
            "band": band,
            "level": compute_level(grade_ko, band),
        },
    }


def build_search_item(node: dict) -> dict:
    return {
        "id": node["id"],
        "word": node["word"],
        "roman": node["roman"],
        "def_ko": node["def_ko"],
        "def_en": node["def_en"],
        "pos": node["pos"],
        "surface": node["surface"],
        "routing": node["routing"],
        "hierarchy": {
            "system": node["hierarchy"]["system"],
            "root": node["hierarchy"]["root"],
            "category": node["hierarchy"]["category"],
            "path_ko": node["hierarchy"]["path_ko"],
            "root_id": node["hierarchy"]["root_id"],
            "root_label": node["hierarchy"]["root_label"],
            "root_en": node["hierarchy"]["root_en"],
            "scene": node["hierarchy"]["scene"],
        },
        "stats": node["stats"],
    }


def publish_outputs(pools: dict, source_rows: list[dict]) -> dict:
    source_map = {row["meaning_id"]: row for row in source_rows}
    stats_map, max_frequency, max_round, rank_map = load_stats_map()
    raw_grade_index = load_raw_grade_index()
    situations = []
    expressions = []
    basics = []
    for meaning_id, cls_info in sorted(pools["CORE"].items()):
        src = source_map[meaning_id]
        node = build_core_node(
            meaning_id,
            cls_info,
            src,
            stats_map,
            max_frequency,
            max_round,
            rank_map,
            raw_grade_index,
        )
        if cls_info["system"] == "상황과 장소":
            situations.append(node)
        elif cls_info["system"] == "마음과 표현":
            expressions.append(node)
        else:
            basics.append(node)

    search = [build_search_item(node) for node in situations + expressions + basics]

    base.write_json_atomic(APP_SITUATIONS, situations)
    base.write_json_atomic(APP_EXPRESSIONS, expressions)
    base.write_json_atomic(APP_BASICS, basics)
    base.write_json_atomic(APP_SEARCH, search)

    summary = {
        "situations_total": len(situations),
        "expressions_total": len(expressions),
        "basics_total": len(basics),
        "search_total": len(search),
        "band_non_null_total": sum(1 for node in situations + expressions + basics if node["stats"]["band"] is not None),
        "level_unrated_total": sum(1 for node in situations + expressions + basics if node["stats"]["level"] == "Unrated"),
    }
    base.write_json_atomic(REV23_DIR / "REV23_PUBLISH_SUMMARY_V1.json", summary)
    return summary


def publish_from_saved_outputs() -> dict:
    source_rows = load_jsonl(MASTER_POOL)
    pools = {
        "CORE": json.loads(REV23_CORE.read_text(encoding="utf-8")),
        "SYSTEM_CAND": json.loads(REV23_SYSTEM.read_text(encoding="utf-8")) if REV23_SYSTEM.exists() else [],
        "CAT_CAND": json.loads(REV23_CATEGORY.read_text(encoding="utf-8")) if REV23_CATEGORY.exists() else [],
        "EXCLUDED": json.loads(REV23_EXCLUDED.read_text(encoding="utf-8")) if REV23_EXCLUDED.exists() else [],
    }
    summary = publish_outputs(pools, source_rows)
    if LATEST_REPORT_FILE.exists():
        latest = json.loads(LATEST_REPORT_FILE.read_text(encoding="utf-8"))
        latest["publish_summary"] = summary
        base.write_json_atomic(LATEST_REPORT_FILE, latest)
    return summary


def run_triage(batch_size: int, limit: int | None, provider: str, fallback_provider: str | None, model: str, timeout: int, max_retries: int, retry_backoff: int, publish: bool) -> None:
    category_dict = load_category_dict()
    categories_by_root, root_to_system = build_category_maps(category_dict)
    source_rows = load_jsonl(MASTER_POOL)
    source_total = len(source_rows)
    all_rows = source_rows[:limit] if limit is not None else source_rows
    is_partial_run = len(all_rows) < source_total

    pools = {"CORE": {}, "SYSTEM_CAND": [], "CAT_CAND": [], "EXCLUDED": []}
    batch_reports = []
    llm_queue = []
    RUN_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    for row in all_rows:
        filtered = base.prefilter_exclusion(row)
        if filtered:
            split = {"CORE": {}, "SYSTEM_CAND": [], "CAT_CAND": [], "EXCLUDED": [{"id": filtered["id"], "reason": filtered["reason"]}]}
            merge_pools(pools, split)
        else:
            llm_queue.append(row)

    checkpoint = load_checkpoint()
    start_offset = 0
    if checkpoint and checkpoint.get("batch_size") == batch_size and checkpoint.get("model") == model and checkpoint.get("provider") == provider and checkpoint.get("fallback_provider") == fallback_provider and checkpoint.get("total_input") == len(all_rows) and checkpoint.get("llm_queue_count") == len(llm_queue):
        pools = checkpoint["pools"]
        batch_reports = checkpoint["batch_reports"]
        start_offset = checkpoint["next_offset"]

    for batch_index, start in enumerate(range(start_offset, len(llm_queue), batch_size), start=(start_offset // batch_size) + 1):
        batch = llm_queue[start:start + batch_size]
        split, report = process_batch(batch_index, batch, provider, model, fallback_provider, timeout, max_retries, retry_backoff, category_dict, categories_by_root, root_to_system)
        merge_pools(pools, split)
        batch_reports.append(report)
        write_checkpoint(pools, batch_reports, start + len(batch), len(llm_queue), len(all_rows), batch_size, provider, fallback_provider, model)
        print(json.dumps({"batch_index": batch_index, "input_count": report["input_count"], "core": report["core_count"], "system_cand": report["system_cand_count"], "cat_cand": report["cat_cand_count"], "excluded": report["excluded_count"]}, ensure_ascii=False))

    if live_quarantine_files():
        raise RuntimeError("격리된 실패 배치가 있어 최종 산출물 쓰기를 중단합니다.")

    base.write_json_atomic(REV23_CORE, pools["CORE"])
    base.write_json_atomic(REV23_SYSTEM, pools["SYSTEM_CAND"])
    base.write_json_atomic(REV23_CATEGORY, pools["CAT_CAND"])
    base.write_json_atomic(REV23_EXCLUDED, pools["EXCLUDED"])

    latest = {
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
    }
    if publish and not is_partial_run:
        latest["publish_summary"] = publish_outputs(pools, source_rows)
    base.write_json_atomic(LATEST_REPORT_FILE, latest)
    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--publish-only", action="store_true")
    parser.add_argument("--batch-size", type=int, default=60)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--provider", default="gemini", choices=["gemini", "openai"])
    parser.add_argument("--fallback-provider", default="openai", choices=["none", "gemini", "openai"])
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--retry-backoff", type=int, default=5)
    args = parser.parse_args()

    fallback_provider = None if args.fallback_provider == "none" else args.fallback_provider
    if fallback_provider == args.provider:
        fallback_provider = None
    model = args.model or (base.DEFAULT_MODEL if args.provider == "gemini" else base.DEFAULT_OPENAI_MODEL)

    if args.publish_only:
        print(json.dumps({"publish_summary": publish_from_saved_outputs()}, ensure_ascii=False))
        return

    if not args.execute:
        print(json.dumps({"mode": "review_only", "master_pool": str(MASTER_POOL), "provider": args.provider, "fallback_provider": fallback_provider, "model": model, "batch_size": args.batch_size, "publish": args.publish}, ensure_ascii=False))
        return

    run_triage(args.batch_size, args.limit, args.provider, fallback_provider, model, args.timeout, args.max_retries, args.retry_backoff, args.publish)


if __name__ == "__main__":
    main()
