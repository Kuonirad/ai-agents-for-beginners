# Browser Use

## Introduction

This lesson covers how to build AI agents that can interact with web browsers to perform tasks autonomously. We will explore the **Browser Use** library, which leverages Playwright and LLMs to navigate websites, extract data, and execute complex workflows.

## Learning Goals

After completing this lesson, you will be able to:

- **Understand the Agent vs. Actor Pattern:** specific to browser automation.
- **Use the Browser Use Library:** to create agents that can "see" and interact with web pages.
- **Implement Vision-Based Extraction:** using LLMs to interpret visual page content.
- **Handle Dynamic Content:** navigating modern single-page applications (SPAs).

## Key Concepts

### Agent vs. Actor Pattern

When automating browser interactions, we distinguish between two modes:

- **Agent:** The "Brain". It receives a high-level goal (e.g., "Find the cheapest flight to Tokyo") and autonomously figures out the steps. It decides where to click, what to type, and how to navigate based on the current page state. This is ideal for dynamic or unknown websites.
- **Actor:** The "Hands". It executes precise, pre-defined actions (e.g., "Click the button with ID `#submit`"). This is faster and more reliable for known, stable environments but brittle if the site changes.

### Browser Use Library

[Browser Use](https://github.com/browser-use/browser-use) is a Python library that combines the power of **Playwright** (for browser control) with **LLMs** (for reasoning and vision).

#### Key Features:
- **Vision Capabilities:** Uses GPT-4o or compatible vision models to "see" the page, allowing it to interact with elements based on their visual appearance rather than just code selectors.
- **Self-Correction:** If an action fails (e.g., a popup appears), the agent can detect the error and try a different approach.
- **Structured Output:** Can extract data from pages and return it in structured formats like JSON or Pydantic models.

### Vision-Based Extraction

Traditional scrapers rely on HTML structure (CSS selectors, XPath). If the site layout changes, the scraper breaks. Vision-based agents look at the rendered page screenshot. This allows them to:
- Identify buttons by their icon or label.
- Understand charts and graphs.
- Adapt to mobile vs. desktop layouts automatically.

## Code Sample

Here is a simple example of a Browser Use agent:

```python
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI
import asyncio

async def main():
    # Initialize the browser
    browser = Browser(headless=False)

    # Initialize the LLM (must support vision)
    llm = ChatOpenAI(model="gpt-4o")

    # Create the agent with a task
    agent = Agent(
        task="Go to reddit.com, find the top post in r/python, and print its title.",
        llm=llm,
        browser=browser
    )

    # Run the agent
    history = await agent.run()

    # Clean up
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Additional Resources

- [Browser Use Documentation](https://docs.browser-use.com/)
- [Playwright Python](https://playwright.dev/python/)
- [LangChain Documentation](https://python.langchain.com/)

## Previous Lesson

[Microsoft Agent Framework](../14-microsoft-agent-framework/README.md)
