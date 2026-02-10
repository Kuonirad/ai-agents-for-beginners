# AI Agents Course Assistant

This is a demo AI agent built with Semantic Kernel and GitHub Models. It is designed to help you navigate the "AI Agents for Beginners" course by answering questions about the lessons and the study guide.

## Features

- **Course RAG:** Uses the `CoursePlugin` to search `STUDY_GUIDE.md` and read individual lesson READMEs.
- **Tool Use:** Demonstrates the Tool Use design pattern (Lesson 4) by automatically calling functions to retrieve information.
- **GitHub Models Integration:** Uses `gpt-4o` via GitHub Models (free tier) or Azure OpenAI.

## Setup

1. **Install Dependencies:**
   Ensure you have installed the root dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the repository root (copy from `.env.example`).
   You need at least one of the following:

   - **GitHub Models (Free):**
     ```env
     GITHUB_TOKEN=your_github_token
     ```
     (Get a token from [GitHub Marketplace](https://github.com/marketplace/models))

   - **Azure OpenAI:**
     ```env
     AZURE_OPENAI_API_KEY=your_key
     AZURE_OPENAI_ENDPOINT=your_endpoint
     AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your_deployment_name
     ```

   - **OpenAI:**
     ```env
     OPENAI_API_KEY=your_key
     ```

## Running the Agent

Run the agent from the repository root:

```bash
python3 demo_agent/agent.py
```

## Example Interactions

- "What is the difference between an Agent and an Actor?" (Searches Study Guide/Lesson 15)
- "Summarize Lesson 5." (Reads Lesson 5 README)
- "How do I use the Tool Use pattern?" (Searches relevant lessons)

## Code Structure

- `agent.py`: Main entry point. Initializes the Kernel, configures the AI service, and runs the chat loop.
- `course_plugin.py`: A Semantic Kernel plugin that provides functions to search and read course content.
