import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LIVE_DIR = ROOT / "09_app" / "public" / "data" / "live"
GRAPH_PATH = ROOT / "09_app" / "public" / "data" / "internal" / "RELATION_GRAPH_CANONICAL_V1.json"
LIVE_SPLITS = [
    LIVE_DIR / "APP_READY_SITUATIONS_TREE.json",
    LIVE_DIR / "APP_READY_EXPRESSIONS_TREE.json",
    LIVE_DIR / "APP_READY_BASICS_TREE.json",
]
STOPWORDS = {
    "것",
    "일",
    "수",
    "때",
    "상태",
    "정도",
    "부분",
    "행위",
    "의미",
    "사용",
    "활동",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", required=True)
    parser.add_argument("--batch-name", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--provenance-basis", required=True)
    parser.add_argument("--revision", default="2026-03-15-PM")
    parser.add_argument("--max-links", type=int, default=5)
    parser.add_argument("--exclude-ids", nargs="*", default=[])
    return parser.parse_args()


def load_live_rows() -> list[dict]:
    rows = []
    for path in LIVE_SPLITS:
        rows.extend(load_json(path))
    return rows


def tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[가-힣A-Za-z0-9]+", text or "")
    return {tok for tok in tokens if len(tok) >= 2 and tok not in STOPWORDS}


def signature(row: dict) -> set[str]:
    hier = row.get("hierarchy", {})
    tokens = set()
    tokens |= tokenize(row.get("word", ""))
    tokens |= tokenize(row.get("def_ko", ""))
    tokens |= tokenize(hier.get("root", ""))
    tokens |= tokenize(hier.get("category", ""))
    return tokens


def main() -> None:
    args = parse_args()
    graph = load_json(GRAPH_PATH)
    live_rows = load_live_rows()
    live_map = {row["id"]: row for row in live_rows}
    exclude_ids = set(args.exclude_ids)

    # Remove previous same-scope draft.
    graph["edges"] = [edge for edge in graph["edges"] if edge.get("scope") != args.scope]

    by_bucket = defaultdict(list)
    for row in live_rows:
        hier = row["hierarchy"]
        by_bucket[(hier["system"], hier["root"], hier["category"])].append(row)

    zero_rows = [
        row
        for row in live_rows
        if row["id"] not in exclude_ids
        and not (row.get("related_vocab") or [])
        and not (((row.get("refs") or {}).get("cross_links") or []))
    ]

    edge_numbers = [
        int(edge["edge_id"].split("_")[-1])
        for edge in graph["edges"]
        if str(edge.get("edge_id", "")).startswith("pilot_edge_")
    ]
    next_edge_num = max(edge_numbers, default=0) + 1
    created_edges = 0
    created_nodes = 0

    for row in zero_rows:
        meaning_id = row["id"]
        graph["nodes"][meaning_id] = {
            "id": row["id"],
            "word": row["word"],
            "pos": row["pos"],
            "system": row["hierarchy"]["system"],
            "root": row["hierarchy"]["root"],
            "category": row["hierarchy"]["category"],
            "chunk_id": row["chunk_id"],
            "anchor_family": args.family,
            "pilot_group": args.scope,
            "current_runtime": {"related_vocab_count": 0, "cross_links_count": 0},
        }
        created_nodes += 1

        bucket = (row["hierarchy"]["system"], row["hierarchy"]["root"], row["hierarchy"]["category"])
        peers = [peer for peer in by_bucket[bucket] if peer["id"] != meaning_id]
        if not peers:
            continue

        src_sig = signature(row)
        scored = []
        for peer in peers:
            peer_sig = signature(peer)
            overlap = len(src_sig & peer_sig)
            popularity = len(peer.get("related_vocab") or [])
            pos_bonus = 2 if peer.get("pos") == row.get("pos") else 0
            score = overlap * 10 + popularity + pos_bonus
            if score <= 0:
                continue
            scored.append((score, peer["id"], peer))
        if not scored:
            # Fall back to popular peers in the same category.
            for peer in peers:
                popularity = len(peer.get("related_vocab") or [])
                pos_bonus = 2 if peer.get("pos") == row.get("pos") else 0
                score = popularity + pos_bonus
                if score <= 0:
                    continue
                scored.append((score, peer["id"], peer))

        scored.sort(key=lambda item: (-item[0], item[1]))
        chosen_terms = set()
        chosen_edges = 0
        for _, _, peer in scored:
            if peer["word"] in chosen_terms:
                continue
            chosen_terms.add(peer["word"])
            graph["edges"].append(
                {
                    "edge_id": f"pilot_edge_{next_edge_num:03d}",
                    "source_id": meaning_id,
                    "target_id": peer["id"],
                    "target_term": peer["word"],
                    "target_system": peer["hierarchy"]["system"],
                    "target_root": peer["hierarchy"]["root"],
                    "target_category": peer["hierarchy"]["category"],
                    "display_intent": "related_vocab",
                    "relation_role": "scope_expand",
                    "jump_purpose": "heuristic_zero_relation_seed",
                    "reason": f"{row['word']} receives a same-category heuristic neighbor seed from current live parity.",
                    "hook_id": "HEURISTIC-SEED",
                    "scope": args.scope,
                    "constraints": {"runtime_safe": True, "draft_only": True, "holdout": False},
                    "provenance": {
                        "source": "APP_READY_SEARCH_INDEX.json",
                        "basis": args.provenance_basis,
                        "revision": args.revision,
                    },
                }
            )
            next_edge_num += 1
            created_edges += 1
            chosen_edges += 1
            if chosen_edges >= args.max_links:
                break

    graph["status"] = f"{args.scope}_draft"
    graph["generated_at"] = datetime.now().isoformat()
    write_json(GRAPH_PATH, graph)
    print(
        json.dumps(
            {
                "status": graph["status"],
                "zero_rows": len(zero_rows),
                "created_nodes": created_nodes,
                "created_edges": created_edges,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
