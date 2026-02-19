# Demo AI Agent

This directory contains a demo AI agent built with **Semantic Kernel** that answers questions about the "AI Agents for Beginners" course.

## Prerequisites

1.  **Python 3.10+**
2.  Install dependencies:
    ```bash
    pip install -r ../requirements.txt
    ```
    (Ensure `semantic-kernel` and `openai` are installed)

## Configuration

Create a `.env` file in this directory or set environment variables for your AI service.

### Option 1: Azure OpenAI
```bash
AZURE_OPENAI_API_KEY="your-key"
AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4"
```

### Option 2: GitHub Models
```bash
GITHUB_TOKEN="your-github-token"
GITHUB_MODEL_NAME="gpt-4o"
```

### Option 3: OpenAI
```bash
OPENAI_API_KEY="sk-..."
OPENAI_MODEL_ID="gpt-4"
```

## Running the Agent

Run the agent script:

```bash
python3 agent.py
```

If no API keys are found, the agent will default to a **keyword search mode** using the local `STUDY_GUIDE.md`.

## Testing

Run the plugin test script to verify content retrieval without an LLM:

```bash
python3 test_agent.py
```
