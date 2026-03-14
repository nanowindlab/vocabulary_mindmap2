import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTHORITATIVE_GENERAL_BATCH_MAX = 60


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


def load_batch_audits(batch_runs_dir: Path):
    audits = {}
    for report_path in sorted(batch_runs_dir.glob("*_report.json")):
        try:
            report = load_json(report_path)
        except Exception:
            continue
        profile = report.get("profile")
        if profile != "general_inventory":
            continue
        if report.get("input_count", 10**9) > AUTHORITATIVE_GENERAL_BATCH_MAX:
            continue
        prefix = report_path.name[: -len("_report.json")]
        validated_path = batch_runs_dir / f"{prefix}_validated.json"
        if not validated_path.exists():
            continue
        validated = load_json(validated_path)
        for decision in validated.get("decisions", []):
            audits[decision["meaning_id"]] = {
                "bucket": decision["bucket"],
                "root": decision.get("root"),
                "note": decision.get("candidate_reason")
                or decision.get("exclusion_reason")
                or decision.get("rationale_short"),
                "source_batch": prefix,
            }
    return audits


def main() -> None:
    source_rows = load_jsonl(
        ROOT / "05_source" / "extracted_corpus" / "snapshot_20260309" / "Lemma_Meanings.jsonl"
    )
    system = {row["id"]: row for row in load_json(ROOT / "08_expansion" / "SYSTEM_CANDIDATES_V1.json")}
    category = {row["id"]: row for row in load_json(ROOT / "08_expansion" / "CATEGORY_CANDIDATES_V1.json")}
    excluded = {row["id"]: row for row in load_json(ROOT / "08_expansion" / "EXCLUDED_WORDS_V1.json")}
    core = load_json(ROOT / "09_app" / "public" / "data" / "internal" / "APP_READY_CORE_PAYLOAD_V1.json")

    audit_actions_path = ROOT / "08_expansion" / "PAYLOAD_136_AUDIT_ACTIONS_V1.json"
    audit_actions = load_json(audit_actions_path) if audit_actions_path.exists() else {}
    root_shift_map = {
        row["meaning_id"]: row for row in audit_actions.get("root_shifts", [])
    }
    candidate_demotion_map = {
        row["meaning_id"]: row for row in audit_actions.get("candidate_demotions", [])
    }
    general_batch_audits = load_batch_audits(ROOT / "08_expansion" / "batch_runs")

    ledger = []
    for row in source_rows:
        mid = row["meaning_id"]
        record = {
            "meaning_id": mid,
            "lemma": row["lemma"],
            "pos_ko": row["pos_ko"],
            "meaning_kr": row["meaning_kr"],
            "frequency": row.get("frequency"),
            "frequency_rank": row.get("frequency_rank"),
            "current_bucket": None,
            "current_root": None,
            "current_reason": None,
            "audit_status": "unaudited",
            "audit_recommended_bucket": None,
            "audit_recommended_root": None,
            "audit_note": None,
        }
        if mid in core:
            record["current_bucket"] = "core"
            record["current_root"] = core[mid]["root"]
        elif mid in system:
            record["current_bucket"] = "system_candidate"
            record["current_reason"] = system[mid]["reason"]
        elif mid in category:
            record["current_bucket"] = "category_candidate"
            record["current_reason"] = category[mid]["reason"]
        elif mid in excluded:
            record["current_bucket"] = "excluded"
            record["current_reason"] = excluded[mid]["reason"]
        else:
            record["current_bucket"] = "untracked"

        if mid in general_batch_audits:
            action = general_batch_audits[mid]
            record["audit_status"] = "audited"
            record["audit_recommended_bucket"] = action["bucket"]
            record["audit_recommended_root"] = action["root"]
            record["audit_note"] = f"{action['source_batch']}|{action['note']}"
        elif mid in root_shift_map:
            action = root_shift_map[mid]
            record["audit_status"] = "audited"
            record["audit_recommended_bucket"] = "core"
            record["audit_recommended_root"] = action["new_root"]
            record["audit_note"] = (
                f"root_shift:{action['old_root']}->{action['new_root']}|{action['rationale_short']}"
            )
        elif mid in candidate_demotion_map:
            action = candidate_demotion_map[mid]
            record["audit_status"] = "audited"
            record["audit_recommended_bucket"] = "candidate"
            record["audit_recommended_root"] = action["suggested_root"]
            record["audit_note"] = action["candidate_reason"]
        elif mid in excluded:
            record["audit_status"] = "audited"
            record["audit_recommended_bucket"] = "excluded"
            record["audit_note"] = record["current_reason"]
        elif mid in core:
            record["audit_status"] = "audited"
            record["audit_recommended_bucket"] = "core"
            record["audit_recommended_root"] = record["current_root"]

        ledger.append(record)

    out_dir = ROOT / "08_expansion" / "inventory"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "INVENTORY_LEDGER_V1.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (out_dir / "INVENTORY_LEDGER_V1.jsonl").open("w", encoding="utf-8") as f:
        for row in ledger:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {
        "total": len(ledger),
        "current_bucket_counts": {},
        "audit_status_counts": {},
    }
    for row in ledger:
        summary["current_bucket_counts"][row["current_bucket"]] = (
            summary["current_bucket_counts"].get(row["current_bucket"], 0) + 1
        )
        summary["audit_status_counts"][row["audit_status"]] = (
            summary["audit_status_counts"].get(row["audit_status"], 0) + 1
        )
    (out_dir / "INVENTORY_LEDGER_SUMMARY_V1.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
