import os
import sys

# Add parent directory to path so we can import as a module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

def main():
    print("Testing CoursePlugin...")
    plugin = CoursePlugin()

    if not plugin.lessons:
        print("Failed to load lessons. Make sure STUDY_GUIDE.md is present in the root.")
        sys.exit(1)

    print(f"Successfully loaded {len(plugin.lessons)} lessons.")

    print("\n--- Testing get_lesson_content(1) ---")
    lesson1 = plugin.get_lesson_content("1")
    print(lesson1[:200] + "...\n")

    print("--- Testing search_content('RAG') ---")
    search_results = plugin.search_content("RAG")
    print(search_results[:300] + "...\n")

    print("All tests passed!")

if __name__ == "__main__":
    main()
