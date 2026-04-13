from course_plugin import CoursePlugin

def run_tests():
    plugin = CoursePlugin()

    print("Testing get_lesson_content('1.'):")
    content = plugin.get_lesson_content('1.')
    print(content[:200] + "...\n")

    print("Testing search_content('RAG'):")
    results = plugin.search_content('RAG')
    print(results + "\n")

if __name__ == "__main__":
    run_tests()
