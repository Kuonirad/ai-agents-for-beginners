import os
import re
from typing import Annotated, List, Dict
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """
    A plugin to access the AI Agents for Beginners course content.
    """

    def __init__(self):
        self.lessons: Dict[int, str] = {}
        try:
            self._load_content()
        except Exception as e:
            print(f"Warning: Failed to load course content: {e}")
            self.lessons = {}

    def _load_content(self):
        """Loads and parses the STUDY_GUIDE.md file."""
        # Navigate up one level from demo_agent/ to root
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "..", "STUDY_GUIDE.md")

        if not os.path.exists(file_path):
            # Fallback if running from root
            file_path = "STUDY_GUIDE.md"

        if not os.path.exists(file_path):
            # Instead of raising, we just return (warning printed by caller if needed, or here)
            raise FileNotFoundError(f"Could not find STUDY_GUIDE.md at {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split by headers like "## 1. "
        # The regex captures the delimiter so we can keep the title
        parts = re.split(r'(## \d+\. .*?)\n', content)

        # parts[0] is intro before first lesson
        # parts[1] is header 1, parts[2] is content 1, parts[3] is header 2...

        current_header = ""
        for part in parts:
            if part.startswith("## "):
                current_header = part.strip()
            elif current_header:
                # Extract lesson number
                match = re.match(r"## (\d+)\.", current_header)
                if match:
                    lesson_num = int(match.group(1))
                    full_text = f"{current_header}\n{part.strip()}"
                    self.lessons[lesson_num] = full_text
                current_header = ""

    @kernel_function(description="Retrieves the content of a specific lesson by its number.")
    def get_lesson_content(
        self,
        lesson_number: Annotated[int, "The lesson number to retrieve (1-15)."]
    ) -> str:
        """
        Returns the text content of the specified lesson.
        """
        if not self.lessons:
            return "Error: Course content not loaded. Please ensure STUDY_GUIDE.md is present."

        if lesson_number in self.lessons:
            return self.lessons[lesson_number]

        return f"Lesson {lesson_number} not found. Available lessons: {min(self.lessons.keys())}-{max(self.lessons.keys())}."

    @kernel_function(description="Searches the course content for a keyword.")
    def search_content(
        self,
        query: Annotated[str, "The keyword or phrase to search for."]
    ) -> str:
        """
        Searches all lessons for the query and returns matching segments.
        """
        if not self.lessons:
            return "Error: Course content not loaded. Please ensure STUDY_GUIDE.md is present."

        results = []
        query_lower = query.lower()

        for num, content in self.lessons.items():
            if query_lower in content.lower():
                # Simple implementation: Return the lesson header.
                header = content.split('\n')[0]
                results.append(f"Found in {header}")

                # Add context around the match
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        snippet = "\n".join(lines[max(0, i-1):min(len(lines), i+2)])
                        results.append(f"...\n{snippet}\n...")
                        break # Only one snippet per lesson to avoid spam

        if not results:
            return "No matches found."

        return "\n".join(results)
