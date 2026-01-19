# Root Makefile - The "Commander" (Poetry Edition)
PROJECTS = "Homework 1"

.PHONY: all lint test check clean help install

help:
	@echo "Available commands:"
	@echo "  make install - Install dependencies via Poetry"
	@echo "  make lint    - Run Pylint (via Poetry)"
	@echo "  make test    - Run unit tests"
	@echo "  make check   - Run full verification"
	@echo "  make clean   - Remove artifacts"

# 0. Setup
# "Guru" Check: Ensures poetry is installed before trying to run it
install:
	@echo ">>> 📦 Installing Dependencies..."
	poetry install

# 1. Repo-Wide Linting
# Uses 'poetry run' to execute pylint from the virtual env
lint:
	@echo "\n>>> 🔍 Running Global Lint Check..."
	poetry run pylint $(PROJECTS) --rcfile=.pylintrc

# 2. Repo-Wide Testing
# Iterates through directories and runs their specific test suites
test:
	@echo "\n>>> 🧪 Running Unit Tests..."
	for dir in $(PROJECTS); do \
		echo "Testing $$dir..."; \
		$(MAKE) -C "$$dir" check || exit 1; \
	done

# 3. Full Check
check: lint test
	@echo "\n>>> ✅ All Systems Go!"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f "Homework 1/before.txt" "Homework 1/after.txt"
