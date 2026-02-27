import os
import sys

# Ensure we can import from local directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

def test_course_plugin():
    print("Initializing Course Plugin...")
    plugin = CoursePlugin()

    print(f"Loaded {len(plugin.lessons)} lessons.")

    if len(plugin.lessons) == 0:
        print("ERROR: No lessons loaded! Check STUDY_GUIDE.md path.")
        return

    # Test retrieving a specific lesson
    print("\n--- Testing get_lesson_content(1) ---")
    content = plugin.get_lesson_content(1)
    print(content[:200] + "...") # Print first 200 chars

    if "Introduction to AI Agents" not in content:
        print("ERROR: Lesson 1 content seems incorrect.")
    else:
        print("SUCCESS: Lesson 1 content retrieved.")

    # Test searching
    print("\n--- Testing search_content('RAG') ---")
    search_results = plugin.search_content("RAG")
    print(search_results)

    if "Lesson 5" in search_results:
        print("SUCCESS: Found RAG in Lesson 5.")
    else:
        print("ERROR: RAG not found in search results.")

if __name__ == "__main__":
    test_course_plugin()
