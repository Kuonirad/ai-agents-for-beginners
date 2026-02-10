import unittest
import os
import sys

# Ensure demo_agent is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

class TestCoursePlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = CoursePlugin()

    def test_search_content(self):
        # Search for a term that definitely exists in STUDY_GUIDE.md
        result = self.plugin.search_content("Agent")
        self.assertIn("Agent", result)
        self.assertNotEqual(result, "Error: STUDY_GUIDE.md not found.")

    def test_get_lesson_content(self):
        # Lesson 1 exists
        result = self.plugin.get_lesson_content(1)
        self.assertIn("Intro to AI Agents", result)
        self.assertNotIn("Error:", result)

    def test_get_lesson_content_invalid(self):
        # Lesson 99 doesn't exist
        result = self.plugin.get_lesson_content(99)
        self.assertIn("Error: Lesson 99 not found", result)

if __name__ == '__main__':
    unittest.main()
