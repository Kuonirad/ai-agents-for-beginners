import os
import re
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    def __init__(self):
        self.lessons = {}
        self._load_lessons()

    def _load_lessons(self):
        content = ""
        try:
            # Navigate up to root
            file_path = os.path.join(os.path.dirname(__file__), "..", "STUDY_GUIDE.md")
            if not os.path.exists(file_path):
                 # Fallback if running from root
                 file_path = "STUDY_GUIDE.md"

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                print("Warning: STUDY_GUIDE.md not found. Using minimal fallback content.")
                content = """
## 1. Introduction to AI Agents
AI Agents extend LLMs with tools and memory.

## 2. Agentic Frameworks
Frameworks include Semantic Kernel and AutoGen.

## 3. Agentic Design Patterns
Space, Time, and Core dimensions. Transparency, Control, Consistency.

## 4. Tool Use Design Pattern
Enables agents to interact with the world via function calling.

## 5. Agentic RAG
Advanced retrieval strategies beyond standard RAG. Maker-Checker loop.

## 15. Browser Use
Enabling agents to autonomously interact with web browsers using Playwright.
"""

            # Split by headers like ## 1.
            parts = re.split(r'(## \d+\. .*?)\n', content)

            # parts[0] is intro before first header
            if parts:
                self.lessons[0] = parts[0].strip()

            for i in range(1, len(parts), 2):
                if i+1 < len(parts):
                    header = parts[i]
                    body = parts[i+1]
                    # Extract number
                    match = re.search(r'## (\d+)\.', header)
                    if match:
                        num = int(match.group(1))
                        self.lessons[num] = f"{header}\n{body}".strip()

        except Exception as e:
            print(f"Error loading study guide: {e}")
            self.lessons = {}

    @kernel_function(
        description="Retrieves the content of a specific lesson from the course study guide.",
        name="get_lesson_content",
    )
    def get_lesson_content(self, lesson_number: int) -> str:
        """
        Returns the text content of the specified lesson.

        Args:
            lesson_number: The integer number of the lesson (e.g., 1 for Intro, 15 for Browser Use).
        """
        return self.lessons.get(lesson_number, f"Lesson {lesson_number} not found.")

    @kernel_function(
        description="Searches the study guide for a given query string.",
        name="search_content",
    )
    def search_content(self, query: str) -> str:
        """
        Searches all lessons for the query string and returns relevant snippets.
        """
        results = []
        for num, content in self.lessons.items():
            if query.lower() in content.lower():
                # Extract a snippet around the match
                idx = content.lower().find(query.lower())
                start = max(0, idx - 50)
                end = min(len(content), idx + 150)
                snippet = content[start:end].replace("\n", " ")
                results.append(f"Found in Lesson {num}: ...{snippet}...")

        if not results:
            return "No matches found."
        return "\n\n".join(results[:5]) # Limit to 5 results
