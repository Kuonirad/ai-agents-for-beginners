import os
import sys
import asyncio
from dotenv import load_dotenv, find_dotenv

# Add parent directory to path so we can import things if needed,
# though for this script we just need local imports.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings, OpenAIChatPromptExecutionSettings

# Import the plugin from the local directory
# We need to ensure python can find it if we run from root or demo_agent dir
try:
    from course_plugin import CoursePlugin
except ImportError:
    # If running from root, maybe need to adjust path or run as module
    sys.path.append(os.path.join(os.getcwd(), 'demo_agent'))
    from course_plugin import CoursePlugin

async def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize Kernel
    kernel = Kernel()

    # Configure AI Service
    service_id = "chat"

    # Check for Azure OpenAI first
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI...")
        deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or "gpt-4o"
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=deployment_name,
                endpoint=endpoint,
                api_key=api_key,
            )
        )
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI...")
        model_id = os.getenv("OPENAI_MODEL") or "gpt-4o"
        api_key = os.getenv("OPENAI_API_KEY")

        # Check for GitHub Models (which use a specific base_url often)
        # But for simplicity, we assume standard OpenAI usage unless specified
        # If using GitHub models via OpenAI client, base_url might be needed.
        # We will trust the environment variables or default behavior.

        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=model_id,
                api_key=api_key,
            )
        )
    else:
        print("Error: neither AZURE_OPENAI_API_KEY nor OPENAI_API_KEY found in environment.")
        print("Please set up your .env file.")
        return

    # Add Plugin
    # Initialize the plugin (it will load the study guide)
    try:
        course_plugin = CoursePlugin()
        kernel.add_plugin(course_plugin, plugin_name="CoursePlugin")
    except Exception as e:
        print(f"Failed to initialize CoursePlugin: {e}")
        return

    # Chat Loop
    history = ChatHistory()
    history.add_system_message("You are a helpful AI assistant for the 'AI Agents for Beginners' course. You answer questions about the course content using the provided CoursePlugin.")

    try:
        chat_completion_service = kernel.get_service(service_id=service_id)
    except Exception as e:
         print(f"Failed to get chat completion service: {e}")
         return

    # Configure execution settings for tool calling
    # Determine which settings class to use based on the service
    if isinstance(chat_completion_service, AzureChatCompletion):
        settings = AzureChatPromptExecutionSettings(service_id=service_id)
    else:
        settings = OpenAIChatPromptExecutionSettings(service_id=service_id)

    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    print("--- AI Agents Course Assistant ---")
    print("Ask me anything about the course! (Type 'exit' to quit)")

    while True:
        try:
            # Check for EOF to support piped input
            try:
                user_input = input("User: ")
            except EOFError:
                break

            if user_input.lower() in ["exit", "quit"]:
                break

            # Print user input for log visibility when running non-interactively
            print(f"Processing: {user_input}")

            history.add_user_message(user_input)

            result = await chat_completion_service.get_chat_message_content(
                chat_history=history,
                settings=settings,
                kernel=kernel,
            )

            print(f"Assistant: {result}")
            history.add_message(result)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error processing request: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())
