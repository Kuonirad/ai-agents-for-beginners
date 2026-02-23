import os
import sys

# Add the current directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

def test_course_plugin():
    print("Testing CoursePlugin...")
    plugin = CoursePlugin()

    # Test 1: Get Lesson 1
    print("\n[Test 1] Fetching Lesson 1 Content:")
    content_1 = plugin.get_lesson_content(1)
    if "Introduction to AI Agents" in content_1:
        print("PASS: Lesson 1 content retrieved successfully.")
    else:
        print("FAIL: Lesson 1 content missing or incorrect.")
        print(f"Content: {content_1[:100]}...")

    # Test 2: Search for "RAG"
    print("\n[Test 2] Searching for 'RAG':")
    search_results = plugin.search_content("RAG")
    if "Lesson 5" in search_results:
        print("PASS: Search for 'RAG' found relevant lessons.")
    else:
        print("FAIL: Search for 'RAG' did not return expected results.")
        print(f"Results: {search_results}")

    # Test 3: Invalid Lesson
    print("\n[Test 3] Fetching Invalid Lesson 99:")
    content_99 = plugin.get_lesson_content(99)
    if "not found" in content_99:
        print("PASS: Invalid lesson handled correctly.")
    else:
        print("FAIL: Invalid lesson not handled correctly.")
        print(f"Content: {content_99}")

if __name__ == "__main__":
    test_course_plugin()
