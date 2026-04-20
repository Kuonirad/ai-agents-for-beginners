import asyncio
import os
import sys
from dotenv import load_dotenv, find_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory

# Add parent directory to path to allow importing the plugin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

async def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize the Kernel
    kernel = Kernel()

    # Configure the chat completion service based on available environment variables
    if os.getenv("GITHUB_TOKEN") and os.getenv("GITHUB_MODEL_ID"):
        from openai import AsyncOpenAI
        # Using GitHub Models
        print("Using GitHub Models configuration...")
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("GITHUB_MODEL_ID"),
            async_client=client,
        )
    elif os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"):
        # Using Azure OpenAI
        print("Using Azure OpenAI configuration...")
        chat_service = AzureChatCompletion()
    elif os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_CHAT_MODEL_ID"):
        # Using OpenAI
        print("Using OpenAI configuration...")
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("OPENAI_CHAT_MODEL_ID"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    else:
        print("❌ Error: No valid AI service configuration found in environment variables.")
        print("Please set GITHUB_TOKEN/GITHUB_MODEL_ID, AZURE_OPENAI_* or OPENAI_* variables.")
        return

    kernel.add_service(chat_service)

    # Add the course plugin
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    # Setup chat history
    chat_history = ChatHistory()
    chat_history.add_system_message("You are a helpful teaching assistant for the 'AI Agents for Beginners' course. Use your CoursePlugin tools to look up information from the study guide to answer the user's questions.")

    # Configure tool use behavior
    req_settings = kernel.get_prompt_execution_settings_from_service_id(chat_service.service_id)
    req_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    print("\n" + "="*50)
    print("🤖 AI Agents Course Assistant Initialized!")
    print("Ask me anything about the course, or type 'exit' to quit.")
    print("="*50 + "\n")

    # Chat loop
    while True:
        try:
            user_input = input("User > ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break

            if not user_input.strip():
                continue

            chat_history.add_user_message(user_input)

            # Get response using get_chat_message_content to handle tool calls
            result = await chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=req_settings,
                kernel=kernel
            )

            print(f"Assistant > {result}\n")
            chat_history.add_assistant_message(str(result))

        except EOFError:
            # Handle EOF gracefully (e.g., in automated environments)
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())