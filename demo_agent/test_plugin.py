import asyncio
import sys
import os

# Add the parent directory to sys.path to allow importing from demo_agent package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

async def main():
    print("Testing CoursePlugin...")
    try:
        # Since we are running from root or inside demo_agent, the relative path
        # inside CoursePlugin handles locating STUDY_GUIDE.md correctly.
        # But we pass the path just in case.
        # CoursePlugin defaults to "../STUDY_GUIDE.md" which is correct if CoursePlugin is in demo_agent/

        plugin = CoursePlugin()

        # Test 1: Check if lessons were loaded
        print(f"Loaded {len(plugin.lessons)} lessons.")
        if len(plugin.lessons) > 0:
            print(f"First lesson title: {plugin.titles.get(1, 'Unknown')}")
        else:
            print("ERROR: No lessons loaded.")
            return

        # Test 2: Search for 'RAG'
        print("\nSearching for 'RAG'...")
        results = plugin.search_content("RAG")
        print(results)

        # Test 3: Get content of lesson 5 (Agentic RAG)
        print("\nGetting content of Lesson 5...")
        content = plugin.get_lesson_content(5)
        print(content[:200] + "...")  # Print first 200 chars

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
