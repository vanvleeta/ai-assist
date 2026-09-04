#!/usr/bin/env python3
"""
Flatten a TRR folder structure into a single output folder.

Input structure:
    root/reports/trr_id/platform/images/
    root/reports/trr_id/platform/ddms/
    root/reports/trr_id/platform/README.md

Output structure (fully flat):
    output/TRR####-README.md
    output/image1.png
    output/image2.jpg
    output/dump1.ddm
    output/...
"""

import argparse
import re
import shutil
from pathlib import Path


def extract_trr_number(readme_path: Path) -> str | None:
    """Extract the TRR number (e.g. TRR1234) from inside a README.md file."""
    content = readme_path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(TRR\d+)", content, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return None


def flatten_trr_folder(root: Path, output: Path, dry_run: bool = False):
    """Walk the root folder and flatten everything into the output folder."""
    reports_dir = root / "reports"
    if not reports_dir.is_dir():
        # Try root itself if there's no 'reports' subfolder
        reports_dir = root

    output.mkdir(parents=True, exist_ok=True)

    readmes_processed = 0
    files_copied = 0

    for readme in reports_dir.rglob("README.md"):
        # The platform dir is the parent of README.md
        platform_dir = readme.parent

        # Extract TRR number from the README content
        trr_number = extract_trr_number(readme)
        if not trr_number:
            # Fallback: try to get it from the folder name (trr_id level)
            trr_id_dir = platform_dir.parent
            fallback_match = re.search(r"(TRR\d+)", trr_id_dir.name, re.IGNORECASE)
            if fallback_match:
                trr_number = fallback_match.group(1).upper()
            else:
                print(f"  WARNING: Could not find TRR number for {readme}, skipping.")
                continue

        new_readme_name = f"{trr_number}-README.md"
        dest_readme = output / new_readme_name

        print(f"  {readme}  ->  {dest_readme}")
        if not dry_run:
            shutil.copy2(readme, dest_readme)
        readmes_processed += 1

        # Copy all files from images/, only .json files from ddms/
        copy_rules = {
            "images": None,            # No filter — copy everything
            "ddms": {".json"},         # Only .json files
        }
        for subdir_name, allowed_exts in copy_rules.items():
            subdir = platform_dir / subdir_name
            if not subdir.is_dir():
                continue

            for src_file in subdir.rglob("*"):
                if not src_file.is_file():
                    continue
                if allowed_exts and src_file.suffix.lower() not in allowed_exts:
                    continue
                dest_file = output / src_file.name
                print(f"  {src_file}  ->  {dest_file}")
                if not dry_run:
                    shutil.copy2(src_file, dest_file)
                files_copied += 1

    print(f"\nDone: {readmes_processed} READMEs processed, {files_copied} supporting files copied.")


def main():
    parser = argparse.ArgumentParser(
        description="Flatten a TRR folder structure into a single directory."
    )
    parser.add_argument("root", type=Path, help="Root folder containing the reports/ tree")
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("flattened_output"),
        help="Destination folder (default: ./flattened_output)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview what would happen without copying anything"
    )
    args = parser.parse_args()

    if not args.root.is_dir():
        parser.error(f"Root folder does not exist: {args.root}")

    print(f"Flattening: {args.root.resolve()}")
    print(f"Output to:  {args.output.resolve()}")
    if args.dry_run:
        print("** DRY RUN — no files will be copied **")
    print()

    flatten_trr_folder(args.root, args.output, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
