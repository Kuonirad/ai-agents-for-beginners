# Lesson 15: Browser Use - Computer Use Agents

Welcome to Lesson 15 of "AI Agents for Beginners"! In this lesson, we explore **Computer Use Agents (CUA)**, specifically focusing on how agents can interact with web browsers to perform tasks autonomously.

## Introduction

This lesson covers:
- What are Computer Use Agents (CUA)?
- The **Agent vs. Actor** pattern in browser automation.
- How to use the **browser-use** library to build web-navigating agents.
- Vision-based extraction and structured data handling.

## Learning Goals

After completing this lesson, you should be able to:
- Build an AI agent that can navigate websites, click buttons, and fill forms.
- Understand the difference between high-level Agent commands and low-level Actor actions.
- Extract structured data from websites using Vision LLMs (e.g., GPT-4o).
- Implement an Airbnb search agent as a practical example.

## Key Concepts

### Agent vs. Actor

- **Agent:** The "Brain". It receives a high-level goal (e.g., "Find the cheapest hotel in Tokyo") and autonomously decides the steps to take. It uses Vision LLMs to "see" the page and decide where to click. It handles dynamic and unknown website layouts well.
- **Actor:** The "Hands". It executes precise, deterministic actions (e.g., "Click the button with ID `#submit`"). It is fast and reliable for known, static workflows but brittle if the site changes.

### Browser-Use Library

[Browser-Use](https://github.com/browser-use/browser-use) is the library we use in this lesson. It connects LLMs (like GPT-4o) to a headless browser (via Playwright).

**Key Features:**
- **Vision Capabilities:** Uses the LLM's vision capabilities to understand page screenshots.
- **Self-Correction:** If an action fails (e.g., a popup appears), the agent sees the error and tries to fix it (e.g., closes the popup).
- **Structured Output:** Can extract data from pages directly into Pydantic models.

## Setup

Ensure you have installed the required dependencies:

```bash
pip install -r requirements.txt
playwright install
```

You will need an API key for a Vision-capable model (e.g., `OPENAI_API_KEY` for GPT-4o or `AZURE_OPENAI_API_KEY`).

## Code Samples

### 1. Basic Agent
See `15-browser-use.ipynb` for an interactive notebook.

### 2. Airbnb Search Demo
Run the standalone script `airbnb_agent.py` to see a full demo:

```bash
python airbnb_agent.py
```

This agent will:
1.  Go to Airbnb.
2.  Search for a location (e.g., "Paris").
3.  Filter for dates and guests.
4.  Extract the top listings with their prices and ratings into a structured JSON format.

## Additional Resources

- [Browser-Use Documentation](https://docs.browser-use.com/)
- [Playwright Documentation](https://playwright.dev/)

## Previous Lesson

[Microsoft Agent Framework](../14-microsoft-agent-framework/README.md)
