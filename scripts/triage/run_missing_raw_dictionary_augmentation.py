import argparse
import json
from pathlib import Path

import llm_data_triage as triage


ROOT = Path(__file__).resolve().parents[2]
AUG_DIR = ROOT / "08_expansion" / "augmentation"
INPUT_FILE = AUG_DIR / "RAW_DICTIONARY_MISSING_CANDIDATES_V1.jsonl"
REPORT_DIR = AUG_DIR / "triage_reports"
QUARANTINE_DIR = AUG_DIR / "triage_quarantine"
AUG_CORE = AUG_DIR / "RAW_DICTIONARY_AUG_CORE_V1.json"
AUG_SYSTEM = AUG_DIR / "RAW_DICTIONARY_AUG_SYSTEM_CANDIDATES_V1.json"
AUG_CATEGORY = AUG_DIR / "RAW_DICTIONARY_AUG_CATEGORY_CANDIDATES_V1.json"
AUG_EXCLUDED = AUG_DIR / "RAW_DICTIONARY_AUG_EXCLUDED_V1.json"

MAIN_CORE = ROOT / "09_app" / "public" / "data" / "internal" / "APP_READY_CORE_PAYLOAD_V1.json"
MAIN_SYSTEM = ROOT / "08_expansion" / "SYSTEM_CANDIDATES_V1.json"
MAIN_CATEGORY = ROOT / "08_expansion" / "CATEGORY_CANDIDATES_V1.json"
MAIN_EXCLUDED = ROOT / "08_expansion" / "EXCLUDED_WORDS_V1.json"


def configure_module_paths() -> None:
    triage.MEANINGS_FILE = INPUT_FILE
    triage.RUN_REPORT_DIR = REPORT_DIR
    triage.CHECKPOINT_FILE = REPORT_DIR / "raw_dictionary_augmentation_checkpoint.json"
    triage.LATEST_REPORT_FILE = REPORT_DIR / "raw_dictionary_augmentation_latest_report.json"
    triage.QUARANTINE_DIR = QUARANTINE_DIR
    triage.CORE_PAYLOAD = AUG_CORE
    triage.SYSTEM_CANDIDATES = AUG_SYSTEM
    triage.CATEGORY_CANDIDATES = AUG_CATEGORY
    triage.EXCLUDED_WORDS = AUG_EXCLUDED


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def merge_unique_rows(existing: list[dict], incoming: list[dict]) -> list[dict]:
    seen = {row["id"] for row in existing}
    merged = list(existing)
    for row in incoming:
        if row["id"] not in seen:
            merged.append(row)
            seen.add(row["id"])
    return merged


def merge_outputs() -> dict:
    main_core = load_json(MAIN_CORE)
    main_system = load_json(MAIN_SYSTEM)
    main_category = load_json(MAIN_CATEGORY)
    main_excluded = load_json(MAIN_EXCLUDED)

    aug_core = load_json(AUG_CORE) if AUG_CORE.exists() else {}
    aug_system = load_json(AUG_SYSTEM) if AUG_SYSTEM.exists() else []
    aug_category = load_json(AUG_CATEGORY) if AUG_CATEGORY.exists() else []
    aug_excluded = load_json(AUG_EXCLUDED) if AUG_EXCLUDED.exists() else []

    collision_ids = sorted(set(main_core) & set(aug_core))
    if collision_ids:
        raise RuntimeError(f"CORE merge collision detected: {collision_ids[:10]}")

    merged_core = {**main_core, **aug_core}
    merged_system = merge_unique_rows(main_system, aug_system)
    merged_category = merge_unique_rows(main_category, aug_category)
    merged_excluded = merge_unique_rows(main_excluded, aug_excluded)

    triage.write_json_atomic(MAIN_CORE, merged_core)
    triage.write_json_atomic(MAIN_SYSTEM, merged_system)
    triage.write_json_atomic(MAIN_CATEGORY, merged_category)
    triage.write_json_atomic(MAIN_EXCLUDED, merged_excluded)

    summary = {
        "aug_core": len(aug_core),
        "aug_system_cand": len(aug_system),
        "aug_cat_cand": len(aug_category),
        "aug_excluded": len(aug_excluded),
        "merged_core_total": len(merged_core),
        "merged_system_total": len(merged_system),
        "merged_category_total": len(merged_category),
        "merged_excluded_total": len(merged_excluded),
    }
    triage.write_json_atomic(REPORT_DIR / "raw_dictionary_augmentation_merge_summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--batch-size", type=int, default=60)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--provider", default="gemini", choices=["gemini", "openai"])
    parser.add_argument("--fallback-provider", default="openai", choices=["none", "gemini", "openai"])
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--retry-backoff", type=int, default=5)
    parser.add_argument("--merge", action="store_true")
    args = parser.parse_args()

    configure_module_paths()

    fallback_provider = None if args.fallback_provider == "none" else args.fallback_provider
    if fallback_provider == args.provider:
        fallback_provider = None
    model = args.model or (
        triage.DEFAULT_MODEL if args.provider == "gemini" else triage.DEFAULT_OPENAI_MODEL
    )

    if not args.execute:
        print(
            json.dumps(
                {
                    "mode": "review_only",
                    "input_file": str(INPUT_FILE),
                    "provider": args.provider,
                    "fallback_provider": fallback_provider,
                    "model": model,
                    "batch_size": args.batch_size,
                    "merge": args.merge,
                },
                ensure_ascii=False,
            )
        )
        return

    triage.run_triage(
        batch_size=args.batch_size,
        limit=args.limit,
        provider=args.provider,
        fallback_provider=fallback_provider,
        model=model,
        timeout=args.timeout,
        max_retries=args.max_retries,
        retry_backoff=args.retry_backoff,
    )

    if args.merge:
        print(json.dumps({"merge_summary": merge_outputs()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
