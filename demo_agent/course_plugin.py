from semantic_kernel.functions import kernel_function
from typing import Annotated
import os
import sys

# Handle import depending on execution context
try:
    from .course_content import load_course_content
except ImportError:
    # If running directly or from a script in the same directory without package context
    try:
        from course_content import load_course_content
    except ImportError:
        # If running from root as module
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from course_content import load_course_content

class CoursePlugin:
    """
    A plugin to access AI Agents for Beginners course content.
    """
    def __init__(self, study_guide_path: str = "STUDY_GUIDE.md"):
        # Resolve path if needed
        if not os.path.exists(study_guide_path):
             # Try parent directory if running from inside demo_agent or if path is relative
             # Check if we are in demo_agent directory
             current_dir = os.path.dirname(os.path.abspath(__file__))
             # Assuming STUDY_GUIDE.md is in the parent of current_dir (repo root)
             root_path = os.path.dirname(current_dir)
             potential_path = os.path.join(root_path, study_guide_path)
             if os.path.exists(potential_path):
                 study_guide_path = potential_path
             else:
                 # Fallback: check ../STUDY_GUIDE.md relative to CWD
                 if os.path.exists("../STUDY_GUIDE.md"):
                     study_guide_path = "../STUDY_GUIDE.md"

        self.content = load_course_content(study_guide_path)

    @kernel_function(description="Get the content of a specific lesson by number.")
    def get_lesson_content(self, lesson_number: Annotated[int, "The lesson number"]) -> str:
        """Returns the full text of the lesson."""
        if not self.content:
            return "No course content available."

        if lesson_number in self.content:
            return self.content[lesson_number]["full_text"]
        return f"Lesson {lesson_number} not found. Available lessons: {min(self.content.keys())}-{max(self.content.keys())}"

    @kernel_function(description="Search the course content for keywords.")
    def search_content(self, query: Annotated[str, "The search query"]) -> str:
        """Searches titles and bodies for the query."""
        results = []
        query_lower = query.lower()
        for num, lesson in self.content.items():
            if query_lower in lesson["title"].lower() or query_lower in lesson["body"].lower():
                results.append(f"Lesson {num}: {lesson['title']}")

        if not results:
            return "No matching lessons found."
        return "Found in:\n" + "\n".join(results)

    @kernel_function(description="List all available lessons.")
    def list_lessons(self) -> str:
        """Returns a list of all lesson titles."""
        if not self.content:
            return "No course content available."

        lines = []
        for num in sorted(self.content.keys()):
            lines.append(f"{num}. {self.content[num]['title']}")
        return "\n".join(lines)
