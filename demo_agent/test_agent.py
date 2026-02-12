import unittest
import os
import sys

# Ensure we can import the plugin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

class TestCoursePlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = CoursePlugin()

    def test_load_content(self):
        """Test if content is loaded and lessons are parsed."""
        self.assertTrue(len(self.plugin.lessons) > 0, "No lessons loaded.")
        self.assertIn(1, self.plugin.lessons, "Lesson 1 not found.")
        self.assertIn(15, self.plugin.lessons, "Lesson 15 not found.")

    def test_get_lesson_content(self):
        """Test retrieving lesson content."""
        content = self.plugin.get_lesson_content(1)
        self.assertIsInstance(content, str)
        self.assertIn("## 1.", content)
        self.assertIn("Introduction to AI Agents", content)

        # Test invalid lesson
        content = self.plugin.get_lesson_content(999)
        self.assertEqual(content, "Lesson 999 not found.")

    def test_search_content(self):
        """Test searching for keywords."""
        # Search for a term likely to exist
        result = self.plugin.search_content("RAG")
        self.assertIn("Found in Lesson", result)
        self.assertIn("RAG", result)

        # Search for nonsense
        result = self.plugin.search_content("xyz123abc")
        self.assertEqual(result, "No matches found.")

if __name__ == "__main__":
    unittest.main()
