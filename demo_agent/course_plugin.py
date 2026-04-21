import os
import re
import logging
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

logger = logging.getLogger(__name__)

class CoursePlugin:
    """
    A Semantic Kernel plugin that parses the course concepts guide
    and allows an agent to search and retrieve content.
    """

    def __init__(self):
        self.lessons = {}
        # Path resolution from within demo_agent directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        guide_path = os.path.join(base_dir, "..", "CONCEPTS_EXPLAINED.md")

        try:
            with open(guide_path, "r", encoding="utf-8") as file:
                content = file.read()
            self._parse_guide(content)
            logger.info(f"Loaded {len(self.lessons)} lessons from CONCEPTS_EXPLAINED.md")
        except FileNotFoundError:
            logger.warning(f"File not found: {guide_path}. Ensure it exists in the repository root. Setting empty lessons dictionary.")
            self.lessons = {}

    def _parse_guide(self, text: str):
        # Splits the text by markdown headers for lessons.
        # Format expected: ## <Number>. <Title>
        parts = re.split(r'(## \d+\. .*?)\n', text)

        # parts[0] is everything before the first lesson header
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                header = parts[i].strip()
                content = parts[i+1].strip()

                # Extract the lesson number, if possible
                match = re.search(r'## (\d+)\.', header)
                if match:
                    lesson_num = match.group(1)
                    # We store it by string key
                    self.lessons[lesson_num] = f"{header}\n\n{content}"
                else:
                    # Fallback storing by full header
                    self.lessons[header] = f"{header}\n\n{content}"

    @kernel_function(
        name="get_lesson_content",
        description="Retrieves the detailed content for a specific lesson by its number (e.g., '1', '15'). Use this when you know exactly which lesson the user is asking about."
    )
    def get_lesson_content(
        self,
        lesson_number: Annotated[str, "The lesson number as a string (e.g. '1', '12')."]
    ) -> Annotated[str, "The content of the requested lesson, or a message saying it was not found."]:
        return self.lessons.get(lesson_number, f"Lesson {lesson_number} not found in the course concepts.")

    @kernel_function(
        name="search_content",
        description="Searches all lesson contents for a specific keyword or phrase and returns matching sections. Use this when you are not sure which lesson contains the information."
    )
    def search_content(
        self,
        query: Annotated[str, "The keyword or phrase to search for across all lessons."]
    ) -> Annotated[str, "A summary of sections containing the keyword."]:
        results = []
        for key, content in self.lessons.items():
            if query.lower() in content.lower():
                # Extracting just the header part for the summary
                header_match = re.match(r'(## .*?)\n', content)
                header = header_match.group(1) if header_match else f"Lesson {key}"
                results.append(f"Found in {header}:\n... {content[:200]} ...\n")

        if results:
            return "\n\n".join(results)
        return f"No results found for query: '{query}'"
