import os
import sys

# Add the current directory to sys.path to ensure we can import the module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from course_plugin import CoursePlugin
except ImportError:
    # Try importing with package prefix if run from root
    from demo_agent.course_plugin import CoursePlugin

def main():
    print("Initializing CoursePlugin...")
    plugin = CoursePlugin()

    print(f"Loaded {len(plugin.lessons)} lessons.")

    # Test get_lesson_content
    print("\n--- Testing get_lesson_content(1) ---")
    lesson1 = plugin.get_lesson_content(1)
    print(lesson1[:200] + "...") # Print first 200 chars

    # Test search_content
    print("\n--- Testing search_content('metacognition') ---")
    search_result = plugin.search_content("metacognition")
    print(search_result)

    # Test search_content with no results
    print("\n--- Testing search_content('xyz123') ---")
    no_result = plugin.search_content("xyz123")
    print(no_result)

if __name__ == "__main__":
    main()
