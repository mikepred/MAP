# Development Workflow & Tooling

This document outlines guidelines for development environment setup, version control, testing, library usage, and performance/security considerations to ensure a smooth and robust development process.

## Development Environment & Tools

1.  **Version Control (Git):**
    *   Assume Git is the version control system.
    *   When suggesting multi-file changes or new files, present them in a way that's easy for the user to understand and commit logically.
    *   If asked to generate commit messages, follow Conventional Commits guidelines (e.g., `feat: add user authentication endpoint`, `fix: resolve issue with pagination`).
2.  **Testing:**
    *   When generating new functionality (functions, classes, modules), and if appropriate for the scope of the request, provide or suggest basic unit tests.
    *   For Python, prefer `pytest` and structure tests clearly in a separate test file or directory.
    *   Focus tests on public interfaces, critical logic paths, and common edge cases.
3.  **Libraries & Frameworks:**
    *   **Default Library Choices (General - use if no project context dictates otherwise):**
        *   HTTP Requests: `requests` (Python), `fetch` API (JavaScript in browsers/Node.js 18+), `axios` (JavaScript if `fetch` is not suitable or older Node).
        *   Date/Time: Python's `datetime` (with `zoneinfo` for timezones), `date-fns` or `Day.js` (JavaScript). Avoid `moment.js` for new projects.
    *   **Adherence to Project Context:** Prioritize using libraries and frameworks already present in the project context provided by the user.
    *   **New Library Suggestions:** If no existing solution is present, you may suggest widely adopted, modern, and well-maintained options. Justify your choice briefly if it's not an obvious default for the task.
    *   **Avoid Outdated Libraries:** Do not suggest libraries or patterns that are widely considered deprecated or superseded by more modern alternatives, unless the user explicitly requests them or the project context demands it.
4.  **Performance & Security Considerations:**
    *   Be mindful of performance implications. Avoid N+1 query patterns, inefficient loops over large datasets, or blocking operations in asynchronous contexts without due consideration.
    *   Generate code that is secure by default. Apply principles of least privilege.
    *   For web contexts or database interactions, explicitly mention the importance of input sanitization (e.g., to prevent XSS, SQL injection) and output encoding, even if not directly implementing it in a small snippet. Point to standard library or framework features for this (e.g., prepared statements for SQL, template engine auto-escaping for XSS).

## Related Rules
- [10-code-language-excellence.md](10-code-language-excellence.md)
- [11-code-architecture-principles.md](11-code-architecture-principles.md)
- [22-workflow-testing-pytest-default.md](22-workflow-testing-pytest-default.md)
