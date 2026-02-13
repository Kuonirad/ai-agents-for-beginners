import asyncio
import os
import sys
import subprocess
import tempfile
import base64
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Playwright imports
from playwright.async_api import async_playwright

# Browser-Use imports
from browser_use import Agent, Browser
from pydantic import BaseModel, Field

# LLM imports
# Check which provider to use
if os.getenv("AZURE_OPENAI_API_KEY"):
    from browser_use import ChatAzureOpenAI
    print("✅ Using Azure OpenAI")
elif os.getenv("OPENAI_API_KEY"):
    from langchain_openai import ChatOpenAI
    print("✅ Using OpenAI")
else:
    print("⚠️  No API key found for Azure OpenAI or OpenAI. Please set AZURE_OPENAI_API_KEY or OPENAI_API_KEY.")
    sys.exit(1)


# --- Structured Output Models ---

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


# --- Helper Functions for CLI Display ---

def display_step(step_number: int, title: str, description: str):
    print(f"\n[{step_number}] {title}")
    print(f"    {description}")

def display_action(action_type: str, details: str):
    print(f"    ⚙️  {action_type}: {details}")

def display_result(success: bool, message: str):
    icon = "✅" if success else "❌"
    print(f"\n{icon} {message}")

def display_screenshot(screenshot_base64: str, caption: str = ""):
    # In CLI, we can't display images, but we can save them
    try:
        filename = f"screenshot_{len(os.listdir('.'))}.png"
        with open(filename, "wb") as f:
            f.write(base64.b64decode(screenshot_base64))
        print(f"    🖼️  Screenshot saved to {filename} ({caption})")
    except Exception as e:
        print(f"    ⚠️  Could not save screenshot: {e}")


# --- Chrome Launcher Helper ---

async def start_chrome_with_cdp(port: int = 9222):
    """
    Start Chrome with CDP (Chrome DevTools Protocol) enabled.
    Returns the Chrome process.
    """
    # Create temporary directory for Chrome user data
    user_data_dir = tempfile.mkdtemp(prefix='chrome_cdp_')

    # Chrome paths for different platforms
    chrome_paths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
        '/usr/bin/google-chrome',  # Linux
        '/usr/bin/chromium-browser',  # Linux Chromium
        'chrome',  # Windows/PATH
        'chromium',  # Generic
        'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', # Windows
        'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe', # Windows
    ]

    chrome_exe = None
    for path in chrome_paths:
        if os.path.exists(path) or path in ['chrome', 'chromium']:
            try:
                # Test if executable works
                test_proc = await asyncio.create_subprocess_exec(
                    path, '--version',
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                await test_proc.wait()
                if test_proc.returncode == 0:
                    chrome_exe = path
                    break
            except Exception:
                continue

    if not chrome_exe:
        raise RuntimeError(
            '❌ Chrome not found. Please install Chrome or Chromium.')

    # Chrome command arguments
    cmd = [
        chrome_exe,
        f'--remote-debugging-port={port}',
        f'--user-data-dir={user_data_dir}',
        '--no-first-run',
        '--no-default-browser-check',
        'about:blank',
    ]

    print(f"    Starting Chrome: {' '.join(cmd)}")

    # Start Chrome process
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for Chrome to start and CDP to be ready
    import aiohttp
    cdp_ready = False
    for i in range(20):  # 20 second timeout
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'http://localhost:{port}/json/version',
                    timeout=aiohttp.ClientTimeout(total=1)
                ) as response:
                    if response.status == 200:
                        cdp_ready = True
                        break
        except Exception:
            pass
        await asyncio.sleep(1)
        if i % 5 == 0:
            print("    Waiting for Chrome CDP...")

    if not cdp_ready:
        process.terminate()
        raise RuntimeError('❌ Chrome failed to start with CDP')

    print(f"✅ Chrome started with CDP on port {port}")
    return process


# --- Agent Class ---

class AirbnbSearchAgent:
    """
    Intelligent Airbnb search agent using Browser-Use integration via CDP.
    """

    def __init__(self, llm, cdp_url: str):
        self.llm = llm
        self.browser = Browser(
            cdp_url=cdp_url,
            keep_alive=True
        )

    async def take_screenshot(self, caption: str = ""):
        """Take and display a screenshot of current page"""
        try:
            pages = await self.browser.get_pages()
            if not pages:
                print("⚠️  No pages available for screenshot")
                return

            page = pages[0]  # Use first page (active page)
            screenshot_bytes = await page.screenshot()
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode()
            display_screenshot(screenshot_base64, caption)
        except Exception as e:
            print(f"⚠️  Could not capture screenshot: {str(e)}")

    async def search_stockholm(self) -> SearchResult:
        """
        Main workflow: Search Airbnb for Stockholm and find cheapest listing.
        """

        # Step 1: Navigate and search
        display_step(
            1,
            "Navigate & Search (AI Agent)",
            "Using AI agent with vision to navigate Airbnb and search for Stockholm listings."
        )

        try:
            # Agent navigates to Airbnb and searches
            search_agent = Agent(
                task=(
                    "Navigate to https://www.airbnb.com. "
                    "Close any pop-ups, cookie banners, or login prompts if they appear. "
                    "Search for 'Stockholm, Sweden' in the search box. "
                    "Wait for the search results page to fully load with listing cards visible."
                ),
                llm=self.llm,
                browser=self.browser,
                use_vision=True
            )

            display_action(
                "Agent", "Navigating to Airbnb and searching for Stockholm...")
            await search_agent.run()

            # Wait for results to load
            await asyncio.sleep(3)
            await self.take_screenshot("Search results page loaded")

            display_result(
                True, "Successfully loaded Stockholm search results")

        except Exception as e:
            display_result(False, f"Search failed: {str(e)}")
            raise

        # Step 2: Extract prices with vision
        display_step(
            2,
            "Extract Prices (Vision + LLM)",
            "Using GPT-4 Vision to read all listing prices from the page and extract structured data."
        )

        try:
            # Get the pages created by the Agent
            pages = await self.browser.get_pages()

            if not pages:
                raise RuntimeError(
                    "No pages available after Agent run. Browser might have closed.")

            # Use the first (active) page
            page = pages[0]

            display_action(
                "Vision", "AI is analyzing the page and reading prices...")

            # Extract structured data using LLM vision
            extraction_prompt = """
Extract ALL Airbnb Home listings visible on this page. DO NOT include "Experiences" or other non-home listings.

For each listing, extract:
- Title/name of the property
- Price per night (numeric value only, without currency symbols)
- Currency (SEK for Swedish Krona)
- Rating if visible
- URL: The full link to the listing detail page (should start with https://www.airbnb.com/rooms/)

After extracting all listings:
- Identify which listing has the LOWEST price
- Calculate the average price across all listings
- Determine the price range (min to max)

Focus on the listing cards on the search results page.
Only include listings where you can clearly see the price.
IMPORTANT: Extract the actual URL/link for each listing so users can click on it.
"""

            search_results = await page.extract_content(
                prompt=extraction_prompt,
                structured_output=SearchResult,
                llm=self.llm
            )

            display_action(
                "Extracted",
                f"Found {search_results.total_listings_found} listings with prices"
            )

            # Display some sample prices
            if len(search_results.listings) > 0:
                sample_prices = [
                    f"{l.price_per_night:.0f} SEK" for l in search_results.listings[:5]]
                display_action(
                    "Sample Prices",
                    f"{', '.join(sample_prices)}{'...' if len(search_results.listings) > 5 else ''}"
                )

            display_result(True, "Price extraction completed successfully")

            return search_results

        except Exception as e:
            display_result(False, f"Price extraction failed: {str(e)}")
            raise


# --- Main Execution ---

async def main():
    print("🏠 Find the Cheapest Airbnb in Stockholm (CLI Demo)")
    print("===================================================")

    # Initialize LLM
    if os.getenv("AZURE_OPENAI_API_KEY"):
        llm = ChatAzureOpenAI(
            model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-4o"),
        )
    else:
        llm = ChatOpenAI(
            model="gpt-4o",
        )

    chrome_process = None
    playwright_browser = None

    try:
        # Step 1: Start Chrome with CDP
        display_action(
            "Chrome", "Starting Chrome with CDP (remote debugging)...")
        chrome_process = await start_chrome_with_cdp(port=9222)
        cdp_url = 'http://localhost:9222'

        # Step 2: Connect Playwright (optional, but good for robust handling)
        display_action(
            "Playwright", "Connecting Playwright to Chrome via CDP...")
        playwright = await async_playwright().start()
        playwright_browser = await playwright.chromium.connect_over_cdp(cdp_url)
        display_result(True, "Playwright connected successfully")

        # Step 3: Create Browser-Use agent
        display_action(
            "Browser-Use", "Creating Browser-Use agent with CDP connection...")
        agent = AirbnbSearchAgent(llm=llm, cdp_url=cdp_url)
        display_result(True, "Agent initialized")

        # Step 4: Search and extract prices
        result = await agent.search_stockholm()

        # Step 5: Display results
        print("\n📊 Search Results")
        print("----------------")
        print(f"Location: {result.location}")
        print(f"Total Listings Found: {result.total_listings_found}")
        print(f"Average Price: {result.average_price:.2f} SEK/night")
        print(f"Price Range: {result.price_range}")

        cheapest = result.cheapest_listing
        print(f"\n🏆 CHEAPEST AIRBNB: {cheapest.title}")
        print(f"   Price: {cheapest.price_per_night:.2f} {cheapest.currency}/night")
        print(f"   Rating: {cheapest.rating}/5.0" if cheapest.rating else "   Rating: N/A")
        print(f"   Link: {cheapest.url}")
        print(f"   Savings: {(result.average_price - cheapest.price_per_night):.2f} SEK vs average")

        if len(result.listings) > 1:
            print("\n📋 All Listings:")
            sorted_listings = sorted(result.listings, key=lambda x: x.price_per_night)
            for idx, listing in enumerate(sorted_listings, 1):
                badge = "🏆 " if listing.price_per_night == cheapest.price_per_night else f"{idx}. "
                print(f"{badge}{listing.title[:40]}... - {listing.price_per_night:.0f} SEK")

    except Exception as e:
        display_result(False, f"Error during search: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        display_action("Cleanup", "Closing browser and cleaning up...")

        if playwright_browser:
            await playwright_browser.close()

        if chrome_process:
            chrome_process.terminate()
            try:
                await asyncio.wait_for(chrome_process.wait(), 5)
            except asyncio.TimeoutError:
                chrome_process.kill()

        display_result(True, "Cleanup complete")

if __name__ == "__main__":
    asyncio.run(main())
