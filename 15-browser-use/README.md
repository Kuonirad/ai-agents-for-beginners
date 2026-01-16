# Browser Use

### Introduction

This lesson will cover:

-   Enabling agents to autonomously interact with web browsers
-   Using the `browser-use` library with Playwright
-   Implementing Agent and Actor patterns for web automation
-   Using Vision-LLMs (like GPT-4o) for visual decision making

## Learning Goals

After completing this lesson, you will know how to:

-   Create an AI agent that can browse the web to achieve goals
-   Extract structured data from websites using AI
-   Understand the difference between high-level Agent navigation and low-level Actor interactions
-   Integrate browser automation into your AI workflows

## Code Samples

Code samples for [Browser Use](https://github.com/browser-use/browser-use) can be found in this repository under `15-browser-use/code_samples/`.

## Understanding Browser Use

The `browser-use` library bridges the gap between Large Language Models and web browsers. While LLMs are powerful reasoning engines, they cannot natively "click" buttons or "scroll" pages. `browser-use` provides this interface by:

1.  **Capturing State**: It takes screenshots and extracts the DOM (Document Object Model) of the current page.
2.  **Reasoning**: It sends this visual and textual information to a Vision-LLM (like GPT-4o or Claude 3.5 Sonnet).
3.  **Acting**: The LLM decides the next action (e.g., "click button #23"), and `browser-use` executes it using Playwright.

### Key Concepts

#### Agent vs. Actor

-   **Agent**: The high-level decision maker. You give it a goal (e.g., "Find the cheapest flight to London"), and it figures out the steps. It handles errors, popups, and dynamic content adaptively.
-   **Actor**: The low-level execution engine. It performs precise actions like clicking, typing, and scrolling. In many cases, you might mix both: letting the Agent navigate complex flows and using the Actor for repetitive, well-defined tasks.

#### Vision-Based Navigation

Modern websites are visual. Buttons might be icons without clear text labels, or layouts might change based on screen size. `browser-use` relies heavily on **Vision-LLMs** to "see" the page. The system highlights interactive elements with numeric labels in the screenshot, allowing the LLM to simply say "click label 5" without needing complex CSS selectors.

#### Structured Output

Beyond just browsing, agents often need to return data. `browser-use` allows you to define a Pydantic model (a data schema), and the agent will extract information from the page to match that schema. This is powerful for scraping jobs, prices, or contact info.

## Setup

To use `browser-use`, you need to install the package and the Playwright browsers:

```bash
pip install browser-use langchain-openai playwright python-dotenv
playwright install
```

You will also need an API key for a Vision-capable LLM, such as OpenAI's GPT-4o (`OPENAI_API_KEY`) or Anthropic's Claude 3.5 Sonnet.

## Examples

### Basic Agent

```python
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

async def main():
    agent = Agent(
        task="Find the latest release of browser-use on GitHub",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

### Structured Data Extraction

```python
from pydantic import BaseModel
from browser_use import Agent, Controller
from langchain_openai import ChatOpenAI

class Product(BaseModel):
    name: str
    price: float

controller = Controller()

async def main():
    agent = Agent(
        task="Go to amazon.com, search for 'laptop', and get the first product details.",
        llm=ChatOpenAI(model="gpt-4o"),
        controller=controller # Use controller to register actions if needed
    )
    # browser-use has built-in extraction capabilities too
    result = await agent.run()

asyncio.run(main())
```

## Additional Resources

-   [Browser Use Documentation](https://docs.browser-use.com/)
-   [GitHub Repository](https://github.com/browser-use/browser-use)
-   [Playwright Python](https://playwright.dev/python/)

## Got More Questions?

Join the [Azure AI Foundry Discord](https://aka.ms/ai-agents/discord) to meet with other learners and get your questions answered.
