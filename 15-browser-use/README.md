# Browser Use

As AI agents become more capable, the ability to interact with the web just like a human is a game-changer. "Browser Use" allows agents to autonomously navigate websites, extract information, and perform actions using a web browser.

## Introduction

In this lesson, we will cover:

- **What is Browser Use?** and how it differs from traditional web scraping.
- **The Browser-Use Library:** A powerful Python library for browser automation with agents.
- **Agent vs. Actor Pattern:** Understanding the two modes of operation.
- **Vision-Based Navigation:** How LLMs "see" and interact with web pages.

## Learning Goals

After completing this lesson, you will understand how to:

- **Deploy the `browser-use` library** to create agents that can surf the web.
- **Implement the Agent Pattern** for autonomous, goal-oriented navigation.
- **Implement the Actor Pattern** for precise, deterministic browser actions.
- **Utilize Vision-LLMs** (like GPT-4o) to interpret page layouts and elements.
- **Extract structured data** from dynamic websites.

## What is Browser Use?

Browser Use refers to the capability of AI agents to control a web browser (like Chromium) to perform tasks. Unlike traditional scraping which parses HTML code, Browser Use agents:

1.  **See the page:** They take screenshots and use Vision-LLMs to understand the UI.
2.  **Interact naturally:** They click buttons, type text, and scroll, just like a user.
3.  **Handle dynamic content:** They work with JavaScript-heavy sites (SPA) and complex workflows that block simple scrapers.

## Key Concepts

### 1. The `browser-use` Library

We utilize the open-source [`browser-use`](https://github.com/browser-use/browser-use) library. It acts as a bridge between your LLM and the Playwright browser automation framework.

### 2. Agent vs. Actor

-   **Agent:** The "Agent" is autonomous. You give it a high-level goal (e.g., "Find the cheapest flight to Tokyo next Tuesday"), and it figures out the steps: searching, filtering, comparing, and clicking. It uses an LLM to decide the next action based on the current page state.
-   **Actor:** The "Actor" is deterministic. It executes specific, pre-defined actions (e.g., "Go to url X", "Click selector Y"). This is useful for stable, repetitive tasks where you know the exact layout.

### 3. Vision-Based Navigation

Modern agents don't just read code; they see pixels. The agent takes a screenshot of the browser viewport and sends it to a Vision-LLM. The model analyzes the image to find buttons, forms, and text, allowing it to interact with elements that might have obscure or changing code identifiers.

## Code Sample

The code sample for this lesson demonstrates how to use the `browser-use` library to create a simple agent that searches the web.

-   **[15-browser-use.ipynb](./15-browser-use.ipynb)**: A Jupyter notebook guiding you through setting up and running your first browser agent.

## Additional Resources

-   [Browser-Use Documentation](https://docs.browser-use.com)
-   [Playwright Python](https://playwright.dev/python/)

## Next Steps

Now that you've explored Browser Use, you can try combining it with other patterns like **Planning** or **Multi-Agent** systems to build even more complex workflows.
