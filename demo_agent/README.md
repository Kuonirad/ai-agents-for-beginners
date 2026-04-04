# Demo AI Agent

This directory contains a RAG-based course assistant implemented with Semantic Kernel (v1.39+) that queries `STUDY_GUIDE.md`.

## Setup

1. Create a Python virtual environment and activate it.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file based on `.env.example`. Required keys are `OPENAI_API_KEY`, `AZURE_OPENAI_API_KEY`, or `GITHUB_TOKEN`.

## Usage

Run the agent:

```bash
python agent.py
```

Run tests to verify the plugin:

```bash
python test_plugin.py
```
