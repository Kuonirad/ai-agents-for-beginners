import sys
import os

# Ensure the demo_agent module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

def main():
    print("Testing CoursePlugin...")
    plugin = CoursePlugin()

    # Test dictionary loading
    num_lessons = len(plugin.lessons)
    print(f"Loaded {num_lessons} lessons.")
    if num_lessons == 0:
        print("Warning: No lessons loaded. Ensure CONCEPTS_EXPLAINED.md exists and is formatted correctly.")
    else:
        print("Keys available:", list(plugin.lessons.keys())[:5], "...")

        # Test get_lesson_content
        print("\n--- Testing get_lesson_content('1') ---")
        lesson_1 = plugin.get_lesson_content('1')
        print(lesson_1[:250] + "...\n")

        # Test search_content
        print("--- Testing search_content('Playwright') ---")
        search_results = plugin.search_content('Playwright')
        print(search_results)

if __name__ == "__main__":
    main()
