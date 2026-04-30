# Demo AI Agent

This directory contains a RAG-based course assistant implemented with Semantic Kernel. The agent parses the `CONCEPTS_EXPLAINED.md` file from the repository root to answer questions related to the "AI Agents for Beginners" course.

## Setup Instructions

1. Ensure you have the required dependencies installed. Navigate to this directory and install them:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in this directory with your credentials. You can use Azure OpenAI, OpenAI, or GitHub Models.

   **Azure OpenAI:**
   ```env
   AZURE_OPENAI_API_KEY="your-azure-key"
   AZURE_OPENAI_ENDPOINT="your-azure-endpoint"
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="your-azure-deployment-name"
   ```

   **OpenAI:**
   ```env
   OPENAI_API_KEY="your-openai-key"
   OPENAI_CHAT_MODEL_ID="your-model-id"
   ```

   **GitHub Models:**
   ```env
   GITHUB_TOKEN="your-github-token"
   GITHUB_MODEL_ID="your-model-id"
   ```

## Usage

To start the demo agent in interactive mode:
```bash
python agent.py
```

To test the `CoursePlugin` functionality without needing active AI service credentials:
```bash
python test_plugin.py
```

## Dependencies
- `semantic-kernel>=1.15.0`
- `python-dotenv`
