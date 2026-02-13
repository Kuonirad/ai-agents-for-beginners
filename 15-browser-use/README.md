# Lesson 15: Building Computer Use Agents (CUA) with Browser Use

![Browser Use](./images/browser-use.png)

> **Note**: This lesson uses the [browser-use](https://github.com/browser-use/browser-use) library to build intelligent web automation agents.

## 🎯 Objectives

In this lesson, you will learn how to:

1.  **Integrate Playwright with Browser-Use**: Combine robust browser management with AI-driven automation.
2.  **Use Vision-Based Extraction**: Let AI "see" and understand web pages to extract data without brittle CSS selectors.
3.  **Extract Structured Data**: Get clean, type-safe data (JSON/Pydantic models) from unstructured web content.
4.  **Build a Real-World Agent**: Create an agent that searches Airbnb for the cheapest listings in Stockholm.

## 🤖 What is a Computer Use Agent (CUA)?

A Computer Use Agent is an AI system that can interact with a computer interface (like a web browser) in the same way a human does. Instead of relying solely on backend APIs or rigid scripts, CUAs use **Vision LLMs** (like GPT-4o) to:

-   View the screen (take screenshots).
-   Analyze the UI elements.
-   Decide on the next action (click, type, scroll).
-   Extract information based on visual context.

This approach is much more resilient to UI changes than traditional scraping because the AI "understands" the page layout.

## 🛠️ Prerequisites

Before starting, ensure you have the required packages installed.

### 1. Install Python Dependencies

Add the following to your `requirements.txt` (if not already present) and install:

```bash
pip install -r requirements.txt
```

Key libraries used:
- `browser-use`: The core library for AI agents.
- `playwright`: For browser automation.
- `langchain-openai`: For connecting to OpenAI/Azure OpenAI models.
- `pydantic`: For defining structured data schemas.

### 2. Install Playwright Browsers

You must install the browser binaries for Playwright to work:

```bash
playwright install chromium
```

### 3. Configure Environment Variables

Create or update your `.env` file with your API keys. You can use either Azure OpenAI or standard OpenAI.

**For Azure OpenAI:**
```bash
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**For OpenAI:**
```bash
OPENAI_API_KEY=your_key_here
```

## 📂 Lesson Content

This directory contains two main files:

### 1. `15-browser-use.ipynb` (Jupyter Notebook)
An interactive notebook that walks you through the concepts step-by-step. It demonstrates:
-   Starting Chrome with CDP (Chrome DevTools Protocol).
-   Connecting Browser-Use to an existing browser session.
-   Defining Pydantic models for `AirbnbListing` and `SearchResult`.
-   Running the agent to search and extract prices.

### 2. `airbnb_agent.py` (Python Script)
A standalone, production-ready version of the agent. This script:
-   Automatically detects your AI provider (Azure vs OpenAI).
-   Launches a headless Chrome instance.
-   Runs the full search workflow.
-   Outputs the cheapest listing and potential savings to the console.

## 🚀 How to Run

### Running the Notebook
Open the notebook in VS Code or Jupyter Lab:

```bash
jupyter notebook 15-browser-use/15-browser-use.ipynb
```

### Running the Agent Script
Run the script directly from your terminal:

```bash
python 15-browser-use/airbnb_agent.py
```

## 🧠 Key Concepts

### Agent vs Actor
-   **Agent**: The AI brain. It decides *what* to do based on the task (e.g., "Find the cheapest hotel"). It uses vision to navigate dynamic environments.
-   **Actor**: The deterministic executor. It performs specific actions (e.g., "Click button #submit"). In `browser-use`, the Agent controls the Actor.

### Vision-Based Extraction
Instead of writing code like `soup.find('div', class_='price')`, we simply tell the AI:
> "Extract all listings visible on this page. For each listing, extract the title and price."

The AI looks at the screenshot, identifies the price tags (even if the HTML structure is complex), and returns the data.

### Structured Output
We use `Pydantic` models to force the LLM to return data in a strict JSON format. This ensures that `price` is always a number and `currency` is always a string, making the data easy to use in your code.

```python
class AirbnbListing(BaseModel):
    title: str
    price_per_night: float
    currency: str
```
