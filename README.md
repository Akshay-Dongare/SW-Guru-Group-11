# 🎓 CSC491/591: Software Engineering Guru - Homework Repository

**Students:** Akshay Ashutosh Dongare, Ryan Mikula

**Semester:** Spring 2026  

Welcome to my submission repository. Below you will find links to individual homework assignments, including source code, tests, and documentation.

## 📂 Assignments Directory

| Assignment | Topic | Status | Links |
| :--- | :--- | :---: | :--- |
| **Homework 1** | **Refactoring & Heuristics**<br>*(Separation of Concerns, Mechanism vs Policy)* | ✅ Complete | [📂 Open Folder](./Homework%201) |
| **Homework 2** | *TBD* | ⏳ Pending | - |
| **Homework 3** | *TBD* | ⏳ Pending | - |
| **Homework 4** | *TBD* | ⏳ Pending | - |

---

## 🚀 Highlights

<details>
<summary><strong>Homework 1: Word Frequency Refactor</strong> (Click to Expand)</summary>

<br>

> **[📂 Go to Homework 1 Folder](./Homework%201)**

Refactored a legacy "spaghetti code" script into a modular, clean architecture.

* **Key Heuristics Applied:**
    * Separation of Concerns (SoC)
    * Single Responsibility Principle (SRP)
    * Mechanism vs. Policy (Config separated from Logic)
* **Bonuses Implemented:**
    1.  Multiple Output Formats (JSON/CSV)
    2.  External Data Loading (`stopwords.txt`)
    3.  Unit Testing (`unittest`)
    4.  Internationalization (Spanish Support)
* **Verification:**
    * Includes a `Makefile` for automated grading checks.
    * Passes strict `diff` checks against the original script.

</details>

---

## 🛠️ How to Grade
1.  Navigate to the specific assignment folder (e.g., expand the section above or use the table).
2.  Follow the instructions in that folder's `README.md` or run `make` if available.

---

## 🔧 Development & Code Quality

We use **Poetry** to manage dependencies and **Pylint** to enforce strict code quality (Guru Standards).

### 1. Setup
Install all dependencies (including the linter and formatter):
```bash
make install
```

### 2. Auto-Formatting
To automatically fix whitespace, indentation, and style violations:
```bash
poetry run autopep8 --in-place --aggressive --recursive "Homework 1"
```

### 3. Verify Quality
To run the full repo-wide check (Target Score: > 8.0/10):
```bash
make lint
```