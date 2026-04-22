import sys
import os

# Ensure we can import from the demo_agent package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

def main():
    print("Testing CoursePlugin...")
    plugin = CoursePlugin()

    # Test getting lesson content
    print("\n--- Testing get_lesson_content(1) ---")
    lesson_1 = plugin.get_lesson_content(1)
    # Print the first 150 chars
    print(f"{lesson_1[:150]}...")

    # Test searching content
    print("\n--- Testing search_content('metacognition') ---")
    search_results = plugin.search_content('metacognition')
    print(search_results)

if __name__ == "__main__":
    main()