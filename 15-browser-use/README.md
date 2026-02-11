# Lesson 15: Browser Use - AI-Powered Web Automation

This lesson demonstrates how to build an intelligent web automation agent that searches Airbnb, extracts prices, and finds the cheapest listing in Stockholm. You'll learn how to integrate **Playwright** with **Browser-Use** for powerful AI-driven automation.

## What You'll Learn
1. **Playwright + Browser-Use Integration**: Combining browser management with AI automation.
2. **Vision-Based Price Extraction**: Let AI "see" and read prices from web pages.
3. **Structured Data Extraction**: Extract listing data with type-safe Pydantic models.
4. **Price Comparison Logic**: Find the cheapest option from multiple listings.
5. **Real-world Application**: Practical price comparison automation.

## Prerequisites
- Azure OpenAI deployment configured (or OpenAI API key)
- Playwright installed (`pip install playwright`)
- `browser-use` library (`pip install browser-use`)
- Understanding of async Python
- Basic web automation concepts

## Architecture: Playwright + Browser-Use

This lesson uses the **official Playwright integration** pattern from Browser-Use documentation.

### Architecture Flow
```
┌──────────────────┐
│   Playwright     │ ◄─── Manages browser lifecycle
│  Browser Manager │      Handles CDP connection
└────────┬─────────┘      Provides browser instance
         │
         │ playwright_browser parameter
         ▼
┌──────────────────┐
│  Browser-Use     │ ◄─── AI-powered automation
│  Browser Object  │      Wraps Playwright browser
└────────┬─────────┘      Provides Agent interface
         │
         │ uses
         ▼
┌──────────────────┐
│   Agent          │ ◄─── Vision + Decision Making
│ (with LLM)       │      Structured output extraction
└──────────────────┘      Natural language tasks
         │
         │ powered by
         ▼
┌──────────────────┐
│  Azure OpenAI    │ ◄─── GPT-4 Vision
│  (LLM + Vision)  │      Analyzes screenshots
└──────────────────┘      Extracts structured data
```

### Why This Approach?

**Playwright provides:**
- ✅ Robust browser lifecycle management
- ✅ Full Chrome DevTools Protocol (CDP) control
- ✅ Stable page and context handling
- ✅ Built-in waiting and synchronization

**Browser-Use adds:**
- ✅ AI-powered element finding (no CSS selectors needed!)
- ✅ Vision-based page understanding
- ✅ Structured output extraction with Pydantic
- ✅ Natural language task execution

## Key Concepts

### Agent vs Actor Pattern

| Scenario | Use Agent | Use Actor |
|----------|-----------|-----------|
| **Dynamic layouts** | ✅ AI adapts to changes | ❌ CSS selectors break |
| **Known structure** | ❌ Slower than direct control | ✅ Fast and precise |
| **Finding elements** | ✅ Natural language queries | ❌ Need exact selectors |
| **Timing control** | ❌ Less predictable | ✅ Full timing control |
| **Complex workflows** | ✅ Handles unexpected UI | ❌ Requires explicit code |

### Vision-Based Extraction
Instead of relying on brittle CSS selectors (e.g., `.div > span.price`), we use the LLM's vision capabilities to "read" the page like a human. This is far more robust against layout changes.

### Structured Output
We define Python classes (Pydantic models) representing the data we want (e.g., `AirbnbListing`). The LLM ensures the extracted data matches this schema, providing type safety and validation.

## Real-World Applications
- **Travel Booking**: Monitor prices, auto-book deals, compare options.
- **E-commerce**: Track inventory, compare prices, automated purchasing.
- **Data Collection**: Scrape dynamic sites, extract structured data.
- **Testing**: Automated UI testing with vision-based verification.
- **Form Automation**: Fill complex multi-step forms intelligently.

## Running the Examples
Check the [Jupyter Notebook](./15-browser-use.ipynb) for a step-by-step interactive tutorial, or run the standalone Python script (if available) for a production-ready example.
