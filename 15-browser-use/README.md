# Building Computer Use Agents (CUA) with Browser-Use

This lesson explores how to build AI Agents that can interact with web browsers to perform autonomous tasks. We will use the **Browser-Use** library, which combines **Playwright** for browser automation with **LLMs (Vision)** for understanding and decision making.

## Introduction

In this lesson, we will cover:
- How to enable agents to "see" and interact with websites.
- The difference between "Agent" and "Actor" patterns in browser automation.
- How to extract structured data from unstructured web pages using Vision models.
- Building an autonomous price comparison agent.

## Learning Goals

After completing this lesson, you should be able to:
- Understand the architecture of Browser-Use (Playwright + LLM).
- Build an agent that can navigate, search, and extract data from websites.
- Use Vision models to handle dynamic websites without brittle CSS selectors.
- Implement structured output extraction using Pydantic models.

## Key Concepts

### Agent vs. Actor Pattern
- **Agent:** Autonomous navigation based on high-level goals (e.g., "Find the cheapest hotel"). The agent decides the steps based on what it sees. Best for dynamic or unknown layouts.
- **Actor:** Precise, scripted actions using selectors (e.g., "Click button #submit"). Best for known, stable structures where reliability is key.

### Vision-Based Extraction
Traditional web scraping often relies on HTML parsing or CSS selectors, which break easily when the website layout changes. **Vision-Based Extraction** uses the LLM to analyze a screenshot of the page, allowing it to "read" the content just like a human would, making it much more robust to layout changes.

### Structured Data Extraction
We can force the LLM to return data in a specific JSON structure (defined by Pydantic models). This turns unstructured web content into reliable, typed Python objects that can be used in your code.

## Sample Code

- [Finding the Cheapest Airbnb (Notebook)](./15-browser-use.ipynb)

## Additional Resources

- [Browser-Use Documentation](https://docs.browser-use.com/)
- [Playwright Python Documentation](https://playwright.dev/python/docs/intro)

## Previous Lesson

[Exploring Microsoft Agent Framework](../14-microsoft-agent-framework/README.md)
