import os
import re
import logging
from typing import Annotated, Dict, Optional
from semantic_kernel.functions.kernel_function_decorator import kernel_function

logger = logging.getLogger(__name__)

class CoursePlugin:
    def __init__(self):
        self.lessons: Dict[str, str] = {}
        self._load_study_guide()

    def _load_study_guide(self):
        try:
            # STUDY_GUIDE.md is in the repository root, one level up from demo_agent
            file_path = os.path.join(os.path.dirname(__file__), '..', 'STUDY_GUIDE.md')
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse lessons using regex to split on headers
            parts = re.split(r'(## \d+\. .*?)\n', content)

            # parts[0] is everything before the first '## \d+.' header
            for i in range(1, len(parts), 2):
                header = parts[i].strip()
                body = parts[i+1].strip() if i+1 < len(parts) else ""

                # Extract lesson number from header, e.g., "## 1. Introduction" -> "1"
                match = re.match(r'## (\d+)\.', header)
                if match:
                    lesson_num = match.group(1)
                    self.lessons[lesson_num] = f"{header}\n\n{body}"

        except FileNotFoundError:
            logger.warning("STUDY_GUIDE.md not found. Agent may not function properly.")
            self.lessons = {}

    @kernel_function(
        description="Gets the complete study guide content for a specific lesson number.",
        name="get_lesson_content"
    )
    def get_lesson_content(
        self,
        lesson_number: Annotated[str, "The lesson number as a string, e.g., '1' for Intro to AI Agents."]
    ) -> str:
        """Returns the content of a specific lesson."""
        if not self.lessons:
            return "Error: Study guide content not available."

        content = self.lessons.get(str(lesson_number))
        if content:
            return content
        else:
            return f"Lesson {lesson_number} not found. Available lessons: {', '.join(self.lessons.keys())}"

    @kernel_function(
        description="Searches the study guide across all lessons for a specific keyword or topic.",
        name="search_content"
    )
    def search_content(
        self,
        query: Annotated[str, "The keyword or topic to search for in the study guide."]
    ) -> str:
        """Searches all loaded lessons for a given query."""
        if not self.lessons:
            return "Error: Study guide content not available."

        results = []
        query_lower = query.lower()

        for lesson_num, content in self.lessons.items():
            if query_lower in content.lower():
                results.append(f"--- Lesson {lesson_num} Match ---\n{content[:500]}...\n")

        if results:
            return "\n".join(results)
        else:
            return f"No results found for '{query}'."
