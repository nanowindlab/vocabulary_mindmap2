import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "09_app" / "public" / "data"
INTERNAL_DIR = DATA_DIR / "internal"
LEGACY_DIR = DATA_DIR / "legacy"
MAIN_CORE = INTERNAL_DIR / "APP_READY_CORE_PAYLOAD_V1.json"
MAIN_TREE = LEGACY_DIR / "APP_READY_CORE_TREE_V1.json"
MAIN_SEARCH = LEGACY_DIR / "APP_READY_SEARCH_INDEX_V1.json"
META_TREE = LEGACY_DIR / "APP_READY_META_TREE_V1.json"
EXPR_TREE = LEGACY_DIR / "APP_READY_EXPRESSION_TREE_V1.json"
BASE_MEANINGS = ROOT / "05_source" / "extracted_corpus" / "snapshot_20260309" / "Lemma_Meanings.jsonl"
AUG_MEANINGS = ROOT / "08_expansion" / "augmentation" / "RAW_DICTIONARY_MISSING_CANDIDATES_V1.jsonl"
REPORT_JSON = ROOT / "08_expansion" / "augmentation" / "CORE_TREE_SEARCH_REBUILD_SUMMARY_V1.json"


GRADE_RE = re.compile(r"\[(초|중|고)\]")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


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


def infer_grade(row: dict) -> str:
    if row.get("grade") in {"초", "중", "고"}:
        return row["grade"]
    notation = row.get("level_pos_notation") or ""
    match = GRADE_RE.search(notation)
    if match:
        return match.group(1)
    return "초"


def grade_en(grade_ko: str) -> str:
    return {
        "초": "Beginner",
        "중": "Intermediate",
        "고": "Advanced",
    }.get(grade_ko, "Beginner")


def build_core_item(meaning_id: str, cls_info: dict, src: dict) -> dict:
    system = cls_info.get("system", "")
    root = cls_info.get("root", "")
    grade_ko = infer_grade(src)
    return {
        "id": meaning_id,
        "word": src.get("lemma", ""),
        "pos": src.get("pos_ko", ""),
        "roman": src.get("phonetic_romanization") or "",
        "def_ko": src.get("meaning_kr", ""),
        "def_en": src.get("e_word") or src.get("meaning_en") or "",
        "hierarchy": {
            "system": system,
            "root": root,
            "path_ko": f"{system} > {root} > {src.get('pos_ko', '')}",
            "root_id": system,
            "root_label": system,
            "root_en": "",
            "scene": root,
            "category": src.get("pos_ko", ""),
        },
        "stats": {
            "freq": src.get("frequency") or 0,
            "rank": src.get("frequency_rank") or 0,
            "grade": grade_ko,
            "grade_en": grade_en(grade_ko),
        },
    }


def build_search_item(core_item: dict) -> dict:
    return {
        "id": core_item["id"],
        "word": core_item["word"],
        "roman": core_item["roman"],
        "def_ko": core_item["def_ko"],
        "def_en": core_item["def_en"],
        "pos": core_item["pos"],
        "surface": "mindmap_core",
        "routing": "mindmap_core",
        "hierarchy": {
            "system": core_item["hierarchy"]["system"],
            "root": core_item["hierarchy"]["root"],
            "path_ko": f"{core_item['hierarchy']['system']} > {core_item['hierarchy']['root']}",
            "root_id": core_item["hierarchy"]["root_id"],
            "root_label": core_item["hierarchy"]["root_label"],
            "root_en": core_item["hierarchy"]["root_en"],
            "scene": core_item["hierarchy"]["scene"],
            "category": core_item["hierarchy"]["category"],
        },
        "stats": core_item["stats"],
    }


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    core_payload = load_json(MAIN_CORE)
    source_map = {}
    source_map.update(load_jsonl_map(BASE_MEANINGS))
    source_map.update(load_jsonl_map(AUG_MEANINGS))

    missing_ids = sorted(mid for mid in core_payload if mid not in source_map)
    if missing_ids:
        raise RuntimeError(f"Source rows missing for core payload ids: {missing_ids[:20]}")

    core_tree = [
        build_core_item(mid, core_payload[mid], source_map[mid])
        for mid in sorted(core_payload.keys())
    ]

    meta_tree = load_json(META_TREE)
    expr_tree = load_json(EXPR_TREE)
    search_index = [build_search_item(item) for item in core_tree] + meta_tree + expr_tree

    write_json(MAIN_TREE, core_tree)
    write_json(MAIN_SEARCH, search_index)
    write_json(
        REPORT_JSON,
        {
            "core_payload_total": len(core_payload),
            "core_tree_total": len(core_tree),
            "meta_total": len(meta_tree),
            "expression_total": len(expr_tree),
            "search_index_total": len(search_index),
            "missing_source_ids": 0,
        },
    )

    print(
        json.dumps(
            {
                "core_tree_total": len(core_tree),
                "search_index_total": len(search_index),
                "report_json": str(REPORT_JSON),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
