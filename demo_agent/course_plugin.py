import os
import re
import logging
from typing import Annotated
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    def __init__(self):
        self.lessons = {}
        # Path to CONCEPTS_EXPLAINED.md in the repo root
        file_path = os.path.join(os.path.dirname(__file__), "..", "CONCEPTS_EXPLAINED.md")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self._parse_content(content)
        except FileNotFoundError:
            logging.warning(f"File {file_path} not found. CoursePlugin will not have course content.")

    def _parse_content(self, text: str):
        # Split text by headers like "## 1. Introduction to AI Agents"
        parts = re.split(r'(## \d+\. .*?)\n', text)

        # parts[0] is typically the text before the first lesson header
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                header = parts[i].strip()
                content = parts[i+1].strip()
                # Extract the lesson number from the header (e.g., "## 1. " -> "1")
                match = re.search(r'## (\d+)\.', header)
                if match:
                    lesson_num = match.group(1)
                    self.lessons[lesson_num] = {
                        "header": header,
                        "content": content
                    }

    @kernel_function(
        name="get_lesson_content",
        description="Gets the content for a specific lesson by lesson number."
    )
    def get_lesson_content(self, lesson_number: Annotated[str, "The lesson number (e.g., '1', '2')"]) -> str:
        lesson = self.lessons.get(str(lesson_number))
        if lesson:
            return f"{lesson['header']}\n\n{lesson['content']}"
        return f"Lesson {lesson_number} not found."

    @kernel_function(
        name="search_content",
        description="Searches all lesson content for a specific keyword or phrase and returns matching excerpts."
    )
    def search_content(self, query: Annotated[str, "The keyword or phrase to search for"]) -> str:
        results = []
        for lesson_num, lesson in self.lessons.items():
            if query.lower() in lesson["content"].lower() or query.lower() in lesson["header"].lower():
                results.append(f"Found in Lesson {lesson_num} ({lesson['header']}).")

        if not results:
            return f"No results found for '{query}'."

        return "\n".join(results)
