#!/usr/bin/env python3
import asyncio
import os
import sys

# Add parent directory to path so we can import plugins if needed,
# though here we import from local file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dotenv import load_dotenv, find_dotenv
    from openai import AsyncOpenAI
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
    from semantic_kernel.contents import ChatHistory
    from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
    from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import OpenAIChatPromptExecutionSettings

    # Import our custom plugin
    # If run as script, we can import directly
    try:
        from course_plugin import CoursePlugin
    except ImportError:
        # If run from root, we might need relative import, but sys.path above handles it
        from demo_agent.course_plugin import CoursePlugin

except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Please install requirements using: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables
load_dotenv(find_dotenv())

async def main():
    print("--- AI Agents Course Assistant ---")
    print("I can help you navigate the 'AI Agents for Beginners' course.")
    print("Ask me about specific lessons or topics!")

    # 1. Initialize Kernel
    kernel = Kernel()

    # 2. Add Plugins
    kernel.add_plugin(CoursePlugin(), plugin_name="Course")

    # 3. Configure AI Service
    # Prioritize Azure OpenAI if available, otherwise GitHub Models/OpenAI
    aoai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    aoai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    aoai_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

    github_token = os.getenv("GITHUB_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")

    service_id = "default"

    if aoai_api_key and aoai_endpoint and aoai_deployment:
        print(f"Using Azure OpenAI Service: {aoai_deployment}")
        from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
        service = AzureChatCompletion(
            deployment_name=aoai_deployment,
            endpoint=aoai_endpoint,
            api_key=aoai_api_key,
            service_id=service_id
        )
    elif github_token or openai_key:
        api_key = github_token or openai_key
        # GitHub Models endpoint
        endpoint = "https://models.inference.ai.azure.com/" if github_token else None
        model_id = "gpt-4o" # Default model

        print(f"Using OpenAI/GitHub Models: {model_id}")

        # Initialize client with base_url if provided
        client_args = {"api_key": api_key}
        if endpoint:
            client_args["base_url"] = endpoint

        client = AsyncOpenAI(**client_args)

        service = OpenAIChatCompletion(
            ai_model_id=model_id,
            async_client=client,
            service_id=service_id
        )
    else:
        print("\n[WARNING] No API Key found.")
        print("Please set GITHUB_TOKEN, OPENAI_API_KEY, or Azure OpenAI variables in .env")
        print("I will run in 'search only' mode for demonstration (no LLM).")

        # Simple fallback loop for demonstration without LLM
        plugin = CoursePlugin()
        while True:
            query = input("\nSearch Query (or 'exit'): ")
            if query.lower() in ["exit", "quit"]: break
            print(plugin.search_content(query))
        return

    kernel.add_service(service)

    # 4. Create Chat History
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a helpful assistant for the 'AI Agents for Beginners' course. "
        "You verify your answers by using the 'Course' plugin to search the study guide or read lesson content. "
        "Always cite the lesson number if applicable."
    )

    # 5. Configure Execution Settings
    execution_settings = OpenAIChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
        service_id=service_id
    )

    # 6. Chat Loop
    print("\nReady! (Type 'exit' to quit)")

    while True:
        try:
            user_input = input("\nUser: ")
        except EOFError:
            break

        if not user_input or user_input.lower() in ["exit", "quit"]:
            break

        chat_history.add_user_message(user_input)

        try:
            # Get response
            response = await service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )

            print(f"Assistant: {response.content}")
            chat_history.add_message(response)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
