import asyncio
import os
import sys

# Add parent directory to sys.path to ensure correct imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv, find_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings, OpenAIChatPromptExecutionSettings

from demo_agent.course_plugin import CoursePlugin

async def main():
    load_dotenv(find_dotenv())

    kernel = Kernel()

    # Add the CoursePlugin
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    service_id = "default"
    service = None
    settings = None

    # 1. Check for Azure OpenAI
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI Service...")
        service = AzureChatCompletion(
            service_id=service_id,
            deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        settings = AzureChatPromptExecutionSettings(service_id=service_id)

    # 2. Check for GitHub Models (Free Tier)
    elif os.getenv("GITHUB_TOKEN") and os.getenv("OPENAI_MODEL_NAME"):
        print("Using GitHub Models...")
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN")
        )
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("OPENAI_MODEL_NAME"),
            async_client=client
        )
        settings = OpenAIChatPromptExecutionSettings(service_id=service_id)

    # 3. Check for Standard OpenAI
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI Service...")
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        settings = OpenAIChatPromptExecutionSettings(service_id=service_id)

    else:
        print("Error: No valid API configuration found.")
        print("Please set AZURE_OPENAI_API_KEY, GITHUB_TOKEN, or OPENAI_API_KEY in .env file.")
        return

    kernel.add_service(service)

    # Enable auto function calling
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    history = ChatHistory()
    history.add_system_message("You are a helpful assistant for the 'AI Agents for Beginners' course. You answer questions about the course content using the provided tools. Always cite the lesson number when answering.")

    print("Agent is ready! (Type 'exit' to quit)")

    while True:
        try:
            user_input = input("User > ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        history.add_user_message(user_input)

        try:
            # Get the chat completion service
            chat_completion = kernel.get_service(service_id)

            # Get the response
            result = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=settings,
                kernel=kernel
            )

            print(f"Agent > {result}")
            history.add_message(result)

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
