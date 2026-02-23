#!/usr/bin/env python3
"""
Dataset Statistics & Integrity Checker for DHSD
================================================
Generates comprehensive statistics for the German Handwriting Street-name
Dataset and optionally produces an 80/20 train/test split.

Usage:
    python dataset_statistics.py                # Print statistics
    python dataset_statistics.py --split        # Also write train.csv / test.csv
    python dataset_statistics.py --verify       # Verify all image files exist
    python dataset_statistics.py --checksums    # Generate checksums.sha256
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data.csv"
IMAGE_DIR = BASE_DIR / "german_hw_data"
RANDOM_SEED = 42
TEST_RATIO = 0.20

# German special characters to check
GERMAN_SPECIAL = set("äöüÄÖÜß")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_annotations(csv_path: Path) -> list[dict]:
    """Load data.csv and return a list of dicts."""
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def print_section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def compute_statistics(rows: list[dict]) -> dict:
    """Compute dataset-level statistics."""
    texts = [r["text"] for r in rows]
    writer_ids = [int(r["writer_id"]) for r in rows]

    writer_counts = Counter(writer_ids)
    unique_texts = set(texts)

    all_chars = set("".join(texts))
    german_chars_present = GERMAN_SPECIAL & all_chars
    german_chars_missing = GERMAN_SPECIAL - all_chars

    char_freq = Counter("".join(texts))

    # Word-length statistics (character count)
    lengths = [len(t) for t in texts]

    return {
        "total_images": len(rows),
        "total_writers": len(writer_counts),
        "unique_words": len(unique_texts),
        "writer_counts": writer_counts,
        "min_words_per_writer": min(writer_counts.values()),
        "max_words_per_writer": max(writer_counts.values()),
        "avg_words_per_writer": sum(writer_counts.values()) / len(writer_counts),
        "german_chars_present": sorted(german_chars_present),
        "german_chars_missing": sorted(german_chars_missing),
        "char_freq": char_freq,
        "avg_word_length": sum(lengths) / len(lengths),
        "min_word_length": min(lengths),
        "max_word_length": max(lengths),
        "writer_ids_sorted": sorted(writer_counts.keys()),
    }


def print_statistics(stats: dict) -> None:
    print_section("DHSD — Dataset Statistics")

    print(f"  Total images          : {stats['total_images']}")
    print(f"  Total writers         : {stats['total_writers']}")
    print(f"  Unique words          : {stats['unique_words']}")
    print(f"  Avg words / writer    : {stats['avg_words_per_writer']:.1f}")
    print(f"  Min words / writer    : {stats['min_words_per_writer']}")
    print(f"  Max words / writer    : {stats['max_words_per_writer']}")

    print_section("Word Length Statistics")
    print(f"  Avg word length (chars): {stats['avg_word_length']:.1f}")
    print(f"  Min word length        : {stats['min_word_length']}")
    print(f"  Max word length        : {stats['max_word_length']}")

    print_section("German Special Characters")
    if stats["german_chars_present"]:
        print(f"  Present : {' '.join(stats['german_chars_present'])}")
    if stats["german_chars_missing"]:
        print(f"  MISSING : {' '.join(stats['german_chars_missing'])}")
    else:
        print("  ✓ All German special characters are represented.")

    print_section("Writer Distribution")
    for wid in stats["writer_ids_sorted"]:
        count = stats["writer_counts"][wid]
        bar = "█" * (count // 5)
        print(f"  Writer {wid:>3d} : {count:>4d} samples  {bar}")

    print_section("Top-20 Most Frequent Characters")
    for char, freq in stats["char_freq"].most_common(20):
        display = repr(char) if char == " " else char
        print(f"  {display:>6s} : {freq:>6d}")


# ---------------------------------------------------------------------------
# Train / Test Split
# ---------------------------------------------------------------------------

def stratified_split(rows: list[dict], test_ratio: float = TEST_RATIO,
                     seed: int = RANDOM_SEED) -> tuple[list[dict], list[dict]]:
    """
    Stratified 80/20 split by writer_id (deterministic).
    Uses a simple modular-hash approach so it is reproducible without numpy.
    """
    import random
    rng = random.Random(seed)

    # Group by writer
    by_writer: dict[int, list[dict]] = {}
    for r in rows:
        wid = int(r["writer_id"])
        by_writer.setdefault(wid, []).append(r)

    train, test = [], []
    for wid in sorted(by_writer):
        samples = by_writer[wid]
        rng.shuffle(samples)
        split_idx = max(1, int(len(samples) * (1 - test_ratio)))
        train.extend(samples[:split_idx])
        test.extend(samples[split_idx:])

    return train, test


def write_split_csv(rows: list[dict], path: Path) -> None:
    fieldnames = ["file_name", "text", "writer_id"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Written {len(rows):>5d} rows → {path.name}")


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_images(rows: list[dict]) -> bool:
    """Check every image referenced in data.csv actually exists."""
    print_section("Image Verification")
    missing = []
    for r in rows:
        img_path = BASE_DIR / r["file_name"]
        if not img_path.is_file():
            missing.append(r["file_name"])

    if missing:
        print(f"  ✗ {len(missing)} image(s) NOT FOUND:")
        for m in missing[:20]:
            print(f"      {m}")
        if len(missing) > 20:
            print(f"      ... and {len(missing) - 20} more.")
        return False
    else:
        print(f"  ✓ All {len(rows)} images verified.")
        return True


# ---------------------------------------------------------------------------
# Checksums
# ---------------------------------------------------------------------------

def generate_checksums(rows: list[dict]) -> None:
    """Generate SHA-256 checksums for all images and data.csv."""
    print_section("Generating SHA-256 Checksums")
    checksum_path = BASE_DIR / "checksums.sha256"

    entries = []

    # Checksum for data.csv
    sha = hashlib.sha256(CSV_PATH.read_bytes()).hexdigest()
    entries.append(f"{sha}  data.csv")

    # Checksums for all images
    total = len(rows)
    for i, r in enumerate(rows, 1):
        img_path = BASE_DIR / r["file_name"]
        if img_path.is_file():
            sha = hashlib.sha256(img_path.read_bytes()).hexdigest()
            entries.append(f"{sha}  {r['file_name']}")
        if i % 1000 == 0 or i == total:
            print(f"  Processed {i}/{total} files ...", end="\r")

    print()
    with open(checksum_path, "w", encoding="utf-8") as f:
        f.write("\n".join(entries) + "\n")

    print(f"  ✓ Wrote {len(entries)} checksums → checksums.sha256")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="DHSD Dataset Statistics & Utilities"
    )
    parser.add_argument(
        "--split", action="store_true",
        help="Generate train.csv and test.csv (80/20 stratified split)"
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Verify that all image files referenced in data.csv exist"
    )
    parser.add_argument(
        "--checksums", action="store_true",
        help="Generate checksums.sha256 for all data files"
    )
    args = parser.parse_args()

    if not CSV_PATH.is_file():
        print(f"Error: {CSV_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    rows = load_annotations(CSV_PATH)
    stats = compute_statistics(rows)
    print_statistics(stats)

    if args.verify:
        verify_images(rows)

    if args.split:
        print_section("Train / Test Split (80/20)")
        train, test = stratified_split(rows)
        write_split_csv(train, BASE_DIR / "train.csv")
        write_split_csv(test, BASE_DIR / "test.csv")
        print(f"\n  Train : {len(train):>5d} ({100 * len(train) / len(rows):.1f}%)")
        print(f"  Test  : {len(test):>5d} ({100 * len(test) / len(rows):.1f}%)")

    if args.checksums:
        generate_checksums(rows)


if __name__ == "__main__":
    main()
