import asyncio
import os
import sys

# Add the current directory to sys.path to import the plugin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from course_plugin import CoursePlugin
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Add the plugin
    # Note: add_plugin signature might vary, in 1.x it's often add_plugin(plugin, plugin_name)
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    # Configure the chat service
    service_id = "chat"

    # Check for Azure OpenAI first
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI Service")
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4"),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            )
        )
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI Service")
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id="gpt-4", # Default model
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        )
    elif os.getenv("GITHUB_TOKEN"):
         print("Using GitHub Models (via OpenAI Protocol)")

         from openai import AsyncOpenAI

         # GitHub Models endpoint
         client = AsyncOpenAI(
             base_url="https://models.inference.ai.azure.com",
             api_key=os.getenv("GITHUB_TOKEN"),
         )

         kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id="gpt-4o",
                async_client=client
            )
         )

    else:
        print("WARNING: No API keys found (OPENAI_API_KEY, AZURE_OPENAI_API_KEY, or GITHUB_TOKEN).")
        print("Entering search-only mode. You can search the study guide directly.")
        print("To search, type: search <query>")
        print("To read a lesson, type: lesson <number>")

        plugin = CoursePlugin()
        while True:
            try:
                if sys.stdin.isatty():
                    user_input = input("User: ")
                else:
                    # Handle non-interactive input (e.g. piped)
                    user_input = sys.stdin.readline().strip()
                    if not user_input:
                        break
            except EOFError:
                break

            if user_input.lower() in ["exit", "quit"]:
                break

            if user_input.startswith("search "):
                query = user_input[7:]
                print(f"Agent: {plugin.search_content(query)}")
            elif user_input.startswith("lesson "):
                try:
                    num = int(user_input[7:])
                    print(f"Agent: {plugin.get_lesson_content(num)}")
                except ValueError:
                    print("Agent: Invalid lesson number.")
            else:
                print("Agent: I can only search or read lessons in this mode. Try 'search <query>' or 'lesson <number>'.")
        return

    # Create a chat history
    history = ChatHistory()
    history.add_system_message("You are a helpful AI assistant for the 'AI Agents for Beginners' course. Use the CoursePlugin to answer questions about the course content.")

    print("Agent: Hello! I am your course assistant. Ask me anything about the AI Agents course.")

    # Start the chat loop
    from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

    while True:
        try:
            if sys.stdin.isatty():
                user_input = input("User: ")
            else:
                user_input = sys.stdin.readline().strip()
                if not user_input:
                    break
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        history.add_user_message(user_input)

        try:
            chat_completion = kernel.get_service(service_id=service_id)

            # Configure function calling
            settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
            settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

            result = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=settings,
                kernel=kernel
            )

            print(f"Agent: {result.content}")
            history.add_message(result)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
