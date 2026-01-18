#!/usr/bin/env python3 -B
"""Word frequency counter - the messy version"""

def count_words(file="essay.txt"):
  """One big function doing everything"""
  # VIOLATION 1: Load entire file
  with open(file) as f:
    text = f.read()
  
  # VIOLATION 2: Print mixed with processing
  print(f"\n{'='*50}")
  print(f"WORD FREQUENCY ANALYSIS - {file}")
  print(f"{'='*50}\n")
  
  # VIOLATION 3: Clean and count inline (hardcoded logic)
  words = text.lower().split()
  counts = {}
  stopwords = ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
               "of", "is", "was", "are", "were", "be", "been", "with"]  # Hardcoded!
  
  for word in words:
    # Hardcoded punctuation removal
    word = word.strip('.,!?;:"()[]')
    if word and word not in stopwords:  # Hardcoded stopwords
      counts[word] = counts.get(word, 0) + 1
  
  # VIOLATION 4: Sort and filter inline
  sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
  top_n = 10  # Hardcoded!
  
  # VIOLATION 5: Print results mixed with computation
  print(f"Total words (after removing stopwords): {sum(counts.values())}")
  print(f"Unique words: {len(counts)}\n")
  print(f"Top {top_n} most frequent words:\n")
  
  # VIOLATION 6: Hardcoded formatting
  for i, (word, count) in enumerate(sorted_words[:top_n], 1):
    bar = "*" * count
    print(f"{i:2}. {word:15} {count:3} {bar}")
  
  print()

count_words("essay.txt")
