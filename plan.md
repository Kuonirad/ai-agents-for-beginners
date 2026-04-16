1. **Create demo_agent directory setup**
   - Create the `demo_agent` directory with `__init__.py` to make it a Python package.
   - Create `demo_agent/requirements.txt` containing `semantic-kernel>=1.15.0` and `python-dotenv`.
2. **Implement CoursePlugin**
   - Create `demo_agent/course_plugin.py`.
   - Implement `CoursePlugin` class that parses `STUDY_GUIDE.md` using the regex `re.split(r'(## \d+\. .*?)\n', text)`.
   - Add `get_lesson_content` and `search_content` kernel functions.
   - Handle `FileNotFoundError` gracefully.
3. **Implement test script for CoursePlugin**
   - Create `demo_agent/test_plugin.py` to test the parsing and searching functionality offline.
4. **Implement the main AI Agent**
   - Create `demo_agent/agent.py`.
   - Use `semantic-kernel` with `FunctionChoiceBehavior.Auto()` to allow dynamic plugin usage.
   - Configure support for Azure OpenAI, standard OpenAI, or GitHub Models (using `AsyncOpenAI` client with custom `base_url`).
   - Implement a robust chat loop with error handling (e.g., `EOFError`).
5. **Add README**
   - Create `demo_agent/README.md` with setup and usage instructions.
6. **Pre-commit checks**
   - Ensure proper testing, verification, review, and reflection are done using `pre_commit_instructions`.
7. **Submit the changes**
   - Submit the repository changes with a descriptive commit message.
