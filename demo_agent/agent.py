import asyncio
import os
import sys

# Add the current directory to sys.path so we can import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from course_plugin import CoursePlugin
except ImportError:
    # If running from root, maybe we need to adjust
    sys.path.append(os.path.join(os.getcwd(), 'demo_agent'))
    from course_plugin import CoursePlugin

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Also try loading from .env in the current directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

async def main():
    print("AI Agents Course Assistant")
    print("--------------------------")

    plugin = CoursePlugin()
    if not plugin.lessons:
        print("Warning: STUDY_GUIDE.md not found. Agent will have limited functionality.")

    # Check for API keys
    api_key = os.getenv("OPENAI_API_KEY")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")

    has_llm = False
    kernel = None
    service_id = "chat"

    if api_key or azure_api_key:
        try:
            from semantic_kernel import Kernel
            from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
            # Import FunctionChoiceBehavior correctly for SK 1.x
            try:
                from semantic_kernel.connectors.ai import FunctionChoiceBehavior
            except ImportError:
                 # Fallback for older versions or if location changed
                from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

            from semantic_kernel.contents import ChatHistory

            kernel = Kernel()

            if azure_api_key:
                deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o")
                endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
                if not endpoint:
                    print("Warning: AZURE_OPENAI_ENDPOINT not set. Falling back to keyword search.")
                else:
                    service = AzureChatCompletion(
                        service_id=service_id,
                        deployment_name=deployment,
                        endpoint=endpoint,
                        api_key=azure_api_key,
                    )
                    kernel.add_service(service)
                    has_llm = True
            elif api_key:
                model = os.getenv("OPENAI_MODEL", "gpt-4o")
                service = OpenAIChatCompletion(
                    service_id=service_id,
                    ai_model_id=model,
                    api_key=api_key,
                )
                kernel.add_service(service)
                has_llm = True

            if has_llm:
                kernel.add_plugin(plugin, plugin_name="CoursePlugin")
                print("LLM mode enabled. You can ask natural language questions about the course.")
        except ImportError as e:
            print(f"Failed to import Semantic Kernel components: {e}")
            print("Falling back to keyword search.")
        except Exception as e:
            print(f"Failed to initialize Kernel: {e}")
            print("Falling back to keyword search.")

    if not has_llm:
        print("No valid API keys found or initialization failed. Running in Keyword Search mode.")
        print("You can search for lessons by keyword.")

    # Main Loop
    history = None
    if has_llm:
        history = ChatHistory()
        history.add_system_message("You are a helpful assistant for the AI Agents for Beginners course. Use the CoursePlugin to answer questions based on the study guide. If the answer is found in the study guide, cite the lesson number.")

    while True:
        try:
            user_input = input("\nUser > ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input.strip():
            continue

        if has_llm:
            try:
                history.add_user_message(user_input)

                # Setup execution settings
                from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings, OpenAIChatPromptExecutionSettings

                if azure_api_key:
                    settings = AzureChatPromptExecutionSettings(service_id=service_id)
                else:
                    settings = OpenAIChatPromptExecutionSettings(service_id=service_id)

                settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

                chat_service = kernel.get_service(service_id)
                result = await chat_service.get_chat_message_content(
                    chat_history=history,
                    settings=settings,
                    kernel=kernel
                )

                print(f"Assistant > {result}")
                history.add_message(result)

            except Exception as e:
                print(f"Error during LLM execution: {e}")
                print("Trying fallback search...")
                print(plugin.search_content(user_input))
        else:
            # Fallback mode
            print("Searching course content...")
            results = plugin.search_content(user_input)
            print(f"Results:\n{results}")

if __name__ == "__main__":
    asyncio.run(main())
