#!/usr/bin/env python3 -B
"""
Word frequency counter - Refactored Guru Version
Course: CSC491/591 SW Guru
Heuristics Applied: SoC, SRP, Mechanism vs Policy, Small Functions, Streaming, Backpacking
"""

import sys
import json
from typing import Iterator, Dict, List, Tuple, Optional, Any, Set

# =============================================================================
# INFRASTRUCTURE (The "VITAL" Layer)
# =============================================================================


def parse_line(line: str, policy: Dict[str, Any],
               mode: Optional[str]) -> Optional[str]:
    """Mechanism: Updates policy dict based on a single YAML line."""
    clean = line.strip()
    if clean.startswith("punct:"):
        policy["punct"] = clean.split(":", 1)[1].strip(' "\'')
        return None
    if clean.startswith("stopwords:"):
        return "stopwords"
    if clean.startswith("- ") and mode == "stopwords":
        policy["stopwords"].add(clean[2:])
    return mode


def load_policy_backpacking(filepath: str) -> Dict[str, Any]:
    """Orchestrator: Reads file and delegates line parsing."""
    policy: Dict[str, Any] = {"stopwords": set(), "punct": '.,!?;:"()[]'}
    mode: Optional[str] = None
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                mode = parse_line(line, policy, mode)
    except FileNotFoundError:
        print(f"[WARN] {filepath} not found. Defaults used.", file=sys.stderr)
    return policy


def load_stopwords_file(filepath: str) -> Set[str]:
    """Infrastructure: Loads unique stopwords from a flat text file."""
    try:
        with open(filepath, encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()

# =============================================================================
# POLICY LAYER (The "Smart Edge")
# =============================================================================


CONFIG: Dict[str, Any] = {
    "file": "essay.txt",
    "policy_file": "config.yaml",

    # Feature Flag: Default to False to ensure identical output for grading.
    # GRADING NOTE: Set this to True to verify Bonus 2 & 4 (External
    # Stopwords).
    "load_external_stopwords": False,

    # Internationalization (I18n) - Bonus 4
    "language": "en",
    "stopwords_file_en": "stopwords.txt",
    "stopwords_file_es": "stopwords_es.txt",

    "top_n": 10,
    "format": "text",
    "bar_char": "*",
    "width_idx": 2,
    "width_word": 15,
    "width_count": 3
}

# 1. Load base policy from YAML
_loaded_policy = load_policy_backpacking(CONFIG["policy_file"])
CONFIG.update(_loaded_policy)

# 2. (Optional) Merge external stopwords if Feature Flag is ON
if CONFIG.get("load_external_stopwords"):
    lang = CONFIG["language"]
    # Determine which file to load based on language (Bonus 4)
    key = f"stopwords_file_{lang}"

    if key in CONFIG:
        fpath = CONFIG[key]
        print(
            f"[INFO] Merging {lang} stopwords from {fpath}...",
            file=sys.stderr)
        CONFIG["stopwords"].update(load_stopwords_file(fpath))
    else:
        print(
            f"[WARN] No stopword file found for language '{lang}'",
            file=sys.stderr)

# =============================================================================
# MECHANISM LAYER (The "Dumb Center") - Model & Logic
# =============================================================================

# Q4: Any small Function problems? How to fix?
# AQ4: Yes, the original had one massive function. We fixed this by breaking
#      it into small, atomic generators (like stream_lines) that are under
#      10 lines of code and do exactly one thing.


def stream_lines(filepath: str) -> Iterator[str]:
    """
    Generator: Yields file content one line at a time.
    Fixes VIOLATION 1 (Loading entire file) by using Streaming (Rule 5).
    """
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            yield line


def stream_words(lines: Iterator[str]) -> Iterator[str]:
    """
    Generator: Tokenizes lines into raw words.
    Mechanism: Splitting text. Policy: None (just whitespace).
    """
    for line in lines:
        for word in line.lower().split():
            yield word

# Q3: Mechanism vs Policy issues? Can you find them?
# AQ3: The original hardcoded punctuation. Here, 'clean_word' is the pure mechanism
#      (it strips characters), but the POLICY (which characters to strip) is injected
#      via CONFIG["punct"], allowing behavior changes without editing code.


def clean_word(word: str) -> str:
    """Removes punctuation from edges of a word."""
    # Uses the punctuation string loaded from config.yaml
    return word.strip(CONFIG["punct"])

# Q2: Single Responsibility Principle (SRP) issues?
# AQ2: This function ONLY filters. It checks against the loaded policy.


def stream_filter(raw_words: Iterator[str]) -> Iterator[str]:
    """Generator: Pipeline filter that cleans and removes stopwords."""
    stopwords: Set[str] = CONFIG["stopwords"]
    for w in raw_words:
        cleaned = clean_word(w)
        if cleaned and cleaned not in stopwords:
            yield cleaned


def count_from_stream(word_stream: Iterator[str]) -> Dict[str, int]:
    """
    Consumer: Accumulates counts from the generator pipeline.
    This is the only point where data is stored in memory.
    """
    counts: Dict[str, int] = {}
    for w in word_stream:
        counts[w] = counts.get(w, 0) + 1
    return counts


def get_sorted_items(counts: Dict[str, int]) -> List[Tuple[str, int]]:
    """Sorts dictionary items by value (descending)."""
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)

# =============================================================================
# PRESENTATION LAYER (I/O Only)
# =============================================================================

# Q1: What Separation of Concerns (SoC) issues?
# AQ1: We completely separated printing from logic. The Model functions
#      above utilize 'yield' and 'return'. The View functions below 'print'.


def print_header(filename: str) -> None:
    print(f"\n{'=' * 50}")
    print(f"WORD FREQUENCY ANALYSIS - {filename}")
    print(f"{'=' * 50}\n")


def print_stats(counts: Dict[str, int]) -> None:
    total = sum(counts.values())
    unique = len(counts)
    print(f"Total words (after removing stopwords): {total}")
    print(f"Unique words: {unique}\n")


def to_json(counts: Dict[str, int]) -> None:
    """Bonus: Dumps results as JSON."""
    print(json.dumps(counts, indent=2))


def to_csv(sorted_items: List[Tuple[str, int]]) -> None:
    """Bonus: Dumps results as CSV."""
    print("rank,word,count")
    for i, (word, count) in enumerate(sorted_items, 1):
        print(f"{i},{word},{count}")


def format_row(i: int, word: str, count: int) -> str:
    """Formats a single output row using CONFIG policies."""
    bar = CONFIG["bar_char"] * count
    return (f"{i:{CONFIG['width_idx']}}. "
            f"{word:{CONFIG['width_word']}} "
            f"{count:{CONFIG['width_count']}} {bar}")


def print_top_n(sorted_items: List[Tuple[str, int]]) -> None:
    n = CONFIG["top_n"]
    print(f"Top {n} most frequent words:\n")
    for i, (word, count) in enumerate(sorted_items[:n], 1):
        print(format_row(i, word, count))
    print()


def print_report(
        filename: str, counts: Dict[str, int], sorted_items: List[Tuple[str, int]]) -> None:
    """Aggregates all print operations."""
    print_header(filename)
    print_stats(counts)
    print_top_n(sorted_items)


def print_formatted(
        filename: str, counts: Dict[str, int], sorted_items: List[Tuple[str, int]]) -> None:
    """Selects the correct output format based on CONFIG."""
    fmt = CONFIG["format"]
    if fmt == "json":
        to_json(counts)
    elif fmt == "csv":
        to_csv(sorted_items)
    else:
        print_report(filename, counts, sorted_items)

# =============================================================================
# CONTROLLER (Orchestration)
# =============================================================================


def run() -> None:
    """Orchestrates the data pipeline (SoC)."""
    # Pipeline: Chain generators lazily (File -> Words -> Filtered)
    stream = stream_filter(stream_words(stream_lines(CONFIG["file"])))

    # Execution & Presentation
    counts = count_from_stream(stream)
    print_formatted(CONFIG["file"], counts, get_sorted_items(counts))


if __name__ == "__main__":
    run()
