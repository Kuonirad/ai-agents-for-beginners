import os
import sys
import asyncio
from dotenv import load_dotenv, find_dotenv

# Ensure we can import from the current directory if run as module
sys.path.append(os.path.dirname(__file__))

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory

# Add specific imports based on environment
from course_plugin import CoursePlugin

async def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Create kernel
    kernel = Kernel()

    # Add the CoursePlugin
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    # Configure the Chat Completion Service
    service_id = "default"

    if os.getenv("AZURE_OPENAI_API_KEY"):
        from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
        # Using Pydantic settings matching the latest Semantic Kernel
        # Requires AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
        chat_service = AzureChatCompletion(service_id=service_id)
    elif os.getenv("GITHUB_TOKEN"):
        from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
        from openai import AsyncOpenAI
        # Using GitHub Models
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )
        chat_service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("GITHUB_MODEL_ID", "gpt-4o"),
            async_client=client
        )
    elif os.getenv("OPENAI_API_KEY"):
        from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
        chat_service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o")
        )
    else:
        print("Please configure your .env file with API credentials.")
        return

    kernel.add_service(chat_service)

    # Configure prompt execution settings
    execution_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are an AI assistant that answers questions about the 'AI Agents for Beginners' course. "
        "Use the CoursePlugin to search for content or get specific lesson content. "
        "Always be helpful and try to base your answers on the course content."
    )

    print("Agent is ready! (Type 'quit' or 'exit' to exit)")
    print("-" * 50)

    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            print("Exiting...")
            break

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        chat_history.add_user_message(user_input)

        try:
            # We use get_chat_message_content with FunctionChoiceBehavior.Auto
            response = await chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )
            print(f"Agent: {response}")
            chat_history.add_message(response)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
