"""Prompt templates and parameter options for the code generator."""

TASKS = {
    "Generate new code": "Write new code that fulfils the request below.",
    "Refactor existing code": "Refactor the code provided in the request: improve readability, structure and performance without changing behaviour.",
    "Debug / fix code": "Find and fix the bugs in the code provided. Briefly explain each bug and show the corrected code.",
    "Write unit tests": "Write thorough unit tests for the code or behaviour described in the request.",
    "Explain code": "Explain the code provided step by step, then suggest improvements.",
    "Add docstrings & comments": "Add clear docstrings and helpful comments to the code provided. Do not change logic.",
}

LANGUAGES = {
    "Python": "py", "JavaScript": "js", "TypeScript": "ts", "Java": "java",
    "C++": "cpp", "C#": "cs", "Go": "go", "Rust": "rs", "SQL": "sql",
    "Bash": "sh", "HTML/CSS": "html", "PHP": "php", "Kotlin": "kt", "Swift": "swift",
}

MODELS = ["claude-sonnet-5-5", "claude-opus-5-5", "claude-haiku-5-5"]

COMMENT_LEVELS = {
    "Minimal": "Use comments only where the logic is non-obvious.",
    "Moderate": "Add concise comments for each logical block.",
    "Detailed": "Comment extensively and add full docstrings for every function and class.",
}

SYSTEM_TEMPLATE = """You are an expert senior {language} engineer.

TASK: {task}

RULES:
- Target language: {language}{framework_line}
- Code style: {style}
- {comment_rule}
- {typing_rule}
- {tests_rule}
- {error_rule}
- Put ALL code inside fenced markdown code blocks tagged with the language.
- Keep explanations {explain_length}.
- Never invent libraries or APIs that do not exist.
"""


def build_system_prompt(p: dict) -> str:
    return SYSTEM_TEMPLATE.format(
        language=p["language"],
        task=TASKS[p["task"]],
        framework_line=f" using {p['framework']}" if p.get("framework") else "",
        style=p["style"],
        comment_rule=COMMENT_LEVELS[p["comments"]],
        typing_rule="Use type hints / static types where the language supports them." if p["type_hints"] else "Type annotations are optional.",
        tests_rule="Also include unit tests in a separate code block." if p["include_tests"] else "Do not include tests.",
        error_rule="Include robust error handling and input validation." if p["error_handling"] else "Keep error handling minimal.",
        explain_length={"None": "to nothing (code only, no prose)", "Short": "brief (2-4 sentences)", "Detailed": "detailed, with reasoning and usage examples"}[p["explanation"]],
    )
