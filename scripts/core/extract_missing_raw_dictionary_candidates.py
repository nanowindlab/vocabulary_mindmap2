import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RAW_DICT = ROOT / "05_source" / "raw_dictionary" / "한국어 어휘사전(영어판)_사전.json"
MEANINGS_FILE = (
    ROOT / "05_source" / "extracted_corpus" / "snapshot_20260309" / "Lemma_Meanings.jsonl"
)
AUG_DIR = ROOT / "08_expansion" / "augmentation"
CANDIDATES_JSONL = AUG_DIR / "RAW_DICTIONARY_MISSING_CANDIDATES_V1.jsonl"
SKIPPED_JSON = AUG_DIR / "RAW_DICTIONARY_MISSING_SKIPPED_V1.json"
SUMMARY_JSON = AUG_DIR / "RAW_DICTIONARY_MISSING_SCAN_SUMMARY_V1.json"

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

NOTATION_POS_MAP = {
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

SPECIAL_POS_BY_LEMMA = {
    "그래도": "접속부사",
    "이래서": "접속부사",
    "얘": "대명사",
}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_text(text: str | None) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"[.。,，·ㆍ:;!?]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def infer_pos(entry: dict, sense: dict) -> str | None:
    raw_pos = entry.get("pos")
    if raw_pos in RAW_POS_MAP:
        return RAW_POS_MAP[raw_pos]

    lemma = entry["headword_ko"]
    if lemma in SPECIAL_POS_BY_LEMMA:
        return SPECIAL_POS_BY_LEMMA[lemma]

    notation = entry.get("level_pos_notation") or ""
    tags = re.findall(r"\[([^\]]+)\]", notation)
    for tag in tags:
        if tag in NOTATION_POS_MAP:
            return NOTATION_POS_MAP[tag]

    definition = sense.get("definition_ko") or ""
    if "줄어든 말" in definition and "'이 아이'" in definition:
        return "대명사"
    if "줄어든 말" in definition and "'그리하여도'" in definition:
        return "접속부사"
    if "줄어든 말" in definition and "'이리하여서'" in definition:
        return "접속부사"

    return None


def next_meaning_id(lemma: str, pos_ko: str, counters: dict[tuple[str, str], int]) -> str:
    counters[(lemma, pos_ko)] += 1
    return f"{lemma}_{pos_ko}-{counters[(lemma, pos_ko)]}"


def main() -> None:
    raw = json.loads(RAW_DICT.read_text(encoding="utf-8"))
    existing_rows = load_jsonl(MEANINGS_FILE)

    existing_keys = set()
    id_counters: dict[tuple[str, str], int] = defaultdict(int)
    for row in existing_rows:
        key = (row["lemma"], row["pos_ko"], row.get("sense_number"))
        existing_keys.add(key)
        prefix = (row["lemma"], row["pos_ko"])
        suffix = row["meaning_id"].rsplit("-", 1)[-1]
        if suffix.isdigit():
            id_counters[prefix] = max(id_counters[prefix], int(suffix))

    candidates = []
    skipped = []
    counters = Counter()

    for item in raw:
        entry = item["entry"]
        lemma = entry["headword_ko"]
        for sense in item.get("senses", []):
            pos_ko = infer_pos(entry, sense)
            key = (lemma, pos_ko, sense.get("sense_no"))
            if pos_ko and key in existing_keys:
                counters["already_present"] += 1
                continue

            record = {
                "lemma": lemma,
                "raw_pos": entry.get("pos"),
                "pos_ko": pos_ko,
                "level_pos_notation": entry.get("level_pos_notation"),
                "raw_homonym_no": entry.get("homonym_no"),
                "raw_sense_no": sense.get("sense_no"),
                "meaning_kr": normalize_text(sense.get("definition_ko")),
                "example_ko": sense.get("example_ko"),
                "e_word": None,
                "meaning_en": None,
                "raw_page_number": None,
            }

            translations = sense.get("translations") or []
            if translations:
                record["e_word"] = translations[0].get("equivalent")
                record["meaning_en"] = translations[0].get("definition")
                record["raw_page_number"] = translations[0].get("page_number")

            if not record["meaning_kr"] or not record["pos_ko"]:
                skipped.append(
                    {
                        **record,
                        "skip_reason": "missing_meaning_or_pos",
                    }
                )
                counters["skipped"] += 1
                continue

            meaning_id = next_meaning_id(lemma, pos_ko, id_counters)
            candidate = {
                "meaning_id": meaning_id,
                "lemma": lemma,
                "pos_ko": pos_ko,
                "meaning_kr": record["meaning_kr"],
                "e_word": record["e_word"],
                "phonetic_romanization": None,
                "frequency": None,
                "frequency_rank": None,
                "meaning_en": record["meaning_en"],
                "meaning_jp": None,
                "meaning_cn": None,
                "e_definition": record["meaning_en"],
                "usage_note": None,
                "sense_number": sense.get("sense_no"),
                "source": "raw_dictionary_augmentation_v1",
                "created_at": str(date.today()),
                "raw_homonym_no": entry.get("homonym_no"),
                "raw_sense_no": sense.get("sense_no"),
                "level_pos_notation": entry.get("level_pos_notation"),
                "example_ko": sense.get("example_ko"),
                "raw_page_number": record["raw_page_number"],
            }
            candidates.append(candidate)
            counters["candidates"] += 1

    AUG_DIR.mkdir(parents=True, exist_ok=True)
    with CANDIDATES_JSONL.open("w", encoding="utf-8") as f:
        for row in candidates:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    write_json(SKIPPED_JSON, skipped)
    write_json(
        SUMMARY_JSON,
        {
            "raw_entries": len(raw),
            "raw_senses": sum(len(item.get("senses", [])) for item in raw),
            "existing_meanings": len(existing_rows),
            "already_present": counters["already_present"],
            "augmentation_candidates": counters["candidates"],
            "skipped": counters["skipped"],
            "candidate_pos_counts": Counter(row["pos_ko"] for row in candidates),
            "skipped_examples": skipped[:20],
        },
    )

    print(
        json.dumps(
            {
                "raw_entries": len(raw),
                "raw_senses": sum(len(item.get("senses", [])) for item in raw),
                "existing_meanings": len(existing_rows),
                "already_present": counters["already_present"],
                "augmentation_candidates": counters["candidates"],
                "skipped": counters["skipped"],
                "candidates_jsonl": str(CANDIDATES_JSONL),
                "skipped_json": str(SKIPPED_JSON),
                "summary_json": str(SUMMARY_JSON),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
