import asyncio
import os
import sys

# Ensure demo_agent module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv, find_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
)
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from openai import AsyncOpenAI

from demo_agent.course_plugin import CoursePlugin

async def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize the Semantic Kernel
    kernel = sk.Kernel()

    # Configure Chat Completion Service
    service_id = "default"

    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI")
        service = AzureChatCompletion(
            service_id=service_id,
            deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        kernel.add_service(service)
    elif os.getenv("GITHUB_TOKEN"):
        print("Using GitHub Models")
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("GITHUB_MODEL_NAME", "gpt-4o"),
            async_client=client,
        )
        kernel.add_service(service)
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI")
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        kernel.add_service(service)
    else:
        print("Error: No valid API key found. Please set AZURE_OPENAI_API_KEY, GITHUB_TOKEN, or OPENAI_API_KEY.")
        return

    # Add the CoursePlugin to the Kernel
    plugin = CoursePlugin()
    kernel.add_plugin(plugin, plugin_name="CoursePlugin")

    # Set up Chat History
    chat_history = ChatHistory()
    chat_history.add_system_message("You are an AI assistant that helps students learn about AI Agents using the 'AI Agents for Beginners' course materials. Use the CoursePlugin to search for content and retrieve lesson details.")

    # Enable auto function calling (Tool Use Design Pattern)
    settings = kernel.get_service(service_id).instantiate_prompt_execution_settings(
        service_id=service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    print("\n🎓 AI Agents Course Assistant Initialized.")
    print("Ask me anything about the course! (Type 'exit' or 'quit' to stop)\n")

    # Interactive Chat Loop
    while True:
        try:
            user_input = input("User > ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if not user_input.strip():
                continue

            # Add user message to history
            chat_history.add_user_message(user_input)

            # Get response from the model
            result = await kernel.get_service(service_id).get_chat_message_content(
                chat_history=chat_history,
                settings=settings,
                kernel=kernel
            )

            # Add assistant message to history
            chat_history.add_assistant_message(str(result))

            print(f"Assistant > {result}\n")

        except EOFError:
            print("\nEOF received. Exiting.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
