import os
import sys

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

def main():
    print("Testing CoursePlugin...")
    plugin = CoursePlugin()

    if not plugin.lessons:
        print("FAIL: No lessons loaded.")
        return

    print(f"Loaded {len(plugin.lessons)} lessons.")

    # Test Search
    query = "RAG"
    print(f"\nSearching for '{query}'...")
    result = plugin.search_content(query)

    if "Agentic RAG" in result:
        print("SUCCESS: RAG search returned relevant content.")
    else:
        print("FAIL: RAG search did not find expected content.")

    # Test Get Lesson
    lesson_num = "1"
    print(f"\nGetting Lesson {lesson_num}...")
    content = plugin.get_lesson_content(lesson_num)

    # Check for "Introduction to AI Agents" which is in the header
    if "Introduction to AI Agents" in content:
        print("SUCCESS: Lesson 1 content retrieved.")
    else:
        print(f"FAIL: Content mismatch. Got: {content[:50]}...")

if __name__ == "__main__":
    main()
