
# Browser Use

Welcome to Lesson 15 of "AI Agents for Beginners"! In this lesson, we explore how AI Agents can interact with the web using a browser, enabling them to perform tasks like searching, data extraction, and navigation autonomously.

## Introduction

This lesson covers:
- What is **Browser Use** and why it is powerful for AI Agents.
- How to integrate **Playwright** with AI Agents.
- Using **Vision** capabilities (e.g., GPT-4o) to "see" and interact with web pages.
- Extracting structured data from unstructured web content.
- Building an agent that can find the cheapest Airbnb listing.

## Learning Goals

After completing this lesson, you should be able to:
- Understand the **Agent vs. Actor** pattern in browser automation.
- Build an agent that can navigate websites using natural language instructions.
- Use vision-based models to extract information from web pages.
- Implement structured output parsing (using Pydantic) for web data.

## Key Concepts

### Browser Automation for Agents

Traditional web automation (like Selenium or raw Playwright scripts) relies on brittle selectors (CSS, XPath) that break when a website changes. AI Agents using **Browser Use** libraries can:
1.  **See** the page using Vision models.
2.  **Reason** about what to do next based on the visual layout and text.
3.  **Act** by clicking, typing, or scrolling, often without needing predefined selectors.

### Agent vs. Actor

-   **Agent:** Autonomous navigation. You give it a high-level goal (e.g., "Find a hotel in Paris"), and it figures out the steps. It handles dynamic layouts and unexpected popups.
-   **Actor:** Precise, scripted actions. You define specific steps (e.g., "Click button #submit"). This is faster but less flexible.
-   **Hybrid Approach:** Use the Agent to navigate and handle complexity, and the Actor for repetitive, well-defined tasks.

### Vision-Based Extraction

Instead of parsing HTML soup, the agent takes a screenshot of the page and uses a Multimodal LLM (like GPT-4o) to "read" the content. This is particularly useful for:
-   Extracting prices, ratings, and descriptions.
-   Understanding complex visual layouts (e.g., charts, calendars).
-   Identifiying interactive elements that are hard to target with code.

### Structured Data Extraction

Agents can convert the unstructured information on a web page into structured, type-safe data (e.g., JSON or Python objects). By defining a schema (like a Pydantic model), you ensure the agent returns data in exactly the format your application needs.

## Sample Code

-   [Browser Use with Playwright](./code_samples/15-browser-use.ipynb): A complete notebook demonstrating how to build an Airbnb search agent that finds the cheapest listing in Stockholm using Playwright and GPT-4 Vision.

## Resources

-   [Playwright Documentation](https://playwright.dev/)
-   [Browser-Use Library](https://github.com/browser-use/browser-use)
-   [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)

## Previous Lesson

[Microsoft Agent Framework](../14-microsoft-agent-framework/README.md)
