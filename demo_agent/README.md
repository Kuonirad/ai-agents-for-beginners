# Demo Agent

This is a RAG-based course assistant implemented with Semantic Kernel (v1.15.0+) that queries `CONCEPTS_EXPLAINED.md`.

## Setup Instructions

1. Install dependencies:
   ```bash
   cd demo_agent
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` at the root directory:
   You can configure one of the following providers:
   - **GitHub Models**: Set `GITHUB_TOKEN` and `GITHUB_MODEL_ID`
   - **Azure OpenAI**: Set `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
   - **OpenAI**: Set `OPENAI_API_KEY` and `OPENAI_CHAT_MODEL_ID`

## Usage

To run the agent:
```bash
python agent.py
```

## Dependencies
- `semantic-kernel>=1.15.0`
- `python-dotenv`