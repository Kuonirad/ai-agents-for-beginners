# Demo AI Agent

This directory contains a demo AI agent that can answer questions about the "AI Agents for Beginners" course. It uses the content from `STUDY_GUIDE.md` as its knowledge base.

## Features

- **RAG-based Question Answering**: Uses the Semantic Kernel framework to search the study guide and answer user questions.
- **Search-Only Mode**: If no API keys are provided, it falls back to a simple keyword search mode.
- **Support for Multiple Providers**: Works with OpenAI, Azure OpenAI, and GitHub Models.

## Setup

1. **Install Dependencies**:
   Ensure you have installed the required packages:
   ```bash
   pip install semantic-kernel python-dotenv
   ```
   (Note: `semantic-kernel` installation might require additional dependencies depending on the version)

2. **Configure Environment Variables**:
   Create a `.env` file in the root directory (or use the existing one) with one of the following configurations:

   **For OpenAI:**
   ```
   OPENAI_API_KEY=your-key
   ```

   **For Azure OpenAI:**
   ```
   AZURE_OPENAI_API_KEY=your-key
   AZURE_OPENAI_ENDPOINT=your-endpoint
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-deployment
   ```

   **For GitHub Models:**
   ```
   GITHUB_TOKEN=your-token
   ```

## Usage

Run the agent from the repository root:

```bash
python3 demo_agent/main.py
```

### Interactive Mode

Once running, you can chat with the agent:
```
Agent: Hello! I am your course assistant. Ask me anything about the AI Agents course.
User: What is RAG?
Agent: RAG stands for Retrieval-Augmented Generation...
```

### Search-Only Mode

If no API keys are found, the agent will run in a limited mode:
```
WARNING: No API keys found...
To search, type: search <query>
To read a lesson, type: lesson <number>
User: search RAG
Agent: ## 5. Agentic RAG...
```
