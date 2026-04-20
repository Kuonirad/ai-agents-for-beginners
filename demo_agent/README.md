# Demo Agent

This directory contains a RAG-based course assistant implemented with Semantic Kernel (v1.15.0+) that queries the `CONCEPTS_EXPLAINED.md` file from the repository root.

## Setup Instructions

1. Install dependencies specific to this demo agent (from inside the `demo_agent` directory):
   ```bash
   pip install -r requirements.txt
   ```

2. Provide credentials via a `.env` file or environment variables. The agent supports three models, and expects one of the following setups:
   - **GitHub Models:** `GITHUB_TOKEN` and `GITHUB_MODEL_ID`
   - **Azure OpenAI:** `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
   - **OpenAI:** `OPENAI_API_KEY` and `OPENAI_CHAT_MODEL_ID`

3. Run the agent:
   ```bash
   python agent.py
   ```

## Dependencies
- `semantic-kernel>=1.15.0`
- `python-dotenv`