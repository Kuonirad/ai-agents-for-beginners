# Browser Use

This lesson explores how to build AI agents that can autonomously interact with web browsers to perform complex tasks like searching, data extraction, and navigation. We will focus on the **Browser-Use** library, which connects Large Language Models (LLMs) with **Playwright** to control a browser.

## Introduction

In this lesson, we will learn how to:
- Integrate **Playwright** with **Browser-Use** for AI-driven automation.
- Use **Vision-Based Extraction** to let the AI "see" and interpret web pages.
- Extract structured data (e.g., Pydantic models) from unstructured web content.
- Implement the **Agent vs. Actor** pattern for robust automation.

## Key Technologies

- **Browser-Use:** A library that wraps Playwright to provide an agentic interface for browser automation. It allows LLMs to interact with the browser using high-level commands.
- **Playwright:** A powerful framework for web testing and automation that controls browsers like Chromium, Firefox, and WebKit.
- **LLM with Vision (e.g., GPT-4o):** Essential for analyzing page layouts and making decisions based on visual cues, which is more robust than relying solely on HTML structure.

## Key Concepts

### Agent vs. Actor Pattern
- **Agent:** Performs autonomous navigation based on high-level goals (e.g., "Find the cheapest hotel in Stockholm"). The agent decides the steps dynamically. Best for dynamic or unknown website layouts.
- **Actor:** Executes precise, scripted actions using selectors (e.g., "Click button #submit"). Best for known, stable structures where reliability is paramount.

### Vision-Based Extraction
Traditional web scraping often breaks when CSS classes change. Vision-based extraction uses the LLM to analyze screenshots of the page to identify elements and extract data (like prices or ratings) based on their visual appearance and context.

### Structured Output
Converting unstructured web content into typed objects (e.g., Pydantic models) ensures that the extracted data is ready for downstream processing (e.g., saving to a database or comparing prices).

### Chrome DevTools Protocol (CDP)
CDP is a low-level protocol used to connect Playwright and Browser-Use to the same browser instance. This enables advanced features like persistent sessions and debugging.

## Sample Code

- Python: [Finding the Cheapest Airbnb](./15-browser-use.ipynb)

## Additional Resources

- [Browser-Use Documentation](https://github.com/browser-use/browser-use)
- [Playwright Python Documentation](https://playwright.dev/python/)
