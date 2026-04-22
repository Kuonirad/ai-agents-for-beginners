import os
import sys
import asyncio
from dotenv import load_dotenv, find_dotenv

# Ensure we can import from the demo_agent package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory

from demo_agent.course_plugin import CoursePlugin

async def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize the kernel
    kernel = Kernel()

    # Configure the chat service based on environment variables
    chat_service = None

    if os.environ.get("GITHUB_TOKEN") and os.environ.get("GITHUB_MODEL_ID"):
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ.get("GITHUB_TOKEN")
        )
        chat_service = OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=os.environ.get("GITHUB_MODEL_ID"),
            async_client=client
        )
    elif os.environ.get("AZURE_OPENAI_API_KEY") and os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"):
        # Relies on Pydantic settings from environment variables
        chat_service = AzureChatCompletion(service_id="chat")
    elif os.environ.get("OPENAI_API_KEY") and os.environ.get("OPENAI_CHAT_MODEL_ID"):
        chat_service = OpenAIChatCompletion(
            service_id="chat",
            ai_model_id=os.environ.get("OPENAI_CHAT_MODEL_ID")
        )
    else:
        print("Error: No valid API configuration found in environment variables.")
        print("Please configure GITHUB_TOKEN/GITHUB_MODEL_ID, AZURE_OPENAI_*, or OPENAI_API_KEY/OPENAI_CHAT_MODEL_ID.")
        sys.exit(1)

    kernel.add_service(chat_service)

    # Add the CoursePlugin to the kernel
    kernel.add_plugin(CoursePlugin(), plugin_name="course")

    # Initialize chat history
    history = ChatHistory()
    history.add_system_message(
        "You are a helpful AI assistant for the 'AI Agents for Beginners' course. "
        "Use the course plugin to answer questions about the course material. "
        "If you don't know the answer based on the course material, say so."
    )

    # Enable automatic function calling
    execution_settings = chat_service.instantiate_prompt_execution_settings(
        service_id="chat",
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    print("🤖 Course Assistant ready! Type 'exit' or 'quit' to stop.")
    print("-" * 50)

    while True:
        try:
            user_input = input("User > ")
            if user_input.lower() in ["exit", "quit"]:
                break

            history.add_user_message(user_input)

            # Get the response from the model
            result = await chat_service.get_chat_message_content(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel
            )

            print(f"Agent > {result}")
            history.add_assistant_message(str(result))

        except EOFError:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main())