# Code Architecture

This document outlines principles for generating well-structured, maintainable, and robust code. These guidelines cover modularity, clarity, configuration, error handling, and API design.

## Code Generation Principles

1.  **Modularity & Reusability:**
    *   Design functions and classes with a single responsibility (SRP).
    *   Prioritize pure functions where feasible to enhance testability and reduce side effects.
    *   Avoid deeply nested control structures; refactor for clarity if complexity increases.
2.  **Clarity & Simplicity (KISS):**
    *   Generate the simplest, most direct solution that fulfills the request. Avoid over-engineering.
    *   If multiple viable solutions exist, briefly explain the trade-offs of the chosen one or offer the most common/idiomatic approach.
3.  **Configuration over Hardcoding:**
    *   **Never** hardcode secrets (API keys, passwords, tokens). Use placeholders like `YOUR_API_KEY` and state they should be sourced from environment variables (e.g., using `os.environ.get('YOUR_API_KEY')` in Python, `process.env.YOUR_API_KEY` in Node.js) or a secure configuration management system.
    *   For non-sensitive configurable parameters, use clear constants at the beginning of a file/module or suggest dedicated configuration files (e.g., YAML, JSON, .env).
4.  **Error Handling & Resilience:**
    *   Implement robust and specific error handling (e.g., `try...except SpecificError as e:` in Python; typed errors in Go/Rust; Promises/async-await rejections in JS/TS).
    *   Provide contextually relevant logging for errors, using standard logging modules where available (e.g., `logging` in Python).
    *   Avoid broad `except Exception:`, `catch (e)` (general), or `except:` clauses without re-raising, specific handling, or logging the specific error.
5.  **API Design (When Applicable):**
    *   Default to RESTful principles for API design.
    *   Use clear, consistent naming conventions for endpoints and resources (e.g., plural nouns for collections).
    *   Specify appropriate HTTP methods (GET, POST, PUT, DELETE, PATCH, etc.).
    *   Suggest proper HTTP status codes for responses (e.g., 200, 201, 204, 400, 401, 403, 404, 500).

## Related Rules
- [10-code-language-excellence.md](10-code-language-excellence.md)
- [12-code-modularity-extensibility.md](12-code-modularity-extensibility.md)
- [21-workflow-tooling-security.md](21-workflow-tooling-security.md)
