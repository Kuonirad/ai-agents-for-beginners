import os
import sys

# Ensure we can import modules from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

def main():
    print("Initializing CoursePlugin...")
    plugin = CoursePlugin()

    # Test 1: Get Lesson 1 Content
    print("\n--- Test 1: Get Lesson 1 Content ---")
    lesson1 = plugin.get_lesson_content(1)
    if "Introduction to AI Agents" in lesson1:
        print("PASS: Lesson 1 content retrieved successfully.")
    else:
        print(f"FAIL: Lesson 1 content incorrect or missing. Got: {lesson1[:100]}...")

    # Test 2: Search Content
    print("\n--- Test 2: Search Content ---")
    search_results = plugin.search_content("framework")
    if "Found in" in search_results:
        print("PASS: Search returned results.")
        print(f"Results:\n{search_results}")
    else:
        print(f"FAIL: Search failed. Got: {search_results}")

    # Test 3: Invalid Lesson
    print("\n--- Test 3: Invalid Lesson ---")
    invalid_lesson = plugin.get_lesson_content(999)
    if "not found" in invalid_lesson:
        print("PASS: Invalid lesson handled correctly.")
    else:
        print(f"FAIL: Invalid lesson not handled correctly. Got: {invalid_lesson}")

if __name__ == "__main__":
    main()
