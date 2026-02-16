import sys
import os
import unittest

# Ensure we can import from local directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

class TestCoursePlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = CoursePlugin()

    def test_get_lesson_content(self):
        # Lesson 1 should exist
        content = self.plugin.get_lesson_content(1)
        self.assertIn("Introduction to AI Agents", content)
        self.assertTrue(content.startswith("## 1."))

        # Lesson 99 should not exist
        content_invalid = self.plugin.get_lesson_content(99)
        self.assertIn("not found", content_invalid)

    def test_search_content(self):
        # Search for a known term
        term = "memory"
        results = self.plugin.search_content(term)
        self.assertIn("Lesson", results)
        # Check if snippet contains term (case insensitive)
        self.assertTrue(term.lower() in results.lower())

        # Search for nonsense
        results_none = self.plugin.search_content("xyzabc123")
        self.assertIn("No results found", results_none)

if __name__ == '__main__':
    unittest.main()
