import asyncio
import logging
import os
import sys

# Add the parent directory to the path so we can run this from anywhere
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv, find_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
    AzureChatPromptExecutionSettings,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory

from demo_agent.course_plugin import CoursePlugin

logging.basicConfig(level=logging.WARNING)

async def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize the kernel
    kernel = Kernel()

    # Check which API key is available and configure accordingly
    if os.getenv("AZURE_OPENAI_API_KEY"):
        print("Using Azure OpenAI...")
        service_id = "default"
        chat_service = AzureChatCompletion(
            service_id=service_id,
        )
        kernel.add_service(chat_service)

        execution_settings = AzureChatPromptExecutionSettings(
            service_id=service_id,
            function_choice_behavior=FunctionChoiceBehavior.Auto()
        )

    elif os.getenv("OPENAI_API_KEY"):
        print("Using standard OpenAI...")
        service_id = "default"
        chat_service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("OPENAI_MODEL_ID", "gpt-4o-mini")
        )
        kernel.add_service(chat_service)

        execution_settings = OpenAIChatPromptExecutionSettings(
            service_id=service_id,
            function_choice_behavior=FunctionChoiceBehavior.Auto()
        )

    elif os.getenv("GITHUB_TOKEN"):
        print("Using GitHub Models...")
        from openai import AsyncOpenAI

        # GitHub Models uses a custom endpoint
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN")
        )

        service_id = "default"
        chat_service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("GITHUB_MODEL_ID", "gpt-4o-mini"),
            async_client=client
        )
        kernel.add_service(chat_service)

        execution_settings = OpenAIChatPromptExecutionSettings(
            service_id=service_id,
            function_choice_behavior=FunctionChoiceBehavior.Auto()
        )

    else:
        print("Error: No API key found. Please set AZURE_OPENAI_API_KEY, OPENAI_API_KEY, or GITHUB_TOKEN in your .env file.")
        sys.exit(1)

    # Add the Course Plugin to the kernel
    print("Loading Course Plugin...")
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    # Initialize chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a helpful AI assistant for the 'AI Agents for Beginners' course. "
        "Use the CoursePlugin to answer questions about the course content. "
        "If the user asks a question, always try to use the search_content or get_lesson_content tools to provide accurate answers based on the STUDY_GUIDE.md."
    )

    print("\n" + "="*50)
    print("Welcome to the AI Agents Course Assistant!")
    print("Ask me anything about the course, or type 'exit' to quit.")
    print("="*50 + "\n")

    # Start the chat loop
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break

            chat_history.add_user_message(user_input)

            # Get the response from the LLM, passing the kernel and execution settings to handle tool calls
            response = await chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )

            # Print the response
            print(f"Assistant: {response}\n")

            # Add the assistant's response to the chat history
            chat_history.add_assistant_message(str(response))

        except EOFError:
            print("\nExiting...")
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
