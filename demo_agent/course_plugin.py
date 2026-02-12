import os
import re
from typing import Dict, List, Optional
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initializes the CoursePlugin by loading the study guide content.

        Args:
            base_dir (str, optional): The base directory to look for STUDY_GUIDE.md.
                                      Defaults to two levels up from this file's location.
        """
        if base_dir:
            self.base_dir = base_dir
        else:
            # Default: this file is in demo_agent/, so root is ../
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.guide_path = os.path.join(self.base_dir, "STUDY_GUIDE.md")
        self.lessons: Dict[int, str] = {}
        self._load_content()

    def _load_content(self):
        """Loads and parses the STUDY_GUIDE.md file."""
        if not os.path.exists(self.guide_path):
            print(f"Warning: STUDY_GUIDE.md not found at {self.guide_path}")
            return

        with open(self.guide_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by level 2 headers (## X. Title)
        # Regex to find "## Num. Title"
        # We use a lookahead or just split and process

        lines = content.split('\n')
        current_lesson_num = 0
        current_content = []

        # Regex for "## 1. Title"
        header_pattern = re.compile(r"^##\s+(\d+)\.\s+(.+)$")

        for line in lines:
            match = header_pattern.match(line)
            if match:
                # Save previous lesson if exists
                if current_lesson_num > 0:
                    self.lessons[current_lesson_num] = "\n".join(current_content).strip()

                current_lesson_num = int(match.group(1))
                current_content = [line] # Include the header in the content
            else:
                if current_lesson_num > 0:
                    current_content.append(line)

        # Save the last lesson
        if current_lesson_num > 0:
            self.lessons[current_lesson_num] = "\n".join(current_content).strip()

    @kernel_function(description="Gets the content of a specific lesson number.")
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Retrieves the content for a given lesson number.

        Args:
            lesson_number (int): The lesson number (1-15).

        Returns:
            str: The content of the lesson or a "not found" message.
        """
        # Ensure int
        try:
            lesson_number = int(lesson_number)
        except ValueError:
            return "Invalid lesson number."

        return self.lessons.get(lesson_number, f"Lesson {lesson_number} not found.")

    @kernel_function(description="Searches for a keyword in the study guide.")
    def search_content(self, query: str) -> str:
        """
        Searches the study guide for the query string.

        Args:
            query (str): The keyword to search for.

        Returns:
            str: A formatted string containing relevant lessons and snippets.
        """
        results = []
        query_lower = query.lower()

        for num, content in self.lessons.items():
            if query_lower in content.lower():
                # Extract a snippet or just return the lesson title/intro
                # Let's return the first 200 chars or lines containing the keyword
                lines = content.split('\n')
                matching_lines = [line for line in lines if query_lower in line.lower()]

                # If we have matches, format them
                if matching_lines:
                    snippet = "\n".join(matching_lines[:3]) # First 3 matching lines
                    results.append(f"Found in Lesson {num}:\n{snippet}\n...")

        if not results:
            return "No matches found."

        return "\n\n".join(results)
