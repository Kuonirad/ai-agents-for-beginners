import logging
import os
import re
from typing import Dict
from semantic_kernel.functions.kernel_function_decorator import kernel_function

logger = logging.getLogger(__name__)

class CoursePlugin:
    """
    A plugin for retrieving course content from the study guide.
    """

    def __init__(self):
        self.lessons: Dict[str, str] = {}
        self._load_study_guide()

    def _load_study_guide(self):
        """Loads and parses the STUDY_GUIDE.md file into lessons."""
        # Find path to STUDY_GUIDE.md (up one level from demo_agent directory)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        guide_path = os.path.join(current_dir, "..", "STUDY_GUIDE.md")

        try:
            with open(guide_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Split the content by lesson headers (e.g., '## 1. ')
            parts = re.split(r'(## \d+\. .*?)\n', content)

            # The first part is everything before the first '## \d+\. ' (table of contents)
            # The rest comes in pairs: [header, content, header, content...]
            for i in range(1, len(parts), 2):
                if i + 1 < len(parts):
                    header = parts[i].strip()
                    lesson_content = parts[i+1].strip()

                    # Extract the lesson number for easier indexing
                    match = re.search(r'## (\d+)\.', header)
                    if match:
                        lesson_num = match.group(1)
                        # Save the lesson content with both the header and content
                        self.lessons[lesson_num] = f"{header}\n\n{lesson_content}"

            logger.info(f"Successfully loaded {len(self.lessons)} lessons from STUDY_GUIDE.md")

        except FileNotFoundError:
            logger.warning(f"Could not find {guide_path}. The agent will not have access to course content.")
            self.lessons = {}
        except Exception as e:
            logger.error(f"Error loading study guide: {e}")
            self.lessons = {}

    @kernel_function(
        description="Gets the detailed content for a specific lesson number in the AI Agents course.",
        name="get_lesson_content"
    )
    def get_lesson_content(self, lesson_number: str) -> str:
        """
        Returns the content of a specific lesson.

        Args:
            lesson_number: The number of the lesson as a string (e.g., "1", "15").

        Returns:
            The content of the lesson or an error message if not found.
        """
        # Ensure it's just the number
        lesson_number = str(lesson_number).strip()
        if not lesson_number.isdigit():
            # Try to extract number if passed with prefix like 'Lesson 1'
            match = re.search(r'(\d+)', lesson_number)
            if match:
                lesson_number = match.group(1)

        if lesson_number in self.lessons:
            return self.lessons[lesson_number]
        else:
            return f"Error: Lesson {lesson_number} not found. Available lessons: {', '.join(sorted(self.lessons.keys(), key=int))}."

    @kernel_function(
        description="Searches all course lessons for a specific concept or keyword.",
        name="search_content"
    )
    def search_content(self, query: str) -> str:
        """
        Searches across all lessons for a keyword or concept.

        Args:
            query: The keyword or concept to search for.

        Returns:
            A string containing all relevant lessons and excerpts that match the query.
        """
        results = []
        query_lower = query.lower()

        for lesson_num, content in self.lessons.items():
            if query_lower in content.lower():
                # Extract a small excerpt around the match
                lines = content.split('\n')
                excerpt_lines = []

                # Always include the header if lines exist
                if lines:
                    excerpt_lines.append(lines[0])

                # Include the line if it matches, else check if it's the title
                match_found = False
                for line in lines[1:]:
                    if query_lower in line.lower():
                        excerpt_lines.append(f"  ... {line.strip()} ...")
                        match_found = True

                if match_found or query_lower in lines[0].lower():
                    results.append("\n".join(excerpt_lines))

        if results:
            return f"Found '{query}' in the following lessons:\n\n" + "\n\n".join(results)
        else:
            return f"No information found about '{query}' in the course material."
