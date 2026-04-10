import os
import re
import logging
from typing import Annotated

from semantic_kernel.functions.kernel_function_decorator import kernel_function

logger = logging.getLogger(__name__)

class CoursePlugin:
    def __init__(self):
        self.lessons = {}
        self._load_study_guide()

    def _load_study_guide(self):
        try:
            # Navigate up one level from course_plugin.py to repository root
            file_path = os.path.join(os.path.dirname(__file__), "..", "STUDY_GUIDE.md")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            parts = re.split(r'(## \d+\. .*?)\n', content)

            # The first part is the intro (before the first matching header).
            # Then it alternates: header, content, header, content...
            for i in range(1, len(parts), 2):
                header = parts[i].strip()
                lesson_num_match = re.search(r'## (\d+)\.', header)
                if lesson_num_match:
                    lesson_num = lesson_num_match.group(1)
                    # The next part is the content for this header
                    lesson_content = parts[i+1].strip() if i + 1 < len(parts) else ""
                    self.lessons[lesson_num] = f"{header}\n{lesson_content}"

        except FileNotFoundError:
            logger.warning(f"Could not find STUDY_GUIDE.md at {file_path}")
            self.lessons = {}
        except Exception as e:
            logger.error(f"Error loading study guide: {e}")
            self.lessons = {}

    @kernel_function(
        description="Gets the complete study guide content for a specific lesson number."
    )
    def get_lesson_content(
        self,
        lesson_number: Annotated[str, "The lesson number as a string (e.g. '1', '2')"]
    ) -> str:
        """Return the complete content for a specific lesson."""
        if not self.lessons:
            return "Study guide content is not currently available."

        lesson = self.lessons.get(lesson_number)
        if lesson:
            return lesson

        available = ", ".join(sorted(self.lessons.keys(), key=lambda x: int(x)))
        return f"Lesson {lesson_number} not found. Available lessons are: {available}."

    @kernel_function(
        description="Searches all lesson contents for a specific topic or keyword."
    )
    def search_content(
        self,
        keyword: Annotated[str, "The keyword or topic to search for across all lessons"]
    ) -> str:
        """Search all lesson contents for a specific topic or keyword."""
        if not self.lessons:
            return "Study guide content is not currently available."

        keyword_lower = keyword.lower()
        results = []

        for num, content in self.lessons.items():
            if keyword_lower in content.lower():
                results.append(f"Lesson {num}: Found matches for '{keyword}'")

        if results:
            return "Found information in the following sections:\n" + "\n".join(results) + "\n\nUse get_lesson_content to read specific lessons."
        else:
            return f"No information found matching '{keyword}'."
