import os
import sys

# Ensure we can import the plugin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

def test_course_plugin():
    print("Testing CoursePlugin...")
    plugin = CoursePlugin()

    # Check if lessons were loaded
    if not plugin.lessons:
        print("FAIL: No lessons loaded from STUDY_GUIDE.md")
        return
    else:
        print(f"SUCCESS: Loaded {len(plugin.lessons)} lessons.")

    # Test get_lesson_content
    lesson_1 = plugin.get_lesson_content(1)
    if "Introduction to AI Agents" in lesson_1:
        print("SUCCESS: Lesson 1 retrieved correctly.")
    else:
        print(f"FAIL: Lesson 1 content unexpected: {lesson_1[:100]}...")

    # Test search_content
    search_res = plugin.search_content("framework")
    if "Found in" in search_res:
        print("SUCCESS: Search returned results.")
    else:
        print(f"FAIL: Search failed: {search_res}")

    # Test invalid lesson
    invalid = plugin.get_lesson_content(999)
    if "not found" in invalid:
        print("SUCCESS: Invalid lesson handled correctly.")
    else:
        print(f"FAIL: Invalid lesson not handled: {invalid}")

if __name__ == "__main__":
    try:
        test_course_plugin()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
