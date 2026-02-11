import asyncio
import os
from typing import Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI, AzureChatOpenAI

# Load environment variables
load_dotenv()

class AirbnbListing(BaseModel):
    """Single Airbnb listing with price information"""
    title: str = Field(description="Name/title of the listing")
    price_per_night: float = Field(
        description="Price per night as a number (extract just the numeric value, ignore currency symbols)")
    currency: str = Field(
        default="SEK", description="Currency code (SEK for Swedish Krona)")
    rating: Optional[float] = Field(
        default=None, description="Rating score if visible")
    url: Optional[str] = Field(
        default=None, description="Full URL link to the listing page")

class SearchResult(BaseModel):
    """Complete search results from Airbnb"""
    location: str = Field(description="Search location (Stockholm, Sweden)")
    total_listings_found: int = Field(
        description="Number of listings found on the page")
    listings: List[AirbnbListing] = Field(
        description="List of all listings with prices extracted from the page")
    cheapest_listing: AirbnbListing = Field(
        description="The listing with the lowest price per night")
    average_price: float = Field(
        description="Average price per night across all listings")
    price_range: str = Field(description="Price range as 'min - max SEK'")

async def main():
    # 1. Initialize LLM
    llm = None
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("✅ Using Azure OpenAI")
        llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
    elif os.getenv("OPENAI_API_KEY"):
        print("✅ Using OpenAI")
        llm = ChatOpenAI(model="gpt-4o")
    else:
        print("❌ No API keys found. Please set AZURE_OPENAI_API_KEY or OPENAI_API_KEY in .env")
        return

    # 2. Define the task
    task = (
        "Navigate to https://www.airbnb.com. "
        "Close any pop-ups, cookie banners, or login prompts if they appear. "
        "Search for 'Stockholm, Sweden' in the search box. "
        "Wait for the search results page to fully load with listing cards visible. "
        "Extract ALL listings with their prices, ratings, and URLs. "
        "Find the cheapest listing."
    )

    print(f"🚀 Starting Agent Task:\n{task}\n")

    # 3. Create and Run Agent
    # We use a standard Browser instance (headless=False to see it working if supported)
    browser = Browser()

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        use_vision=True,  # Enable vision for better extraction
    )

    try:
        # Run the agent
        history = await agent.run()

        # 4. Extract Structured Data
        # We can use the agent's final result or explicitly ask for extraction
        # Here we demonstrate using the extraction tool explicitly if needed,
        # but the Agent's run loop typically handles the task.
        # For this demo, we assume the agent returns the result in the final step or we can process the history.

        print("\n✅ Task Completed!")
        print(f"Steps taken: {len(history.history)}")

        # In a real extraction scenario with Browser-Use, you might want to call `agent.extract_content`
        # specifically if the task implies purely data extraction, or inspect the final result.

        # Let's try to perform a specific extraction pass on the final page
        print("\n🔍 Performing final extraction pass...")
        page = await browser.get_current_page()

        extraction_prompt = """
        Extract ALL Airbnb listings visible on this page.
        Identify the cheapest listing.
        """

        result = await page.extract_content(
            prompt=extraction_prompt,
            structured_output=SearchResult,
            llm=llm
        )

        print("\n📊 Extraction Results:")
        print(f"Location: {result.location}")
        print(f"Total Listings: {result.total_listings_found}")
        print(f"Average Price: {result.average_price:.2f} {result.cheapest_listing.currency}")
        print(f"Cheapest Listing: {result.cheapest_listing.title}")
        print(f"Price: {result.cheapest_listing.price_per_night} {result.cheapest_listing.currency}")
        print(f"URL: {result.cheapest_listing.url}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
