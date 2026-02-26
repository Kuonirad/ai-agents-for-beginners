import os
import re
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    def __init__(self):
        self.lessons = {}
        self._load_lessons()

    def _load_lessons(self):
        try:
            # Assuming this file is in demo_agent/ and STUDY_GUIDE.md is in root/
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, "STUDY_GUIDE.md")

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split by headers like ## 1. Lesson Name
            # The capture group in split keeps the separator in the result list
            parts = re.split(r'(## \d+\. .*?)\n', content)

            current_lesson = None

            # parts[0] is usually content before the first lesson (intro)
            # parts[1] is header, parts[2] is content, parts[3] is header...

            for part in parts:
                if part.startswith("## "):
                    # Extract lesson number
                    match = re.search(r'## (\d+)\.', part)
                    if match:
                        current_lesson = int(match.group(1))
                        self.lessons[current_lesson] = part + "\n"
                elif current_lesson is not None:
                    self.lessons[current_lesson] += part

        except FileNotFoundError:
            print("Warning: STUDY_GUIDE.md not found.")
            self.lessons = {}

    @kernel_function(
        description="Retrieves the content of a specific lesson from the course study guide.",
        name="get_lesson_content",
    )
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Returns the content of the specified lesson number.
        """
        return self.lessons.get(lesson_number, "Lesson not found.")

    @kernel_function(
        description="Searches for a query string within the course study guide.",
        name="search_content",
    )
    def search_content(self, query: str) -> str:
        """
        Returns a list of lesson titles that contain the query string.
        """
        results = []
        for lesson_num, content in self.lessons.items():
            if query.lower() in content.lower():
                # Extract title from first line
                title_line = content.split('\n')[0]
                results.append(f"Found in {title_line}")

        if not results:
            return "No relevant content found."
        return "\n".join(results)
