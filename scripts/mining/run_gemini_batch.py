import argparse
import subprocess
from pathlib import Path


DEFAULT_MODEL = "gemini-2.5-flash"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_name")
    parser.add_argument("input_path")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--profile", default="general_inventory")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    input_path = Path(args.input_path)
    if not input_path.is_absolute():
        input_path = (root / input_path).resolve()

    output_prefix = root / "08_expansion" / "batch_runs" / args.batch_name
    cmd = [
        "python3",
        str(root / "gemini_batch_refiner.py"),
        "--model",
        args.model,
        "--profile",
        args.profile,
        "--input",
        str(input_path),
        "--output-prefix",
        str(output_prefix),
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
