import os
import glob
from typing import Annotated
from semantic_kernel.functions import kernel_function

class CoursePlugin:
    """Plugin to access course content."""

    @kernel_function(description="Search the course content for a specific topic.")
    def search_content(self, query: Annotated[str, "The topic to search for"]) -> str:
        """
        Searches the STUDY_GUIDE.md file for the query string.
        If not found or if the file is missing, searches lesson READMEs.
        Returns relevant sections or a summary if found.
        """
        try:
            results = []
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            study_guide_path = os.path.join(base_dir, "STUDY_GUIDE.md")

            # 1. Search STUDY_GUIDE.md if it exists
            if os.path.exists(study_guide_path):
                with open(study_guide_path, "r", encoding="utf-8") as f:
                    content = f.read()

                paragraphs = content.split("\n\n")
                for p in paragraphs:
                    if query.lower() in p.lower():
                        results.append(f"[Study Guide] {p.strip()}")

            # 2. If results are sparse (less than 3 matches) or STUDY_GUIDE missing, search lessons
            if len(results) < 3:
                # Find all lesson directories (00- to 15-)
                lesson_dirs = glob.glob(os.path.join(base_dir, "[0-9][0-9]-*"))

                for lesson_dir in lesson_dirs:
                    readme_path = os.path.join(lesson_dir, "README.md")
                    if os.path.exists(readme_path):
                        with open(readme_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        # Extract lesson name from directory
                        lesson_name = os.path.basename(lesson_dir)

                        paragraphs = content.split("\n\n")
                        for p in paragraphs:
                            if query.lower() in p.lower():
                                results.append(f"[{lesson_name}] {p.strip()}")
                                if len(results) >= 5: # Limit total results
                                    break
                    if len(results) >= 5:
                        break

            if not results:
                return f"No information found for '{query}' in the course materials."

            return "\n\n".join(results[:5]) # Return top 5 matches

        except Exception as e:
            return f"Error searching content: {str(e)}"

    @kernel_function(description="Get the full content of a specific lesson.")
    def get_lesson_content(self, lesson_number: Annotated[int, "The lesson number (1-15)"]) -> str:
        """
        Retrieves the README.md content for a given lesson number.
        """
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # Find directory starting with the lesson number
            # Format is usually '01-intro...', '15-browser-use'
            # We need to handle single digit numbers by adding leading zero
            lesson_prefix = f"{lesson_number:02d}-"

            search_pattern = os.path.join(base_dir, f"{lesson_prefix}*")
            matches = glob.glob(search_pattern)

            if not matches:
                return f"Error: Lesson {lesson_number} not found."

            lesson_dir = matches[0]
            readme_path = os.path.join(lesson_dir, "README.md")

            if not os.path.exists(readme_path):
                return f"Error: README.md not found for Lesson {lesson_number}."

            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()

            return content[:2000] + "\n...(truncated for context limits)..." if len(content) > 2000 else content

        except Exception as e:
            return f"Error retrieving lesson content: {str(e)}"
