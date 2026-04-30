import os
import re
import logging
from typing import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class CoursePlugin:
    """
    A Semantic Kernel plugin for retrieving course content from CONCEPTS_EXPLAINED.md.
    """

    def __init__(self):
        self.lessons = {}
        # Resolve path up one level from the current file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'CONCEPTS_EXPLAINED.md')

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self._parse_content(content)
        except FileNotFoundError:
            logging.warning(f"File not found: {file_path}. Initialization continuing with empty lessons dictionary.")
            self.lessons = {}

    def _parse_content(self, text: str):
        """
        Parses the content by splitting on the markdown headers for lessons.
        Format example: '## 1. Introduction to AI Agents'
        """
        # Split text into header and content chunks
        chunks = re.split(r'(## \d+\. .*?)\n', text)

        # The first element is content before the first lesson header (e.g., Table of Contents)
        if len(chunks) > 0:
            self.lessons["0. Course Setup"] = chunks[0].strip()

        # Iterate over the chunks pairing headers with their subsequent content
        for i in range(1, len(chunks) - 1, 2):
            header = chunks[i].strip()
            content = chunks[i+1].strip()
            self.lessons[header] = content

    @kernel_function(
        name="get_lesson_content",
        description="Gets the detailed content for a specific lesson based on a lesson header key. Returns available lesson keys if the key is not found."
    )
    def get_lesson_content(self, lesson_key: Annotated[str, "The exact header key for the lesson to retrieve."]) -> str:
        if lesson_key in self.lessons:
            return self.lessons[lesson_key]
        else:
            available_keys = "\n".join(self.lessons.keys())
            return f"Lesson key not found. Available lessons:\n{available_keys}"

    @kernel_function(
        name="search_content",
        description="Searches all lessons for a specific keyword or phrase."
    )
    def search_content(self, query: Annotated[str, "The keyword or phrase to search for across course content."]) -> str:
        results = []
        lower_query = query.lower()
        for key, content in self.lessons.items():
            if lower_query in key.lower() or lower_query in content.lower():
                # Provide a snippet or indicating it matches this lesson
                results.append(f"Match found in section: {key}")

        if results:
            return "\n".join(results)
        else:
            return "No matching content found."
