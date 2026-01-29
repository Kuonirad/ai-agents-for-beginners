import asyncio
import os
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Browser-Use imports
from browser_use import Agent, Browser, ChatAzureOpenAI, ChatOpenAI

# Load environment variables
load_dotenv()

# Structured Output Models
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
    """
    Main execution function for Airbnb price comparison agent.
    """
    print("🚀 Starting Airbnb Search Agent...")

    # Initialize LLM
    # Checks for Azure OpenAI first, then falls back to standard OpenAI
    if os.getenv("AZURE_OPENAI_API_KEY"):
        print("✅ Using Azure OpenAI")
        llm = ChatAzureOpenAI(
            model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o"),
        )
    elif os.getenv("OPENAI_API_KEY"):
        print("✅ Using Standard OpenAI")
        llm = ChatOpenAI(model="gpt-4o")
    else:
        # Fallback/Error if no keys
        print("⚠️  No API Key found in environment variables.")
        print("   Please set AZURE_OPENAI_API_KEY or OPENAI_API_KEY in .env")
        return

    # Initialize Browser
    # Run visible (headless=False) to see what's happening
    browser = Browser(
        headless=False,
    )

    try:
        # Step 1: Navigate and Search
        print("\n📍 Step 1: Navigating and Searching...")
        search_agent = Agent(
            task=(
                "Navigate to https://www.airbnb.com. "
                "Close any pop-ups, cookie banners, or login prompts if they appear. "
                "Search for 'Stockholm, Sweden' in the search box. "
                "Wait for the search results page to fully load with listing cards visible."
            ),
            llm=llm,
            browser=browser,
            use_vision=True
        )

        await search_agent.run()

        # Step 2: Extract Prices
        print("\n📍 Step 2: Extracting Prices with Vision AI...")

        # Get the active page from the browser
        pages = await browser.get_pages()
        if not pages:
            raise RuntimeError("No pages available.")
        page = pages[0]

        extraction_prompt = """
        Extract ALL Airbnb Home listings visible on this page. DO NOT include "Experiences".

        For each listing, extract:
        - Title
        - Price per night (numeric)
        - Currency
        - Rating
        - URL

        After extracting:
        - Identify the LOWEST price
        - Calculate average price
        - Determine price range
        """

        search_results = await page.extract_content(
            prompt=extraction_prompt,
            structured_output=SearchResult,
            llm=llm
        )

        # Display Results
        print("\n" + "="*50)
        print("📊 SEARCH RESULTS")
        print("="*50)
        print(f"Location: {search_results.location}")
        print(f"Listings Found: {search_results.total_listings_found}")
        if search_results.listings:
            print(f"Average Price: {search_results.average_price:.2f} {search_results.listings[0].currency}")
        print(f"Price Range: {search_results.price_range}")

        cheapest = search_results.cheapest_listing
        print("\n🏆 CHEAPEST LISTING:")
        print(f"Title: {cheapest.title}")
        print(f"Price: {cheapest.price_per_night} {cheapest.currency}")
        print(f"Rating: {cheapest.rating}")
        print(f"URL: {cheapest.url}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        # Cleanup
        await browser.close()
        print("\n✅ Agent finished.")

if __name__ == "__main__":
    asyncio.run(main())
