# Building Computer Use Agents (CUA) with Browser Use

## Introduction

This lesson covers how to build an intelligent web automation agent using Playwright and Browser-Use. You'll learn how to integrate these tools to create agents that can navigate the web, understand visual content, and perform complex tasks like finding the cheapest Airbnb.

## Learning Goals

After completing this lesson, you should be able to:
- **Understand Playwright + Browser-Use Integration**: How to combine browser management with AI automation.
- **Implement Vision-Based Extraction**: Enable AI to "see" and read content from web pages.
- **Use Structured Data Extraction**: Extract data into type-safe Pydantic models.
- **Differentiate Agent vs Actor Patterns**: Know when to use autonomous navigation vs deterministic actions.

## Content

This lesson focuses on the **Browser Use** library, which allows LLMs to interact with web browsers.

### Key Concepts

- **Agent Pattern**: The AI autonomously determines the steps to reach a goal (e.g., "Find the cheapest hotel"). This is best for dynamic environments.
- **Actor Pattern**: The AI executes deterministic, pre-defined actions using selectors. This is best for known, stable structures.
- **Vision Capabilities**: Using models like GPT-4o to analyze screenshots allows the agent to interact with visual elements that might be hard to select via code.

## Sample Code

- [Finding the Cheapest Airbnb](./15-browser-use.ipynb): A notebook demonstrating how to build an agent that searches Airbnb for listings in Stockholm, extracts prices using vision, and identifies the cheapest option.

## Resources

- [Browser Use Documentation](https://docs.browser-use.com/)
- [Playwright Python Documentation](https://playwright.dev/python/docs/intro)
