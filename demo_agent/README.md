# Demo AI Agent

This directory contains a standalone demo AI agent for the "AI Agents for Beginners" course.
It demonstrates the following concepts:
- **Tool Use Design Pattern** (Lesson 4): The agent uses a custom plugin to access course content.
- **RAG (Retrieval Augmented Generation)** (Lesson 5): The agent retrieves relevant information from the `STUDY_GUIDE.md` file.
- **Agentic Memory** (Lesson 13): The agent maintains conversation history.
- **Semantic Kernel Framework** (Lesson 2): Uses the latest Python SDK (v1.x).

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Copy `.env.example` to `.env` and fill in your API keys.
   ```bash
   cp .env.example .env
   ```

   You can use one of the following:
   - **GitHub Models (Free):** Set `GITHUB_TOKEN` (get one from [GitHub Settings](https://github.com/settings/tokens)) and `OPENAI_MODEL_NAME`.
   - **Azure OpenAI:** Set `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`.
   - **Standard OpenAI:** Set `OPENAI_API_KEY` and `OPENAI_MODEL_NAME`.

3. **Run the Agent:**
   ```bash
   python agent.py
   ```

## Files

- `agent.py`: The main agent script.
- `course_plugin.py`: A Semantic Kernel plugin that parses and searches the study guide.
- `test_plugin.py`: A utility script to verify the plugin without running the full agent.
- `requirements.txt`: Python dependencies.

## Features

- Ask questions like "What is RAG?" or "Explain Lesson 4".
- The agent will search the study guide and provide an answer based on the content.
- It cites the lesson number in its response.
