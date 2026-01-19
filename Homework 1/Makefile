# Define phony targets so Make knows these aren't files
.PHONY: check clean bonus-demo

# The default target (what happens when you just type 'make')
check:
	@echo ">>> 1. Running Original Script (Baseline)..."
	python3 wc0.py > before.txt
	
	@echo ">>> 2. Running Refactored Script..."
	python3 wc0_fixed.py > after.txt
	
	@echo ">>> 3. Verifying Identical Output (diff)..."
	# If this fails, the make command will stop here
	diff before.txt after.txt
	@echo "    [OK] Output matches perfectly."
	
	@echo ">>> 4. Running Unit Tests..."
	python3 test_wc0.py
	@echo "\n>>> SUCCESS: All tests passed and output is clean! <<<"

# A handy utility to clean up the temporary files
clean:
	rm -f before.txt after.txt *.pyc
	rm -rf __pycache__

# Bonus: A way to easily see your new features in action
bonus-demo:
	@echo ">>> DEMO: Turning on Bonus Features (CSV Output + Spanish)..."
	# We temporarily set the flag to True using a sed hack or just Python one-liner
	# This demonstrates the features without editing the file
	python3 -c "import wc0_fixed; wc0_fixed.CONFIG.update({'load_external_stopwords': True, 'language': 'es', 'format': 'csv'}); wc0_fixed.run()"