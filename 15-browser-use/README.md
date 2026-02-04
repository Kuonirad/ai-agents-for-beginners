# Lesson 15: Building Computer Use Agents with Browser-Use

Welcome to Lesson 15! In this lesson, we explore how to build **Computer Use Agents (CUA)**—AI agents that can autonomously navigate the web, interact with websites, and extract data using a browser, just like a human would.

We utilize **[Browser-Use](https://github.com/browser-use/browser-use)**, a powerful library that bridges the gap between Large Language Models (LLMs) and browser automation tools like **Playwright**.

## 🎯 Learning Objectives

By the end of this lesson, you will understand:
1.  **The Difference between Agent and Actor patterns** in browser automation.
2.  **How to integrate Playwright with Browser-Use** for robust navigation.
3.  **Vision-Based Extraction**: Using Multimodal LLMs (like GPT-4o) to "see" and interpret web pages.
4.  **Structured Data Extraction**: Converting unstructured web content into type-safe Pydantic models.

## 🛠️ Key Technologies

-   **Browser-Use**: The core library for agentic browser automation.
-   **Playwright**: A reliable framework for controlling browsers (Chromium, Firefox, WebKit).
-   **Azure OpenAI / OpenAI**: Providing the LLM (Reasoning) and Vision capabilities.
-   **LangChain**: Used under the hood for model abstraction.

## 🧠 Key Concepts

### Agent vs. Actor Pattern

-   **Agent Pattern**: The AI is given a high-level goal (e.g., "Find the cheapest flight to London"). It autonomously decides which buttons to click, what to type, and how to navigate based on what it sees. This is ideal for dynamic websites or when the specific steps aren't known in advance.
-   **Actor Pattern**: The code executes a precise, pre-defined sequence of actions (e.g., `click('#submit-button')`). This is faster and more reliable for known, static workflows but brittle if the website changes.

### Vision-Based Extraction

Traditional web scraping relies on analyzing the HTML DOM (Document Object Model) and using CSS selectors. This is fragile because website layouts change often.

**Vision-Based Extraction** sends a screenshot of the page to a Vision-capable LLM (like GPT-4o). The model "reads" the image—interpreting prices, text, and layout just like a human—making it incredibly robust to code changes.

## 🚀 Getting Started

### 1. Installation

Ensure you have the required packages installed:

```bash
pip install -r ../requirements.txt
playwright install chromium
```

### 2. Running the Notebook

This lesson is centered around the Jupyter Notebook `15-browser-use.ipynb`. It contains a complete, step-by-step example of building an agent that:
1.  Navigates to **Airbnb**.
2.  Searches for listings in **Stockholm**.
3.  Uses **Vision** to extract prices and ratings.
4.  Identifies the **cheapest option**.

### 3. Example Code Snippet

Here's a simplified example of what you'll build:

```python
import os
from browser_use import Agent, Browser, ChatAzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
llm = ChatAzureOpenAI(
    model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    # Browser-Use automatically picks up AZURE_OPENAI_ENDPOINT and API_KEY
)

# Create the Agent
agent = Agent(
    task="Go to google.com and search for 'AI Agents for Beginners Microsoft'",
    llm=llm,
)

# Run the Agent
async def main():
    await agent.run()

# In a notebook, you can just await agent.run()
```

## ⚠️ Important Considerations

-   **Cost**: Vision-based agents process images, which can consume more tokens than text-only agents. Monitor your API usage.
-   **Latency**: Analyzing screenshots takes more time than parsing HTML.
-   **Ethics**: Always respect `robots.txt` and terms of service when automating website interactions.

## 📚 Resources

-   [Browser-Use Documentation](https://docs.browser-use.com/)
-   [Playwright Python Documentation](https://playwright.dev/python/)
-   [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
