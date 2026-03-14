import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BATCH_SIZE = 60


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path):
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_name")
    parser.add_argument("--size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument(
        "--bucket",
        default="system_candidate",
        choices=["system_candidate", "category_candidate", "excluded", "all_unaudited"],
    )
    parser.add_argument("--sort", default="frequency", choices=["frequency", "lexical"])
    args = parser.parse_args()

    ledger = load_json(ROOT / "08_expansion" / "inventory" / "INVENTORY_LEDGER_V1.json")

    if args.bucket == "all_unaudited":
        rows = [row for row in ledger if row["audit_status"] == "unaudited"]
    else:
        rows = [
            row
            for row in ledger
            if row["audit_status"] == "unaudited" and row["current_bucket"] == args.bucket
        ]

    if args.sort == "frequency":
        rows.sort(
            key=lambda row: (
                row["frequency_rank"] is None,
                row["frequency_rank"] if row["frequency_rank"] is not None else 10**9,
                row["meaning_id"],
            )
        )
    else:
        rows.sort(key=lambda row: row["meaning_id"])

    selected_ids = [row["meaning_id"] for row in rows[: args.size]]
    source_map = {
        row["meaning_id"]: row
        for row in load_jsonl(
            ROOT / "05_source" / "extracted_corpus" / "snapshot_20260309" / "Lemma_Meanings.jsonl"
        )
    }
    ledger_map = {row["meaning_id"]: row for row in ledger}
    batch_rows = []
    for mid in selected_ids:
        source = source_map[mid]
        meta = ledger_map[mid]
        batch_rows.append(
            {
                "meaning_id": source["meaning_id"],
                "lemma": source["lemma"],
                "pos_ko": source["pos_ko"],
                "meaning_kr": source["meaning_kr"],
                "frequency": source.get("frequency"),
                "frequency_rank": source.get("frequency_rank"),
                "current_bucket": meta["current_bucket"],
                "current_root": meta["current_root"],
                "current_reason": meta["current_reason"],
            }
        )
    out_dir = ROOT / "08_expansion" / "batch_inputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.batch_name}.json"
    out_path.write_text(json.dumps(batch_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "batch_name": args.batch_name,
                "count": len(batch_rows),
                "bucket": args.bucket,
                "sort": args.sort,
                "output": str(out_path),
                "first_ids": selected_ids[:10],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
