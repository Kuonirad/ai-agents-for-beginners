import asyncio
import os
import sys
from dotenv import load_dotenv, find_dotenv

# Add current directory to path so we can import the plugin
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from course_plugin import CoursePlugin
except ImportError:
    from demo_agent.course_plugin import CoursePlugin

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

# Load environment variables
load_dotenv(find_dotenv())

async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Configure AI Service
    service_id = "default"

    # Check for Azure OpenAI first, then OpenAI
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI...")
        service = AzureChatCompletion(
            service_id=service_id,
            deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI...")
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif os.getenv("GITHUB_TOKEN"):
        print("Using GitHub Models...")
        # GitHub models use OpenAI client but with a specific base URL
        # We need to manually construct the client if arguments aren't passed through
        # But Semantic Kernel OpenAIChatCompletion might not accept base_url directly in all versions
        # Let's try passing it via kwargs or rely on the user having set up environment correctly
        # Ideally we inject the client
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )
        service = OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id=os.getenv("GITHUB_MODEL_NAME", "gpt-4o"),
            async_client=client
        )
    else:
        print("Error: No API keys found. Please set AZURE_OPENAI_API_KEY, OPENAI_API_KEY, or GITHUB_TOKEN in .env file.")
        print("The agent cannot run without an LLM connection.")
        return

    kernel.add_service(service)

    # Register the plugin
    try:
        kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")
    except Exception as e:
        print(f"Failed to register plugin: {e}")
        return

    # Create chat history
    history = ChatHistory()
    history.add_system_message("You are a helpful AI assistant who is an expert on the 'AI Agents for Beginners' course. You use the CoursePlugin to retrieve information from the study guide to answer user questions.")

    # Enable auto function calling
    try:
        execution_settings = service.get_prompt_execution_settings_class()(service_id=service_id)
        execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    except Exception as e:
        print(f"Warning: Could not set function choice behavior: {e}")
        execution_settings = None

    # Interactive loop or Demo mode
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        print("Interactive mode. Type 'exit' to quit.")
        while True:
            try:
                user_input = input("User: ")
            except EOFError:
                break
            if user_input.lower() in ["exit", "quit"]:
                break

            history.add_user_message(user_input)
            try:
                chat_completion = kernel.get_service(service_id)
                result = await chat_completion.get_chat_message_content(
                    chat_history=history,
                    settings=execution_settings,
                    kernel=kernel
                )
                print(f"Agent: {result.content}")
                history.add_message(result)
            except Exception as e:
                print(f"Error: {e}")
    else:
        questions = [
            "What is the 'Maker-Checker loop' in Agentic RAG?",
            "What are the three dimensions of Agentic Design Patterns?",
        ]

        print("Agent initialized. Processing demo questions (pass --interactive to chat)...")

        for question in questions:
            print(f"\nUser: {question}")
            history.add_user_message(question)

            # Get the response
            try:
                 chat_completion = kernel.get_service(service_id)
                 result = await chat_completion.get_chat_message_content(
                     chat_history=history,
                     settings=execution_settings,
                     kernel=kernel
                 )

                 print(f"Agent: {result.content}")
                 history.add_message(result)

            except Exception as e:
                print(f"Error processing request: {e}")

    print("\nDemo completed.")

if __name__ == "__main__":
    asyncio.run(main())
