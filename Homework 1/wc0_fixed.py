#!/usr/bin/env python3 -B
"""
Word frequency counter - Refactored Guru Version
Course: CSC491/591 SW Guru
Heuristics Applied: SoC, SRP, Mechanism vs Policy, Small Functions, Streaming, Backpacking
"""

import sys

# =============================================================================
# INFRASTRUCTURE (The "VITAL" Layer)
# =============================================================================

def parse_line(line, policy, mode):
    """Mechanism: Updates policy dict based on a single YAML line."""
    clean = line.strip()
    if clean.startswith("punct:"):
        policy["punct"] = clean.split(":", 1)[1].strip(' "\'')
        return None
    if clean.startswith("stopwords:"): return "stopwords"
    if clean.startswith("- ") and mode == "stopwords":
        policy["stopwords"].add(clean[2:])
    return mode

def load_policy_backpacking(filepath):
    """Orchestrator: Reads file and delegates line parsing."""
    policy, mode = {"stopwords": set(), "punct": '.,!?;:"()[]'}, None
    try:
        with open(filepath) as f:
            for line in f: mode = parse_line(line, policy, mode)
    except FileNotFoundError:
        print(f"[WARN] {filepath} not found. Defaults used.", file=sys.stderr)
    return policy

# =============================================================================
# POLICY LAYER (The "Smart Edge")
# =============================================================================

# Q3: Mechanism vs Policy issues?
# AQ3: Policies (stopwords, punct) are now completely externalized to 'config.yaml'.
#      You can change the language or rules without touching a single line of Python.
CONFIG = {
    "file": "essay.txt",
    "policy_file": "config.yaml",
    "top_n": 10,
    "bar_char": "*",
    # Presentation policies
    "width_idx": 2,
    "width_word": 15,
    "width_count": 3
}

# Load external policies and merge into CONFIG
_loaded_policy = load_policy_backpacking(CONFIG["policy_file"])
CONFIG.update(_loaded_policy)

# =============================================================================
# MECHANISM LAYER (The "Dumb Center") - Model & Logic
# =============================================================================

def stream_lines(filepath):
    """
    Generator: Yields file content one line at a time.
    Fixes VIOLATION 1 (Loading entire file) by using Streaming (Rule 5).
    """
    with open(filepath) as f:
        for line in f:
            yield line

def stream_words(lines):
    """
    Generator: Tokenizes lines into raw words.
    Mechanism: Splitting text. Policy: None (just whitespace).
    """
    for line in lines:
        for word in line.lower().split():
            yield word

def clean_word(word):
    """Removes punctuation from edges of a word."""
    # Uses the punctuation string loaded from config.yaml
    return word.strip(CONFIG["punct"])

# Q2: Single Responsibility Principle (SRP) issues?
# AQ2: This function ONLY filters. It checks against the loaded policy.
def stream_filter(raw_words):
    """Generator: Pipeline filter that cleans and removes stopwords."""
    stopwords = CONFIG["stopwords"]
    for w in raw_words:
        cleaned = clean_word(w)
        if cleaned and cleaned not in stopwords:
            yield cleaned

def count_from_stream(word_stream):
    """
    Consumer: Accumulates counts from the generator pipeline.
    This is the only point where data is stored in memory.
    """
    counts = {}
    for w in word_stream:
        counts[w] = counts.get(w, 0) + 1
    return counts

def get_sorted_items(counts):
    """Sorts dictionary items by value (descending)."""
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)

# =============================================================================
# PRESENTATION LAYER (I/O Only)
# =============================================================================

# Q1: What Separation of Concerns (SoC) issues?
# AQ1: We completely separated printing from logic. The Model functions 
#      above utilize 'yield' and 'return'. The View functions below 'print'.

def print_header(filename):
    print(f"\n{'='*50}")
    print(f"WORD FREQUENCY ANALYSIS - {filename}")
    print(f"{'='*50}\n")

def print_stats(counts):
    total = sum(counts.values())
    unique = len(counts)
    print(f"Total words (after removing stopwords): {total}")
    print(f"Unique words: {unique}\n")

def format_row(i, word, count):
    """Formats a single output row using CONFIG policies."""
    bar = CONFIG["bar_char"] * count
    return (f"{i:{CONFIG['width_idx']}}. "
            f"{word:{CONFIG['width_word']}} "
            f"{count:{CONFIG['width_count']}} {bar}")

def print_top_n(sorted_items):
    n = CONFIG["top_n"]
    print(f"Top {n} most frequent words:\n")
    for i, (word, count) in enumerate(sorted_items[:n], 1):
        print(format_row(i, word, count))
    print()

def print_report(filename, counts, sorted_items):
    """Aggregates all print operations."""
    print_header(filename)
    print_stats(counts)
    print_top_n(sorted_items)

# =============================================================================
# CONTROLLER (Orchestration)
# =============================================================================

def run():
    """Orchestrates the data pipeline (SoC)."""
    # Pipeline: Chain generators lazily (File -> Words -> Filtered)
    stream = stream_filter(stream_words(stream_lines(CONFIG["file"])))
    
    # Execution: Consume stream, sort, and report
    counts = count_from_stream(stream)
    print_report(CONFIG["file"], counts, get_sorted_items(counts))
    
if __name__ == "__main__":
    run()