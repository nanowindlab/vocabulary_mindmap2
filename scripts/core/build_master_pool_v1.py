import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_MEANINGS = ROOT / "05_source" / "extracted_corpus" / "snapshot_20260309" / "Lemma_Meanings.jsonl"
AUG_MEANINGS = ROOT / "08_expansion" / "augmentation" / "RAW_DICTIONARY_MISSING_CANDIDATES_V1.jsonl"
CORE_PAYLOAD = ROOT / "09_app" / "public" / "data" / "internal" / "APP_READY_CORE_PAYLOAD_V1.json"
SYSTEM_CAND = ROOT / "08_expansion" / "SYSTEM_CANDIDATES_V1.json"
CATEGORY_CAND = ROOT / "08_expansion" / "CATEGORY_CANDIDATES_V1.json"
MASTER_DIR = ROOT / "08_expansion" / "master_pool"
MASTER_JSONL = MASTER_DIR / "MASTER_POOL_V1.jsonl"
SUMMARY_JSON = MASTER_DIR / "MASTER_POOL_SUMMARY_V1.json"


def load_jsonl_map(path: Path) -> dict[str, dict]:
    rows = {}
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                rows[row["meaning_id"]] = row
    return rows


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    source_map = {}
    source_map.update(load_jsonl_map(BASE_MEANINGS))
    source_map.update(load_jsonl_map(AUG_MEANINGS))

    core = json.loads(CORE_PAYLOAD.read_text(encoding="utf-8"))
    system_cand = json.loads(SYSTEM_CAND.read_text(encoding="utf-8"))
    category_cand = json.loads(CATEGORY_CAND.read_text(encoding="utf-8"))

    rows = []
    missing_source = []

    for meaning_id, cls in sorted(core.items()):
        src = source_map.get(meaning_id)
        if not src:
            missing_source.append(meaning_id)
            continue
        rows.append(
            {
                **src,
                "current_status": "CORE",
                "current_system": cls.get("system"),
                "current_root": cls.get("root"),
                "current_category": None,
                "current_reason": None,
                "master_pool_source": "rev21_core",
            }
        )

    for row in system_cand:
        src = source_map.get(row["id"])
        if not src:
            missing_source.append(row["id"])
            continue
        rows.append(
            {
                **src,
                "current_status": "SYSTEM_CAND",
                "current_system": None,
                "current_root": None,
                "current_category": None,
                "current_reason": row.get("reason"),
                "master_pool_source": "rev21_system_cand",
            }
        )

    for row in category_cand:
        src = source_map.get(row["id"])
        if not src:
            missing_source.append(row["id"])
            continue
        rows.append(
            {
                **src,
                "current_status": "CAT_CAND",
                "current_system": row.get("system"),
                "current_root": None,
                "current_category": None,
                "current_reason": row.get("reason"),
                "master_pool_source": "rev21_category_cand",
            }
        )

    MASTER_DIR.mkdir(parents=True, exist_ok=True)
    with MASTER_JSONL.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {
        "master_pool_total": len(rows),
        "core_count": len(core),
        "system_cand_count": len(system_cand),
        "cat_cand_count": len(category_cand),
        "status_counts": Counter(row["current_status"] for row in rows),
        "missing_source_ids": missing_source,
    }
    write_json(SUMMARY_JSON, summary)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
