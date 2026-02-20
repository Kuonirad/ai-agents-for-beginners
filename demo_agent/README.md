# AI Agents Course Demo Agent

This is a simple AI agent built with Microsoft Semantic Kernel. It demonstrates the **Tool Use Design Pattern** by using a custom plugin (`CoursePlugin`) to retrieve information from the course study guide (`STUDY_GUIDE.md`).

## Prerequisites

1. Python 3.10+
2. An OpenAI API Key, Azure OpenAI API Key, or GitHub Token (for GitHub Models).

## Setup

1. Navigate to this directory:
   ```bash
   cd demo_agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in this directory (or the root) with your API keys:

   **For OpenAI:**
   ```env
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL_ID=gpt-4o
   ```

   **For Azure OpenAI:**
   ```env
   AZURE_OPENAI_API_KEY=...
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
   ```

   **For GitHub Models:**
   ```env
   GITHUB_TOKEN=ghp_...
   OPENAI_MODEL_ID=gpt-4o
   ```

## Running the Agent

Run the agent script:

```bash
python agent.py
```

## Testing

You can verify that the plugin is correctly reading the study guide by running:

```bash
python test_agent.py
```

## How it Works

- **`agent.py`**: Initializes the Semantic Kernel, configures the AI service, and runs the chat loop. It uses `FunctionChoiceBehavior.Auto()` to allow the LLM to automatically call the `CoursePlugin` when needed.
- **`course_plugin.py`**: Defines a plugin with two functions:
  - `get_lesson_content(lesson_number)`: Retrieves the full content of a lesson.
  - `search_content(query)`: Searches the study guide for keywords.
- **`STUDY_GUIDE.md`**: The source of truth for the course content.

## Example Interaction

```text
User: What is lesson 4 about?
Assistant: Lesson 4 covers the **Tool Use Design Pattern**...

User: How do I build trustworthy agents?
Assistant: To build trustworthy agents (Lesson 6), you should focus on safety, security, and reliability...
```
