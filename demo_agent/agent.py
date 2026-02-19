import asyncio
import os
import sys

# Ensure we can import modules from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
from openai import AsyncOpenAI

from course_plugin import CoursePlugin

async def main():
    load_dotenv()

    kernel = Kernel()

    # Configure AI Service
    service_id = "default"

    # Check for Azure OpenAI
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI...")
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            )
        )
    # Check for GitHub Models (using OpenAI interface with custom endpoint)
    elif os.getenv("GITHUB_TOKEN") and os.getenv("GITHUB_MODEL_NAME"):
        print("Using GitHub Models...")
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN")
        )
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=os.getenv("GITHUB_MODEL_NAME", "gpt-4o"),
                async_client=client
            )
        )
    # Check for OpenAI (Standard)
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI...")
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=os.getenv("OPENAI_MODEL_ID", "gpt-4"),
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        )

    # Register the Course Plugin
    course_plugin = CoursePlugin()
    kernel.add_plugin(course_plugin, plugin_name="Course")

    print("\n--- AI Agents Course Assistant ---")

    # Fallback to manual mode if no LLM
    if not kernel.services:
        print("No AI service configured (Azure OpenAI / OpenAI / GitHub Models).")
        print("Falling back to keyword search mode.")
        print("Enter a keyword to search the study guide (or 'exit' to quit).")

        while True:
            try:
                user_input = input("Search: ")
            except EOFError:
                break

            if user_input.lower() in ["exit", "quit"]:
                break

            result = course_plugin.search_content(user_input)
            print(f"Result:\n{result}\n")
        return

    # Chat Mode
    chat_completion = kernel.get_service(service_id=service_id)
    history = ChatHistory()
    history.add_system_message("You are a helpful AI assistant for the 'AI Agents for Beginners' course. You answer questions using the Course plugin.")

    # Enable automatic function calling
    # Assuming the service supports function calling (which OpenAI/Azure/GitHub Models do)
    execution_settings = chat_completion.instantiate_prompt_execution_settings(
        service_id=service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    print("Ask a question about the course (or type 'exit' to quit).")

    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        history.add_user_message(user_input)

        try:
            # Get the response from the AI
            result = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel
            )

            print(f"Agent: {result}")
            history.add_message(result)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
