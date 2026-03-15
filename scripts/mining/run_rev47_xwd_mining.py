import argparse
import json
import math
import os
import re
import sys
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "triage"))

import llm_data_triage as base

DATA_DIR = ROOT / "09_app" / "public" / "data"
LIVE_DIR = DATA_DIR / "live"
INTERNAL_DIR = DATA_DIR / "internal"
XWD_JSON = ROOT / "08_expansion" / "XWD_DISCOVERY_FRAMEWORK_V1.json"
RUN_DIR = ROOT / "08_expansion" / "rev47"
REPORT_DIR = RUN_DIR / "triage_reports"
QUARANTINE_DIR = RUN_DIR / "triage_quarantine"
CHECKPOINT_FILE = REPORT_DIR / "rev47_xwd_checkpoint.json"
LATEST_REPORT_FILE = REPORT_DIR / "rev47_xwd_latest_report.json"
LINKS_JSON = RUN_DIR / "REV47_RELATED_LINKS_V1.json"
PUBLISH_SUMMARY = RUN_DIR / "REV47_PUBLISH_SUMMARY_V1.json"
INTERNAL_RELATION_GRAPH = INTERNAL_DIR / "RELATION_GRAPH_CANONICAL_V1.json"

SITUATIONS = LIVE_DIR / "APP_READY_SITUATIONS_TREE.json"
EXPRESSIONS = LIVE_DIR / "APP_READY_EXPRESSIONS_TREE.json"
BASICS = LIVE_DIR / "APP_READY_BASICS_TREE.json"
SEARCH = LIVE_DIR / "APP_READY_SEARCH_INDEX.json"

DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_BATCH_SIZE = 20
DEFAULT_TIMEOUT = 300
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 5
STOPWORDS = {
    "것",
    "일",
    "사람",
    "상태",
    "행위",
    "의미",
    "표현",
    "관련",
    "나타내다",
    "하다",
    "되다",
    "있는",
    "없는",
    "정도",
    "부분",
    "사용",
    "활동",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(path.parent)) as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def load_core_pool() -> list[dict]:
    items = []
    for path in [SITUATIONS, EXPRESSIONS, BASICS]:
        items.extend(load_json(path))
    return items


def summarize_duplicate_ids(items: list[dict]) -> dict[str, int]:
    counts = Counter(item["id"] for item in items)
    return {meaning_id: count for meaning_id, count in counts.items() if count > 1}


def validate_runtime_projection_contract(
    split_items: list[dict],
    search_items: list[dict],
    *,
    overlay_ids: set[str] | None = None,
    node_metadata: dict[str, dict] | None = None,
    phase: str,
) -> None:
    split_counts = Counter(item["id"] for item in split_items)
    search_counts = Counter(item["id"] for item in search_items)
    duplicate_split = summarize_duplicate_ids(split_items)
    duplicate_search = summarize_duplicate_ids(search_items)
    mismatched_counts = sorted(
        meaning_id
        for meaning_id in set(split_counts) | set(search_counts)
        if split_counts.get(meaning_id, 0) != search_counts.get(meaning_id, 0)
    )

    issues = []
    if duplicate_split:
        sample = dict(list(sorted(duplicate_split.items()))[:10])
        issues.append(f"duplicate split ids={len(duplicate_split)} sample={sample}")
    if duplicate_search:
        sample = dict(list(sorted(duplicate_search.items()))[:10])
        issues.append(f"duplicate search ids={len(duplicate_search)} sample={sample}")
    if mismatched_counts:
        issues.append(f"split/search count mismatch ids={len(mismatched_counts)} sample={mismatched_counts[:10]}")

    if overlay_ids is not None:
        split_id_set = set(split_counts)
        missing_overlay = sorted(overlay_ids - split_id_set)
        if missing_overlay:
            issues.append(
                "overlay ids missing from live runtime. "
                "publish-only is relation overlay only and cannot admit new runtime ids. "
                f"missing_count={len(missing_overlay)} sample={missing_overlay[:10]}"
            )

    if node_metadata:
        split_by_id = {item["id"]: item for item in split_items}
        hierarchy_mismatch = []
        for meaning_id, meta in node_metadata.items():
            live_item = split_by_id.get(meaning_id)
            if not live_item:
                continue
            live_hier = live_item.get("hierarchy", {})
            diffs = []
            if meta.get("system") != live_hier.get("system"):
                diffs.append(("system", meta.get("system"), live_hier.get("system")))
            if meta.get("root") != live_hier.get("root"):
                diffs.append(("root", meta.get("root"), live_hier.get("root")))
            if meta.get("category") != live_hier.get("category"):
                diffs.append(("category", meta.get("category"), live_hier.get("category")))
            if diffs:
                hierarchy_mismatch.append({"id": meaning_id, "diffs": diffs})
        if hierarchy_mismatch:
            issues.append(
                "internal canonical node hierarchy differs from live runtime. "
                "publish-only cannot be used for runtime reclassification. "
                f"mismatch_count={len(hierarchy_mismatch)} sample={hierarchy_mismatch[:10]}"
            )

    if issues:
        raise RuntimeError(
            f"Runtime projection contract violation during {phase}: " + " | ".join(issues)
        )


def role_rank(role: str) -> int:
    precedence = {
        "sense_disambiguation": 0,
        "grammar_anchor": 1,
        "scene_jump": 2,
        "collocation_expand": 3,
        "compare": 4,
        "substitute": 5,
        "contrast_lite": 6,
        "scope_expand": 7,
    }
    return precedence.get(role, 999)


def normalize_display_intent(value: str | None) -> str | None:
    if value in {"related_widget", "related_vocab"}:
        return "related_vocab"
    if value in {"jump_link", "cross_links"}:
        return "cross_links"
    return None


def build_projection_from_internal_canonical() -> dict | None:
    if not INTERNAL_RELATION_GRAPH.exists():
        return None

    payload = load_json(INTERNAL_RELATION_GRAPH)
    edges = payload.get("edges")
    if not isinstance(edges, list):
        return None

    all_items = load_core_pool()
    id_to_item = {item["id"]: item for item in all_items}
    pilot = payload.get("pilot", {})
    nodes = payload.get("nodes", {})
    overlay_ids = set(nodes.keys()) if isinstance(nodes, dict) and nodes else set()
    if not overlay_ids:
        overlay_ids = set(pilot.get("include_term_ids") or [])
        overlay_ids.update(pilot.get("holdout_term_ids") or [])
    if not overlay_ids:
        overlay_ids.update(edge.get("source_id") for edge in edges if isinstance(edge, dict))
    overlay_ids.discard(None)

    chosen_edges = {}
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        source_id = edge.get("source_id")
        target_id = edge.get("target_id")
        if source_id not in overlay_ids or target_id not in id_to_item:
            continue
        intent = normalize_display_intent(edge.get("display_intent"))
        if intent is None:
            continue
        pair = (source_id, target_id)
        candidate = (
            role_rank(edge.get("relation_role")),
            0 if intent == "cross_links" else 1,
            edge.get("edge_id", ""),
        )
        existing = chosen_edges.get(pair)
        if existing is None or candidate < existing[0]:
            chosen_edges[pair] = (candidate, edge, intent)

    related_vocab_map = {source_id: [] for source_id in overlay_ids}
    cross_links_map = {source_id: [] for source_id in overlay_ids}
    seen_terms = defaultdict(set)
    seen_targets = defaultdict(set)

    for (_, _), (_, edge, intent) in sorted(chosen_edges.items(), key=lambda row: row[1][0]):
        source_id = edge["source_id"]
        target = id_to_item[edge["target_id"]]
        if intent == "related_vocab":
            term = target["word"]
            if term in seen_terms[source_id]:
                continue
            related_vocab_map[source_id].append(term)
            seen_terms[source_id].add(term)
        else:
            target_id = target["id"]
            if target_id in seen_targets[source_id]:
                continue
            cross_links_map[source_id].append(
                {
                    "target_id": target_id,
                    "target_term": target["word"],
                    "target_system": target["hierarchy"]["system"],
                    "target_root": target["hierarchy"]["root"],
                    "target_category": target["hierarchy"]["category"],
                    "hook_id": edge.get("hook_id", "DRAFT-REL"),
                }
            )
            seen_targets[source_id].add(target_id)

    for source_id in overlay_ids:
        related_vocab_map[source_id] = related_vocab_map[source_id][:5]
        cross_links_map[source_id] = cross_links_map[source_id][:5]

    return {
        "overlay_ids": sorted(overlay_ids),
        "related_vocab_map": related_vocab_map,
        "cross_links_map": cross_links_map,
        "graph_status": payload.get("status"),
        "edge_count": len(edges),
        "node_metadata": {
            meaning_id: {
                "system": node.get("system"),
                "root": node.get("root"),
                "category": node.get("category"),
            }
            for meaning_id, node in (nodes.items() if isinstance(nodes, dict) else [])
        },
    }


def load_xwd_hooks() -> list[dict]:
    return load_json(XWD_JSON)["hooks"]


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[가-힣A-Za-z0-9]+", text or "")
    return [tok for tok in tokens if len(tok) >= 2 and tok not in STOPWORDS]


def signature(item: dict) -> set[str]:
    hier = item.get("hierarchy", {})
    tokens = set(tokenize(item.get("def_ko", "")))
    tokens.update(tokenize(item.get("word", "")))
    tokens.update(tokenize(hier.get("root", "")))
    tokens.update(tokenize(hier.get("category", "")))
    return tokens


def build_candidate_pool(source_item: dict, all_items: list[dict], index_by_id: dict[str, dict], limit: int = 60) -> list[dict]:
    src_sig = signature(source_item)
    src_system = source_item["hierarchy"]["system"]
    scored = []
    for candidate in all_items:
        if candidate["id"] == source_item["id"]:
            continue
        cand_sig = signature(candidate)
        overlap = len(src_sig & cand_sig)
        same_system = candidate["hierarchy"]["system"] == src_system
        score = overlap * 10
        if not same_system:
            score += 5
        if candidate["hierarchy"]["root"] == source_item["hierarchy"]["root"]:
            score += 3
        if candidate["hierarchy"]["category"] == source_item["hierarchy"]["category"]:
            score += 2
        if overlap > 0 or not same_system:
            scored.append((score, candidate["id"]))
    scored.sort(key=lambda row: (-row[0], row[1]))
    return [index_by_id[item_id] for _, item_id in scored[:limit]]


def build_system_prompt(hooks: list[dict]) -> str:
    lines = []
    for hook in hooks:
        lines.append(f"- {hook['id']} {hook['name']}: {hook['logic']}")
    return f"""너는 한국어 어휘 XWD 연관 데이터 마이닝 엔진이다.
목표는 3대 축을 넘나드는 맥락적 연관어를 보수적으로 추출하는 것이다.

[허용 훅]
{chr(10).join(lines)}

[핵심 규칙]
1. 단순 유사어 나열보다 맥락적 연결을 우선한다.
2. 후보군 밖의 단어를 만들지 말 것
3. 각 source는 최대 5개만 선택
4. self-link 금지
5. bidirectional 후처리를 전제로 하므로, source 입장에서 가장 설득력 있는 연결만 고를 것
6. 설명은 짧게 유지

[반환 규칙]
- JSON object만 반환
- 최상위 키는 `links`
- 각 항목은 `source_id`, `related` 포함
- `related`는 최대 5개 리스트
- 각 related 항목은 `target_id`, `hook_id`, `reason` 포함
"""


def build_user_prompt(batch: list[dict], candidate_pool_map: dict[str, list[dict]]) -> str:
    payload = []
    for item in batch:
        payload.append(
            {
                "source": {
                    "id": item["id"],
                    "word": item["word"],
                    "def_ko": item["def_ko"],
                    "system": item["hierarchy"]["system"],
                    "root": item["hierarchy"]["root"],
                    "category": item["hierarchy"]["category"],
                },
                "candidates": [
                    {
                        "id": cand["id"],
                        "word": cand["word"],
                        "def_ko": cand["def_ko"],
                        "system": cand["hierarchy"]["system"],
                        "root": cand["hierarchy"]["root"],
                        "category": cand["hierarchy"]["category"],
                    }
                    for cand in candidate_pool_map[item["id"]]
                ],
            }
        )
    return "아래 source별로 맥락적 연관어를 후보군 안에서만 선택하라.\n\n" + json.dumps(payload, ensure_ascii=False, indent=2)


def parse_links(raw_text: str, batch: list[dict]) -> dict:
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"XWD 응답 JSON 파싱 실패: {exc}") from exc
    if isinstance(parsed, list):
        parsed = {"links": parsed}
    if "links" not in parsed or not isinstance(parsed["links"], list):
        raise RuntimeError("XWD 응답에 links 리스트가 없습니다.")
    return parsed


def lemma_from_meaning_id(meaning_id: str | None) -> str | None:
    if not meaning_id or "_" not in meaning_id:
        return None
    return meaning_id.rsplit("_", 1)[0]


def normalize_links(
    parsed: dict,
    candidate_pool_map: dict[str, list[dict]],
    hooks: list[dict],
    expected_source_ids: list[str] | None = None,
) -> dict:
    hook_ids = {hook["id"] for hook in hooks}
    normalized_rows = {}
    for row in parsed.get("links", []):
        if not isinstance(row, dict):
            continue
        source_id = row.get("source_id")
        if not source_id:
            continue
        candidates = candidate_pool_map.get(source_id, [])
        candidate_ids = {cand["id"] for cand in candidates}
        candidate_by_word = defaultdict(list)
        for cand in candidates:
            candidate_by_word[cand["word"]].append(cand["id"])

        cleaned_related = []
        seen = set()
        for rel in row.get("related", []) if isinstance(row.get("related"), list) else []:
            if not isinstance(rel, dict):
                continue
            target_id = rel.get("target_id")
            if target_id not in candidate_ids:
                target_word = lemma_from_meaning_id(target_id)
                if target_word and len(candidate_by_word.get(target_word, [])) == 1:
                    target_id = candidate_by_word[target_word][0]
                else:
                    continue
            if target_id == source_id or target_id in seen:
                continue
            if rel.get("hook_id") not in hook_ids:
                continue
            reason = rel.get("reason")
            if not reason:
                continue
            cleaned_related.append(
                {
                    "target_id": target_id,
                    "hook_id": rel["hook_id"],
                    "reason": reason,
                }
            )
            seen.add(target_id)
        normalized_rows[source_id] = {"source_id": source_id, "related": cleaned_related[:5]}

    if expected_source_ids is None:
        return {"links": list(normalized_rows.values())}

    ordered = []
    for source_id in expected_source_ids:
        ordered.append(normalized_rows.get(source_id, {"source_id": source_id, "related": []}))
    return {"links": ordered}


def validate_links(parsed: dict, batch: list[dict], candidate_pool_map: dict[str, list[dict]], hooks: list[dict]) -> list[str]:
    issues = []
    parsed = normalize_links(
        parsed,
        candidate_pool_map,
        hooks,
        [item["id"] for item in batch],
    )
    hook_ids = {hook["id"] for hook in hooks}
    expected_ids = [item["id"] for item in batch]
    source_ids = [row.get("source_id") for row in parsed["links"] if isinstance(row, dict)]
    if source_ids != expected_ids:
        issues.append("입력 source 순서와 출력 source 순서가 다름")
    for row in parsed["links"]:
        if not isinstance(row, dict):
            issues.append("dict가 아닌 link 항목 존재")
            continue
        source_id = row.get("source_id")
        related = row.get("related")
        if not isinstance(related, list):
            issues.append(f"{source_id}: related가 리스트가 아님")
            continue
        if len(related) > 5:
            issues.append(f"{source_id}: related가 5개 초과")
        candidate_ids = {cand["id"] for cand in candidate_pool_map.get(source_id, [])}
        seen = set()
        for rel in related:
            target_id = rel.get("target_id")
            if target_id == source_id:
                issues.append(f"{source_id}: self-link")
            if target_id not in candidate_ids:
                issues.append(f"{source_id}: 후보군 밖 target `{target_id}`")
            if rel.get("hook_id") not in hook_ids:
                issues.append(f"{source_id}: invalid hook_id `{rel.get('hook_id')}`")
            if not rel.get("reason"):
                issues.append(f"{source_id}: reason 누락")
            if target_id in seen:
                issues.append(f"{source_id}: target 중복 `{target_id}`")
            seen.add(target_id)
    return issues


def quarantine_batch(batch_index: int, batch: list[dict], raw_text: str, issues: list[str]) -> None:
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        QUARANTINE_DIR / f"batch_{batch_index:04d}.json",
        {"batch_index": batch_index, "issues": issues, "items": batch, "response": raw_text},
    )


def mine_batch(batch_index: int, batch: list[dict], all_items: list[dict], index_by_id: dict[str, dict], hooks: list[dict], provider: str, model: str, fallback_provider: str | None, timeout: int, max_retries: int, retry_backoff: int) -> tuple[dict, dict]:
    candidate_pool_map = {item["id"]: build_candidate_pool(item, all_items, index_by_id) for item in batch}
    system_prompt = build_system_prompt(hooks)
    user_prompt = build_user_prompt(batch, candidate_pool_map)
    provider_used = provider
    try:
        raw_text = base.call_model(provider, system_prompt, user_prompt, model, timeout, max_retries, retry_backoff)
    except Exception as exc:
        if not fallback_provider:
            raise
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
    expected_source_ids = [item["id"] for item in batch]
    parsed = parse_links(raw_text, batch)
    parsed = normalize_links(parsed, candidate_pool_map, hooks, expected_source_ids)
    issues = validate_links(parsed, batch, candidate_pool_map, hooks)
    if issues:
        quarantine_batch(batch_index, batch, raw_text, issues)
        raise RuntimeError(f"batch_{batch_index:04d} 검증 실패: {'; '.join(issues[:5])}")
    report = {
        "batch_index": batch_index,
        "provider_used": provider_used,
        "input_count": len(batch),
        "source_with_links": sum(1 for row in parsed["links"] if row.get("related")),
        "link_count": sum(len(row.get("related", [])) for row in parsed["links"]),
    }
    return parsed, report


def merge_bidirectional(batches: list[dict]) -> dict[str, list[dict]]:
    relation_map = defaultdict(dict)
    for parsed in batches:
        for row in parsed["links"]:
            source_id = row["source_id"]
            for rel in row.get("related", []):
                relation_map[source_id][rel["target_id"]] = {
                    "target_id": rel["target_id"],
                    "hook_id": rel["hook_id"],
                    "reason": rel["reason"],
                }
                relation_map[rel["target_id"]][source_id] = {
                    "target_id": source_id,
                    "hook_id": rel["hook_id"],
                    "reason": rel["reason"],
                }
    return {
        source_id: sorted(list(targets.values()), key=lambda row: (row["hook_id"], row["target_id"]))[:5]
        for source_id, targets in relation_map.items()
    }


def enforce_bidirectional_limit(
    links_map: dict[str, list[dict]], max_links: int = 5
) -> dict[str, list[dict]]:
    edge_map = {}
    order_index = {}
    for source_id, rels in links_map.items():
        for idx, rel in enumerate(rels):
            target_id = rel["target_id"]
            pair = tuple(sorted((source_id, target_id)))
            edge = edge_map.setdefault(
                pair,
                {
                    "nodes": pair,
                    "count": 0,
                    "best_hook": rel["hook_id"],
                    "best_reason": rel["reason"],
                    "rank_sum": 0,
                },
            )
            edge["count"] += 1
            edge["rank_sum"] += idx
            if rel["hook_id"] < edge["best_hook"]:
                edge["best_hook"] = rel["hook_id"]
                edge["best_reason"] = rel["reason"]
            order_index[(source_id, target_id)] = idx

    sorted_edges = sorted(
        edge_map.values(),
        key=lambda edge: (
            -edge["count"],
            edge["rank_sum"],
            edge["best_hook"],
            edge["nodes"][0],
            edge["nodes"][1],
        ),
    )

    selected = defaultdict(list)
    selected_sets = defaultdict(set)
    for edge in sorted_edges:
        a, b = edge["nodes"]
        if len(selected[a]) >= max_links or len(selected[b]) >= max_links:
            continue
        if b in selected_sets[a] or a in selected_sets[b]:
            continue
        payload_ab = {
            "target_id": b,
            "hook_id": edge["best_hook"],
            "reason": edge["best_reason"],
        }
        payload_ba = {
            "target_id": a,
            "hook_id": edge["best_hook"],
            "reason": edge["best_reason"],
        }
        selected[a].append(payload_ab)
        selected[b].append(payload_ba)
        selected_sets[a].add(b)
        selected_sets[b].add(a)

    for source_id, rels in selected.items():
        rels.sort(key=lambda row: (row["hook_id"], row["target_id"]))
        selected[source_id] = rels[:max_links]
    return dict(selected)


def write_checkpoint(parsed_batches: list[dict], batch_reports: list[dict], next_offset: int, total_input: int, batch_size: int, provider: str, fallback_provider: str | None, model: str) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "next_offset": next_offset,
        "total_input": total_input,
        "batch_size": batch_size,
        "provider": provider,
        "fallback_provider": fallback_provider,
        "model": model,
        "parsed_batches": parsed_batches,
        "batch_reports": batch_reports,
    }
    write_json(CHECKPOINT_FILE, payload)
    bidirectional = merge_bidirectional(parsed_batches)
    write_json(
        LATEST_REPORT_FILE,
        {
            "total_input": total_input,
            "next_offset": next_offset,
            "provider": provider,
            "fallback_provider": fallback_provider,
            "model": model,
            "linked_terms": len(bidirectional),
            "link_edges": sum(len(v) for v in bidirectional.values()),
            "batch_reports": batch_reports,
        },
    )


def load_checkpoint() -> dict | None:
    if CHECKPOINT_FILE.exists():
        return load_json(CHECKPOINT_FILE)
    return None


def publish_relations(bidirectional: dict[str, list[dict]], all_items: list[dict]) -> dict:
    bidirectional = enforce_bidirectional_limit(bidirectional)
    related_vocab_map = {}
    cross_links_map = {}
    id_to_item = {item["id"]: item for item in all_items}
    for source_id, rels in bidirectional.items():
        words = []
        cross = []
        source = id_to_item[source_id]
        for rel in rels:
            target = id_to_item.get(rel["target_id"])
            if not target:
                continue
            same_classification = (
                target["hierarchy"]["system"] == source["hierarchy"]["system"]
                and target["hierarchy"]["root"] == source["hierarchy"]["root"]
                and target["hierarchy"]["category"] == source["hierarchy"]["category"]
            )
            if same_classification:
                words.append(target["word"])
            else:
                cross.append(
                    {
                        "target_id": target["id"],
                        "target_term": target["word"],
                        "target_system": target["hierarchy"]["system"],
                        "target_root": target["hierarchy"]["root"],
                        "target_category": target["hierarchy"]["category"],
                        "hook_id": rel["hook_id"],
                    }
                )
        related_vocab_map[source_id] = words
        cross_links_map[source_id] = cross

    split_paths = [SITUATIONS, EXPRESSIONS, BASICS]
    split_items = []
    for path in split_paths:
        items = load_json(path)
        for item in items:
            item["related_vocab"] = related_vocab_map.get(item["id"], [])
            item["refs"] = {"cross_links": cross_links_map.get(item["id"], [])}
            if "chunk_id" not in item and item["id"] in id_to_item:
                item["chunk_id"] = id_to_item[item["id"]].get("chunk_id")
        split_items.extend(items)
        write_json(path, items)

    split_by_id = {item["id"]: item for item in split_items}
    search_items = load_json(SEARCH)
    for item in search_items:
        item["related_vocab"] = related_vocab_map.get(item["id"], [])
        item["refs"] = {"cross_links": cross_links_map.get(item["id"], [])}
        if item["id"] in split_by_id:
            item["chunk_id"] = split_by_id[item["id"]].get("chunk_id")
    write_json(SEARCH, search_items)

    summary = {
        "linked_terms": sum(1 for rels in bidirectional.values() if rels),
        "related_terms": sum(1 for rels in related_vocab_map.values() if rels),
        "cross_system_terms": sum(1 for rels in cross_links_map.values() if rels),
        "avg_links_per_linked_term": round(
            sum(len(v) for v in bidirectional.values()) / max(1, sum(1 for v in bidirectional.values() if v)),
            2,
        ),
    }
    write_json(PUBLISH_SUMMARY, summary)
    return summary


def publish_from_saved_links() -> dict:
    internal_projection = build_projection_from_internal_canonical()
    if internal_projection is not None:
        overlay_ids = set(internal_projection["overlay_ids"])
        related_vocab_map = internal_projection["related_vocab_map"]
        cross_links_map = internal_projection["cross_links_map"]
        node_metadata = internal_projection.get("node_metadata") or {}

        split_paths = [SITUATIONS, EXPRESSIONS, BASICS]
        split_items = []
        split_payloads = {}
        search_items = load_json(SEARCH)
        for path in split_paths:
            items = load_json(path)
            split_payloads[path] = items
            split_items.extend(items)
        validate_runtime_projection_contract(
            split_items,
            search_items,
            overlay_ids=overlay_ids,
            node_metadata=node_metadata,
            phase="publish-only preflight",
        )

        split_items = []
        for path in split_paths:
            items = split_payloads[path]
            for item in items:
                if item["id"] in overlay_ids:
                    item["related_vocab"] = related_vocab_map.get(item["id"], [])
                    refs = item.get("refs", {}) if isinstance(item.get("refs"), dict) else {}
                    refs["cross_links"] = cross_links_map.get(item["id"], [])
                    item["refs"] = refs
                split_items.extend([item])
            write_json(path, items)

        split_by_id = {item["id"]: item for item in split_items}
        for item in search_items:
            if item["id"] in overlay_ids:
                item["related_vocab"] = related_vocab_map.get(item["id"], [])
                refs = item.get("refs", {}) if isinstance(item.get("refs"), dict) else {}
                refs["cross_links"] = cross_links_map.get(item["id"], [])
                item["refs"] = refs
                if item["id"] in split_by_id:
                    item["chunk_id"] = split_by_id[item["id"]].get("chunk_id")
        validate_runtime_projection_contract(
            split_items,
            search_items,
            overlay_ids=overlay_ids,
            node_metadata=node_metadata,
            phase="publish-only postflight",
        )
        write_json(SEARCH, search_items)

        summary = {
            "mode": "internal_canonical_overlay",
            "graph_status": internal_projection["graph_status"],
            "graph_edge_count": internal_projection["edge_count"],
            "overlay_terms": len(overlay_ids),
            "related_terms": sum(1 for source_id in overlay_ids if related_vocab_map.get(source_id)),
            "cross_system_terms": sum(1 for source_id in overlay_ids if cross_links_map.get(source_id)),
            "avg_links_per_overlay_term": round(
                (
                    sum(len(related_vocab_map.get(source_id, [])) + len(cross_links_map.get(source_id, [])) for source_id in overlay_ids)
                    / max(1, len(overlay_ids))
                ),
                2,
            ),
        }
        latest = load_json(LATEST_REPORT_FILE)
        latest["publish_summary"] = summary
        latest["linked_terms"] = sum(
            1
            for source_id in overlay_ids
            if related_vocab_map.get(source_id) or cross_links_map.get(source_id)
        )
        latest["link_edges"] = sum(
            len(related_vocab_map.get(source_id, [])) + len(cross_links_map.get(source_id, []))
            for source_id in overlay_ids
        )
        write_json(LATEST_REPORT_FILE, latest)
        write_json(PUBLISH_SUMMARY, summary)
        return summary

    bidirectional = load_json(LINKS_JSON)
    summary = publish_relations(bidirectional, load_core_pool())
    latest = load_json(LATEST_REPORT_FILE)
    latest["publish_summary"] = summary
    latest["linked_terms"] = sum(1 for rels in enforce_bidirectional_limit(bidirectional).values() if rels)
    latest["link_edges"] = sum(len(v) for v in enforce_bidirectional_limit(bidirectional).values())
    write_json(LATEST_REPORT_FILE, latest)
    return summary


def run(batch_size: int, limit: int | None, provider: str, fallback_provider: str | None, model: str, timeout: int, max_retries: int, retry_backoff: int, publish: bool) -> None:
    hooks = load_xwd_hooks()
    all_items = load_core_pool()
    if limit is not None:
        all_items = all_items[:limit]
    total_input = len(all_items)
    index_by_id = {item["id"]: item for item in all_items}

    checkpoint = load_checkpoint()
    parsed_batches = []
    batch_reports = []
    start_offset = 0
    if checkpoint and checkpoint.get("batch_size") == batch_size and checkpoint.get("provider") == provider and checkpoint.get("fallback_provider") == fallback_provider and checkpoint.get("model") == model and checkpoint.get("total_input") == total_input:
        parsed_batches = checkpoint["parsed_batches"]
        batch_reports = checkpoint["batch_reports"]
        start_offset = checkpoint["next_offset"]

    for batch_index, start in enumerate(range(start_offset, total_input, batch_size), start=(start_offset // batch_size) + 1):
        batch = all_items[start:start + batch_size]
        parsed, report = mine_batch(batch_index, batch, all_items, index_by_id, hooks, provider, model, fallback_provider, timeout, max_retries, retry_backoff)
        parsed_batches.append(parsed)
        batch_reports.append(report)
        write_checkpoint(parsed_batches, batch_reports, start + len(batch), total_input, batch_size, provider, fallback_provider, model)
        print(json.dumps(report, ensure_ascii=False))

    bidirectional = merge_bidirectional(parsed_batches)
    write_json(LINKS_JSON, bidirectional)
    latest = load_json(LATEST_REPORT_FILE)
    latest["linked_terms"] = sum(1 for rels in bidirectional.values() if rels)
    latest["link_edges"] = sum(len(v) for v in bidirectional.values())
    if publish:
        latest["publish_summary"] = publish_relations(bidirectional, load_core_pool())
    write_json(LATEST_REPORT_FILE, latest)
    if CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--publish-only", action="store_true")
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--provider", default="gemini", choices=["gemini", "openai"])
    parser.add_argument("--fallback-provider", default="openai", choices=["none", "gemini", "openai"])
    parser.add_argument("--model", default="gemini-2.5-flash")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--retry-backoff", type=int, default=5)
    args = parser.parse_args()

    fallback_provider = None if args.fallback_provider == "none" else args.fallback_provider
    if fallback_provider == args.provider:
        fallback_provider = None
    if args.publish_only:
        print(json.dumps({"publish_summary": publish_from_saved_links()}, ensure_ascii=False))
        return

    if not args.execute:
        print(json.dumps({"mode": "review_only", "hook_count": len(load_xwd_hooks()), "batch_size": args.batch_size, "publish": args.publish}, ensure_ascii=False))
        return

    run(args.batch_size, args.limit, args.provider, fallback_provider, args.model, args.timeout, args.max_retries, args.retry_backoff, args.publish)


if __name__ == "__main__":
    main()
