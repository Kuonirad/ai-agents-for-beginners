import asyncio
import os
import logging
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Semantic Kernel imports
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

# Import the plugin
try:
    from course_plugin import CoursePlugin
except ImportError:
    import sys
    sys.path.append(os.path.dirname(__file__))
    from course_plugin import CoursePlugin

async def main():
    # Configure Logging (optional, set to INFO/DEBUG to see tool calls)
    logging.basicConfig(level=logging.CRITICAL)

    # Initialize Kernel
    kernel = Kernel()

    # Configure AI Service
    service_id = "agent"

    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    service = None

    if azure_key:
        print("Using Azure OpenAI Service...")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        service = AzureChatCompletion(
            service_id=service_id,
            deployment_name=deployment,
            endpoint=endpoint,
            api_key=azure_key,
        )
    elif openai_key:
        print("Using OpenAI Service...")
        model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4")
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=model_id,
            api_key=openai_key,
        )
    elif github_token:
        print("Using GitHub Models...")
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=github_token,
            base_url="https://models.inference.ai.azure.com/"
        )
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("OPENAI_MODEL_ID", "gpt-4o"),
            async_client=client
        )
    else:
        print("Error: No API key found. Please set AZURE_OPENAI_API_KEY, OPENAI_API_KEY, or GITHUB_TOKEN.")
        # For demo purposes, we might want to allow running without keys just to show the loop?
        # But we can't do inference.
        # Fallback to manual mode or mock? No, let's just return.

        # Actually, let's create a mock service if no keys, so I can at least test the loop logic in my test script?
        # No, better to fail fast.
        return

    kernel.add_service(service)

    # Add Plugin
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    # Enable auto tool calling
    settings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create Chat History
    history = ChatHistory()
    history.add_system_message("""You are a helpful assistant for the 'AI Agents for Beginners' course.
You have access to the full study guide via the CoursePlugin.
Always check the study guide content using `get_lesson_content` or `search_content` before answering questions about specific lessons or concepts.
If the user asks "What is lesson X?", use `get_lesson_content(X)`.
If the user asks about a concept, use `search_content`.
Answer concisely and helpfully.""")

    print("\n--- AI Agents Course Assistant ---")
    print("Ask a question about the course (or type 'exit' to quit).")

    while True:
        try:
            user_input = input("\nUser: ")
        except EOFError:
            break

        if not user_input or user_input.lower() in ["exit", "quit"]:
            break

        history.add_user_message(user_input)
        print("Assistant: ", end="", flush=True)

        try:
            # Get response
            result = await service.get_chat_message_content(
                chat_history=history,
                settings=settings,
                kernel=kernel
            )

            print(result.content)
            history.add_message(result)

        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main())
