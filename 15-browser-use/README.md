# Lesson 15: Browser Use

This lesson introduces the **Browser Use** library, a powerful tool that enables AI agents to interact with web browsers to perform tasks like searching, data extraction, and navigation.

## Overview

Browser Use wraps the Playwright automation library to provide an agentic interface for browser automation. It allows LLMs to "see" web pages using vision capabilities (or DOM parsing) and make autonomous decisions on how to navigate and interact with the page to achieve a goal.

## Key Concepts

### Agent vs. Actor Pattern
- **Agent Pattern**: The AI navigates autonomously based on high-level goals (e.g., "Find the cheapest hotel in Tokyo"). This is ideal for dynamic layouts or when the exact steps are not known in advance.
- **Actor Pattern**: Precise, scripted actions using specific selectors (e.g., "Click button #submit"). This is better for known, stable website structures where speed and reliability are paramount.

### Vision-Based Navigation
Modern AI Agents use vision capabilities (like GPT-4o or equivalent) to analyze screenshots of the web page. This allows them to understand the visual layout, identify interactive elements, and make decisions based on what a human user would see, rather than just relying on the underlying HTML structure.

### Structured Output
Browser Use can extract unstructured data from web pages and convert it into structured, typed objects (e.g., Pydantic models). This ensures that the data collected by the agent is ready for downstream processing or storage.

## Key Technologies

- **[Browser-Use](https://github.com/browser-use/browser-use)**: The core library for agentic browser automation.
- **[Playwright](https://playwright.dev/)**: The underlying engine for controlling the browser (Chromium, Firefox, WebKit).
- **LLMs (e.g., GPT-4o, Azure OpenAI)**: The "brain" that plans actions and interprets page content.

## Code Samples

Code samples are located in the `code_samples/` directory:

- `15-browser-use.ipynb`: A comprehensive Jupyter Notebook demonstrating an Airbnb search agent that finds the cheapest listing in a given city.
- `simple_browser_agent.py`: A simplified, standalone Python script that demonstrates the basic usage of the Browser Use library.

## Prerequisites

- Python 3.12+
- `browser-use` and `playwright` packages installed.
- Access to an LLM provider (OpenAI, Azure OpenAI, Anthropic, etc.).

> **Note:** After installing the dependencies, you must install the Playwright browsers by running:
> ```bash
> playwright install
> ```
