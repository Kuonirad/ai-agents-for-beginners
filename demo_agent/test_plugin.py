import os
import sys

# Add the directory containing the file to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from demo_agent.course_plugin import CoursePlugin
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

def test_course_plugin():
    print("Initializing CoursePlugin...")
    plugin = CoursePlugin()

    print("\nAvailable Lessons:")
    for lesson in plugin.lessons.keys():
        print(f"- {lesson}")

    print("\nTesting search for 'Agentic RAG':")
    search_results = plugin.search_content("Agentic RAG")
    print(search_results)

    print("\nTesting get_lesson_content for '## 5. Agentic RAG':")
    content = plugin.get_lesson_content("## 5. Agentic RAG")
    print(content[:200] + "..." if len(content) > 200 else content)

if __name__ == "__main__":
    test_course_plugin()
