import os
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    def __init__(self):
        # Resolve path to STUDY_GUIDE.md relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.study_guide_path = os.path.join(base_dir, "STUDY_GUIDE.md")

        if not os.path.exists(self.study_guide_path):
            raise FileNotFoundError(f"Study guide not found at {self.study_guide_path}")

        with open(self.study_guide_path, "r", encoding="utf-8") as f:
            self.content = f.read()

    @kernel_function(description="Gets the content of a specific lesson from the study guide.")
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Retrieves the content of a specific lesson based on its number.
        """
        # The study guide uses headers like "## 1. Title"
        # We need to find the start of the requested lesson and the start of the next one.

        start_marker = f"## {lesson_number}. "
        start_index = self.content.find(start_marker)

        if start_index == -1:
            return f"Lesson {lesson_number} not found in the study guide."

        # Find the next lesson's header or end of file
        # We search for "\n## " to find any next h2 header
        # We start searching after the current header
        search_start = start_index + len(start_marker)
        next_header_index = self.content.find("\n## ", search_start)

        if next_header_index != -1:
            return self.content[start_index:next_header_index].strip()
        else:
            # This is the last lesson or no more headers found
            return self.content[start_index:].strip()

    @kernel_function(description="Searches for keywords in the study guide.")
    def search_content(self, query: str) -> str:
        """
        Searches the study guide for the given query and returns relevant snippets.
        """
        if not query:
            return "Please provide a search query."

        lines = self.content.split('\n')
        results = []
        query_lower = query.lower()

        for i, line in enumerate(lines):
            if query_lower in line.lower():
                # Get a small context window around the match
                start = max(0, i - 1)
                end = min(len(lines), i + 4) # 1 line before, match, 3 lines after
                snippet = "\n".join(lines[start:end])
                results.append(f"--- Match in line {i+1} ---\n{snippet}")

        if not results:
            return f"No results found for '{query}'."

        return "\n\n".join(results[:5]) # Return top 5 matches
