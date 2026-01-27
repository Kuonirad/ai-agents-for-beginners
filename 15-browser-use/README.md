# Lesson 15: Browser Use - Building Computer Use Agents

## Overview
This lesson explores how to build AI Agents capable of interacting with web browsers to perform tasks autonomously. We use the [Browser-Use](https://github.com/browser-use/browser-use) library, which leverages Large Language Models (LLMs) with vision capabilities to navigate websites, extract data, and execute complex workflows.

## Key Concepts

### 1. Agent vs. Actor Pattern
- **Agent**: The autonomous "brain" that receives a high-level goal (e.g., "Find the cheapest flight to Tokyo"). It decides which actions to take based on the current state of the page. It handles dynamic and unpredictable website layouts.
- **Actor**: The deterministic execution layer (based on Playwright) that performs specific actions like clicking, typing, or scrolling. It ensures precision and reliability.

### 2. Vision-Based Extraction
Traditional web scraping relies on brittle CSS selectors or XPath. Browser Use employs **Vision LLMs** (like GPT-4o) to "see" the page as a human does. This allows the agent to:
- Identify elements by their visual context (e.g., "the blue 'Sign Up' button").
- Adapt to layout changes without breaking.
- Understand complex visual information (charts, images).

### 3. Structured Output
Agents can extract unstructured data from web pages and convert it into structured formats (JSON, Pydantic models). This is critical for integrating web data into downstream applications or databases.

### 4. Playwright Integration
Browser Use is built on top of **Playwright**, a powerful browser automation framework. This provides:
- Support for multiple browsers (Chromium, Firefox, WebKit).
- Headless execution for speed.
- Ability to handle modern web features (Single Page Applications, Popups, Authentication).

## Code Samples

- **[15-browser-use.ipynb](./15-browser-use.ipynb)**: A Jupyter notebook demonstrating how to:
  - Set up a Browser Use agent.
  - Define a task.
  - Run the agent and observe its actions.
  - Extract structured data.

## Documentation
For detailed API documentation, parameter reference, and advanced configuration, refer to the local [llms.txt](./llms.txt) file, which contains the full `browser-use` documentation context.
