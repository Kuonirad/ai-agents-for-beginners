# Demo AI Agent

This is a demonstration of an AI agent built using the **Semantic Kernel** framework and patterns from the "AI Agents for Beginners" course.

## Features
- **RAG (Retrieval Augmented Generation):** Uses the course `STUDY_GUIDE.md` as a knowledge base.
- **Tool Use:** Demonstrates how to expose functions to the LLM via plugins.
- **Fallback Mode:** If no LLM keys are provided, it falls back to a simple keyword search over the study guide.

## Setup

1. **Install Dependencies:**
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in this directory or set environment variables:
   - `OPENAI_API_KEY` (Required for OpenAI models)
   - `AZURE_OPENAI_API_KEY` (Required for Azure OpenAI)
   - `AZURE_OPENAI_ENDPOINT` (Required for Azure OpenAI)
   - `AZURE_OPENAI_DEPLOYMENT_NAME` (Required for Azure OpenAI)

3. **Run the Agent:**
   ```bash
   python agent.py
   ```

## Usage
Once running, you can ask questions like:
- "What is the Maker-Checker loop?"
- "Tell me about Lesson 5."
- "What frameworks are mentioned in the course?"

If no LLM keys are present, you can search for keywords:
- "search: Agent"
- "lesson: 1"
