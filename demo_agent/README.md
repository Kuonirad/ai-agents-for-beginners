# Demo AI Agent

This directory contains a standalone AI agent that demonstrates how to build a RAG-based assistant using the **Semantic Kernel** framework and the course content (`STUDY_GUIDE.md`).

## Features
- **RAG (Retrieval Augmented Generation):** The agent reads the `STUDY_GUIDE.md` file to answer questions about the course.
- **Tool Use:** It uses a custom `CoursePlugin` to retrieve specific lessons or search for keywords.
- **Multi-Model Support:** Works with Azure OpenAI or standard OpenAI (including GitHub Models).

## Prerequisites

1. **Python 3.10+**
2. **API Keys:** You need either an Azure OpenAI key or an OpenAI API key (or GitHub Token).

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Ensure you have a `.env` file in the root directory (or in this directory) with the necessary keys.

   Example for **OpenAI / GitHub Models**:
   ```
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-4o
   ```

   Example for **Azure OpenAI**:
   ```
   AZURE_OPENAI_API_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
   ```

## Usage

Run the agent from the repository root:

```bash
python demo_agent/agent.py
```

Or from within the `demo_agent` directory:

```bash
cd demo_agent
python agent.py
```

## How it works

1. `agent.py`: Initializes the Semantic Kernel and the Chat Service.
2. `course_plugin.py`: A custom plugin that parses `STUDY_GUIDE.md` and exposes functions:
   - `get_lesson_content(lesson_number)`
   - `search_content(query)`
3. The agent loop takes user input, adds it to chat history, and lets the LLM decide whether to call the plugin functions to answer the question.
