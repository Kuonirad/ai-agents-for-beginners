# AI Agents Course Assistant Demo

This directory contains a demo AI agent that acts as a course assistant for the "AI Agents for Beginners" course. It uses Retrieval Augmented Generation (RAG) concepts by dynamically searching and retrieving content from the `STUDY_GUIDE.md` file using Semantic Kernel plugins.

## Features

- Built with **Semantic Kernel (v1.15.0+)**.
- Utilizes the **Tool Use** design pattern via `FunctionChoiceBehavior.Auto()`.
- Supports multiple LLM backends:
  - Azure OpenAI
  - Standard OpenAI
  - GitHub Models (Free tier available)
- Custom `CoursePlugin` parses and searches the course study guide.

## Setup

1. **Navigate to the demo agent directory:**
   ```bash
   cd demo_agent
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This demo requires `semantic-kernel>=1.15.0` which may differ from the root requirements.*

3. **Configure Environment Variables:**
   Create a `.env` file in the root of the repository (or in the `demo_agent` directory) with one of the following configurations:

   **For GitHub Models (Easiest, Free):**
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_MODEL_ID=gpt-4o  # Optional, defaults to gpt-4o
   ```

   **For OpenAI:**
   ```env
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_CHAT_MODEL_ID=gpt-4o  # Optional, defaults to gpt-4o
   ```

   **For Azure OpenAI:**
   ```env
   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-chat-deployment-name
   ```

## Usage

**Run the offline plugin test:**
```bash
python test_plugin.py
```
This script tests the study guide parsing and searching logic without needing any API keys.

**Run the interactive AI Agent:**
```bash
python agent.py
```
Start asking questions about the course, such as "What is Agentic RAG?" or "Summarize the lesson on the Microsoft Agent Framework."
