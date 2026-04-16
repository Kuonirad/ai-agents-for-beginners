import asyncio
import os
import sys
import logging
from dotenv import load_dotenv, find_dotenv

# Add parent directory to path so we can import as a module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_agent.course_plugin import CoursePlugin

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
from openai import AsyncOpenAI

logging.basicConfig(level=logging.WARNING)

async def main():
    load_dotenv(find_dotenv())

    kernel = Kernel()

    # Configure the chat completion service based on available environment variables
    if os.getenv("AZURE_OPENAI_API_KEY"):
        # Relies on AZURE_OPENAI_CHAT_DEPLOYMENT_NAME and other Pydantic settings
        chat_service = AzureChatCompletion()
    elif os.getenv("OPENAI_API_KEY"):
        chat_service = OpenAIChatCompletion(ai_model_id=os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o"))
    elif os.getenv("GITHUB_TOKEN"):
        # Use GitHub Models
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("GITHUB_MODEL_ID", "gpt-4o"),
            async_client=client,
        )
    else:
        print("Error: No valid API key found. Please set AZURE_OPENAI_API_KEY, OPENAI_API_KEY, or GITHUB_TOKEN.")
        sys.exit(1)

    kernel.add_service(chat_service)
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a helpful AI assistant specialized in answering questions about the "
        "'AI Agents for Beginners' course. Use your CoursePlugin to lookup information "
        "from the study guide. Be concise and educational."
    )

    # Note: FunctionChoiceBehavior needs to be used in execution settings or when getting message content
    print("\n" + "="*50)
    print("Welcome to the AI Agents Course Assistant!")
    print("Ask me anything about the course, or type 'exit' to quit.")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break

            chat_history.add_user_message(user_input)

            # get_chat_message_content manages tool calls and history updates
            response = await chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=chat_service.instantiate_prompt_execution_settings(
                    service_id=chat_service.service_id,
                    function_choice_behavior=FunctionChoiceBehavior.Auto()
                ),
                kernel=kernel
            )

            print(f"\nAssistant: {response}\n")
            chat_history.add_assistant_message(str(response))

        except EOFError:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(main())
