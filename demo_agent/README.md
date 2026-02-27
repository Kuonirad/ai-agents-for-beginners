# Demo Agent - Course Assistant

This folder contains a simple AI agent built using Semantic Kernel (Python). The agent acts as a course assistant for "AI Agents for Beginners", answering questions by retrieving information directly from the `STUDY_GUIDE.md` file.

## Features

- **RAG (Retrieval Augmented Generation):** Uses a custom plugin (`CoursePlugin`) to read and search the course study guide.
- **Tool Use:** The agent autonomously decides when to use the plugin to fetch lesson content or search for keywords.
- **Multi-Service Support:** Works with OpenAI, Azure OpenAI, and GitHub Models.

## Setup

1. **Install Dependencies:**
   Ensure you have installed the requirements from the root of the repository:
   ```bash
   pip install -r ../requirements.txt
   ```

   Or install the specific requirements for this agent:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Make sure you have a `.env` file in the root directory (or in this directory) with your API keys.

   For **GitHub Models** (Free):
   ```
   GITHUB_TOKEN=your_github_token_here
   GITHUB_MODEL_NAME=gpt-4o
   ```

   For **OpenAI**:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL_NAME=gpt-4o
   ```

   For **Azure OpenAI**:
   ```
   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your_deployment_name
   ```

## Usage

Run the agent from the root of the repository or from the `demo_agent` directory:

```bash
# From the root
python demo_agent/agent.py
```

### Example Interaction

```
User > What is Agentic RAG?
Assistant > (Calls search_content plugin...) Agentic RAG involves an iterative process called the "Maker-Checker Loop"...
```

## Code Structure

- `agent.py`: Main entry point. Initializes the Semantic Kernel, configures the AI service, and runs the chat loop.
- `course_plugin.py`: Defines the `CoursePlugin` class which exposes functions to `get_lesson_content` and `search_content` from the study guide.
- `test_plugin.py`: A script to verify the plugin logic without making LLM calls.
