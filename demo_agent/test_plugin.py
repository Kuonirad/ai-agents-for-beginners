import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

def main():
    print("Testing CoursePlugin...")
    plugin = CoursePlugin()

    # Test getting lesson content
    print("\n--- Testing get_lesson_content('1') ---")
    content = plugin.get_lesson_content("1")
    print(content[:200] + "..." if len(content) > 200 else content)

    # Test searching content
    print("\n--- Testing search_content('agent') ---")
    search_results = plugin.search_content("agent")
    print(search_results)

if __name__ == "__main__":
    main()
