import os
import re
from typing import Annotated
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    def __init__(self):
        self.lessons = {}
        # Resolve path relative to this file
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "STUDY_GUIDE.md"))
        self._load_content()

    def _load_content(self):
        try:
            if not os.path.exists(self.file_path):
                print(f"Warning: {self.file_path} not found.")
                return

            with open(self.file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Split by headers like "## 1. Introduction"
            # Captures the header as well
            parts = re.split(r'(## \d+\. .*?)\n', text)

            # The first part is introductory text (before the first lesson)
            # Subsequent parts are (header, content) pairs
            for i in range(1, len(parts), 2):
                header = parts[i].strip() # e.g. "## 1. Introduction to AI Agents"
                content = parts[i+1].strip()

                # Extract lesson number
                # Header format: ## <number>. <Title>
                match = re.search(r'## (\d+)\.', header)
                if match:
                    lesson_num = int(match.group(1))
                    self.lessons[lesson_num] = {
                        "title": header.replace("## ", ""),
                        "content": content
                    }
        except Exception as e:
            print(f"Error loading study guide: {e}")

    @kernel_function(
        description="Retrieves the content of a specific lesson from the course study guide.",
        name="get_lesson_content",
    )
    def get_lesson_content(
        self,
        lesson_number: Annotated[int, "The lesson number to retrieve (e.g., 1, 2, 15)."]
    ) -> Annotated[str, "The content of the lesson, including title and details."]:
        """
        Retrieves the content of a specific lesson.
        """
        if lesson_number in self.lessons:
            lesson = self.lessons[lesson_number]
            return f"{lesson['title']}\n\n{lesson['content']}"
        else:
            return f"Lesson {lesson_number} not found. Available lessons: {list(self.lessons.keys())}"

    @kernel_function(
        description="Searches for a specific term or concept in the study guide.",
        name="search_content",
    )
    def search_content(
        self,
        query: Annotated[str, "The term or concept to search for."]
    ) -> Annotated[str, "A list of lessons containing the search term."]:
        """
        Searches the study guide for a query string.
        """
        results = []
        for num, data in self.lessons.items():
            if query.lower() in data['content'].lower() or query.lower() in data['title'].lower():
                results.append(f"Lesson {num}: {data['title']}")

        if results:
            return "Found in:\n" + "\n".join(results)
        return "No matches found."
