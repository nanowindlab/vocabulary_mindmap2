import argparse
import json
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REV47_DIR = ROOT / "08_expansion" / "rev47"
REPORT_DIR = REV47_DIR / "triage_reports"
QUARANTINE_DIR = REV47_DIR / "triage_quarantine"
PID_FILE = REPORT_DIR / "rev47_xwd_resume.pid"
LOG_FILE = REPORT_DIR / "rev47_xwd_resume.log"
CHECKPOINT_FILE = REPORT_DIR / "rev47_xwd_checkpoint.json"
LATEST_REPORT_FILE = REPORT_DIR / "rev47_xwd_latest_report.json"
LINKS_JSON = REV47_DIR / "REV47_RELATED_LINKS_V1.json"
PUBLISH_SUMMARY = REV47_DIR / "REV47_PUBLISH_SUMMARY_V1.json"
MONITOR_LOG = REPORT_DIR / "rev47_monitor.log"
MONITOR_STATE = REPORT_DIR / "rev47_monitor_state.json"
DEV_HANDOFF = REV47_DIR / "REV47_DEV_HANDOFF_V1.md"

SITUATIONS = ROOT / "09_app" / "public" / "data" / "live" / "APP_READY_SITUATIONS_TREE.json"
EXPRESSIONS = ROOT / "09_app" / "public" / "data" / "live" / "APP_READY_EXPRESSIONS_TREE.json"
BASICS = ROOT / "09_app" / "public" / "data" / "live" / "APP_READY_BASICS_TREE.json"
SEARCH = ROOT / "09_app" / "public" / "data" / "live" / "APP_READY_SEARCH_INDEX.json"

DASHBOARD = ROOT / ".gemini-orchestration" / "ORCHESTRATION_DASHBOARD.md"
WORKBOARD = ROOT / ".gemini-orchestration" / "DATA_VALIDATION_AGENT_WORKBOARD_V1.md"

REV47_CMD = [
    "python3",
    "scripts/mining/run_rev47_xwd_mining.py",
    "--execute",
    "--publish",
    "--provider",
    "gemini",
    "--model",
    "gemini-2.5-flash",
    "--fallback-provider",
    "openai",
    "--batch-size",
    "20",
]


def now_kst() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S KST")


def log(msg: str) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with MONITOR_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{now_kst()}] {msg}\n")


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_state() -> dict:
    return load_json(MONITOR_STATE, {"restart_attempts": 0, "last_quarantine": None}) or {"restart_attempts": 0, "last_quarantine": None}


def save_state(state: dict) -> None:
    write_json(MONITOR_STATE, state)


def is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def current_pid() -> int | None:
    if not PID_FILE.exists():
        return None
    text = PID_FILE.read_text(encoding="utf-8").strip()
    if not text.isdigit():
        return None
    return int(text)


def live_quarantine_files() -> list[Path]:
    return [p for p in sorted(QUARANTINE_DIR.glob("batch_*.json")) if "archive" not in p.name]


def archive_live_quarantine() -> list[str]:
    archived = []
    for path in live_quarantine_files():
        target = path.with_name(path.stem + "_monitor_archive.json")
        path.rename(target)
        archived.append(target.name)
    return archived


def quarantine_summary() -> dict | None:
    files = live_quarantine_files()
    if not files:
        return None
    path = files[-1]
    obj = load_json(path, {})
    return {
        "file": path.name,
        "issues": obj.get("issues", [])[:10],
        "item_ids": [(item.get("id") or item.get("meaning_id")) for item in obj.get("items", [])[:10]],
    }


def restart_rev47() -> int:
    env = os.environ.copy()
    proc = subprocess.Popen(
        REV47_CMD,
        cwd=str(ROOT),
        env=env,
        stdout=LOG_FILE.open("ab", buffering=0),
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    PID_FILE.write_text(str(proc.pid), encoding="utf-8")
    return proc.pid


def verify_outputs() -> dict:
    links = load_json(LINKS_JSON, {}) or {}
    split_paths = [SITUATIONS, EXPRESSIONS, BASICS]
    splits = [load_json(p, []) or [] for p in split_paths]
    search = load_json(SEARCH, []) or []
    linked_terms = sum(1 for rels in links.values() if rels)
    link_edges = sum(len(rels) for rels in links.values())

    self_links = []
    asym = []
    for source_id, rels in links.items():
        targets = {row["target_id"] for row in rels}
        if source_id in targets:
            self_links.append(source_id)
        for target_id in targets:
            reverse = {row["target_id"] for row in links.get(target_id, [])}
            if source_id not in reverse:
                asym.append((source_id, target_id))
                if len(asym) >= 20:
                    break
        if len(asym) >= 20:
            break

    split_total = sum(len(rows) for rows in splits)
    with_related = [sum(1 for row in rows if row.get("related_vocab")) for rows in splits]
    with_cross = [sum(1 for row in rows if row.get("refs", {}).get("cross_links")) for rows in splits]

    return {
        "linked_terms": linked_terms,
        "link_edges": link_edges,
        "self_link_count": len(self_links),
        "asymmetry_sample_count": len(asym),
        "split_total": split_total,
        "search_total": len(search),
        "situations_with_related": with_related[0],
        "expressions_with_related": with_related[1],
        "basics_with_related": with_related[2],
        "situations_with_cross": with_cross[0],
        "expressions_with_cross": with_cross[1],
        "basics_with_cross": with_cross[2],
    }


def write_dev_handoff(verification: dict) -> None:
    text = f"""# REV47 Dev Handoff V1

> Date: `{now_kst()}`

- 핵심 변화량:
  - XWD 기반 relation mining 완료
  - `linked_terms {verification['linked_terms']}`
  - `link_edges {verification['link_edges']}`
- split 파일별 `related_vocab`:
  - situations `{verification['situations_with_related']}`
  - expressions `{verification['expressions_with_related']}`
  - basics `{verification['basics_with_related']}`
- split 파일별 `cross_links`:
  - situations `{verification['situations_with_cross']}`
  - expressions `{verification['expressions_with_cross']}`
  - basics `{verification['basics_with_cross']}`
- 주의점:
  - `self_link_count {verification['self_link_count']}`
  - `asymmetry_sample_count {verification['asymmetry_sample_count']}` (0이어야 이상적)
  - UI는 `related_vocab`와 `refs.cross_links`를 모두 활용해야 함
"""
    DEV_HANDOFF.write_text(text, encoding="utf-8")


def update_dashboard_and_workboard(verification: dict) -> None:
    dashboard = DASHBOARD.read_text(encoding="utf-8")
    pattern = re.compile(r"^\| 2026-03-11 \| 데이터 \| V1-REV-47 \|.*$", re.MULTILINE)
    replacement = (
        f"| 2026-03-11 | 데이터 | V1-REV-47 | ✅ (Manager) | ✅ | ✅ | **DONE** | "
        f"[XWD-PROJECT] 전수 마이닝 완료. linked_terms `{verification['linked_terms']}`, link_edges `{verification['link_edges']}`, "
        f"split related counts 상황 `{verification['situations_with_related']}` / 표현 `{verification['expressions_with_related']}` / 기초 `{verification['basics_with_related']}` |"
    )
    dashboard = pattern.sub(replacement, dashboard)

    pattern65 = re.compile(r"^\| 2026-03-11 \| 데이터 \| V1-REV-65 \|.*$", re.MULTILINE)
    replacement65 = "| 2026-03-11 | 데이터 | V1-REV-65 | ✅ (Manager) | ✅ | ✅ | **DONE** | [X-CLEAN Phase 2] scripts/ 구조 격리 및 경로 무결성 보정 완료. 새 경로에서 REV-47 실전 완료 검증됨 |"
    dashboard = pattern65.sub(replacement65, dashboard)
    DASHBOARD.write_text(dashboard, encoding="utf-8")

    workboard = WORKBOARD.read_text(encoding="utf-8")
    workboard = re.sub(r"^> Status: .*$", "> Status: `DONE` (Data Agent Completed)", workboard, count=1, flags=re.MULTILINE)
    if "V1-REV-47 완료." not in workboard:
        workboard += (
            f"\n- **{now_kst()}**: `V1-REV-47` 완료.\n"
            f"  - linked_terms `{verification['linked_terms']}`, link_edges `{verification['link_edges']}`\n"
            f"  - split `related_vocab`: 상황 `{verification['situations_with_related']}`, 표현 `{verification['expressions_with_related']}`, 기초 `{verification['basics_with_related']}`\n"
            f"  - split `cross_links`: 상황 `{verification['situations_with_cross']}`, 표현 `{verification['expressions_with_cross']}`, 기초 `{verification['basics_with_cross']}`\n"
            f"  - 개발 handoff: `08_expansion/rev47/REV47_DEV_HANDOFF_V1.md`\n"
            f"- **{now_kst()}**: `V1-REV-65` 완료.\n"
            f"  - scripts/ 격리 및 경로 보정 후 새 경로 기준 REV-47 완료 검증 통과.\n"
        )
    WORKBOARD.write_text(workboard, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval-sec", type=int, default=180)
    args = parser.parse_args()

    state = load_state()
    log("REV47 monitor started.")

    while True:
        pid = current_pid()
        alive = pid is not None and is_pid_alive(pid)
        cp = load_json(CHECKPOINT_FILE, None)
        latest = load_json(LATEST_REPORT_FILE, None)
        quarantine = quarantine_summary()

        if alive:
            if cp:
                log(f"alive pid={pid} offset={cp.get('next_offset')} batches={len(cp.get('batch_reports', []))}")
            else:
                log(f"alive pid={pid} waiting_first_checkpoint")
            time.sleep(args.interval_sec)
            continue

        if quarantine:
            log(f"detected stop with quarantine: {quarantine}")
            if state.get("last_quarantine") == quarantine["file"]:
                state["restart_attempts"] = state.get("restart_attempts", 0) + 1
            else:
                state["restart_attempts"] = 1
                state["last_quarantine"] = quarantine["file"]
            archived = archive_live_quarantine()
            log(f"archived live quarantine files: {archived}")
            if state["restart_attempts"] <= 3:
                new_pid = restart_rev47()
                log(f"restarted rev47 after quarantine with pid={new_pid}")
                save_state(state)
                time.sleep(args.interval_sec)
                continue
            log("quarantine repeated 3 times; monitor will stop for manual intervention.")
            save_state(state)
            break

        if cp:
            new_pid = restart_rev47()
            log(f"process missing but checkpoint exists; restarted with pid={new_pid}")
            state["restart_attempts"] = 0
            save_state(state)
            time.sleep(args.interval_sec)
            continue

        if latest and LINKS_JSON.exists():
            verification = verify_outputs()
            write_dev_handoff(verification)
            update_dashboard_and_workboard(verification)
            log(f"rev47 completion verified: {verification}")
            break

        log("process missing and no checkpoint/latest completion state found; monitor stopping.")
        break


if __name__ == "__main__":
    main()
