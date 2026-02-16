# AI Agents for Beginners - Demo Agent

This is a RAG-based course assistant implemented with **Semantic Kernel** (Python). It uses the content from `STUDY_GUIDE.md` to answer questions about the course.

## Prerequisites

- Python 3.12+
- `pip`

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory (or `demo_agent/`) with your API keys:

   ```env
   # For Azure OpenAI
   AZURE_OPENAI_API_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

   # OR For OpenAI
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o

   # OR For GitHub Models
   GITHUB_TOKEN=ghp_...
   GITHUB_MODEL_NAME=gpt-4o
   ```

   *Note: If no API keys are provided, the agent will run in "Manual Mode" using simple keyword search.*

## Usage

Run the agent from the repository root:

```bash
python demo_agent/agent.py
```

### Features

- **Course Q&A:** Ask questions like "What are the design patterns?" or "Explain Lesson 5".
- **Lesson Retrieval:** Ask "Show me Lesson 3".
- **Manual Mode:** Works without LLM using direct keyword search if no API keys are found.

## How it Works

- **`course_plugin.py`**: Parses the `STUDY_GUIDE.md` file and exposes functions to retrieve lesson content and search for keywords.
- **`agent.py`**: Initializes the Semantic Kernel, configures the AI service, and runs the chat loop. It uses the `CoursePlugin` to provide context to the LLM.
