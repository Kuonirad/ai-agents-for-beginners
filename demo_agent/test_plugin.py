import sys
import os

# Add the parent directory to the path so we can run this from anywhere
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

def main():
    print("Testing CoursePlugin...\n")

    # Initialize the plugin
    plugin = CoursePlugin()

    # Test 1: Check if lessons were loaded
    print(f"Loaded {len(plugin.lessons)} lessons.")
    if not plugin.lessons:
        print("Failed to load lessons. Make sure STUDY_GUIDE.md is in the parent directory.")
        sys.exit(1)

    print("\n--- Test 2: get_lesson_content ---")
    lesson_4 = plugin.get_lesson_content("4")
    print(f"Lesson 4 excerpt (first 100 chars): {lesson_4[:100]}...")

    # Test prefix handling
    lesson_5 = plugin.get_lesson_content("Lesson 5")
    if lesson_5.startswith("## 5"):
         print("Successfully extracted lesson number from string prefix.")

    print("\n--- Test 3: search_content ---")
    results = plugin.search_content("Browser Use")
    if "Found 'Browser Use'" in results:
        print("Search successful. Found reference to 'Browser Use'.")
        print(results)
    else:
        print("Search failed to find 'Browser Use'.")
        print("Actual output:", results)

if __name__ == "__main__":
    main()
