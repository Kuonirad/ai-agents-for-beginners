import re
import os

def load_course_content(filepath: str) -> dict:
    """
    Reads the study guide and returns a dictionary where keys are lesson numbers
    and values are the content of that lesson.
    """
    content = {}
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return {}

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}

    # Regex to find sections starting with "## [number]. [Title]"
    # It captures (number), (title), (body)
    # The body matches until the next "## " or end of string.
    pattern = re.compile(r'## (\d+)\. (.*?)\n(.*?)(?=\n## |\Z)', re.DOTALL)

    matches = pattern.findall(text)

    for match in matches:
        lesson_num = int(match[0])
        title = match[1].strip()
        body = match[2].strip()
        content[lesson_num] = {
            "title": title,
            "body": body,
            "full_text": f"## {lesson_num}. {title}\n\n{body}"
        }

    return content

if __name__ == "__main__":
    # Simple test when running directly
    # Assumes running from repo root
    path = "STUDY_GUIDE.md"
    if not os.path.exists(path):
        # try one level up if running from inside demo_agent
        path = "../STUDY_GUIDE.md"

    data = load_course_content(path)
    print(f"Loaded {len(data)} lessons.")
    if 1 in data:
        print(f"Lesson 1 Title: {data[1]['title']}")
