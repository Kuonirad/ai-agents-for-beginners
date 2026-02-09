# AI Agents Course Assistant

This directory contains a demo AI agent that helps users navigate the "AI Agents for Beginners" course content. It uses Semantic Kernel to interact with the `STUDY_GUIDE.md` file.

## Features

- **LLM Mode:** Uses OpenAI or Azure OpenAI to answer natural language questions about the course.
- **Search Mode:** Fallback mode that performs keyword search on the study guide if no API keys are configured.
- **Course Plugin:** A custom plugin that extracts lesson content and performs searches.

## Setup

1. **Install Dependencies:**
   Ensure you have installed the requirements from the root directory:
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Configure API Keys:**
   Create a `.env` file in the root directory (copy from `.env.example`) and set one of the following:
   - `OPENAI_API_KEY` (and optionally `OPENAI_MODEL_ID`)
   - `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
   - `GITHUB_TOKEN` (Note: Script may require manual base_url config for GitHub Models, otherwise it falls back to Search Mode)

## Running the Agent

Run the agent from the root directory:

```bash
python demo_agent/agent.py
```

Or from within the directory:

```bash
cd demo_agent
python agent.py
```

## Usage

- **LLM Mode:** Ask questions like "What is covered in lesson 5?" or "Explain the difference between Agent and Actor".
- **Search Mode:** Enter keywords like "context engineering" or "RAG" to find relevant sections in the study guide.
