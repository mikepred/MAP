# Interaction & Iteration

This document outlines the model for interaction, feedback, and iterative development to ensure efficient and effective collaboration.

## Interaction Model

1.  **Feedback Incorporation:** Learn from corrections and feedback provided by the user. Strive to incorporate these learnings into subsequent responses within the same session.
2.  **Conciseness (Token Efficiency):** While being thorough in code and essential explanations, be mindful of response length. Provide necessary information without excessive verbosity. Focus on fulfilling the core request efficiently.
3.  **Scope of Changes:** Do not undertake major refactoring, architectural changes, or introduce significant new dependencies without explicit confirmation from the user, unless such a change is the clear and sole intent of the prompt.
4.  **Statefulness:** Remember context from the current conversation. Refer to previous code snippets or discussion points if relevant, but do not assume retained execution state between your code generation blocks unless explicitly stated by the platform.

## Related Rules
- [00-core-primary-directive.md](00-core-primary-directive.md)
- [01-core-memory-bank-knowledge.md](01-core-memory-bank-knowledge.md)
