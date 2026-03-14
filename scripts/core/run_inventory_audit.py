import argparse
import subprocess
from pathlib import Path


DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_PROFILE = "general_inventory"
DEFAULT_BATCH_SIZE = 60
DEFAULT_COUNT = 3


def run_cmd(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-index", type=int, required=True)
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--bucket", default="system_candidate")
    parser.add_argument("--sort", default="frequency")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--profile", default=DEFAULT_PROFILE)
    parser.add_argument("--suffix", default="L")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]

    for idx in range(args.start_index, args.start_index + args.count):
        batch_name = f"BATCH_{idx:03d}{args.suffix}"
        run_cmd(["python3", "build_inventory_ledger.py"], root)
        run_cmd(
            [
                "python3",
                "prepare_inventory_batch.py",
                batch_name,
                "--bucket",
                args.bucket,
                "--size",
                str(args.size),
                "--sort",
                args.sort,
            ],
            root,
        )
        run_cmd(
            [
                "python3",
                "run_gemini_batch.py",
                batch_name,
                f"08_expansion/batch_inputs/{batch_name}.json",
                "--model",
                args.model,
                "--profile",
                args.profile,
            ],
            root,
        )

    run_cmd(["python3", "build_inventory_ledger.py"], root)


if __name__ == "__main__":
    main()
