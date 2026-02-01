import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

# Load environment variables
load_dotenv(find_dotenv())

# Import from browser_use
from browser_use import Agent
# Note: In some versions, ChatOpenAI/ChatAzureOpenAI are imported from langchain_openai,
# but browser-use documentation suggests importing them from browser_use for compatibility.
# We will try importing from browser_use, and fallback if needed, or stick to what docs say.
try:
    from browser_use import ChatOpenAI, ChatAzureOpenAI
except ImportError:
    # Fallback to langchain_openai if browser_use re-exports are missing/changed
    from langchain_openai import ChatOpenAI, AzureChatOpenAI as ChatAzureOpenAI

# Define structured output for Airbnb listings
class AirbnbListing(BaseModel):
    title: str = Field(description="The title of the listing")
    price_per_night: str = Field(description="The price per night")
    rating: Optional[str] = Field(description="The rating of the listing")
    link: Optional[str] = Field(description="The link to the listing detail page")

class AirbnbListings(BaseModel):
    listings: List[AirbnbListing]

async def main():
    # Initialize LLM based on available keys
    if os.getenv('AZURE_OPENAI_API_KEY'):
        print("Using Azure OpenAI...")
        llm = ChatAzureOpenAI(
            model=os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT_NAME', 'gpt-4o'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-05-01-preview'),
            temperature=0.0
        )
    elif os.getenv('OPENAI_API_KEY'):
        print("Using OpenAI...")
        llm = ChatOpenAI(model='gpt-4o', temperature=0.0)
    else:
        print("Warning: No API key found. Please set AZURE_OPENAI_API_KEY or OPENAI_API_KEY in .env")
        print("The agent might fail to run without a valid LLM configuration.")
        # We'll try to initialize default to let it fail gracefully or user might have other config
        llm = ChatOpenAI(model='gpt-4o')

    # Define the task
    task = """
    1. Go to https://www.airbnb.com/
    2. Search for "Tokyo, Japan"
    3. Select dates: Check-in next month 1st, Check-out next month 7th.
    4. Select 2 adults.
    5. Find the top 3 listings.
    6. Extract their title, price per night, rating, and link.
    """

    print(f"Starting Agent with task:\n{task}")

    # Create the agent
    agent = Agent(
        task=task,
        llm=llm,
        output_model_schema=AirbnbListings
    )

    # Run the agent
    history = await agent.run()

    # Process results
    if history.structured_output:
        print("\n✅ Found Listings:")
        print(history.structured_output.model_dump_json(indent=2))

        # Save to file
        with open("airbnb_listings.json", "w") as f:
            f.write(history.structured_output.model_dump_json(indent=2))
        print("\nSaved listings to airbnb_listings.json")
    else:
        print("\n⚠️ No structured output found.")
        print("Final Result:", history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
