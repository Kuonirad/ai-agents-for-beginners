import asyncio
import os
import sys

# Ensure demo_agent is in path so we can import course_plugin
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Workaround for import issues if running from root
try:
    from course_plugin import CoursePlugin
except ImportError:
    try:
        from demo_agent.course_plugin import CoursePlugin
    except ImportError:
        # If running as a module, imports might be relative
        from .course_plugin import CoursePlugin


from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import OpenAIChatPromptExecutionSettings

# Try to load env
try:
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
except ImportError:
    pass

async def main():
    print("--- Course Assistant Agent ---")

    # 1. Initialize Kernel
    kernel = Kernel()

    # 2. Add Plugin
    course_plugin = CoursePlugin("STUDY_GUIDE.md")

    # Check if content loaded
    if not course_plugin.content:
        print("Warning: Course content not loaded. Check STUDY_GUIDE.md path.")
    else:
        print(f"Loaded {len(course_plugin.content)} lessons.")

    kernel.add_plugin(course_plugin, plugin_name="CoursePlugin")

    # 3. Configure AI Service
    api_key = os.getenv("GITHUB_TOKEN") or os.getenv("OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://models.inference.ai.azure.com/")
    model_id = "gpt-4o"

    if not api_key:
        print("Error: OPENAI_API_KEY or GITHUB_TOKEN not found.")
        return

    try:
        service = OpenAIChatCompletion(
            ai_model_id=model_id,
            api_key=api_key,
            base_url=endpoint
        )
        kernel.add_service(service)
    except Exception as e:
        print(f"Failed to initialize AI Service: {e}")
        return

    # 4. Chat Setup
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a helpful AI assistant for the 'AI Agents for Beginners' course. "
        "You can answer questions about the course content, list lessons, and search for specific topics. "
        "Use the CoursePlugin tools to get accurate information."
    )

    execution_settings = OpenAIChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    # 5. Interaction Loop
    # Detect non-interactive mode (piped input)
    if not sys.stdin.isatty():
        user_input = sys.stdin.read().strip()
        if user_input:
            print(f"User: {user_input}")
            chat_history.add_user_message(user_input)
            try:
                response = await service.get_chat_message_content(
                    chat_history=chat_history,
                    settings=execution_settings,
                    kernel=kernel
                )
                print(f"Agent: {response.content}")
            except Exception as e:
                print(f"Error: {e}")
        return

    print("Agent is ready. Ask me anything about the course! (Type 'exit' to quit)")

    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break

        if not user_input or user_input.lower() in ["exit", "quit"]:
            break

        chat_history.add_user_message(user_input)

        try:
            response = await service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )
            print(f"Agent: {response.content}")
            chat_history.add_message(response)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
