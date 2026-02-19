import os
import re
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """
    A plugin for retrieving content from the AI Agents for Beginners study guide.
    """
    def __init__(self):
        self.lessons = {}
        self._load_study_guide()

    def _load_study_guide(self):
        # Assuming STUDY_GUIDE.md is one level up from demo_agent/
        guide_path = os.path.join(os.path.dirname(__file__), "..", "STUDY_GUIDE.md")

        try:
            with open(guide_path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Warning: {guide_path} not found.")
            return

        # Split by lesson headers (e.g., "## 1. Introduction to AI Agents")
        # We use a capturing group to keep the delimiter to identify the lesson number
        parts = re.split(r'(## \d+\. .*?)\n', content)

        # parts[0] is intro text before the first lesson (or empty)
        # parts[1] is the first header, parts[2] is the first body, etc.

        for i in range(1, len(parts), 2):
            header = parts[i]
            body = parts[i+1] if i+1 < len(parts) else ""

            # Extract lesson number from header "## 1. Title"
            match = re.search(r'## (\d+)\.', header)
            if match:
                lesson_num = int(match.group(1))
                self.lessons[lesson_num] = header + "\n" + body

    @kernel_function(description="Retrieves the full content of a specific lesson number.")
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Returns the content of the specified lesson.

        Args:
            lesson_number: The integer number of the lesson (e.g., 1 for Intro, 15 for Browser Use).
        """
        return self.lessons.get(lesson_number, f"Lesson {lesson_number} not found.")

    @kernel_function(description="Searches for lessons containing the given query string.")
    def search_content(self, query: str) -> str:
        """
        Returns a summary of lessons containing the query.
        """
        results = []
        for num, content in self.lessons.items():
            if query.lower() in content.lower():
                # Extract the title from the first line
                title_line = content.split('\n')[0]
                results.append(f"Found in {title_line}")

        if not results:
            return "No matching content found."
        return "\n".join(results)
