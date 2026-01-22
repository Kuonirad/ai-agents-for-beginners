# Lesson 15: Browser Use - Building Computer Use Agents

Welcome to Lesson 15! In this lesson, we explore the cutting-edge field of **Computer Use Agents (CUA)**. Unlike traditional web scrapers that rely on rigid code selectors, these agents use **Vision-LLMs** (like GPT-4o) to "see" the screen and interact with web browsers just like a human would—clicking buttons, typing text, and extracting information from complex, dynamic websites.

## Introduction

This lesson focuses on the **Browser Use** library, a powerful tool that bridges the gap between Large Language Models and web browser automation (via Playwright).

### What is "Computer Use"?
Computer Use refers to AI agents that can operate a computer interface. Instead of just generating text, they perform actions:
-   **Perceive:** They take screenshots of the current page.
-   **Reason:** The LLM analyzes the screenshot to understand the UI layout and find elements (e.g., "Where is the 'Search' button?").
-   **Act:** They execute actions like `click`, `type`, `scroll`, or `navigate`.

## Learning Goals

By the end of this lesson, you will be able to:
1.  **Understand the Browser-Use Architecture**: How LLMs, Playwright, and Python code work together.
2.  **Implement Vision-Based Extraction**: Use AI to "read" data from a webpage without writing fragile CSS selectors.
3.  **Build an Autonomous Agent**: Create an agent that can navigate a website (e.g., Airbnb), perform a search, and make decisions based on what it finds.
4.  **Use Structured Output**: Extract clean, type-safe data (using Pydantic models) from unstructured web content.

## Key Concepts

### 1. Agent vs. Actor Pattern
-   **The Agent (Autonomous)**: You give it a high-level goal (e.g., "Find the cheapest hotel in Stockholm"). The agent figures out the steps, handles pop-ups, and adapts to layout changes. It uses "Vision" to make decisions.
-   **The Actor (Deterministic)**: You give it specific instructions (e.g., "Click the button with ID `#submit`"). This is faster and cheaper but breaks easily if the website changes.
-   **Hybrid Approach**: The best solutions often combine both—using an Agent to navigate complex/unknown flows and an Actor for repetitive, stable tasks.

### 2. Vision-Based Extraction
Traditional web scraping requires inspecting HTML source code to find `<div>` tags and `class` names. Vision-based extraction simply sends a screenshot to the LLM and asks, "What is the price listed here?". This is incredibly robust against HTML structure changes.

### 3. Structured Data with Pydantic
LLMs are great at text, but software needs structured data. We use **Pydantic models** to force the LLM to output data in a strict JSON format (e.g., enforcing that `price` is a number and `currency` is a string).

## Lesson Content: Airbnb Search Agent

In the accompanying notebook, we build a practical **Airbnb Search Agent**.

**The Workflow:**
1.  **Launch Browser**: Start a real Chrome instance visible to you.
2.  **Navigate & Search**: The Agent goes to Airbnb.com, handles cookie banners, and searches for "Stockholm, Sweden".
3.  **Vision Analysis**: The Agent takes a screenshot of the results page.
4.  **Extraction**: It identifies all listing cards, extracts the title, price, rating, and link for each.
5.  **Logic**: It calculates the average price and identifies the absolute cheapest option.
6.  **Result**: It outputs the data as a structured Python object.

## Setup Instructions

### Prerequisites
-   **Python 3.12+**
-   **Azure OpenAI** (GPT-4o or similar Vision-capable model) OR **OpenAI API Key**

### Installation
This lesson requires specific packages. Run the following in your terminal (or let the notebook install them):

```bash
pip install browser-use langchain-openai playwright pydantic
playwright install chromium
```

### Environment Variables
Ensure your `.env` file is configured with your API keys. If using Azure OpenAI, you will need:
-   `AZURE_OPENAI_API_KEY`
-   `AZURE_OPENAI_ENDPOINT`
-   `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` (must be a vision-capable model)

## Code Sample

Open the notebook to start building:
-   [15-browser-use.ipynb](./15-browser-use.ipynb)

## Additional Resources
-   **Browser-Use Documentation**: [docs.browser-use.com](https://docs.browser-use.com)
-   **Playwright Python**: [playwright.dev/python](https://playwright.dev/python/)
