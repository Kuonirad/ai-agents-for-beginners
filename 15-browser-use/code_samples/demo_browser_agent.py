from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables (ensure OPENAI_API_KEY is set)
load_dotenv()

async def main():
    # Initialize the LLM (using gpt-4o-mini as a cost-effective option, or user's preference)
    # We check for OPENAI_API_KEY. If not present, we can't run.
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        return

    llm = ChatOpenAI(model="gpt-4o-mini")

    # Define a simple task
    task = "Go to https://github.com/microsoft/ai-agents-for-beginners and find the number of stars this repository has."

    # Create the agent
    agent = Agent(
        task=task,
        llm=llm,
    )

    # Run the agent and get the history
    history = await agent.run()

    # Print the final result
    print("Agent finished!")
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
