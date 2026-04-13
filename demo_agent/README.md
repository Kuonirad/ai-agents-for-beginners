# AI Agents for Beginners - Demo Agent

This directory contains a standalone demo AI agent that acts as a course assistant. It uses Semantic Kernel to implement the "Tool Use" design pattern, utilizing a custom plugin to query the course's `STUDY_GUIDE.md`.

## Prerequisites

- Python 3.12+
- `STUDY_GUIDE.md` present in the repository root

## Setup

1. **Install dependencies:**
   This demo agent has its own requirements, separate from the root repository.
   ```bash
   cd demo_agent
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   The agent supports Azure OpenAI, standard OpenAI, and GitHub Models. Create a `.env` file in the repository root (or copy `.env.example`) and configure the appropriate keys based on your chosen provider:

   **For Azure OpenAI:**
   - `AZURE_OPENAI_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`

   **For standard OpenAI:**
   - `OPENAI_API_KEY`
   - `OPENAI_CHAT_MODEL_ID` (optional, defaults to gpt-4o)

   **For GitHub Models:**
   - `GITHUB_TOKEN`
   - `GITHUB_MODEL_ID` (optional, defaults to gpt-4o)

## Usage

Run the agent interactively:

```bash
cd demo_agent
python agent.py
```

You can ask the agent questions like:
- "What is lesson 1 about?"
- "Can you search the course for information on RAG?"
- "Summarize the metacognition design pattern."

## Testing

To verify the plugin logic without requiring an LLM connection, run the test script:

```bash
cd demo_agent
python test_plugin.py
```
