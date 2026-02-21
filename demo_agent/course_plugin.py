import os
import re
from typing import Annotated
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """
    A plugin to search and retrieve content from the 'AI Agents for Beginners' study guide.
    """

    def __init__(self):
        # Resolve the path to the study guide (parent directory)
        self.study_guide_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "STUDY_GUIDE.md")
        self.lessons = {}
        self._load_content()

    def _load_content(self):
        """Parses the STUDY_GUIDE.md into a dictionary of lessons."""
        if not os.path.exists(self.study_guide_path):
            print(f"Warning: Study guide not found at {self.study_guide_path}")
            return

        with open(self.study_guide_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by lesson headers (e.g., "## 1. Introduction")
        # Regex matches "## " followed by a number, a dot, and the title
        sections = re.split(r'(## \d+\. .*?)\n', content)

        # sections[0] is intro before first lesson
        # sections[1] is header, sections[2] is content, etc.

        for i in range(1, len(sections), 2):
            header = sections[i].strip()
            body = sections[i+1].strip()

            # Extract lesson number
            match = re.search(r'## (\d+)\.', header)
            if match:
                lesson_num = match.group(1)
                self.lessons[lesson_num] = {
                    "title": header.replace("## ", ""),
                    "content": body
                }

    @kernel_function(description="Search the study guide for a specific topic or keyword.")
    def search_content(
        self,
        query: Annotated[str, "The topic or keyword to search for"]
    ) -> str:
        """
        Searches the study guide for the given query and returns relevant sections.
        """
        query = query.lower()
        results = []

        for num, lesson in self.lessons.items():
            if query in lesson["title"].lower() or query in lesson["content"].lower():
                # Return the full lesson summary as they are concise in the study guide
                results.append(f"--- Lesson {num}: {lesson['title']} ---\n{lesson['content']}")

        if not results:
            return "No specific lessons found matching that query. Try broader terms."

        # Limit to top 3 results to save context
        return "\n\n".join(results[:3])

    @kernel_function(description="Get the full content of a specific lesson by number.")
    def get_lesson_content(
        self,
        lesson_number: Annotated[str, "The lesson number (e.g., '1', '15')"]
    ) -> str:
        """
        Retrieves the full content of a specific lesson.
        """
        # Strip any "Lesson " prefix if the user/LLM includes it
        lesson_number = str(lesson_number).lower().replace("lesson", "").strip()

        if lesson_number in self.lessons:
            lesson = self.lessons[lesson_number]
            return f"--- {lesson['title']} ---\n\n{lesson['content']}"
        else:
            return f"Lesson {lesson_number} not found. Available lessons: {', '.join(sorted(self.lessons.keys(), key=int))}"
