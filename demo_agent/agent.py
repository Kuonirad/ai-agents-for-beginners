import os
import sys
import asyncio
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
from demo_agent.course_plugin import CoursePlugin
from openai import AsyncOpenAI

async def main():
    load_dotenv(find_dotenv())

    kernel = Kernel()

    # Determine which service to use based on environment variables
    if os.getenv("AZURE_OPENAI_API_KEY"):
        print("Using Azure OpenAI...")
        chat_service = AzureChatCompletion()
        kernel.add_service(chat_service)
    elif os.getenv("GITHUB_TOKEN"):
        print("Using GitHub Models...")
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN")
        )
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("GITHUB_MODEL_ID", "gpt-4o"),
            async_client=client
        )
        kernel.add_service(chat_service)
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI...")
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o")
        )
        kernel.add_service(chat_service)
    else:
        print("Error: No AI service credentials found in environment variables.")
        print("Please set AZURE_OPENAI_API_KEY, GITHUB_TOKEN, or OPENAI_API_KEY.")
        sys.exit(1)

    # Add the plugin
    plugin = CoursePlugin()
    kernel.add_plugin(plugin, plugin_name="CoursePlugin")

    history = ChatHistory()
    history.add_system_message(
        "You are a helpful AI assistant that answers questions about the "
        "'AI Agents for Beginners' course. Use the CoursePlugin to search and "
        "retrieve information from the course materials."
    )

    execution_settings = chat_service.instantiate_prompt_execution_settings(
        service_id=chat_service.service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    print("\nAgent initialized. Type 'exit' or 'quit' to stop.")
    while True:
        try:
            user_input = input("User > ")
        except EOFError:
            break
        except KeyboardInterrupt:
            print()
            break

        if user_input.lower() in ['exit', 'quit']:
            break

        history.add_user_message(user_input)

        try:
            result = await chat_service.get_chat_message_content(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel
            )
            print(f"Agent > {result}")
            history.add_message(result)
        except Exception as e:
            print(f"Error calling AI service: {e}")

if __name__ == "__main__":
    asyncio.run(main())
