import os
import sys
import asyncio
import re
from dotenv import load_dotenv, find_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the plugin (will use dummy decorator if SK not installed)
from course_plugin import CoursePlugin

async def main():
    load_dotenv(find_dotenv())

    # Check for API keys
    azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    kernel = None

    # Initialize Kernel if keys are available
    if azure_openai_key or openai_api_key or github_token:
        try:
            import semantic_kernel as sk
            from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion
            from semantic_kernel.contents.chat_history import ChatHistory
            from semantic_kernel.functions.kernel_arguments import KernelArguments
            # Try importing FunctionChoiceBehavior (location varies by version)
            try:
                from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
            except ImportError:
                 try:
                     from semantic_kernel.connectors.ai import FunctionChoiceBehavior
                 except ImportError:
                     FunctionChoiceBehavior = None

            kernel = sk.Kernel()

            service_id = "chat"

            if azure_openai_key:
                endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
                deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
                if endpoint and deployment:
                    kernel.add_service(
                        AzureChatCompletion(
                            service_id=service_id,
                            deployment_name=deployment,
                            endpoint=endpoint,
                            api_key=azure_openai_key
                        )
                    )
            elif openai_api_key:
                model = os.getenv("OPENAI_MODEL", "gpt-4o")
                kernel.add_service(
                    OpenAIChatCompletion(
                        service_id=service_id,
                        ai_model_id=model,
                        api_key=openai_api_key
                    )
                )

            # Register the plugin
            kernel.add_plugin(CoursePlugin(), plugin_name="CoursePlugin")

            print("AI Agent initialized with LLM support.")

        except ImportError as e:
            print(f"Warning: Failed to import Semantic Kernel components: {e}")
            print("Running in fallback mode (Keyword Search).")
            kernel = None
        except Exception as e:
            print(f"Warning: Failed to initialize Semantic Kernel: {e}")
            print("Running in fallback mode (Keyword Search).")
            kernel = None
    else:
        print("No API keys found. Running in fallback mode (Keyword Search).")

    # Instance of plugin for direct use in fallback mode
    plugin = CoursePlugin()

    # Chat loop
    print("Welcome to the AI Agents Course Assistant!")
    print("Ask a question about the course, or type 'exit' to quit.")

    chat_history = None
    if kernel:
        try:
            from semantic_kernel.contents.chat_history import ChatHistory
            chat_history = ChatHistory()
        except ImportError:
            pass

    while True:
        try:
            user_input = input("\nYou: ")
        except EOFError:
            break

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input.strip():
            continue

        if kernel and chat_history:
            try:
                chat_service = kernel.get_service(service_id="chat")
                chat_history.add_user_message(user_input)

                execution_settings = None
                if FunctionChoiceBehavior:
                     # Attempt to create settings with auto function calling
                     # This part is tricky as APIs differ.
                     # We will try a generic approach or catch errors.
                     try:
                        from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings, OpenAIChatPromptExecutionSettings
                        if azure_openai_key:
                            execution_settings = AzureChatPromptExecutionSettings(service_id=service_id)
                        else:
                            execution_settings = OpenAIChatPromptExecutionSettings(service_id=service_id)

                        execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
                     except Exception as ex:
                         print(f"DEBUG: Could not set function choice behavior: {ex}")

                # Get response
                response = await chat_service.get_chat_message_content(
                    chat_history=chat_history,
                    settings=execution_settings,
                    kernel=kernel
                )

                print(f"Agent: {response}")
                chat_history.add_message(response)

            except Exception as e:
                print(f"Error calling LLM: {e}")
                # Fallback logic
                results = plugin.search_content(user_input)
                print(f"Agent (Fallback): Found these snippets:\n{results}")

        else:
            # Fallback mode: Simple keyword matching
            # Logic: If user asks for specific lesson, show it. Otherwise search.

            lesson_match = re.search(r'lesson\s*(\d+)', user_input.lower())
            if lesson_match:
                num = lesson_match.group(1)
                content = plugin.get_lesson_content(num)
                # Show first 500 chars to avoid flooding
                print(f"Agent: {content[:500]}...\n(Content truncated)")
            else:
                results = plugin.search_content(user_input)
                print(f"Agent: {results}")

if __name__ == "__main__":
    asyncio.run(main())
