import os
import re
from typing import Annotated
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    def __init__(self, study_guide_path: str = "../STUDY_GUIDE.md"):
        self.study_guide_path = study_guide_path
        self.lessons = {}
        self._load_guide()

    def _load_guide(self):
        """Loads and parses the study guide."""
        if not os.path.exists(self.study_guide_path):
            # Fallback for when running from root or different location
            if os.path.exists("STUDY_GUIDE.md"):
                self.study_guide_path = "STUDY_GUIDE.md"
            elif os.path.exists(os.path.join(os.path.dirname(__file__), "../STUDY_GUIDE.md")):
                self.study_guide_path = os.path.join(os.path.dirname(__file__), "../STUDY_GUIDE.md")
            else:
                print(f"Warning: STUDY_GUIDE.md not found at {self.study_guide_path}")
                return

        with open(self.study_guide_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split content by lesson headers (e.g., "## 1. Introduction")
        # Regex to find headers starting with ## followed by a number
        # We assume the format "## <number>. <Title>"
        parts = re.split(r'^##\s+(\d+)\.', content, flags=re.MULTILINE)

        # parts[0] is intro before first lesson
        # parts[1] is lesson number 1
        # parts[2] is content of lesson 1
        # parts[3] is lesson number 2
        # parts[4] is content of lesson 2
        # etc.

        for i in range(1, len(parts), 2):
            try:
                lesson_num = int(parts[i])
                lesson_content = parts[i+1].strip()
                # Add back the header title which is part of the content but stripped of "## N."
                # Actually re.split consumes the delimiter. parts[i+1] starts with the title line.
                self.lessons[lesson_num] = f"## {lesson_num}.{lesson_content}"
            except ValueError:
                continue

    @kernel_function(description="Retrieves the content of a specific lesson number from the course.")
    def get_lesson_content(
        self,
        lesson_number: Annotated[int, "The number of the lesson to retrieve (1-15)."]
    ) -> str:
        """Returns the content of the specified lesson."""
        if lesson_number in self.lessons:
            return self.lessons[lesson_number]
        else:
            return f"Lesson {lesson_number} not found. Available lessons: {list(self.lessons.keys())}"

    @kernel_function(description="Searches the study guide for a specific keyword or query.")
    def search_content(
        self,
        query: Annotated[str, "The keyword or phrase to search for."]
    ) -> str:
        """Searches for the query in all lessons and returns relevant sections."""
        results = []
        for num, content in self.lessons.items():
            if query.lower() in content.lower():
                # Extract a snippet around the match
                idx = content.lower().find(query.lower())
                start = max(0, idx - 50)
                end = min(len(content), idx + 150)
                snippet = content[start:end].replace("\n", " ")
                results.append(f"Lesson {num}: ...{snippet}...")

        if not results:
            return f"No results found for '{query}'."
        return "\n".join(results[:5]) # Limit to top 5 results
