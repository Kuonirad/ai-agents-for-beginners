import asyncio
import os
import sys
from dotenv import load_dotenv, find_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory

# Ensure local imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from demo_agent.course_plugin import CoursePlugin

async def main():
    load_dotenv(find_dotenv())

    kernel = Kernel()

    # Configure the AI Service
    if os.getenv("AZURE_OPENAI_API_KEY"):
        # Azure OpenAI Configuration
        print("Using Azure OpenAI...")
        chat_service = AzureChatCompletion()
    elif os.getenv("GITHUB_TOKEN"):
        # GitHub Models Configuration
        print("Using GitHub Models...")
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("GITHUB_MODEL_ID", "gpt-4o"),
            async_client=client,
        )
    elif os.getenv("OPENAI_API_KEY"):
        # standard OpenAI Configuration
        print("Using OpenAI...")
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o"),
        )
    else:
        print("Error: No valid API credentials found. Please set AZURE_OPENAI_API_KEY, GITHUB_TOKEN, or OPENAI_API_KEY in your .env file.")
        sys.exit(1)

    kernel.add_service(chat_service)

    # Add the plugin
    course_plugin = CoursePlugin()
    kernel.add_plugin(course_plugin, plugin_name="CoursePlugin")

    # Set up chat execution settings with auto function calling
    req_settings = kernel.get_prompt_execution_settings_from_service_id(chat_service.service_id)
    req_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Initialize chat history
    history = ChatHistory()
    system_message = (
        "You are a helpful AI Agent designed to answer questions about the 'AI Agents for Beginners' course. "
        "You must use the 'CoursePlugin' to retrieve accurate information from the course materials. "
        "If you don't know the answer, use the search_content function. If asked about a specific lesson, use get_lesson_content."
    )
    history.add_system_message(system_message)

    print("\n" + "="*50)
    print("Welcome to the AI Agents Course Assistant!")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("You: > ")
            if not user_input or user_input.strip().lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            history.add_user_message(user_input)

            # Process the response using get_chat_message_content to handle tool calls automatically
            response = await chat_service.get_chat_message_content(
                chat_history=history,
                settings=req_settings,
                kernel=kernel
            )

            history.add_assistant_message(str(response))
            print(f"Agent: > {response}\n")

        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
