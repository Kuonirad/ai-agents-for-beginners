from course_plugin import CoursePlugin

def test_course_plugin():
    print("Initializing CoursePlugin...")
    plugin = CoursePlugin()

    print(f"Parsed {len(plugin.lessons)} lessons.")

    # Test getting lesson 1
    print("\n--- Testing get_lesson_content('1') ---")
    lesson1 = plugin.get_lesson_content("1")
    print(lesson1[:200] + "..." if len(lesson1) > 200 else lesson1)

    # Test search
    print("\n--- Testing search_content('RAG') ---")
    search_results = plugin.search_content("RAG")
    print(search_results)

    print("\n--- Testing search_content('notfoundword') ---")
    search_results = plugin.search_content("notfoundword")
    print(search_results)

if __name__ == "__main__":
    test_course_plugin()
