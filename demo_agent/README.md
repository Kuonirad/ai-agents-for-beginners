# AI Agents Course Assistant (Demo Agent)

This is a demo AI agent built using [Semantic Kernel](https://github.com/microsoft/semantic-kernel) that answers questions about the "AI Agents for Beginners" course by retrieving information from the [STUDY_GUIDE.md](../STUDY_GUIDE.md).

## Features

- **RAG (Retrieval Augmented Generation):** Uses a custom plugin (`CoursePlugin`) to read and search the course study guide.
- **Function Calling:** Automatically selects the appropriate tool (`get_lesson_content` or `search_content`) based on the user's query.
- **Multi-Service Support:** Supports both OpenAI and Azure OpenAI.

## Prerequisites

- Python 3.10+
- An OpenAI API Key OR Azure OpenAI Service credentials.

## Setup

1. **Install Dependencies:**
   Navigate to this directory and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in this directory (or the root) with your API keys. You can copy `.env.example` from the root and add the following if not present:

   **For OpenAI:**
   ```
   OPENAI_API_KEY=your-key-here
   OPENAI_MODEL_NAME=gpt-4
   ```

   **For Azure OpenAI:**
   ```
   AZURE_OPENAI_API_KEY=your-key-here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4
   ```

## Running the Agent

Run the agent script:

```bash
python agent.py
```

## Example Usage

```
User: What is covered in Lesson 1?
Assistant: Lesson 1 covers the fundamentals of AI Agents...

User: Search for "RAG"
Assistant: Found in:
Lesson 5: Agentic RAG
Lesson 9: Metacognition
...
```
