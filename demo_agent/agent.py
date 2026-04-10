import asyncio
import os
import sys
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    OpenAIChatCompletion,
    AzureChatPromptExecutionSettings,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents import ChatHistory
from demo_agent.course_plugin import CoursePlugin

# Load environment variables
load_dotenv(find_dotenv())

async def main():
    kernel = Kernel()

    # Configure chat completion service based on environment variables
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"):
        print("Using Azure OpenAI")
        service_id = "chat-completion"
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
            )
        )
        execution_settings = AzureChatPromptExecutionSettings(
            service_id=service_id,
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
        )
    elif os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_CHAT_MODEL_ID"):
        print("Using OpenAI")
        service_id = "chat-completion"
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=os.getenv("OPENAI_CHAT_MODEL_ID"),
            )
        )
        execution_settings = OpenAIChatPromptExecutionSettings(
            service_id=service_id,
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
        )
    elif os.getenv("GITHUB_TOKEN") and os.getenv("GITHUB_MODEL_ID"):
        print("Using GitHub Models")
        from openai import AsyncOpenAI

        client = AsyncOpenAI(
            api_key=os.getenv("GITHUB_TOKEN"),
            base_url="https://models.inference.ai.azure.com",
        )
        service_id = "chat-completion"
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=os.getenv("GITHUB_MODEL_ID"),
                async_client=client,
            )
        )
        execution_settings = OpenAIChatPromptExecutionSettings(
            service_id=service_id,
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
        )
    else:
        print("Error: No valid AI service configuration found in environment variables.")
        print("Please set AZURE_OPENAI_API_KEY (with endpoint and deployment), OPENAI_API_KEY (with OPENAI_CHAT_MODEL_ID), or GITHUB_TOKEN (with GITHUB_MODEL_ID).")
        return

    # Add the CoursePlugin to the kernel
    kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

    history = ChatHistory()
    history.add_system_message(
        "You are a helpful AI assistant that answers questions about the 'AI Agents for Beginners' course. "
        "Use the CoursePlugin to search for topics or get the content of specific lessons to answer user queries accurately."
    )

    print("Agent initialized. Type 'exit' or 'quit' to stop.")

    chat_completion = kernel.get_service(service_id)

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            history.add_user_message(user_input)

            response = await chat_completion.get_chat_message_content(
                chat_history=history,
                settings=execution_settings,
                kernel=kernel,
            )

            print(f"Agent: {response}")
            history.add_assistant_message(str(response))

        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())
