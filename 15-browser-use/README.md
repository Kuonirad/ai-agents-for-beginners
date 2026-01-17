# Building Computer Use Agents (CUA) with Browser Use

![Browser Use](../images/repo-thumbnailv2.png)

### Introduction

This lesson covers how to build **Computer Use Agents (CUA)** that can autonomously interact with web browsers to perform tasks. Unlike traditional web scraping which relies on brittle selectors, these agents use **Vision-LLMs** (like GPT-4o) to "see" the page and make decisions, making them far more resilient to UI changes.

We will use the **Browser-Use** library, which integrates with **Playwright** to provide a high-level interface for agents to control the browser.

### Learning Goals

After completing this lesson, you will know how to:
- Understand the **Agent vs. Actor** pattern for browser automation.
- Build agents that can navigate, search, and extract data from websites autonomously.
- Use **Vision-based extraction** to convert unstructured web pages into structured data (Pydantic models).
- Integrate **Playwright** with **Browser-Use** for advanced browser control.

## Code Samples

The code sample for this lesson is available in:
- [15-browser-use.ipynb](./15-browser-use.ipynb)

## Key Concepts

### 1. Agent vs. Actor Pattern

When automating browser tasks, we distinguish between two modes:

*   **Agent (Autonomous)**: The AI decides what to do based on a high-level goal (e.g., "Find the cheapest hotel"). It uses vision to understand the page and takes actions dynamically. This is robust but can be slower.
*   **Actor (Scripted)**: The code performs precise, predefined actions (e.g., "Click the button with ID `#submit`"). This is fast and reliable but breaks if the UI changes.

Effective CUA implementations often mix both: using the Agent to handle dynamic navigation and the Actor for repetitive, known tasks.

### 2. Vision-Based Extraction

Traditional scraping requires reverse-engineering HTML structures and CSS selectors. **Vision-based extraction** simplifies this by taking a screenshot of the page and asking a Vision-LLM to "Read the prices and names from this image".

This approach is:
- **Resilient**: It works even if class names are obfuscated (e.g., React/Tailwind classes).
- **Human-like**: It interprets the page as a user sees it.

### 3. Browser-Use Library

[Browser-Use](https://browser-use.com/) is a library designed to make browser automation with LLMs easy. It handles:
- **Context Management**: Passing the page state (DOM + Screenshot) to the LLM.
- **Action Execution**: Converting LLM responses into Playwright actions (click, type, scroll).
- **Self-Correction**: If an action fails, the agent can retry with a different strategy.

## The Airbnb Example

In the provided notebook, we build an agent that:
1.  **Navigates** to Airbnb.com.
2.  **Searches** for a location (Stockholm).
3.  **Identifies** listing cards visually.
4.  **Extracts** structured data (Price, Rating, Title) into a Python object.
5.  **Compares** results to find the cheapest option.

## Additional Resources

- [Browser-Use Documentation](https://docs.browser-use.com/)
- [Playwright Python Documentation](https://playwright.dev/python/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
