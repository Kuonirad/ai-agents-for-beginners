import re
import os
from typing import Dict, List
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """
    A plugin to provide information about the 'AI Agents for Beginners' course
    by parsing the STUDY_GUIDE.md file.
    """

    def __init__(self, study_guide_path: str = "../STUDY_GUIDE.md"):
        self.lessons: Dict[int, str] = {}
        self.titles: Dict[int, str] = {}
        self._load_study_guide(study_guide_path)

    def _load_study_guide(self, path: str):
        try:
            # Resolve path relative to this file if it's not absolute
            if not os.path.isabs(path):
                base_dir = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(base_dir, path)

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split content by headers like "## 1. Introduction"
            # Regex captures the number and the title
            # The split will result in [preamble, number1, title1, content1, number2, title2, content2, ...]
            parts = re.split(r'^## (\d+)\. (.*?)$', content, flags=re.MULTILINE)

            # parts[0] is the preamble (Table of Contents, etc.) which we might ignore or store
            # Then we iterate in chunks of 3: number, title, content
            for i in range(1, len(parts), 3):
                if i + 2 < len(parts):
                    lesson_num = int(parts[i])
                    title = parts[i+1].strip()
                    lesson_content = parts[i+2].strip()

                    self.lessons[lesson_num] = f"## {lesson_num}. {title}\n\n{lesson_content}"
                    self.titles[lesson_num] = title
        except FileNotFoundError:
            print(f"Warning: Study guide not found at {path}. CoursePlugin will be empty.")
        except Exception as e:
            print(f"Error loading study guide: {e}")

    @kernel_function(description="Retrieves the full content of a specific lesson by its number.")
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Returns the content of the specified lesson.

        Args:
            lesson_number: The number of the lesson to retrieve (1-15).
        """
        return self.lessons.get(lesson_number, f"Lesson {lesson_number} not found.")

    @kernel_function(description="Searches for lessons containing specific keywords.")
    def search_content(self, query: str) -> str:
        """
        Searches the course content for the given query string.
        Returns a summary of matching lessons.

        Args:
            query: The keyword or phrase to search for.
        """
        results = []
        query = query.lower()

        for num, content in self.lessons.items():
            if query in content.lower():
                # specific match found
                title = self.titles.get(num, "Unknown Title")
                results.append(f"Lesson {num}: {title}")

        if not results:
            return "No lessons found matching your query."

        return "Found matches in the following lessons:\n" + "\n".join(results) + "\n\nUse `get_lesson_content(number)` to read the details."
