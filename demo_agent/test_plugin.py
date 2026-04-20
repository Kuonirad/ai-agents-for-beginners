import sys
import os

# Add parent directory to path to allow importing the plugin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

def run_tests():
    print("Testing CoursePlugin...")
    plugin = CoursePlugin()

    # Test 1: Verify parsing was successful
    if not plugin.lessons:
        print("❌ FAIL: Plugin has no lessons loaded.")
        return False
    print(f"✅ Loaded {len(plugin.lessons)} sections/lessons.")

    # Test 2: Search for a known concept
    search_query = "Browser-Use"
    print(f"\nSearching for '{search_query}'...")
    search_results = plugin.search_content(search_query)
    if "Browser Use" in search_results:
        print(f"✅ Found '{search_query}' in search results.")
    else:
        print(f"❌ FAIL: '{search_query}' not found in search results.")
        print(f"Results were:\n{search_results}")
        return False

    # Test 3: Get content of a specific lesson
    lesson_title = "Browser Use"
    print(f"\nGetting content for '{lesson_title}'...")
    content = plugin.get_lesson_content(lesson_title)
    if "Playwright" in content:
        print(f"✅ Found expected content in '{lesson_title}' lesson.")
    else:
        print(f"❌ FAIL: Expected content not found in '{lesson_title}' lesson.")
        print(f"Content was:\n{content}")
        return False

    print("\n✅ All tests passed!")
    return True

if __name__ == "__main__":
    run_tests()