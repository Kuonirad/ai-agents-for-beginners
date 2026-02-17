import sys
import os
import asyncio

# Ensure we can import from demo_agent directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

async def test():
    print("Initializing CoursePlugin...")
    plugin = CoursePlugin()

    print("\nTesting get_lesson_content('1')...")
    lesson1 = plugin.get_lesson_content('1')
    if "Introduction to AI Agents" in lesson1:
        print("PASS: Lesson 1 content retrieved successfully.")
    else:
        print(f"FAIL: Lesson 1 content verification failed. Got: {lesson1[:100]}...")

    print("\nTesting search_content('Agent')...")
    search_results = plugin.search_content('Agent')
    if "Lesson" in search_results:
        print("PASS: Search returned results.")
    else:
        print(f"FAIL: Search failed. Got: {search_results}")

    print("\nTesting missing lesson...")
    missing = plugin.get_lesson_content('999')
    if "not found" in missing:
         print("PASS: Missing lesson handled correctly.")
    else:
         print(f"FAIL: Missing lesson handling failed. Got: {missing}")

if __name__ == "__main__":
    asyncio.run(test())
