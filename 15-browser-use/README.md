# Lesson 15: Browser Use

## Goal
Enabling agents to autonomously interact with web browsers to perform tasks like searching, data extraction, and navigation.

## Key Technologies
- **Browser-Use:** A library that wraps Playwright to provide an agentic interface for browser automation.
- **Playwright:** A framework for web testing and automation that controls the browser (Chromium, Firefox, WebKit).
- **LLM with Vision (e.g., GPT-4o):** Essential for "seeing" the page content and making decisions based on visual layout, not just HTML structure.

## Key Concepts
- **Agent vs. Actor Pattern:**
  - **Agent:** Autonomous navigation based on high-level goals (e.g., "Find the cheapest hotel"). Good for dynamic or unknown layouts.
  - **Actor:** Precise, scripted actions using selectors (e.g., "Click button #submit"). Good for known, stable structures.
- **Vision-Based Extraction:** Using the LLM to analyze screenshots of the page to extract structured data (e.g., prices, ratings) without relying on brittle CSS selectors.
- **Structured Output:** Converting unstructured web content into typed objects (e.g., Pydantic models) for reliable downstream processing.
- **CDP (Chrome DevTools Protocol):** A low-level protocol used to connect Playwright and Browser-Use to the same browser instance, enabling advanced debugging and persistent sessions.

## About the Notebook: Finding the Cheapest Airbnb
The included notebook `15-browser-use.ipynb` demonstrates how to build an intelligent web automation agent that searches Airbnb, extracts prices, and finds the cheapest listing in Stockholm.

### What You'll Learn:
1. **Playwright + Browser-Use Integration**: Combining browser management with AI automation
2. **Vision-Based Price Extraction**: Let AI "see" and read prices from web pages
3. **Structured Data Extraction**: Extract listing data with type-safe Pydantic models
4. **Price Comparison Logic**: Find the cheapest option from multiple listings
5. **Real-world Application**: Practical price comparison automation

### When to Use Agent vs Actor

| Scenario | Use Agent | Use Actor |
|---|---|---|
| **Dynamic layouts** | ✅ AI adapts to changes | ❌ CSS selectors break |
| **Known structure** | ❌ Slower than direct control | ✅ Fast and precise |
| **Finding elements** | ✅ Natural language queries | ❌ Need exact selectors |
| **Timing control** | ❌ Less predictable | ✅ Full timing control |
| **Complex workflows** | ✅ Handles unexpected UI | ❌ Requires explicit code |
