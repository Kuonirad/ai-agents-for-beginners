import os
import asyncio
import sys
from dotenv import load_dotenv

# Try to import Semantic Kernel components
try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import (
        AzureChatCompletion,
        OpenAIChatCompletion,
        AzureChatPromptExecutionSettings,
        OpenAIChatPromptExecutionSettings
    )
    from semantic_kernel.contents import ChatHistory
    from semantic_kernel.functions import KernelArguments
except ImportError:
    Kernel = None

# Import our plugin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use explicit import from local package if running as script
try:
    from demo_agent.course_plugin import CoursePlugin
except ImportError:
    # Fallback if run directly from within demo_agent/
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from course_plugin import CoursePlugin

async def main():
    load_dotenv()

    # Check for keys
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    use_llm = False
    kernel = None
    chat_service = None
    service_id = "default"

    if (azure_key or openai_key or github_token) and Kernel:
        print("Initializing Semantic Kernel with AI Service...")
        kernel = Kernel()

        if azure_key:
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
            if endpoint and deployment:
                chat_service = AzureChatCompletion(
                    service_id=service_id,
                    deployment_name=deployment,
                    endpoint=endpoint,
                    api_key=azure_key
                )
                kernel.add_service(chat_service)
                use_llm = True
        elif openai_key:
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            chat_service = OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=model,
                api_key=openai_key
            )
            kernel.add_service(chat_service)
            use_llm = True
        elif github_token:
            # GitHub Models support via OpenAIChatCompletion with custom base_url
            model = os.getenv("GITHUB_MODEL_ID", "gpt-4o")
            endpoint = os.getenv("GITHUB_ENDPOINT", "https://models.github.ai/inference")
            chat_service = OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=model,
                api_key=github_token,
                base_url=endpoint
            )
            kernel.add_service(chat_service)
            use_llm = True

        if use_llm:
            # Register the plugin
            plugin = CoursePlugin()
            kernel.add_plugin(plugin, plugin_name="CoursePlugin")
            print("CoursePlugin registered.")

    if not use_llm:
        print("\nNo valid AI service configuration found (or semantic-kernel not installed).")
        print("Entering Keyword Search Mode.")
        print("Type 'Lesson X' to view a lesson, or any keyword to search.")
        print("Type 'exit' or 'quit' to stop.")

        plugin = CoursePlugin()

        while True:
            try:
                user_input = input("\nQuery: ").strip()
            except EOFError:
                break

            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input:
                continue

            # Check for "Lesson X"
            if user_input.lower().startswith("lesson "):
                try:
                    num = int(user_input.split(" ")[1])
                    print(f"\n--- Lesson {num} ---\n")
                    print(plugin.get_lesson_content(num))
                except (ValueError, IndexError):
                    print("Invalid lesson format. Use 'Lesson X'.")
            else:
                # Search
                print(f"\n--- Search Results for '{user_input}' ---\n")
                print(plugin.search_content(user_input))

    else:
        # LLM Mode
        print("\nAI Agent is ready! Ask me anything about the course.")

        history = ChatHistory()
        history.add_system_message("You are a helpful AI assistant for the 'AI Agents for Beginners' course. Use the CoursePlugin to retrieve lesson content and answer questions.")

        # Configure settings for auto function calling
        if azure_key:
            settings = AzureChatPromptExecutionSettings(tool_choice="auto")
        else:
            settings = OpenAIChatPromptExecutionSettings(tool_choice="auto")

        while True:
            try:
                user_input = input("\nUser: ").strip()
            except EOFError:
                break

            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input:
                continue

            history.add_user_message(user_input)

            try:
                result = await chat_service.get_chat_message_content(
                    chat_history=history,
                    settings=settings,
                    kernel=kernel
                )
                print(f"\nAI: {result.content}\n")
                history.add_message(result)
            except Exception as e:
                print(f"Error during AI processing: {e}")

if __name__ == "__main__":
    asyncio.run(main())
