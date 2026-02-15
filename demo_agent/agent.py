import os
import asyncio
import sys
import re
from dotenv import load_dotenv, find_dotenv

# Add parent dir to path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from course_plugin import CoursePlugin

# Semantic Kernel imports
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory

# Load env vars
load_dotenv(find_dotenv())

async def main():
    print("Initializing AI Agent...")

    # Check for API Keys
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    kernel = Kernel()

    # Add the Course Plugin
    # In SK 1.x add_plugin takes the plugin instance and a name
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    service_id = "default"
    service = None

    if azure_key and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI...")
        service = AzureChatCompletion(
            service_id=service_id,
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=azure_key,
        )
    elif openai_key:
        print("Using OpenAI...")
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("OPENAI_MODEL", "gpt-4"),
            api_key=openai_key,
        )

    if service:
        kernel.add_service(service)
    else:
        print("\nWARNING: No API keys found (AZURE_OPENAI_API_KEY or OPENAI_API_KEY).")
        print("Entering limited 'Keyword Search' mode.")
        print("You can search for topics or ask for specific lessons.")
        await run_fallback_mode()
        return

    # Create chat history
    history = ChatHistory()
    history.add_system_message("You are a helpful AI assistant for the 'AI Agents for Beginners' course. Use the CoursePlugin to answer questions.")

    # Enable auto function calling
    settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    print("\nAI Agent ready! (Type 'exit' to quit)")

    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input.strip():
            continue

        history.add_user_message(user_input)

        # Get response using the chat completion service directly
        chat_completion = kernel.get_service(service_id)

        try:
            # get_chat_message_content is the standard method in SK 1.x
            result = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=settings,
                kernel=kernel
            )

            print(f"Agent: {result.content}")
            history.add_message(result)

        except Exception as e:
            print(f"Error: {e}")

async def run_fallback_mode():
    """
    Simple fallback mode that uses the plugin directly without an LLM.
    """
    plugin = CoursePlugin()

    while True:
        try:
            user_input = input("\nSearch (or 'exit'): ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input.strip():
            continue

        # Check if user wants a specific lesson
        lesson_match = re.search(r"lesson\s*(\d+)", user_input.lower())
        if lesson_match:
            lesson_num = int(lesson_match.group(1))
            print(f"--- Lesson {lesson_num} ---")
            print(plugin.get_lesson_content(lesson_num))
        else:
            print(f"--- Searching for '{user_input}' ---")
            print(plugin.search_content(user_input))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
