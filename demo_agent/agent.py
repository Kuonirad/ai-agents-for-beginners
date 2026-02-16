import os
import sys
import asyncio
from dotenv import load_dotenv, find_dotenv

# Ensure we can import from local directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings, OpenAIChatPromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory

# Try to import FunctionChoiceBehavior based on version quirks
try:
    from semantic_kernel.connectors.ai import FunctionChoiceBehavior
except ImportError:
    try:
        from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
    except ImportError:
        # Fallback or older version
        FunctionChoiceBehavior = None

from course_plugin import CoursePlugin

async def main():
    load_dotenv(find_dotenv())

    # Check for API keys
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    plugin = CoursePlugin()

    # If no keys, fallback to manual mode
    if not azure_key and not openai_key and not github_token:
        print("No valid API keys found (AZURE_OPENAI_API_KEY, OPENAI_API_KEY, or GITHUB_TOKEN).")
        print("Entering manual search mode using CoursePlugin directly.")
        print("Type 'exit' to quit.")
        while True:
            try:
                query = input("User: ")
                if not query:
                    continue
                if query.lower() in ["exit", "quit"]:
                    break

                # Try to parse as lesson number
                if query.isdigit():
                    num = int(query)
                    content = plugin.get_lesson_content(num)
                    # Truncate for readability
                    print(f"Agent: {content[:500]}..." if len(content) > 500 else f"Agent: {content}")
                else:
                    results = plugin.search_content(query)
                    print(f"Agent: {results}")
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"Error: {e}")
        return

    # Initialize Kernel
    kernel = Kernel()

    service_id = "default"

    if azure_key:
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=deployment,
                endpoint=endpoint,
                api_key=azure_key,
            )
        )
    elif openai_key:
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        kernel.add_service(
            OpenAIChatCompletion(
                service_id=service_id,
                ai_model_id=model,
                api_key=openai_key,
            )
        )
    elif github_token:
        # GitHub Models support via AzureChatCompletion
        endpoint = "https://models.inference.ai.azure.com"
        model = os.getenv("GITHUB_MODEL_NAME", "gpt-4o")
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                deployment_name=model,
                endpoint=endpoint,
                api_key=github_token,
            )
        )

    # Add plugin
    kernel.add_plugin(plugin, plugin_name="CoursePlugin")

    # Chat loop
    chat_history = ChatHistory()
    chat_history.add_system_message("You are a helpful AI assistant for the 'AI Agents for Beginners' course. Use the CoursePlugin to answer questions based on the study guide. Always cite the lesson number.")

    chat_completion = kernel.get_service(service_id)

    # Configure settings
    if azure_key or github_token:
        settings = AzureChatPromptExecutionSettings(service_id=service_id)
    else:
        settings = OpenAIChatPromptExecutionSettings(service_id=service_id)

    if FunctionChoiceBehavior:
        settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    else:
        print("Warning: FunctionChoiceBehavior not found, tool use may not work.")

    print("Agent ready! Ask me anything about the course. Type 'exit' to quit.")

    while True:
        try:
            user_input = input("User: ")
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                break

            chat_history.add_user_message(user_input)

            # Get response
            try:
                result = await chat_completion.get_chat_message_content(
                    chat_history=chat_history,
                    settings=settings,
                    kernel=kernel
                )

                if result:
                    print(f"Agent: {result.content}")
                    chat_history.add_message(result)
                else:
                    print("Agent: I'm sorry, I couldn't generate a response.")
            except Exception as e:
                print(f"Error calling LLM: {e}")

        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":
    asyncio.run(main())
