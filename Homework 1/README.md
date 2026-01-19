# Homework 1: Word Frequency Refactor

[![HW1 - Word Frequency Refactor](https://github.com/Akshay-Dongare/SW-Guru-Group-11/actions/workflows/hw1-grading.yml/badge.svg?branch=main)](https://github.com/Akshay-Dongare/SW-Guru-Group-11/actions/workflows/hw1-grading.yml)

**Student:** Akshay Ashutosh Dongare, Ryan Mikula

**Course:** CSC491/591 - Software Guru

## 📝 Overview
This project refactors a monolithic, legacy Python script (`wc0.py`) into a clean, modular architecture adhering to strict Software Engineering heuristics.

**Key Heuristics Applied:**
* **Separation of Concerns (SoC):** Distinct layers for Infrastructure, Policy, Mechanism, and Presentation.
* **Single Responsibility Principle (SRP):** Each function does exactly one thing.
* **Mechanism vs. Policy:** Logic (sorting, counting) is separated from Configuration (stopwords, punctuation).
* **Small Functions:** All functions are under 10 lines of code (Rule 4).

---

## ⚡ Automated Grading (The Makefile)

I have included a `Makefile` to automate the verification process and ensure zero regressions.

### 1. Run the Full Check (Recommended)
To run the original script, the new script, verify identical output (diff), and run all unit tests:

```bash
make
```
What this does:

Runs wc0.py (Original) → saves to before.txt.

Runs wc0_fixed.py (Refactored) → saves to after.txt.

Runs diff before.txt after.txt → Ensures 100% backward compatibility.

Runs python3 test_wc0.py → Verifies all 9 unit tests pass.

### 2. Clean Up
To remove temporary artifacts (*.txt, \_\_pycache\_\_):
```bash
make clean
```

### 3. 🏆 Bonus Challenges & Feature Flags
IMPORTANT GRADING NOTE: To ensure the automated diff check passes, all bonus features are disabled by default using Feature Flags.

How to Verify Bonuses
You can verify the bonuses are implemented using the automated demo target:
```bash
make bonus-demo
```
This runs the script with flags enabled to demonstrate:

Multiple Formats: CSV Output (Strategy Pattern).

External Data: Merging stopwords.txt (Data vs Config).

Internationalization: Spanish support via stopwords_es.txt.

### 4. Manual Verification
Alternatively, you can manually toggle the flags in wc0_fixed.py

---

## 🤖 Continuous Integration (GitHub Actions)
This project uses a Conditional Monorepo Workflow to ensure code quality.

Workflow File: .github/workflows/hw1-grading.yml

Trigger: Runs only when files in the Homework 1/ directory are modified.

Jobs:

Linting: Runs pylint with a strict failure threshold of 8.0/10.

Grading: Runs make (Regression Testing + Unit Tests).

Smoke Test: Runs make bonus-demo to ensure feature flags function correctly.
