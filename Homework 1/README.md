# Homework 1: Word Frequency Refactor

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