# Lesson 15: Browser Use

**Goal:** Enable AI agents to autonomously interact with web browsers to perform tasks like searching, data extraction, and navigation.

## Overview
This lesson demonstrates how to build intelligent web automation agents using **Browser-Use** and **Playwright**. Unlike traditional web scrapers that rely on brittle CSS selectors, these agents use **LLM Vision** capabilities to "see" the page and make decisions, allowing them to handle dynamic layouts and complex interactions.

## Key Technologies
- **Browser-Use:** A library that wraps Playwright to provide an agentic interface for browser automation.
- **Playwright:** A framework for web testing and automation that controls the browser.
- **LLM with Vision (e.g., GPT-4o):** Essential for interpreting page layout and extracting data from screenshots.

## Key Concepts
- **Agent vs. Actor Pattern:**
  - **Agent:** Autonomous navigation based on high-level goals (e.g., "Find the cheapest hotel"). Best for unknown or dynamic environments.
  - **Actor:** Precise, scripted actions (e.g., "Click button #submit"). Best for stable, known workflows.
- **Vision-Based Extraction:** Using the LLM to analyze screenshots for structured data extraction, avoiding the need for complex parsing logic.
- **Structured Output:** Converting unstructured web content into typed Python objects (Pydantic models).

## Getting Started

### Prerequisites
1. **Azure OpenAI** or **OpenAI** API access (with Vision support).
2. Python 3.12+ environment.

### Setup
1. **Install Dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```
   *Ensures `browser-use`, `playwright`, and `langchain-openai` are installed.*

2. **Install Playwright Browsers:**
   ```bash
   playwright install chromium
   ```

3. **Configure Environment:**
   Ensure your `.env` file in the project root contains your API keys:
   ```env
   AZURE_OPENAI_ENDPOINT=...
   AZURE_OPENAI_API_KEY=...
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=...
   AZURE_OPENAI_API_VERSION=...
   # Or for standard OpenAI
   OPENAI_API_KEY=...
   ```

## Running the Code

### 1. Jupyter Notebook
The main lesson content is in `15-browser-use.ipynb`.
- It walks through building an Airbnb search agent.
- Demonstrates connecting Playwright with Browser-Use.
- Shows how to extract structured pricing data.

### 2. Demo Script
A standalone Python script `airbnb_agent.py` is provided for running the automation directly from the terminal.

```bash
python airbnb_agent.py
```

## What the Agent Does
1. Launches a Chrome browser instance.
2. Navigates to Airbnb.com.
3. Searches for "Stockholm, Sweden".
4. Uses Vision AI to read listings and prices from the search results.
5. Identifies and highlights the cheapest listing.

## Resources
- [Browser-Use Documentation](https://docs.browser-use.com/)
- [Playwright Documentation](https://playwright.dev/)
