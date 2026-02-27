import os
import re
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    def __init__(self):
        # Assuming STUDY_GUIDE.md is in the root of the repo, one level up from demo_agent
        self.study_guide_path = os.path.join(os.path.dirname(__file__), '..', 'STUDY_GUIDE.md')
        self.lessons = {}
        self._load_study_guide()

    def _load_study_guide(self):
        try:
            with open(self.study_guide_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split by headers like "## 1. Introduction to AI Agents"
            # This regex captures the header and the content following it
            sections = re.split(r'(## \d+\. .*?)\n', content)

            # The first element is usually the intro before the first lesson
            # Subsequent elements are (header, content) pairs
            for i in range(1, len(sections), 2):
                header = sections[i].strip()
                body = sections[i+1].strip()

                # Extract lesson number from header
                match = re.search(r'## (\d+)\.', header)
                if match:
                    lesson_num = int(match.group(1))
                    self.lessons[lesson_num] = {
                        'title': header.replace('## ', ''),
                        'content': body
                    }
        except FileNotFoundError:
            print(f"Warning: Study guide not found at {self.study_guide_path}")
            self.lessons = {}

    @kernel_function(
        description="Retrieves the content of a specific lesson number from the course study guide.",
        name="get_lesson_content"
    )
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Get the content of a specific lesson.

        Args:
            lesson_number: The integer number of the lesson to retrieve.

        Returns:
            The content of the lesson or a message if not found.
        """
        lesson = self.lessons.get(lesson_number)
        if lesson:
            return f"# {lesson['title']}\n\n{lesson['content']}"
        else:
            return f"Lesson {lesson_number} not found. Available lessons: {list(self.lessons.keys())}"

    @kernel_function(
        description="Searches for a keyword or phrase across all lessons in the study guide.",
        name="search_content"
    )
    def search_content(self, query: str) -> str:
        """
        Search for a query string in the study guide.

        Args:
            query: The string to search for.

        Returns:
            A string containing snippets of matching lessons.
        """
        results = []
        query_lower = query.lower()

        for num, data in self.lessons.items():
            if query_lower in data['title'].lower() or query_lower in data['content'].lower():
                # Find the context in the content
                content_lower = data['content'].lower()
                start_idx = content_lower.find(query_lower)

                snippet = ""
                if start_idx != -1:
                    start = max(0, start_idx - 50)
                    end = min(len(data['content']), start_idx + len(query) + 50)
                    snippet = f"...{data['content'][start:end]}..."
                else:
                    snippet = "Found in title."

                results.append(f"Lesson {num}: {data['title']}\nSnippet: {snippet}\n")

        if results:
            return "\n".join(results)
        else:
            return f"No results found for '{query}'."
