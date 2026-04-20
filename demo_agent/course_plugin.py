import re
import os
import logging
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

logger = logging.getLogger(__name__)

class CoursePlugin:
    def __init__(self):
        self.lessons = {}
        # Resolve the path to CONCEPTS_EXPLAINED.md by navigating up one level from this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        guide_path = os.path.join(current_dir, "..", "CONCEPTS_EXPLAINED.md")

        try:
            with open(guide_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self._parse_guide(content)
        except FileNotFoundError:
            logger.warning(f"Warning: {guide_path} not found. Lessons will be empty.")
            self.lessons = {}

    def _parse_guide(self, text):
        parts = re.split(r'(## \d+\. .*?)\n', text)
        current_lesson = "0. Course Setup"
        self.lessons[current_lesson] = parts[0].strip() if parts else ""

        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                header = parts[i].strip()
                content = parts[i+1].strip()

                # Extract lesson title
                # E.g., "## 1. Introduction to AI Agents" -> "Introduction to AI Agents"
                title_match = re.search(r'## \d+\.\s*(.*)', header)
                if title_match:
                    lesson_title = title_match.group(1).strip()
                    self.lessons[lesson_title] = content

    @kernel_function(
        name="get_lesson_content",
        description="Gets the full content of a specific lesson."
    )
    def get_lesson_content(self, lesson_title: Annotated[str, "The title of the lesson to retrieve (e.g., 'Introduction to AI Agents')"]) -> Annotated[str, "The content of the lesson"]:
        if not self.lessons:
            return "No lessons available (CONCEPTS_EXPLAINED.md not found)."

        for title, content in self.lessons.items():
            if lesson_title.lower() in title.lower():
                return f"Content for {title}:\n\n{content}"

        return f"Lesson containing '{lesson_title}' not found. Available lessons: {list(self.lessons.keys())}"

    @kernel_function(
        name="search_content",
        description="Searches all course lessons for a specific keyword or phrase."
    )
    def search_content(self, query: Annotated[str, "The keyword or phrase to search for"]) -> Annotated[str, "Search results matching the query"]:
        if not self.lessons:
            return "No lessons available to search (CONCEPTS_EXPLAINED.md not found)."

        results = []
        for title, content in self.lessons.items():
            if query.lower() in content.lower() or query.lower() in title.lower():
                # Provide a snippet around the match if found in content
                match_index = content.lower().find(query.lower())
                if match_index != -1:
                    start = max(0, match_index - 50)
                    end = min(len(content), match_index + len(query) + 50)
                    snippet = content[start:end].replace('\n', ' ')
                    results.append(f"- **{title}**: ...{snippet}...")
                else:
                    results.append(f"- **{title}**: Query matched in title.")

        if results:
            return "Search Results:\n" + "\n".join(results)
        else:
            return f"No matches found for '{query}' in the course content."