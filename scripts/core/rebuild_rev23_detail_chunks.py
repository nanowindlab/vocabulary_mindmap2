import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "09_app" / "public" / "data"
LIVE_DIR = DATA_DIR / "live"
INTERNAL_DIR = DATA_DIR / "internal"
SITUATIONS = LIVE_DIR / "APP_READY_SITUATIONS_TREE.json"
EXPRESSIONS = LIVE_DIR / "APP_READY_EXPRESSIONS_TREE.json"
BASICS = LIVE_DIR / "APP_READY_BASICS_TREE.json"
SEARCH = LIVE_DIR / "APP_READY_SEARCH_INDEX.json"
MANIFEST = LIVE_DIR / "CHUNK_MANIFEST_V1.json"
REPORT = ROOT / "08_expansion" / "rev23" / "REV42_DETAIL_CHUNK_REBUILD_SUMMARY_V1.json"

SCHEMA_COMPLETE = INTERNAL_DIR / "APP_READY_SCHEMA_COMPLETE_V1.json"
MASTER_POOL = ROOT / "08_expansion" / "master_pool" / "MASTER_POOL_V1.jsonl"
EXAMPLES_JSONL = ROOT / "05_source" / "extracted_corpus" / "snapshot_20260309" / "Lemma_Examples.jsonl"
RAW_DICT = ROOT / "05_source" / "raw_dictionary" / "한국어 어휘사전(영어판)_사전.json"
LEGACY_PROJECTION = INTERNAL_DIR / "APP_READY_PROJECTION_V2_DETAIL_LITE.json"
LEGACY_ARCHIVE_DIR = ROOT / "archive" / "09_app_v2" / "public" / "data"

CHUNK_SIZE = 400

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


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def collect_live_tree_rows() -> tuple[list[dict], dict[str, list[dict]]]:
    split_rows = {
        "situations": load_json(SITUATIONS),
        "expressions": load_json(EXPRESSIONS),
        "basics": load_json(BASICS),
    }
    ordered = split_rows["situations"] + split_rows["expressions"] + split_rows["basics"]
    return ordered, split_rows


def summarize_duplicate_ids(rows: list[dict]) -> dict[str, list[dict]]:
    positions = defaultdict(list)
    for idx, row in enumerate(rows, start=1):
        positions[row["id"]].append(
            {
                "row_index": idx,
                "word": row.get("word"),
                "system": (row.get("hierarchy") or {}).get("system"),
                "root": (row.get("hierarchy") or {}).get("root"),
                "category": (row.get("hierarchy") or {}).get("category"),
            }
        )
    return {
        meaning_id: entries
        for meaning_id, entries in positions.items()
        if len(entries) > 1
    }


def validate_unique_live_inputs(rows: list[dict]) -> None:
    duplicates = summarize_duplicate_ids(rows)
    if not duplicates:
        return
    sample = {
        meaning_id: entries
        for meaning_id, entries in list(sorted(duplicates.items()))[:10]
    }
    raise RuntimeError(
        "Duplicate ids detected in live tree inputs. "
        f"duplicate_id_count={len(duplicates)} sample={json.dumps(sample, ensure_ascii=False)}"
    )


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"[.。,，·ㆍ:;!?]+$", "", text)
    text = re.sub(r"\s+", "", text)
    return text


def build_raw_index() -> dict[tuple[str, str], list[dict]]:
    raw = load_json(RAW_DICT)
    index = defaultdict(list)
    for row in raw:
        entry = row["entry"]
        lemma = entry["headword_ko"]
        pos_ko = RAW_POS_MAP.get(entry.get("pos"), entry.get("pos"))
        for sense in row.get("senses", []):
            index[(lemma, pos_ko)].append(
                {
                    "sense_no": sense.get("sense_no"),
                    "definition": normalize_text(sense.get("definition_ko")),
                    "example_ko": sense.get("example_ko"),
                    "related_vocab": entry.get("related_vocab") or [],
                }
            )
    return index


def find_raw_match(raw_index: dict, src: dict) -> dict | None:
    candidates = raw_index.get((src.get("lemma"), src.get("pos_ko")), [])
    if not candidates:
        return None
    exact = [cand for cand in candidates if cand["sense_no"] == src.get("sense_number")]
    if len(exact) == 1:
        return exact[0]
    norm_def = normalize_text(src.get("meaning_kr"))
    fuzzy = [
        cand
        for cand in candidates
        if cand["definition"] and norm_def and (norm_def in cand["definition"] or cand["definition"] in norm_def)
    ]
    if len(fuzzy) == 1:
        return fuzzy[0]
    if len(exact) >= 1:
        return exact[0]
    return candidates[0]


def build_examples_map() -> dict[str, list[dict]]:
    examples_map = defaultdict(list)
    for row in load_jsonl(EXAMPLES_JSONL):
        examples_map[row["meaning_id"]].append(
            {
                "ko": row.get("example_sentence"),
                "en": row.get("translation_en"),
                "round": None,
                "category": row.get("example_type"),
            }
        )
    return examples_map


def build_legacy_related_vocab_map() -> dict[str, list[str]]:
    word_map = defaultdict(set)

    projection = load_json(LEGACY_PROJECTION)
    for row in projection:
        rel = tuple(row.get("related_vocab") or [])
        if row.get("word") and rel:
            word_map[row["word"]].add(rel)

    for path in sorted(LEGACY_ARCHIVE_DIR.glob("APP_READY_CHUNK_RICH_chunk_*.json")):
        data = load_json(path)
        for row in data.values():
            word = row.get("word")
            rel = tuple(row.get("related_vocab") or [])
            if word and rel:
                word_map[word].add(rel)

    return {word: list(next(iter(values))) for word, values in word_map.items() if len(values) == 1}


def build_legacy_detail_map() -> dict[str, dict]:
    detail_map = defaultdict(lambda: {"related_vocab": set(), "cross_links": []})
    source_count = Counter()

    projection = load_json(LEGACY_PROJECTION)
    for row in projection:
        word = row.get("word")
        if not word:
            continue
        rel = tuple(row.get("related_vocab") or [])
        refs = row.get("refs", {}).get("cross_links") or []
        if rel or refs:
            source_count[word] += 1
            if rel:
                detail_map[word]["related_vocab"].add(rel)
            if refs:
                detail_map[word]["cross_links"].append(refs)

    for path in sorted(LEGACY_ARCHIVE_DIR.glob("APP_READY_CHUNK_RICH_chunk_*.json")):
        data = load_json(path)
        for row in data.values():
            word = row.get("word")
            if not word:
                continue
            rel = tuple(row.get("related_vocab") or [])
            refs = row.get("refs", {}).get("cross_links") or []
            if rel or refs:
                source_count[word] += 1
                if rel:
                    detail_map[word]["related_vocab"].add(rel)
                if refs:
                    detail_map[word]["cross_links"].append(refs)

    final = {}
    for word, payload in detail_map.items():
        related_vocab = []
        if len(payload["related_vocab"]) == 1:
            related_vocab = list(next(iter(payload["related_vocab"])))
        cross_links = payload["cross_links"][0] if len(payload["cross_links"]) == 1 else []
        if related_vocab or cross_links:
            final[word] = {"related_vocab": related_vocab, "cross_links": cross_links}
    return final


def build_legacy_examples_map() -> dict[str, list[dict]]:
    word_map = defaultdict(list)
    for path in sorted(LEGACY_ARCHIVE_DIR.glob("APP_READY_CHUNK_EXAMPLES_chunk_*.json")):
        obj = load_json(path)
        data = obj.get("data", {})
        for key, row in data.items():
            if not key.startswith("lemma__"):
                continue
            parts = key.split("__")
            if len(parts) < 2:
                continue
            word = parts[1]
            if row.get("attested_sentences"):
                word_map[word].append(row["attested_sentences"])
    return {word: values[0] for word, values in word_map.items() if len(values) == 1}


def build_source_map() -> dict[str, dict]:
    source = {}
    schema = load_json(SCHEMA_COMPLETE)
    for meaning_id, row in schema.items():
        source[meaning_id] = {
            "meaning_id": meaning_id,
            "lemma": row.get("lemma") or row.get("word"),
            "pos_ko": row.get("pos"),
            "meaning_kr": row.get("meaning_kr"),
            "phonetic_romanization": row.get("phonetic"),
            "sentences": row.get("sentences") or [],
            "related_vocab": row.get("related_vocab") or [],
            "sense_number": None,
        }
    for row in load_jsonl(MASTER_POOL):
        source.setdefault(row["meaning_id"], row)
    return source


def build_attested_sentences(src: dict, examples_map: dict[str, list[dict]], raw_match: dict | None, legacy_examples_map: dict[str, list[dict]]) -> list[dict]:
    rows = []
    for sent in src.get("sentences") or []:
        text = sent.get("sentence") or sent.get("ko")
        if text:
            rows.append({"ko": text, "en": sent.get("en"), "round": None, "category": sent.get("type")})
    for sent in examples_map.get(src["meaning_id"], []):
        if sent.get("ko"):
            rows.append(sent)
    if raw_match and raw_match.get("example_ko"):
        rows.append({"ko": raw_match["example_ko"], "en": None, "round": None, "category": "국어사전"})
    if not rows and legacy_examples_map.get(src.get("lemma")):
        rows.extend(legacy_examples_map[src.get("lemma")])

    unique = []
    seen = set()
    for row in rows:
        key = row.get("ko")
        if not key or key in seen:
            continue
        unique.append(row)
        seen.add(key)
    return unique[:8]


def rebuild() -> dict:
    trees, split_rows = collect_live_tree_rows()
    validate_unique_live_inputs(trees)

    source_map = build_source_map()
    raw_index = build_raw_index()
    examples_map = build_examples_map()
    legacy_related_map = build_legacy_related_vocab_map()
    legacy_detail_map = build_legacy_detail_map()
    legacy_examples_map = build_legacy_examples_map()

    rich_chunks = {}
    example_chunks = {}
    manifest = {"version": "REV23", "generated_at": datetime.now().isoformat(), "chunks": {}}

    related_non_empty = 0
    example_non_empty = 0

    for idx, node in enumerate(trees):
        chunk_no = (idx // CHUNK_SIZE) + 1
        chunk_id = f"chunk_{chunk_no:03d}"
        node["chunk_id"] = chunk_id

        src = source_map.get(node["id"], {})
        raw_match = find_raw_match(raw_index, src)
        node_has_related_vocab = "related_vocab" in node
        node_has_cross_links = isinstance(node.get("refs"), dict) and "cross_links" in node["refs"]

        related_vocab = (
            node.get("related_vocab", [])
            if node_has_related_vocab
            else (
                (src.get("related_vocab") or [])
                or (raw_match.get("related_vocab") if raw_match else [])
                or legacy_related_map.get(node.get("word"))
                or []
            )
        )
        cross_links = (
            node.get("refs", {}).get("cross_links", [])
            if node_has_cross_links
            else (
                legacy_detail_map.get(node.get("word"), {}).get("cross_links")
                or []
            )
        )
        attested = build_attested_sentences(src, examples_map, raw_match, legacy_examples_map)
        phonetic = src.get("phonetic_romanization") or node.get("roman") or ""

        if related_vocab:
            related_non_empty += 1
        if attested:
            example_non_empty += 1

        node["related_vocab"] = related_vocab
        node["refs"] = {"cross_links": cross_links}
        node["is_center_profile"] = False

        rich_chunks.setdefault(chunk_id, {})[node["id"]] = {
            "id": node["id"],
            "def_ko": node.get("def_ko"),
            "related_vocab": related_vocab,
            "is_center_profile": False,
            "refs": {"cross_links": cross_links},
            "phonetic_romanization": phonetic,
        }
        example_chunks.setdefault(chunk_id, {"chunk_id": chunk_id, "data": {}})["data"][node["id"]] = {
            "attested_sentences": attested,
            "related_vocab": related_vocab,
            "phonetic_romanization": phonetic,
        }

    # overwrite tree/search with chunk_id-enriched nodes
    situations_len = len(split_rows["situations"])
    expressions_len = len(split_rows["expressions"])
    basics_len = len(split_rows["basics"])
    situations_nodes = trees[:situations_len]
    expressions_nodes = trees[situations_len:situations_len + expressions_len]
    basics_nodes = trees[situations_len + expressions_len:]
    search_nodes = [
        {**node, "chunk_id": node["chunk_id"]}
        for node in trees
    ]

    write_json(SITUATIONS, situations_nodes)
    write_json(EXPRESSIONS, expressions_nodes)
    write_json(BASICS, basics_nodes)
    write_json(SEARCH, search_nodes)

    for chunk_id, data in rich_chunks.items():
        write_json(LIVE_DIR / f"APP_READY_CHUNK_RICH_{chunk_id}.json", data)
        write_json(LIVE_DIR / f"APP_READY_CHUNK_EXAMPLES_{chunk_id}.json", example_chunks[chunk_id])
        manifest["chunks"][chunk_id] = {
            "file_name": f"APP_READY_CHUNK_RICH_{chunk_id}.json",
            "item_count": len(data),
        }

    write_json(MANIFEST, manifest)

    summary = {
        "tree_total": len(trees),
        "chunk_count": len(rich_chunks),
        "related_non_empty": related_non_empty,
        "examples_non_empty": example_non_empty,
    }
    write_json(REPORT, summary)
    return summary


def main() -> None:
    summary = rebuild()
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
