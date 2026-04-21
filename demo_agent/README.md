# Demo Agent

This directory contains a demonstration of a RAG-based AI Agent built using Semantic Kernel. The agent answers questions based on the `CONCEPTS_EXPLAINED.md` file located in the root of the repository.

## Dependencies

- `semantic-kernel>=1.15.0`
- `python-dotenv`

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the root of the repository or within `demo_agent/` with the appropriate credentials. You can use Azure OpenAI, OpenAI, or GitHub Models. For example, for OpenAI:
   ```env
   OPENAI_API_KEY="your-openai-api-key"
   OPENAI_CHAT_MODEL_ID="gpt-4o"
   ```

## Usage

1. Run the agent script:
   ```bash
   python agent.py
   ```
2. Interact with the agent in the terminal. Type `exit` to quit.

You can also run `python test_plugin.py` to verify the underlying `CoursePlugin` parses the concepts file correctly.
