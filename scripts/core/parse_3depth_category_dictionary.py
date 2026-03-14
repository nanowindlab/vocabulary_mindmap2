import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_MD = ROOT / "08_expansion" / "IA_V4_3DEPTH_CATEGORY_DICTIONARY_V1.md"
OUTPUT_JSON = ROOT / "08_expansion" / "IA_V4_3DEPTH_CATEGORY_DICTIONARY_V1.json"


SYSTEM_RE = re.compile(r"^## \d+\. \[(.+?)\]")
ROOT_RE = re.compile(r"^### \d+\.\d+\. (.+?) \(")
CATEGORY_RE = re.compile(r"^- \*\*(.+?)\*\*: (.+)$")


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    lines = SOURCE_MD.read_text(encoding="utf-8").splitlines()
    systems = {}
    system_name = None
    root_name = None

    for line in lines:
        line = line.rstrip()
        system_match = SYSTEM_RE.match(line)
        if system_match:
            system_name = system_match.group(1)
            systems.setdefault(system_name, {})
            root_name = None
            continue

        root_match = ROOT_RE.match(line)
        if root_match and system_name:
            root_name = root_match.group(1)
            systems[system_name].setdefault(root_name, {"categories": [], "exclusions": []})
            continue

        category_match = CATEGORY_RE.match(line)
        if category_match and system_name and root_name:
            label = category_match.group(1)
            desc = category_match.group(2)
            target = "exclusions" if label == "[배제]" else "categories"
            systems[system_name][root_name][target].append(
                {"label": label, "description": desc}
            )

    write_json(OUTPUT_JSON, systems)
    print(json.dumps({"systems": len(systems), "output_json": str(OUTPUT_JSON)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
