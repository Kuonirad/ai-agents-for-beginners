import sys
import os
import unittest

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

class TestCoursePlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = CoursePlugin()

    def test_load_lessons(self):
        # Check if lessons were loaded
        print(f"Loaded {len(self.plugin.lessons)} lessons.")
        self.assertTrue(len(self.plugin.lessons) > 0, "No lessons loaded")
        # Check for Lesson 1
        self.assertIn(1, self.plugin.lessons)
        self.assertIn("Introduction to AI Agents", self.plugin.lessons[1])

    def test_get_lesson_content(self):
        content = self.plugin.get_lesson_content(1)
        self.assertIsInstance(content, str)
        self.assertTrue("Introduction to AI Agents" in content)

        # Test non-existent lesson
        content = self.plugin.get_lesson_content(999)
        self.assertTrue("not found" in content)

    def test_search_content(self):
        # Search for something known
        result = self.plugin.search_content("Agentic Design Patterns")
        self.assertNotEqual(result, "No matches found.")
        self.assertTrue("Lesson 3" in result)

        # Search for nonsense
        result = self.plugin.search_content("Supercalifragilisticexpialidocious")
        self.assertEqual(result, "No matches found.")

if __name__ == '__main__':
    unittest.main()
