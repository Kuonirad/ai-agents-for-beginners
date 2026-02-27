import asyncio
import os
import sys

# Add the parent directory to sys.path to ensure modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv, find_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory

# Try to import the plugin, handling potential path issues if run as script vs module
try:
    from demo_agent.course_plugin import CoursePlugin
except ImportError:
    # If running from demo_agent directory directly
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from course_plugin import CoursePlugin

async def main():
    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize the kernel
    kernel = Kernel()

    # Configure the AI Service
    service_id = "chat"

    # Check for Azure OpenAI first, then OpenAI/GitHub Models
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("Using Azure OpenAI Service...")
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            )
        )
    elif os.getenv("GITHUB_TOKEN"):
        # GitHub Models uses OpenAI interface with a specific base URL
        print("Using GitHub Models...")
        from openai import AsyncOpenAI

        # We need to manually construct the client for GitHub models to point to the right endpoint
        client = AsyncOpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )

        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=os.getenv("GITHUB_MODEL_NAME", "gpt-4o"),
                async_client=client
            )
        )
    else:
        print("Using OpenAI Service...")
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"),
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        )

    # Register the plugin
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    # Create chat history
    history = ChatHistory()
    history.add_system_message("You are a helpful AI assistant for the 'AI Agents for Beginners' course. "
                               "You can answer questions about the course content by looking up lessons "
                               "in the study guide. Always check the study guide first if you don't know the answer.")

    # Get the service
    chat_service = kernel.get_service(service_id)

    # Enable automatic function calling
    # The new pattern for SK 1.x is to create the execution settings properly
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings, AzureChatPromptExecutionSettings

    if isinstance(chat_service, AzureChatCompletion):
        execution_settings = AzureChatPromptExecutionSettings(service_id=service_id)
    else:
        execution_settings = OpenAIChatPromptExecutionSettings(service_id=service_id)

    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    print("------------------------------------------------------------------")
    print("Welcome to the AI Agents Course Assistant!")
    print("Ask me anything about the course content (or type 'exit' to quit).")
    print("------------------------------------------------------------------")

    while True:
        try:
            user_input = input("User > ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        history.add_user_message(user_input)

        # Get the response from the AI using the service directly to ensure context/history is respected
        try:
            result = await chat_service.get_chat_message_content(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel
            )

            print(f"Assistant > {result}")
            history.add_message(result)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())
