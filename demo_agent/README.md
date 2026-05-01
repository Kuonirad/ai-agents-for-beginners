# Demo AI Agent

This folder contains a demo AI agent built using Semantic Kernel that queries the `CONCEPTS_EXPLAINED.md` file to answer user questions about the course.

## Dependencies
- `semantic-kernel>=1.15.0`
- `python-dotenv`

## Setup

1. Make sure you are in the `demo_agent` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` in the root directory (or use a `.env` in this directory) and configure your model API keys.
   - For Azure: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
   - For GitHub Models: `GITHUB_TOKEN`, `GITHUB_MODEL_ID`
   - For OpenAI: `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL_ID`

## Usage

Run the agent:

```bash
python agent.py
```
