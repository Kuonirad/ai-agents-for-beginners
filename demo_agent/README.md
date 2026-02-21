# Demo AI Agent - Course Assistant

This is a demonstration of an AI Agent built using **Semantic Kernel**. It implements the **Tool Use** and **RAG** (Retrieval Augmented Generation) design patterns taught in the "AI Agents for Beginners" course.

## Features

- **Course Plugin**: A custom plugin (`course_plugin.py`) that searches the `STUDY_GUIDE.md` for answers.
- **RAG Pattern**: The agent retrieves relevant course content before generating an answer.
- **Tool Use**: The agent autonomously decides when to search the study guide.
- **Support for GitHub Models & Azure OpenAI**: Works with free GitHub Models or Azure OpenAI Service.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    (Note: You can also use the root `requirements.txt`)

2.  **Configure Environment**:
    Create a `.env` file in the root directory (or use the existing one) with your API keys.

    **For GitHub Models (Free):**
    ```env
    GITHUB_TOKEN=your_github_token
    OPENAI_MODEL_ID=gpt-4o
    ```

    **For Azure OpenAI:**
    ```env
    AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
    AZURE_OPENAI_API_KEY=your_key
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
    ```

    **For OpenAI:**
    ```env
    OPENAI_API_KEY=sk-...
    OPENAI_MODEL_ID=gpt-4o
    ```

3.  **Run the Agent**:
    ```bash
    python demo_agent/agent.py
    ```

## How it Works

1.  The `CoursePlugin` loads the `STUDY_GUIDE.md` file.
2.  The `agent.py` initializes the Semantic Kernel and registers the plugin.
3.  When you ask a question (e.g., "What is RAG?"), the LLM calls `CoursePlugin.search_content("RAG")`.
4.  The plugin returns the relevant section from the study guide.
5.  The LLM uses this information to answer your question.
