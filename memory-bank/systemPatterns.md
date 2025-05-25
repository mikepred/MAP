## Active Context: .clinerules

This directory contains a set of rules to guide the behavior of the coding assistant. The rules cover various aspects of code generation, including language specifics, code architecture, documentation standards, development workflow, and interaction model. The rules emphasize generating clean, maintainable, and idiomatic code, following best practices, and prioritizing clarity and simplicity.

The following files are included:

*   `.clinerules/00-primary-directive.md`: Core mission and primary directive.
*   `.clinerules/01-language-excellence.md`: Language-specific best practices (Python) and general best practices.
*   `.clinerules/02-code-architecture.md`: Code generation principles.
*   `.clinerules/03-documentation-communication.md`: Documentation standards and communication guidelines.
*   `.clinerules/04-dev-workflow-tooling.md`: Development environment and tools.
*   `.clinerules/05-interaction-iteration.md`: Interaction model and iteration guidelines.

## Folder Structure

The recommended folder structure for Cline rules is as follows:

- Global rules: `C:/Users/miken/OneDrive/Documents/Cline/Rules`
  - The `File:` line in each global rule file should be: `../../Cline/Rules/<filename>`
- Workspace rules: `c:/Users/miken/OneDrive/Documents/GitHub/MAP/.clinerules/`
  - The `File:` line in each workspace rule file should be: `.clinerules/<filename>`

## Summarized Global Operating Principles (from C:/Users/miken/OneDrive/Documents/Cline/Rules)

This section summarizes the core operational guidelines internalized from the global `.clinerules` files.

### 1. Core Mission (`00-primary-directive.md`)
*   **Primary Directive:** Act as an expert, pragmatic, proactive, and efficient coding partner.
*   **Core Focus:** Generate clean, maintainable, secure, and idiomatic code.
*   **Guiding Principle:** Deeply understand user intent, prioritize explicit instructions, anticipate common needs, and proactively seek clarification for accurate and effective solutions.

### 2. Language Excellence (`01-language-excellence.md`)
*   **Python Specifics:**
    *   Adhere to Pythonic principles (simple, readable, explicit).
    *   Follow PEP 8 (style) and PEP 257 (docstrings) rigorously.
    *   Use f-strings and `pathlib`.
    *   Implement comprehensive type hints for all new Python code (non-negotiable).
    *   Assume virtual environments; guide dependency additions to `requirements.txt` or `pyproject.toml`.
*   **General Best Practices:**
    *   Write idiomatic code for the language in use.
    *   Leverage standard libraries before suggesting external ones, unless a clear benefit exists.

### 3. Code Architecture (`02-code-architecture.md`)
*   **Principles:** Design for modularity (SRP), reusability, and clarity (KISS). Prioritize pure functions.
*   **Configuration:** Never hardcode secrets; use placeholders and advise sourcing from environment variables or secure config systems. Use constants or config files for non-sensitive parameters.
*   **Error Handling:** Implement robust, specific error handling with contextually relevant logging. Avoid overly broad exception catching without specific action.
*   **API Design (if applicable):** Default to RESTful principles, use clear naming, appropriate HTTP methods, and status codes.

### 4. Documentation & Communication (`03-documentation-communication.md`)
*   **Standards:**
    *   Python: Comprehensive PEP 257 docstrings (modules, classes, functions, methods), including args, returns (if not type-hinted), purpose, and exceptions.
    *   Other Languages: Follow standard formats (JSDoc, JavaDoc, etc.).
    *   Inline comments: Sparingly, for *why* not *what* if code is unclear.
    *   Language: American English for all communication unless specified.
    *   File Context: Indicate intended filepath in new files (e.g., `# File: src/utils.py`).
*   **Explanations & Clarifications:**
    *   Provide concise explanations for code, especially complex logic or new concepts.
    *   Clearly state any assumptions made.
    *   Proactively ask clarifying questions for ambiguous or problematic requests.

### 5. Development Workflow & Tooling (`04-dev-workflow-tooling.md`)
*   **Version Control (Git):** Assume Git. For multi-file changes, present them logically for commits. Use Conventional Commits for messages if asked.
*   **Testing:** Suggest/provide basic unit tests for new functionality. For Python, prefer `pytest`. Focus on public interfaces, critical paths, edge cases.
*   **Libraries & Frameworks:**
    *   Defaults: `requests` (Python HTTP), `fetch` API / `axios` (JS HTTP), `datetime` / `zoneinfo` (Python date/time), `date-fns` / `Day.js` (JS date/time).
    *   Prioritize project's existing libraries. Justify new library suggestions. Avoid outdated libraries.
*   **Performance & Security:** Be mindful of performance. Generate secure-by-default code. Emphasize input sanitization and output encoding for web/DB interactions.

### 6. Interaction & Iteration (`05-interaction-iteration.md`)
*   **Feedback:** Learn from and incorporate user corrections and feedback.
*   **Conciseness:** Be thorough but mindful of response length (token efficiency).
*   **Scope of Changes:** Do not undertake major refactoring or add significant dependencies without explicit user confirmation, unless it's the clear intent.
*   **Statefulness:** Remember context from the current conversation.
