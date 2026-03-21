import os
import re
import logging
from typing import Dict, Any

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class CoursePlugin:
    """
    Plugin to retrieve information from the course STUDY_GUIDE.md.
    """

    def __init__(self):
        self.lessons: Dict[int, Dict[str, str]] = {}
        self._load_study_guide()

    def _load_study_guide(self):
        """Loads and parses STUDY_GUIDE.md."""
        try:
            # Resolve path to STUDY_GUIDE.md
            current_dir = os.path.dirname(os.path.abspath(__file__))
            guide_path = os.path.join(current_dir, '..', 'STUDY_GUIDE.md')

            with open(guide_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse content based on headers
            parts = re.split(r'(## \d+\. .*?)\n', content)

            # parts will contain [intro_text, header1, content1, header2, content2, ...]
            # We skip the first element (intro text)

            for i in range(1, len(parts), 2):
                if i + 1 < len(parts):
                    header = parts[i].strip()
                    body = parts[i+1].strip()

                    # Extract lesson number from header, e.g., "## 1. Introduction to AI Agents" -> 1
                    match = re.search(r'## (\d+)\. (.*)', header)
                    if match:
                        lesson_num = int(match.group(1))
                        lesson_title = match.group(2)

                        self.lessons[lesson_num] = {
                            "title": lesson_title,
                            "content": f"{header}\n{body}"
                        }

        except FileNotFoundError:
            logging.warning("STUDY_GUIDE.md not found. CoursePlugin will have no content.")
            self.lessons = {}
        except Exception as e:
            logging.error(f"Error loading STUDY_GUIDE.md: {e}")
            self.lessons = {}


    @kernel_function(
        description="Gets the detailed content for a specific lesson by lesson number.",
        name="get_lesson_content"
    )
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Returns the content of a specific lesson.
        """
        lesson = self.lessons.get(lesson_number)
        if lesson:
            return lesson["content"]
        else:
            return f"Lesson {lesson_number} not found."

    @kernel_function(
        description="Searches the study guide for a specific concept or keyword.",
        name="search_content"
    )
    def search_content(self, query: str) -> str:
        """
        Searches all lessons for the given query (case-insensitive) and returns matching excerpts.
        """
        results = []
        query_lower = query.lower()

        for lesson_num, lesson_data in self.lessons.items():
            if query_lower in lesson_data["content"].lower():
                # Extract a snippet around the first match
                content = lesson_data["content"]
                # We could do a basic context extraction here, or just return the whole lesson
                results.append(f"Match found in Lesson {lesson_num}: {lesson_data['title']}\n{content[:500]}...\n")

        if results:
            return "\n".join(results)
        else:
            return f"No results found for '{query}'."
