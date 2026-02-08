import os
import re
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """
    A plugin to search the course study guide.
    """
    def __init__(self):
        self.sections = {}
        self._load_content()

    def _load_content(self):
        """Loads the STUDY_GUIDE.md file and parses it into sections."""
        # Find the STUDY_GUIDE.md file relative to this script
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "STUDY_GUIDE.md")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Could not find STUDY_GUIDE.md at {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by headers
        # The study guide has headers like "## 1. Introduction to AI Agents"
        # We can use regex to find these sections.

        # Split by "## " followed by a number
        # re.split includes the capture groups in the result
        sections = re.split(r'\n## (\d+)\. ', content)

        # The first element is the intro before the first lesson
        self.sections["0"] = sections[0].strip()

        # The rest are alternating: number, title + content
        # e.g. ["1", "Introduction to AI Agents\n\n**Goal:**...", "2", "Agentic Frameworks..."]

        for i in range(1, len(sections), 2):
            lesson_num = sections[i]
            # The content includes the title line first
            text = sections[i+1]

            # Format nicely
            self.sections[lesson_num] = f"## {lesson_num}. {text.strip()}"

    @kernel_function(description="Search the study guide for relevant content based on a query.")
    def search_content(self, query: str) -> str:
        """
        Searches the study guide for the most relevant section based on the query.
        Returns the content of the relevant section.
        """
        query = query.lower()
        best_match = None
        max_score = 0

        # Simple keyword matching
        for lesson_num, content in self.sections.items():
            if lesson_num == "0": continue # Skip intro

            score = 0
            # Split query into words
            words = query.split()
            for word in words:
                if word in content.lower():
                    score += 1

            if score > max_score:
                max_score = score
                best_match = content

        if best_match:
            return best_match
        return "No relevant content found in the study guide."

    @kernel_function(description="Get the content of a specific lesson number.")
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Returns the content of the specified lesson number.
        """
        key = str(lesson_number)
        if key in self.sections:
            return self.sections[key]
        return f"Lesson {lesson_number} not found."
