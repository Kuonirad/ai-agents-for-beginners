import unittest
import os
import sys

# Ensure we can import the plugin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from course_plugin import CoursePlugin

class TestCoursePlugin(unittest.TestCase):
    def setUp(self):
        # We assume STUDY_GUIDE.md exists in the parent directory
        # The plugin will load it automatically
        self.plugin = CoursePlugin()

    def test_load_content(self):
        # Check if any content was loaded
        self.assertTrue(len(self.plugin.sections) > 0, "No sections loaded from STUDY_GUIDE.md")
        # Check specific known sections like "1" (Intro)
        self.assertIn("1", self.plugin.sections)
        self.assertIn("Introduction to AI Agents", self.plugin.sections["1"])

    def test_search_content_found(self):
        # Search for a known term
        query = "RAG"
        result = self.plugin.search_content(query)
        self.assertNotEqual(result, "No relevant content found in the study guide.")
        self.assertIn("RAG", result)

    def test_search_content_not_found(self):
        # Search for a nonsense term
        query = "xyzabc123"
        result = self.plugin.search_content(query)
        self.assertEqual(result, "No relevant content found in the study guide.")

    def test_get_lesson_content(self):
        result = self.plugin.get_lesson_content(1)
        self.assertIn("Introduction to AI Agents", result)

        result_missing = self.plugin.get_lesson_content(999)
        self.assertEqual(result_missing, "Lesson 999 not found.")

if __name__ == '__main__':
    unittest.main()
