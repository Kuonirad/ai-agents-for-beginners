import sys
import os

# Ensure we can import the plugin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from course_plugin import CoursePlugin
except ImportError:
    # If running from root
    sys.path.append(os.path.abspath("demo_agent"))
    from demo_agent.course_plugin import CoursePlugin

def test_plugin():
    plugin = CoursePlugin()

    # Check if lessons are loaded
    print(f"Loaded {len(plugin.lessons)} lessons.")

    # Test specific lesson retrieval
    lesson_1 = plugin.get_lesson_content(1)
    if "Introduction to AI Agents" in lesson_1:
        print("✓ Lesson 1 retrieval successful.")
    else:
        print("✗ Lesson 1 retrieval failed.")
        print(f"Content: {lesson_1[:100]}...")

    # Test search
    search_results = plugin.search_content("RAG")
    if "Found in" in search_results:
        print("✓ Search successful.")
        print(search_results)
    else:
        print("✗ Search failed.")
        print(f"Results: {search_results}")

if __name__ == "__main__":
    test_plugin()
