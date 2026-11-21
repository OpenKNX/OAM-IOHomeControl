#!/usr/bin/env python3
"""Check the OAM's exact OFM dependency and optionally the generated module version."""
import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OFM = "lib/OFM-IOHomeControl"
URL = "https://github.com/OpenKNX/OFM-IOHomeControl"


def read_pin(root):
    rows = [line.split() for line in (root / "dependencies.txt").read_text().splitlines()]
    rows = [row for row in rows if len(row) >= 3 and row[2] == OFM]
    if len(rows) != 1 or len(rows[0]) != 4:
        raise SystemExit("Expected one OFM-IOHomeControl dependency row")
    revision, branch, _, url = rows[0]
    if not re.fullmatch(r"[0-9a-f]{40}", revision) or url.removesuffix(".git") != URL:
        raise SystemExit("The OFM dependency must name an exact GitHub commit")
    return revision, branch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--print-ref", action="store_true")
    parser.add_argument("--checkout", type=Path, help="resolved checkout if it is outside lib/")
    parser.add_argument("--versions", type=Path)
    args = parser.parse_args()
    revision, branch = read_pin(args.root)
    if args.print_ref:
        print(revision)
        return

    checkout = args.checkout or args.root / OFM
    head = subprocess.check_output(["git", "-C", checkout, "rev-parse", "HEAD"], text=True).strip()
    if head != revision:
        raise SystemExit(f"OFM checkout {head} differs from {branch} pin {revision}")
    library = json.loads((checkout / "library.json").read_text())
    version = library["version"]
    if library["name"] != "OFM-IOHomeControl" or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit("OFM library metadata has an invalid module name or version")
    if args.versions:
        macro = re.search(r'^#define MODULE_IOHomeControl_Version "([^"]+)"$',
                          args.versions.read_text(), re.MULTILINE)
        if not macro:
            raise SystemExit("Generated IOHomeControl version is missing")
        recorded_version, separator, recorded_revision = macro[1].partition("+")
        if not separator or recorded_version != version or not revision.startswith(recorded_revision) or len(recorded_revision) < 7:
            raise SystemExit("Generated IOHomeControl version does not match the pinned dependency")
    print(f"OFM {version} at {revision} ({branch})")


if __name__ == "__main__":
    main()
