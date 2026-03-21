# AI Agents for Beginners - Demo Agent

This demo agent is a Retrieval-Augmented Generation (RAG) assistant built using [Semantic Kernel](https://github.com/microsoft/semantic-kernel). It acts as a helpful tutor, answering questions about the "AI Agents for Beginners" course by searching and retrieving content from the `STUDY_GUIDE.md` file.

The agent demonstrates the **Tool Use Design Pattern** by automatically invoking a custom `CoursePlugin` to find relevant information based on your questions.

## Features

*   **RAG Implementation:** Dynamically retrieves course content to ground answers in factual data.
*   **Tool Use (Function Calling):** Uses `FunctionChoiceBehavior.Auto()` to let the LLM decide when to call the search functions.
*   **Multiple LLM Backends:** Supports Azure OpenAI, standard OpenAI, or free GitHub Models.
*   **Persistent Chat History:** Maintains conversation context throughout the session.

## Setup Instructions

1.  **Navigate to the demo agent directory:**
    ```bash
    cd demo_agent
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Ensure you have a `.env` file in the root repository directory (or in this directory). You need to provide credentials for *one* of the following services:

    *   **GitHub Models (Free):**
        *   `GITHUB_TOKEN`: Your GitHub Personal Access Token.
        *   `GITHUB_MODEL_NAME` (Optional): The model to use (default: `gpt-4o`).
    *   **Azure OpenAI:**
        *   `AZURE_OPENAI_API_KEY`: Your API key.
        *   `AZURE_OPENAI_ENDPOINT`: Your endpoint URL.
        *   `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`: The name of your chat deployment.
    *   **OpenAI:**
        *   `OPENAI_API_KEY`: Your OpenAI API key.
        *   `OPENAI_MODEL_NAME` (Optional): The model to use (default: `gpt-4o`).

## Usage

**To run the interactive chat agent:**

```bash
python agent.py
```

*Example interaction:*
> **User >** What is the course about?
> **Assistant >** Let me check the study guide for you...
>
> **User >** Summarize the lesson on Tool Use.
> **Assistant >** Lesson 4 covers the Tool Use Design Pattern...

**To run the plugin tests (no API keys required):**

```bash
python test_plugin.py
```

## Dependencies

*   `semantic-kernel>=1.0.0`
*   `python-dotenv`
*   `openai`
