import os
import re
from typing import Annotated
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """
    A plugin to access the content of the AI Agents for Beginners course.
    It reads from the STUDY_GUIDE.md file.
    """

    def __init__(self):
        self.lessons = {}
        self._load_content()

    def _load_content(self):
        # Look for STUDY_GUIDE.md in the parent directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        guide_path = os.path.join(base_dir, "..", "STUDY_GUIDE.md")

        if not os.path.exists(guide_path):
            print(f"Warning: STUDY_GUIDE.md not found at {guide_path}")
            return

        try:
            with open(guide_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split by lesson headers (e.g., "## 1. Introduction")
            # We look for "## " followed by a number and a dot
            parts = re.split(r'(## \d+\. .*?)\n', content)

            current_lesson_num = 0

            # The first part is the intro before lessons
            if parts:
                self.lessons[0] = parts[0]

            for i in range(1, len(parts), 2):
                header = parts[i]
                body = parts[i+1] if i+1 < len(parts) else ""

                # Extract lesson number
                match = re.search(r'## (\d+)\.', header)
                if match:
                    lesson_num = int(match.group(1))
                    self.lessons[lesson_num] = header + "\n" + body

        except Exception as e:
            print(f"Error loading study guide: {e}")

    @kernel_function(description="Retrieves the content of a specific lesson number.")
    def get_lesson_content(
        self,
        lesson_number: Annotated[int, "The number of the lesson to retrieve (1-15)."]
    ) -> str:
        """
        Returns the full text of the requested lesson.
        """
        if lesson_number in self.lessons:
            return self.lessons[lesson_number]
        else:
            return f"Lesson {lesson_number} not found. Available lessons: {list(self.lessons.keys())}"

    @kernel_function(description="Searches the course content for a specific query.")
    def search_content(
        self,
        query: Annotated[str, "The topic or keyword to search for."]
    ) -> str:
        """
        Searches all lessons for the query string and returns relevant snippets.
        """
        results = []
        query_lower = query.lower()

        for lesson_num, content in self.lessons.items():
            if query_lower in content.lower():
                # Find the context window around the match
                start_idx = content.lower().find(query_lower)
                # Take 200 chars before and after
                snippet_start = max(0, start_idx - 200)
                snippet_end = min(len(content), start_idx + 200 + len(query))
                snippet = content[snippet_start:snippet_end].replace('\n', ' ')

                results.append(f"Lesson {lesson_num}: ...{snippet}...")

        if not results:
            return "No relevant content found in the course materials."

        return "\n\n".join(results[:5]) # Return top 5 matches
