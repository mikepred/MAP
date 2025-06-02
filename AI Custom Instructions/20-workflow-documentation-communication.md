# Documentation & Communication

This document outlines the standards for code documentation, comments, and general communication practices to ensure clarity and maintainability.

## Documentation Standards

1.  **Docstrings & Code Comments:**
    *   **Python:** Generate comprehensive PEP 257 compliant docstrings for all modules, classes, functions, and methods. Include arguments, return types (if not covered by type hints, though type hints are preferred), and a concise summary of purpose. Note any exceptions raised.
    *   **Other Languages:** Follow standard documentation comment formats (e.g., JSDoc for JavaScript/TypeScript, JavaDoc for Java, XML docs for C#).
    *   Use inline comments sparingly, only to clarify complex, non-obvious logic, or important assumptions. Comments should explain *why*, not *what* the code is doing if the code itself is clear.
2.  **Language:** All documentation, comments, and communication must be in **American English** unless explicitly specified otherwise by the user for a particular output.
3.  **File Context:** When providing code for a new file, clearly indicate the intended filepath as a comment at the top (e.g., `# File: src/core/utils.py` or `// File: src/core/utils.ts`).

## Explanations & Clarifications

1.  **Concise Explanations:** Provide brief explanations for your code, especially for complex logic, non-trivial choices, or when introducing new concepts/libraries.
2.  **Assumption Declaration:** If you must make an assumption to fulfill a request, state it clearly (e.g., "Assuming you want to sort the results in ascending order...").
3.  **Clarification Protocol:** If a request is ambiguous, incomplete, or potentially problematic (e.g., security risks, overly complex for the apparent goal), **ask clarifying questions** before generating code. Prioritize understanding the user's true intent and constraints.

## Related Rules
- [01-core-memory-bank-knowledge.md](01-core-memory-bank-knowledge.md)
- [10-code-language-excellence.md](10-code-language-excellence.md)
