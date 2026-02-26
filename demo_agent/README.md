# Course Expert Agent Demo

This is a demonstration of an AI Agent built using **Semantic Kernel** and the **Tool Use Design Pattern**. The agent uses Retrieval Augmented Generation (RAG) principles to answer questions about the "AI Agents for Beginners" course by querying the `STUDY_GUIDE.md`.

## Features
- **Semantic Kernel Integration**: Uses the latest Semantic Kernel Python SDK.
- **Custom Plugin**: Implementing a `CoursePlugin` to read and search the study guide.
- **Auto Function Calling**: The LLM automatically decides when to call the plugin functions.
- **RAG-Lite**: Retrieves specific lesson content to ground its answers.

## Prerequisites
- Python 3.12+
- Dependencies listed in the root `requirements.txt`.

## Setup

1.  **Install Dependencies** (if not already done):
    ```bash
    pip install -r ../requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory (or use the existing one) and add your API keys:

    ```env
    # For OpenAI
    OPENAI_API_KEY=your-key-here
    OPENAI_MODEL_NAME=gpt-4

    # OR for Azure OpenAI
    AZURE_OPENAI_API_KEY=your-key-here
    AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-deployment-name

    # OR for GitHub Models
    GITHUB_TOKEN=your-github-token
    GITHUB_MODEL_NAME=gpt-4o
    ```

## Running the Agent

To run the agent in demo mode (processes a list of predefined questions):

```bash
python3 -m demo_agent.agent
```

To run the agent in interactive mode:

```bash
python3 -m demo_agent.agent --interactive
```

## Testing the Plugin

You can verify the plugin logic (file reading and searching) without making LLM calls by running the test script:

```bash
python3 -m demo_agent.test_plugin
```
