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
