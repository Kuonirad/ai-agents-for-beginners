import os
import sys

# Ensure demo_agent module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

def test_plugin():
    print("Testing CoursePlugin initialization...")
    plugin = CoursePlugin()

    if not plugin.lessons:
        print("Failed to load lessons. Make sure STUDY_GUIDE.md exists in the parent directory.")
        return

    print(f"Successfully loaded {len(plugin.lessons)} lessons.\n")

    print("Testing get_lesson_content for Lesson 1:")
    lesson_1_content = plugin.get_lesson_content(1)
    if "Introduction to AI Agents" in lesson_1_content:
        print("Success! Excerpt:")
        print(f"{lesson_1_content[:200]}...\n")
    else:
        print("Failed to get correct content for Lesson 1.\n")

    print("Testing search_content for 'semantic':")
    search_results = plugin.search_content("semantic")
    if "semantic" in search_results.lower():
        print("Success! Search returned results:")
        print(f"{search_results[:300]}...\n")
    else:
        print("Failed to find results for 'semantic'.\n")

if __name__ == "__main__":
    test_plugin()
