#!/usr/bin/env python3
import asyncio
import os
import sys

# Add the current directory to sys.path to ensure course_plugin can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv, find_dotenv
    from openai import AsyncOpenAI
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
    from semantic_kernel.contents import ChatHistory
    from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
    from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import OpenAIChatPromptExecutionSettings

    from course_plugin import CoursePlugin
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Please install requirements using: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables
load_dotenv(find_dotenv())

async def main():
    print("--- AI Agents for Beginners - Course Assistant ---")

    # 1. Initialize Kernel
    kernel = Kernel()

    # 2. Add Plugins
    # Initialize our custom plugin
    course_plugin = CoursePlugin()
    if not course_plugin.lessons:
        print("Error: Could not load course content. Check if STUDY_GUIDE.md exists.")
        return

    kernel.add_plugin(course_plugin, plugin_name="CoursePlugin")

    # 3. Configure AI Service
    # Prioritize Azure OpenAI if keys exist, otherwise standard OpenAI/GitHub Models
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    service_id = "default"

    if endpoint and api_key and deployment_name:
        print(f"Using Azure OpenAI Service: {deployment_name}")
        service = AzureChatCompletion(
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            service_id=service_id
        )
    else:
        # Fallback to OpenAI / GitHub Models
        api_key = os.getenv("GITHUB_TOKEN") or os.getenv("OPENAI_API_KEY")
        model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4o") # Default to gpt-4o

        if not api_key:
            print("\n[WARNING] No API Key found.")
            print("Please set GITHUB_TOKEN (for GitHub Models) or OPENAI_API_KEY (for OpenAI) in .env file.")
            print("You can get a free token from https://github.com/marketplace/models")
            print("Exiting...")
            return

        print(f"Using OpenAI/GitHub Models: {model_id}")

        # Initialize the AsyncOpenAI client explicitly to handle custom endpoints if needed (like GitHub Models)
        # GitHub models endpoint: https://models.inference.ai.azure.com/
        base_url = os.getenv("OPENAI_BASE_URL", "https://models.inference.ai.azure.com/")

        client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        service = OpenAIChatCompletion(
            ai_model_id=model_id,
            async_client=client,
            service_id=service_id
        )

    kernel.add_service(service)

    # 4. Create Chat History and Settings
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a helpful teaching assistant for the 'AI Agents for Beginners' course. "
        "Your goal is to help students understand the course material. "
        "You have access to the full 'Study Guide' via the CoursePlugin. "
        "ALWAYS use the CoursePlugin to search for information before answering questions about the course. "
        "If you don't find the answer in the study guide, admit it gracefully."
    )

    # Enable auto function calling
    execution_settings = OpenAIChatPromptExecutionSettings(
        service_id=service_id,
        function_choice_behavior=FunctionChoiceBehavior.Auto()
    )

    print("\nAssistant ready! (Type 'exit' to quit)")
    print("Example: 'What are the design patterns for agents?' or 'Tell me about Lesson 5'")

    # 5. Chat Loop
    while True:
        try:
            user_input = input("\nYou: ")
        except EOFError:
            break

        if not user_input or user_input.lower() in ["exit", "quit"]:
            break

        chat_history.add_user_message(user_input)

        try:
            # Get response from the agent
            response = await service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=kernel
            )

            print(f"Agent: {response.content}")
            chat_history.add_message(response)

        except Exception as e:
            print(f"Error occurred: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
