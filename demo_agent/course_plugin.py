import os
import re
import logging
from typing import Annotated

from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """
    A plugin for retrieving course content from CONCEPTS_EXPLAINED.md.
    """
    def __init__(self):
        self.lessons = {}
        # Resolve the path to CONCEPTS_EXPLAINED.md in the repo root
        file_path = os.path.join(os.path.dirname(__file__), "..", "CONCEPTS_EXPLAINED.md")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse the content based on lesson headers like "## 1. Introduction to AI Agents"
            # It results in a list: [intro_text, header_1, content_1, header_2, content_2, ...]
            parts = re.split(r'(## \d+\. .*?)\n', content)

            # parts[0] is the text before the first matching header
            for i in range(1, len(parts), 2):
                header = parts[i].strip()
                lesson_content = parts[i+1].strip() if i+1 < len(parts) else ""

                # Extract the lesson number from the header (e.g., "## 1." -> 1)
                match = re.match(r'## (\d+)\.', header)
                if match:
                    lesson_num = int(match.group(1))
                    self.lessons[lesson_num] = {
                        "header": header,
                        "content": lesson_content
                    }

        except FileNotFoundError:
            logging.warning(f"File not found: {file_path}. Agent will return empty content.")
            self.lessons = {}

    @kernel_function(
        description="Gets the content of a specific lesson by its number.",
        name="get_lesson_content"
    )
    def get_lesson_content(self, lesson_number: Annotated[int, "The number of the lesson to retrieve (e.g., 1 for Lesson 1)"]) -> Annotated[str, "The content of the lesson"]:
        if not self.lessons:
            return "Error: Course content is not available."

        lesson = self.lessons.get(lesson_number)
        if lesson:
            return f"{lesson['header']}\n\n{lesson['content']}"
        else:
            return f"Lesson {lesson_number} not found. Available lessons: {list(self.lessons.keys())}"

    @kernel_function(
        description="Searches all lessons for a specific keyword or phrase.",
        name="search_content"
    )
    def search_content(self, query: Annotated[str, "The keyword or phrase to search for in the course content"]) -> Annotated[str, "A summary of matching lessons and excerpts"]:
        if not self.lessons:
            return "Error: Course content is not available."

        results = []
        query_lower = query.lower()

        for lesson_num, lesson_data in self.lessons.items():
            if query_lower in lesson_data["header"].lower() or query_lower in lesson_data["content"].lower():
                # Extract a small snippet around the first match
                content = lesson_data["content"]
                match_idx = content.lower().find(query_lower)

                start_idx = max(0, match_idx - 50)
                end_idx = min(len(content), match_idx + len(query) + 50)
                snippet = content[start_idx:end_idx]

                if start_idx > 0:
                    snippet = "..." + snippet
                if end_idx < len(content):
                    snippet = snippet + "..."

                results.append(f"Found in Lesson {lesson_num} ({lesson_data['header']}):\n\"{snippet}\"")

        if results:
            return "\n\n".join(results)
        else:
            return f"No matches found for '{query}'."