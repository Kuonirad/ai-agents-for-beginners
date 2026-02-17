import os
import re
from typing import Dict

# Try importing the decorator, fallback to a dummy if not installed (for testing without deps)
try:
    from semantic_kernel.functions import kernel_function
except ImportError:
    def kernel_function(description=""):
        def decorator(func):
            func.__doc__ = description
            return func
        return decorator

class CoursePlugin:
    def __init__(self):
        self.lessons = self._load_study_guide()

    def _load_study_guide(self) -> Dict[str, str]:
        # Path to STUDY_GUIDE.md relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to finding STUDY_GUIDE.md
        study_guide_path = os.path.join(current_dir, "..", "STUDY_GUIDE.md")

        if not os.path.exists(study_guide_path):
             print(f"Warning: STUDY_GUIDE.md not found at {study_guide_path}")
             return {}

        with open(study_guide_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by headers like "## 1. "
        parts = re.split(r'(## \d+\. .*?)\n', content)

        lessons = {}
        current_lesson = None

        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Check if it's a header
            header_match = re.match(r'## (\d+)\. (.*)', part)
            if header_match:
                current_lesson = header_match.group(1)
                lessons[current_lesson] = part # Start content with header
            elif current_lesson:
                lessons[current_lesson] += "\n\n" + part

        return lessons

    @kernel_function(description="Retrieves the content of a specific lesson number from the course study guide.")
    def get_lesson_content(self, lesson_number: str) -> str:
        """
        Retrieves the content of a specific lesson number.
        """
        return self.lessons.get(str(lesson_number), f"Lesson {lesson_number} not found.")

    @kernel_function(description="Searches for a keyword in the study guide and returns relevant snippets.")
    def search_content(self, query: str) -> str:
        """
        Searches for a keyword in the study guide.
        """
        results = []
        for lesson_num, content in self.lessons.items():
            if query.lower() in content.lower():
                # Find the first occurrence to create a snippet
                idx = content.lower().find(query.lower())
                start = max(0, idx - 50)
                end = min(len(content), idx + 150)
                snippet = content[start:end].replace('\n', ' ')
                results.append(f"Lesson {lesson_num}: ...{snippet}...")

        if not results:
            return "No results found."

        return "\n".join(results[:5])
