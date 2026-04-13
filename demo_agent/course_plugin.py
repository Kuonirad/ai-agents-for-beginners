import os
import re
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from typing import Annotated

class CoursePlugin:
    """
    A plugin to search and retrieve course content from STUDY_GUIDE.md.
    """
    def __init__(self):
        self.lessons = {}
        # Path to STUDY_GUIDE.md in the root directory relative to this file
        guide_path = os.path.join(os.path.dirname(__file__), "..", "STUDY_GUIDE.md")
        try:
            with open(guide_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Use regex to split the content by headers starting with "## " followed by digits.
                # E.g. "## 1. Intro to AI Agents"
                parts = re.split(r'(## \d+\. .*?)\n', content)

                # The first part is the introduction before any lesson header
                if parts and not parts[0].startswith("## "):
                    self.lessons["Introduction"] = parts[0].strip()
                    parts = parts[1:]

                # Iterate through the split parts and pair headers with their content
                for i in range(0, len(parts), 2):
                    if i+1 < len(parts):
                        header = parts[i].strip()
                        text = parts[i+1].strip()
                        self.lessons[header] = text
        except FileNotFoundError:
            print(f"Warning: Could not find STUDY_GUIDE.md at {guide_path}")

    @kernel_function(
        name="get_lesson_content",
        description="Retrieves the full content of a specific lesson based on its exact title or lesson number."
    )
    def get_lesson_content(self, lesson_id: Annotated[str, "The lesson number or title to retrieve (e.g. '1', '1.', or 'Intro to AI Agents')"]) -> Annotated[str, "The content of the lesson"]:
        """Retrieves lesson content based on ID or part of the title."""
        for header, content in self.lessons.items():
            if lesson_id.lower() in header.lower():
                return f"{header}\n\n{content}"
        return f"Lesson '{lesson_id}' not found."

    @kernel_function(
        name="search_content",
        description="Searches all lessons for a specific keyword or phrase."
    )
    def search_content(self, query: Annotated[str, "The keyword or phrase to search for in the course content"]) -> Annotated[str, "A summary of matching lessons and their relevant excerpts"]:
        """Searches all lesson contents for a specific query."""
        results = []
        for header, content in self.lessons.items():
            if query.lower() in content.lower() or query.lower() in header.lower():
                # Extract a snippet around the first occurrence
                lower_content = content.lower()
                idx = lower_content.find(query.lower())
                start = max(0, idx - 50)
                end = min(len(content), idx + 100)
                snippet = content[start:end].replace('\n', ' ')
                results.append(f"Found in {header}:\n...{snippet}...")

        if results:
            return "\n\n".join(results)
        return f"No matches found for '{query}'."
