import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_MD = ROOT / "08_expansion" / "XWD_DISCOVERY_FRAMEWORK_V1.md"
OUTPUT_JSON = ROOT / "08_expansion" / "XWD_DISCOVERY_FRAMEWORK_V1.json"

HOOK_RE = re.compile(
    r"^\|\s+\*\*(H\d+)\*\*\s+\|\s+\*\*\[(.+?)\]\*\*\s+\|\s+(.+?)\s+\|\s+`(.+?)`\s+↔\s+`(.+?)`\s+\|\s+(.+?)\s+\|$"
)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    hooks = []
    for line in SOURCE_MD.read_text(encoding="utf-8").splitlines():
        match = HOOK_RE.match(line.rstrip())
        if not match:
            continue
        hooks.append(
            {
                "id": match.group(1),
                "name": match.group(2),
                "logic": match.group(3),
                "example_a": match.group(4),
                "example_b": match.group(5),
                "crossing": match.group(6),
            }
        )

    write_json(OUTPUT_JSON, {"hook_count": len(hooks), "hooks": hooks})
    print(json.dumps({"hook_count": len(hooks), "output_json": str(OUTPUT_JSON)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
