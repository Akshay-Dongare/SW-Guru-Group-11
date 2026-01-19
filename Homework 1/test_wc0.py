import unittest
import inspect
import os
import wc0_fixed

class TestSEPrinciples(unittest.TestCase):
    """Verifies Software Engineering Heuristics."""

    def test_function_sizes(self):
        """
        Enforce Rule 4: Small Functions (< 10 lines).
        Now checks every function, including the new infrastructure ones.
        """
        functions = inspect.getmembers(wc0_fixed, inspect.isfunction)
        for name, func in functions:
            # Ignore Python internal functions (like __annotate__)
            if name.startswith("__"):
                continue

            # Ensure we only check functions defined in this file (not imports)
            if func.__module__ != wc0_fixed.__name__:
                continue

            lines = inspect.getsourcelines(func)[0]
            line_count = len(lines)
            
            self.assertLessEqual(
                line_count, 10, 
                f"Violation: '{name}' is {line_count} lines long (limit is 10)."
            )

    def test_clean_word(self):
        """Test Mechanism: Punctuation stripping logic."""
        # Note: Relies on the config loaded in wc0_fixed
        self.assertEqual(wc0_fixed.clean_word("hello,"), "hello")
        self.assertEqual(wc0_fixed.clean_word("[test]"), "test")

    def test_count_frequencies(self):
        """Test Mechanism: Counting logic."""
        data = ["apple", "banana", "apple"]
        expected = {"apple": 2, "banana": 1}
        self.assertEqual(wc0_fixed.count_from_stream(data), expected)


class TestInfrastructure(unittest.TestCase):
    """Verifies the custom 'Backpacking' YAML parser."""

    def test_parse_line_punct(self):
        """Test parsing a single key-value line."""
        policy = {}
        # Simulate reading: punct: ".,!"
        mode = wc0_fixed.parse_line('punct: ".,!"', policy, None)
        
        self.assertEqual(policy["punct"], ".,!")
        self.assertIsNone(mode) # Should not enter list mode

    def test_parse_line_stopwords(self):
        """Test parsing the start of a list block."""
        policy = {}
        # Simulate reading: stopwords:
        mode = wc0_fixed.parse_line("stopwords:", policy, None)
        
        self.assertEqual(mode, "stopwords") # Should enter list mode

    def test_parse_line_item(self):
        """Test parsing a list item."""
        policy = {"stopwords": set()}
        # Simulate reading: - the
        mode = wc0_fixed.parse_line("- the", policy, "stopwords")
        
        self.assertIn("the", policy["stopwords"])
        self.assertEqual(mode, "stopwords") # Should stay in list mode

    def test_full_loader(self):
        """Integration test: Create a dummy file and load it."""
        filename = "test_config.yaml"
        content = """
        punct: "@#"
        stopwords:
        - foo
        - bar
        """
        # Create dummy file
        with open(filename, "w") as f:
            f.write(content)
            
        try:
            # Test the loader
            policy = wc0_fixed.load_policy_backpacking(filename)
            self.assertEqual(policy["punct"], "@#")
            self.assertIn("foo", policy["stopwords"])
            self.assertIn("bar", policy["stopwords"])
        finally:
            # Cleanup
            if os.path.exists(filename):
                os.remove(filename)
    
    def test_load_stopwords_file_valid(self):
        """Bonus 2 Test: Verify loading from a flat text file."""
        filename = "dummy_stopwords.txt"
        # Create a messy file with whitespace and empty lines
        content = "the\n  and  \n\nof\n"
        
        with open(filename, "w") as f:
            f.write(content)
            
        try:
            # Test: Should strip whitespace and ignore empty lines
            result = wc0_fixed.load_stopwords_file(filename)
            self.assertEqual(result, {"the", "and", "of"})
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_load_stopwords_file_missing(self):
        """Bonus 2 Test: Verify graceful failure (empty set) if file missing."""
        result = wc0_fixed.load_stopwords_file("non_existent_ghost.txt")
        self.assertEqual(result, set())

if __name__ == '__main__':
    unittest.main(verbosity=2)