# Browser Use for AI Agents

In this lesson, we will explore how AI Agents can interact with the web using **Browser-Use** and **Playwright**. This enables agents to perform tasks like searching, data extraction, and navigation autonomously.

## Introduction

This lesson covers:
- **Browser-Use Library**: An agentic interface for browser automation.
- **Playwright**: A framework for reliable web testing and automation.
- **Vision-Based Navigation**: Using LLMs to "see" and interact with web pages.
- **Structured Data Extraction**: Converting web content into structured Pydantic models.

## Available Implementations

This lesson includes a comprehensive notebook tutorial:

- **[15-browser-use.ipynb](./15-browser-use.ipynb)**: A complete guide to building an Airbnb Search Agent that finds the cheapest listing in Stockholm using vision and structured data extraction.

## Learning Goals

After completing this lesson, you will know how to:
- **Initialize Browser-Use Agents** with Playwright integration.
- **Use Vision Capabilities** to allow agents to interpret visual page layouts.
- **Extract Structured Data** (JSON/Pydantic) from unstructured web pages.
- **Implement the Agent vs. Actor Pattern** for robust automation.

## Key Concepts

### Agent vs. Actor Pattern

- **Agent**: Operates autonomously based on high-level goals (e.g., "Find the cheapest hotel"). It uses the LLM to decide the next action based on the current page state. Best for dynamic or unknown websites.
- **Actor**: Executes precise, pre-defined scripts using selectors (e.g., "Click button #submit"). Best for known, stable workflows where speed and reliability are paramount.

### Vision-Based Extraction

Traditional scraping often relies on fragile CSS selectors that break when a website updates. **Vision-Based Extraction** uses the LLM's multimodal capabilities to analyze screenshots of the page, allowing it to "read" prices, ratings, and details just like a human would, making the agent much more resilient to layout changes.

### Structured Output

Using libraries like Pydantic, we can force the LLM to return data in a strict schema (e.g., a list of `Listing` objects with `price` as a float). This ensures that the data extracted from the web is ready for programmatic use in your application.

## Prerequisites

To run the code samples in this lesson, you will need:
- **Playwright Browsers**: Run `playwright install` to download the necessary browser binaries (Chromium, Firefox, WebKit).
- **Azure OpenAI or OpenAI API Key**: Required for the vision capabilities of the agent.

## Getting Started

1. Ensure you have installed the project dependencies (from the repository root):
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. Open the notebook:
   ```bash
   jupyter notebook 15-browser-use/15-browser-use.ipynb
   ```
