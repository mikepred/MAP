# Language Excellence

This document outlines guidelines for writing high-quality, idiomatic code across various programming languages, with specific attention to Python. Adherence to these principles ensures consistency, readability, and maintainability.

## Python Specifics

1.  **Pythonic Principles:**
    *   Strive for code that is simple, readable, and explicit (reflecting `import this`).
    *   Utilize list comprehensions, generator expressions, and built-in functions effectively.
    *   Follow PEP 8 for style and PEP 257 for docstring conventions rigorously.
    *   Employ f-strings for string formatting (Python 3.6+).
    *   Prefer `pathlib` for path manipulations over `os.path`.
2.  **Type Hinting (Python):**
    *   Generate all new Python code with comprehensive type hints using the `typing` module. This is non-negotiable.
    *   For existing Python code, infer and add type hints where appropriate and unambiguous.
3.  **Virtual Environments & Dependencies (Python):**
    *   Assume Python code will be run in a virtual environment.
    *   When suggesting new libraries, instruct the user to add them to `requirements.txt` or `pyproject.toml` (mentioning Poetry or PDM conventions if context suggests). Default to `requirements.txt` if no other context is available.

## General Language Best Practices (Apply to all languages unless specified)

1.  **Idiomatic Code:** Adhere to established idioms and community best practices for the language in use (e.g., effective Java, idiomatic JavaScript).
2.  **Standard Libraries:** Leverage standard libraries first before suggesting external dependencies, unless an external library offers a significant advantage explicitly requested or clearly beneficial.

## Related Rules
- [00-core-primary-directive.md](00-core-primary-directive.md)
- [11-code-architecture-principles.md](11-code-architecture-principles.md)
- [20-workflow-documentation-communication.md](20-workflow-documentation-communication.md)
- [21-workflow-tooling-security.md](21-workflow-tooling-security.md)
