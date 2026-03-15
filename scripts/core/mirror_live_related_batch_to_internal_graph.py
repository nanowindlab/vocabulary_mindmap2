import argparse
import json
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


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", required=True)
    parser.add_argument("--batch-name", required=True)
    parser.add_argument("--family", required=True)
    parser.add_argument("--ids", nargs="+")
    parser.add_argument("--provenance-basis", required=True)
    parser.add_argument("--revision", default="2026-03-15-PM")
    parser.add_argument("--jump-purpose", default="time_reference_navigation")
    parser.add_argument("--all-live-with-relations", action="store_true")
    parser.add_argument("--all-live", action="store_true")
    parser.add_argument("--include-cross-links", action="store_true")
    return parser.parse_args()


def load_live_map() -> dict[str, dict]:
    rows = []
    for path in LIVE_SPLITS:
        rows.extend(load_json(path))
    return {row["id"]: row for row in rows}


def resolve_candidate_ids(args: argparse.Namespace, live_map: dict[str, dict]) -> list[str]:
    if args.all_live:
        return sorted(live_map.keys())
    if args.all_live_with_relations:
        ids = [
            meaning_id
            for meaning_id, row in live_map.items()
            if (row.get("related_vocab") or []) or ((row.get("refs") or {}).get("cross_links") or [])
        ]
        return sorted(ids)
    if args.ids:
        return args.ids
    raise RuntimeError("Either --ids or --all-live-with-relations must be provided.")


def main() -> None:
    args = parse_args()
    graph = load_json(GRAPH_PATH)
    live_map = load_live_map()
    candidate_ids = resolve_candidate_ids(args, live_map)
    missing = [meaning_id for meaning_id in candidate_ids if meaning_id not in live_map]
    if missing:
        raise RuntimeError(f"Missing live ids: {missing}")

    candidate_rows = {meaning_id: live_map[meaning_id] for meaning_id in candidate_ids}
    base_family = args.family

    for meaning_id in candidate_ids:
        graph["nodes"].pop(meaning_id, None)

    graph["edges"] = [
        edge
        for edge in graph["edges"]
        if edge.get("scope") != args.scope and edge.get("source_id") not in set(candidate_ids)
    ]

    for meaning_id, row in candidate_rows.items():
        graph["nodes"][meaning_id] = {
            "id": row["id"],
            "word": row["word"],
            "pos": row["pos"],
            "system": row["hierarchy"]["system"],
            "root": row["hierarchy"]["root"],
            "category": row["hierarchy"]["category"],
            "chunk_id": row["chunk_id"],
            "anchor_family": base_family,
            "pilot_group": args.scope,
            "current_runtime": {
                "related_vocab_count": len(row.get("related_vocab") or []),
                "cross_links_count": len(((row.get("refs") or {}).get("cross_links") or [])),
            },
        }

    edge_numbers = [
        int(edge["edge_id"].split("_")[-1])
        for edge in graph["edges"]
        if str(edge.get("edge_id", "")).startswith("pilot_edge_")
    ]
    max_edge_num = max(edge_numbers, default=0)
    next_edge_num = max_edge_num + 1
    created_edges = 0
    seen_edges = set()

    for meaning_id, row in candidate_rows.items():
        for target_term in row.get("related_vocab") or []:
            target_id = None
            for live_id, live_row in live_map.items():
                if live_row["word"] != target_term:
                    continue
                if live_row["hierarchy"]["system"] != row["hierarchy"]["system"]:
                    continue
                if live_row["hierarchy"]["root"] != row["hierarchy"]["root"]:
                    continue
                if live_row["hierarchy"]["category"] != row["hierarchy"]["category"]:
                    continue
                target_id = live_id
                break
            if target_id is None or target_id == meaning_id:
                continue
            edge_key = (meaning_id, target_id, "related_vocab")
            if edge_key in seen_edges:
                continue

            target_row = live_map[target_id]
            graph["edges"].append(
                {
                    "edge_id": f"pilot_edge_{next_edge_num:03d}",
                    "source_id": meaning_id,
                    "target_id": target_id,
                    "target_term": target_row["word"],
                    "target_system": target_row["hierarchy"]["system"],
                    "target_root": target_row["hierarchy"]["root"],
                    "target_category": target_row["hierarchy"]["category"],
                    "display_intent": "related_vocab",
                    "relation_role": "scope_expand",
                    "jump_purpose": args.jump_purpose,
                    "reason": f"{row['word']} keeps learner-facing neighborhood parity with current live related terms.",
                    "hook_id": "DRAFT-REL",
                    "scope": args.scope,
                    "constraints": {"runtime_safe": True, "draft_only": True, "holdout": False},
                    "provenance": {
                        "source": "APP_READY_SEARCH_INDEX.json",
                        "basis": args.provenance_basis,
                        "revision": args.revision,
                    },
                }
            )
            seen_edges.add(edge_key)
            next_edge_num += 1
            created_edges += 1

        if args.include_cross_links:
            for cross in ((row.get("refs") or {}).get("cross_links") or []):
                target_id = cross.get("target_id")
                if not target_id or target_id == meaning_id or target_id not in live_map:
                    continue
                edge_key = (meaning_id, target_id, "cross_links")
                if edge_key in seen_edges:
                    continue
                target_row = live_map[target_id]
                graph["edges"].append(
                    {
                        "edge_id": f"pilot_edge_{next_edge_num:03d}",
                        "source_id": meaning_id,
                        "target_id": target_id,
                        "target_term": target_row["word"],
                        "target_system": target_row["hierarchy"]["system"],
                        "target_root": target_row["hierarchy"]["root"],
                        "target_category": target_row["hierarchy"]["category"],
                        "display_intent": "cross_links",
                        "relation_role": "scene_jump",
                        "jump_purpose": args.jump_purpose,
                        "reason": f"{row['word']} keeps learner-facing jump parity with current live cross-links.",
                        "hook_id": cross.get("hook_id") or "DRAFT-REL",
                        "scope": args.scope,
                        "constraints": {"runtime_safe": True, "draft_only": True, "holdout": False},
                        "provenance": {
                            "source": "APP_READY_SEARCH_INDEX.json",
                            "basis": args.provenance_basis,
                            "revision": args.revision,
                        },
                    }
                )
                seen_edges.add(edge_key)
                next_edge_num += 1
                created_edges += 1

    graph["status"] = f"{args.scope}_draft"
    graph["generated_at"] = datetime.now().isoformat()
    write_json(GRAPH_PATH, graph)

    print(
        json.dumps(
            {
                "status": graph["status"],
                "node_count": len(graph["nodes"]),
                "edge_count": len(graph["edges"]),
                "created_nodes": len(candidate_ids),
                "created_edges": created_edges,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
