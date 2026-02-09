import os
import sys
import asyncio

# Ensure demo_agent is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
# Add parent dir too for STUDY_GUIDE relative path handling if run from here
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments
from dotenv import load_dotenv

# Try importing the plugin
try:
    from demo_agent.course_plugin import CoursePlugin
except ImportError:
    try:
        from course_plugin import CoursePlugin
    except ImportError:
        print("Error: Could not import CoursePlugin.")
        sys.exit(1)

# Load environment variables
load_dotenv()

async def main():
    print("Initializing AI Agent...")

    kernel = Kernel()

    # Configure AI Service
    service_id = "chat"
    use_llm = False

    openai_key = os.getenv("OPENAI_API_KEY")
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    try:
        if azure_key:
            print("Using Azure OpenAI...")
            deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            kernel.add_service(
                AzureChatCompletion(
                    service_id=service_id,
                    deployment_name=deployment_name,
                    endpoint=endpoint,
                    api_key=azure_key
                )
            )
            use_llm = True
        elif openai_key:
            print("Using OpenAI...")
            model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4o")
            kernel.add_service(
                OpenAIChatCompletion(
                    service_id=service_id,
                    ai_model_id=model_id,
                    api_key=openai_key
                )
            )
            use_llm = True
        elif github_token:
            print("GitHub Token found. To use GitHub Models, please set OPENAI_API_KEY and OPENAI_BASE_URL manually.")
            print("Falling back to Search Mode.")
            use_llm = False
        else:
            print("No OpenAI/Azure API keys found.")
            use_llm = False

    except Exception as e:
        print(f"Error initializing AI service: {e}")
        use_llm = False

    # Add the plugin
    course_plugin = CoursePlugin()
    kernel.add_plugin(course_plugin, plugin_name="CoursePlugin")

    if use_llm:
        print("\n--- AI Agents Course Assistant (LLM Mode) ---")
        print("I can answer questions about the course using the Study Guide.")
        print("Type 'exit' to quit.\n")

        chat_history = ChatHistory()
        chat_service = kernel.get_service(service_id)

        # Configure execution settings
        execution_settings = kernel.get_prompt_execution_settings_from_service_id(service_id)
        execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                break

            try:
                if user_input.lower() in ["exit", "quit"]:
                    break
                if not user_input:
                    continue

                chat_history.add_user_message(user_input)

                # Get response
                result = await chat_service.get_chat_message_content(
                    chat_history=chat_history,
                    settings=execution_settings,
                    kernel=kernel
                )

                print(f"Agent: {result.content}\n")
                chat_history.add_message(result)

            except Exception as e:
                print(f"Error: {e}")

    else:
        print("\n--- AI Agents Course Search (Fallback Mode) ---")
        print("No LLM configured. Enter search terms to find content in the Study Guide.")
        print("Type 'exit' to quit.\n")

        # Get function directly
        search_func = kernel.plugins["CoursePlugin"]["search_content"]

        while True:
            try:
                user_input = input("Search Query: ").strip()
            except EOFError:
                break

            try:
                if user_input.lower() in ["exit", "quit"]:
                    break
                if not user_input:
                    continue

                # Invoke search directly
                arguments = KernelArguments(query=user_input)
                result = await kernel.invoke(function=search_func, arguments=arguments)
                print(f"Results:\n{result}\n")

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
