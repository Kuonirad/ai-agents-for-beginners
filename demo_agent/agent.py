import asyncio
import os
import sys

# Add the current directory to sys.path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv, find_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory

from course_plugin import CoursePlugin

async def main():
    load_dotenv(find_dotenv())

    kernel = Kernel()

    service_id = "default"

    # Check for Azure OpenAI first
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI...")
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4"),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            )
        )
    # Check for OpenAI
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI...")
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        )
    else:
        print("Error: No API keys found. Please set AZURE_OPENAI_API_KEY or OPENAI_API_KEY in .env")
        # Start a limited mode or just exit?
        # For now, exit, as the agent requires an LLM.
        return

    # Add the plugin
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    # Get the service to configure settings
    chat_completion_service = kernel.get_service(service_id)

    # Enable automatic function calling
    execution_settings = chat_completion_service.instantiate_prompt_execution_settings(
        service_id=service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    chat_history = ChatHistory()
    chat_history.add_system_message("You are a helpful assistant for the 'AI Agents for Beginners' course. You answer questions using the study guide provided via plugins.")

    print("--- AI Agents Course Assistant ---")
    print("Ask a question about the course (or type 'exit' to quit).")

    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        chat_history.add_user_message(user_input)

        try:
            # Get the response from the AI
            result = await chat_completion_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )

            print(f"Assistant: {result}")
            chat_history.add_message(result)

        except Exception as e:
            print(f"Error during interaction: {e}")

if __name__ == "__main__":
    asyncio.run(main())
