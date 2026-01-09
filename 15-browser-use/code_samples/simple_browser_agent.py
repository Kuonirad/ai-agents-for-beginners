import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Browser Use components
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI, AzureChatOpenAI

async def main():
    """
    A simple example of a Browser Use agent.
    This agent will navigate to Google, search for a query, and return the result.
    """

    llm = None

    # Check for API keys and initialize appropriate LLM
    if os.getenv("OPENAI_API_KEY"):
        print("🔑 Using OpenAI API")
        llm = ChatOpenAI(model="gpt-4o")
    elif os.getenv("AZURE_OPENAI_API_KEY"):
        print("🔑 Using Azure OpenAI API")
        llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview")
        )
    else:
        print("❌ Error: OPENAI_API_KEY or AZURE_OPENAI_API_KEY is not set.")
        print("Please set it in your .env file.")
        return

    print("🚀 Starting Simple Browser Agent...")

    # Initialize the Browser
    # headless=False lets you see the browser actions in real-time
    browser = Browser(headless=False)

    # Define the task
    task = "Go to google.com and search for 'AI Agents for beginners'. Return the title of the first organic result."

    # Create the Agent
    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
    )

    try:
        # Run the agent
        history = await agent.run()

        # Get the result
        result = history.final_result()
        print("\n✅ Task Completed!")
        print(f"Result: {result}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Clean up
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
