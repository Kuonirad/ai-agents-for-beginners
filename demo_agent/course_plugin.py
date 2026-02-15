import os
import re
from typing import Annotated, Dict, List
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """
    A plugin to access the content of the AI Agents for Beginners course.
    """

    def __init__(self):
        # Assuming the script is run from a location where STUDY_GUIDE.md is accessible relative to this file
        # If run from demo_agent/agent.py, __file__ is demo_agent/course_plugin.py
        # STUDY_GUIDE.md is in the parent directory of demo_agent
        self.guide_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "STUDY_GUIDE.md")
        self.lessons: Dict[int, str] = {}
        self._load_content()

    def _load_content(self) -> None:
        if not os.path.exists(self.guide_path):
            print(f"Warning: Study guide not found at {self.guide_path}")
            return

        with open(self.guide_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse lessons based on headers like "## 1. Introduction to AI Agents"
        # The regex looks for ## followed by a number and a dot
        pattern = re.compile(r"^## (\d+)\. (.*)$", re.MULTILINE)
        matches = list(pattern.finditer(content))

        for i, match in enumerate(matches):
            lesson_num = int(match.group(1))
            start_pos = match.start()

            # Determine end position (start of next match or end of file)
            if i + 1 < len(matches):
                end_pos = matches[i+1].start()
            else:
                end_pos = len(content)

            lesson_text = content[start_pos:end_pos].strip()
            self.lessons[lesson_num] = lesson_text

    @kernel_function(description="Gets the content of a specific lesson from the course.")
    def get_lesson_content(
        self,
        lesson_number: Annotated[int, "The number of the lesson to retrieve (e.g., 1, 2, ... 15)."]
    ) -> Annotated[str, "The content of the requested lesson."]:
        """
        Retrieves the content of a specific lesson.
        """
        if lesson_number in self.lessons:
            return self.lessons[lesson_number]
        return f"Lesson {lesson_number} not found. Available lessons: {list(self.lessons.keys())}"

    @kernel_function(description="Searches the course content for a given query.")
    def search_content(
        self,
        query: Annotated[str, "The search query to look for in the course material."]
    ) -> Annotated[str, "The relevant sections or a summary of findings."]:
        """
        Searches the study guide for the query and returns relevant excerpts.
        """
        results = []
        query_lower = query.lower()

        for lesson_num, text in self.lessons.items():
            if query_lower in text.lower():
                # Extract a snippet around the match
                # For simplicity, let's just take the first match in each lesson
                match_index = text.lower().find(query_lower)
                # Context window
                start = max(0, match_index - 50)
                end = min(len(text), match_index + 150)
                snippet = text[start:end].replace("\n", " ")
                results.append(f"Lesson {lesson_num}: ...{snippet}...")

        if results:
            return "\n".join(results[:3]) # Limit to top 3

        return "No relevant content found."
