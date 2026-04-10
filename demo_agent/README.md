# Demo Agent

This is a RAG-based course assistant implemented with Semantic Kernel that queries `STUDY_GUIDE.md`.

## Setup
1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables in an `.env` file:
   - For Azure OpenAI: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`
   - For OpenAI: `OPENAI_API_KEY`, `OPENAI_CHAT_MODEL_ID`
   - For GitHub Models: `GITHUB_TOKEN`, `GITHUB_MODEL_ID`

## Usage
Run the agent:
```bash
python agent.py
```
Run tests:
```bash
python test_plugin.py
```