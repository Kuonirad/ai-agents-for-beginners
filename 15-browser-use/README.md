# Browser Use

This folder contains resources and examples for "Browser Use", a library enabling AI agents to autonomously interact with web browsers.

## Overview

**Browser Use** enables agents to perform tasks like:
- Searching the web (Google, etc.)
- Data extraction from websites.
- Navigation through complex sites.
- Interacting with forms and UI elements.

## Key Technologies

- **Browser-Use Library**: Wraps Playwright to provide an agentic interface.
- **Playwright**: Controls the browser (Chromium, Firefox, WebKit).
- **LLM with Vision**: Uses models like GPT-4o to "see" and interpret the page layout.

## Contents

- `15-browser-user.ipynb`: A Jupyter notebook demonstrating how to use the library.
- `llms.txt`: Comprehensive documentation and API reference for the Browser Use library, including:
    - API endpoints (Check Balance, Me, Uploads, Browser Profiles, Tasks, etc.)
    - Python Client usage.
    - Integration examples (N8N, LangChain).
    - Supported Models (OpenAI, Anthropic, Gemini, etc.).
    - Browser Configuration (Local, Remote, Proxy).

## Getting Started

To run the examples, ensure you have the necessary dependencies installed (see `requirements.txt` in the root) and your API keys configured in `.env`.

See `llms.txt` for detailed documentation on the library's capabilities and configuration.
