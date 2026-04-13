import asyncio
import os
import sys

# Ensure demo_agent is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv, find_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory

# Import our custom plugin
from demo_agent.course_plugin import CoursePlugin

async def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize the Kernel
    kernel = sk.Kernel()

    # Configure the Chat Completion Service based on available environment variables
    if os.getenv("AZURE_OPENAI_API_KEY"):
        print("Using Azure OpenAI...")
        # AzureChatCompletion uses Pydantic settings that look for AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
        chat_service = AzureChatCompletion()
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI...")
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o")
        )
    elif os.getenv("GITHUB_TOKEN"):
        print("Using GitHub Models...")
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN")
        )
        chat_service = OpenAIChatCompletion(
            ai_model_id=os.getenv("GITHUB_MODEL_ID", "gpt-4o"),
            async_client=client
        )
    else:
        print("Error: No valid API key found. Please set AZURE_OPENAI_API_KEY, OPENAI_API_KEY, or GITHUB_TOKEN.")
        sys.exit(1)

    kernel.add_service(chat_service)

    # Add the CoursePlugin to the kernel
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    # Create chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a helpful AI assistant for the 'AI Agents for Beginners' course. "
        "Use the CoursePlugin to answer questions about the course content, search for topics, "
        "and summarize lessons. Always base your answers on the provided course material."
    )

    # Enable automatic function calling
    execution_settings = chat_service.instantiate_prompt_execution_settings(
        service_id=chat_service.service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    print("\n--- Course Assistant Agent Initialized ---")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ['exit', 'quit']:
                break

            chat_history.add_user_message(user_input)

            # Get the response from the LLM, allowing it to use tools
            response = await chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )

            print(f"Agent: {response.content}\n")
            chat_history.add_assistant_message(response.content)

        except EOFError:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
