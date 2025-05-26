# System Patterns

This document outlines the system architecture, key technical decisions, and design patterns employed in the project.

## Text Analyzer Project

### System Architecture (Text Analyzer)

The `analyzer.py` script is designed to follow a linear data processing pipeline. The full target pipeline is:

1. **Data Input & Validation**: Functions like `read_file()`, `validate_file_path()`, and `get_filename_from_user()` handle loading text content from a specified file, ensuring the path is valid and handling potential I/O errors. (Implemented in Module 3B of the lesson plan)
2. **Text Cleaning**: The `clean_text()` (for general sentence structure) and `clean_text_for_words()` (for word analysis) functions normalize text. (Implemented in Module 3C of the lesson plan)
3. **Word Tokenization**: The `count_words()` function internally uses `text.split()` for tokenization after specific cleaning via `clean_text_for_words()`. (Logic from Module 3C, refined in Module 3E)
4. **Token Filtering (Optional)**: Integrated within `count_words()`, the `remove_stop_words()` function can filter common stop words from the token list if enabled. (Introduced in Module 4B)
5. **Frequency Counting**: The `count_words()` function then uses `collections.Counter` to count token occurrences on the (potentially filtered) tokens. (Logic from Module 3C, `count_words` enhanced in Module 4B)
6. **Comprehensive Analysis**: The `analyze_text_complete()` function orchestrates word analysis, sentence analysis, and general statistics generation. (Module 3C/3E)
7. **Results Display**: Functions like `display_complete_analysis()` and `display_summary()` present the analysis results in a user-friendly format. (Implemented in Module 3D/3E)

This pipeline structure ensures a clear and sequential flow of data processing.

### Key Technical Decisions (Text Analyzer)

* **Use of Standard Library**: The project primarily relies on Python's standard library (e.g., `collections`, `string`, `re`, `os`, `pathlib`) to minimize external dependencies and ensure accessibility for beginners.
* **Modular Design**: The script is structured with single-responsibility functions to improve readability, maintainability, and testability.
* **Simple Tokenization**: The `.split()` method is used for tokenization due to its simplicity and effectiveness for basic word separation. More advanced tokenization techniques are discussed conceptually but not implemented in the core script.

### Design Patterns (Text Analyzer)

* **Functional Decomposition**: The problem of text analysis is broken down into a series of smaller, independent functions, each responsible for a specific task. This promotes code reusability and makes the script easier to understand and modify.
* **Pipeline Pattern**: The data flows through a series of processing stages (functions), with each stage transforming the data and passing it to the next.

## Git Branch Visualizer Project

### System Architecture (Git Branch Visualizer)

The `branch_visualizer.py` script follows this architecture:

1. **Git Command Execution**: Uses the `subprocess` module to run `git for-each-ref` (to get local branch names) and `git log` (to get commit history with parent SHAs and references).

2. **Output Parsing**:

    * Parses the output of `git for-each-ref` to create a set of local branch names.
    * Parses the formatted output of `git log` to extract commit SHAs, parent SHAs, and decorator strings (refs like branch names, HEAD).

3. **Reference Analysis**: The `parse_commit_refs_for_local_branches` function specifically analyzes the decorator strings for each commit to determine which local branches point to it.

4. **Mermaid Code Generation**: The `generate_mermaid_code` function iterates through the chronological commit data:

    * Determines a primary line of development (e.g., `main` or `master`) to start the graph.
    * Manages the `checkout` state in Mermaid to draw commits on the correct branch.
    * Creates new `branch` commands in Mermaid as new local branches are encountered.
    * Identifies merge commits (commits with multiple parents) and uses the `merge` command in Mermaid, attempting to identify the source branch of the merge.
    * Constructs a Mermaid `gitGraph LR;` (Left-to-Right) textual representation.

5. **File Output**: Writes the generated Mermaid string to `branch_visualization.mermaid.txt`.

### Key Technical Decisions (Git Branch Visualizer)

* **External Tool Dependency**: Relies on the `git` command-line tool being installed and accessible in the system's PATH.
* **Mermaid for Visualization**: Chose Mermaid `gitGraph` syntax for its simplicity, text-based nature (easy to generate), and wide support in rendering tools (e.g., online editors, IDE extensions, Markdown processors).
* **Focus on Local Branches**: The current implementation prioritizes visualizing the structure of local branches. Remote branches are not explicitly drawn unless they are pointed to by HEAD and have a local counterpart.
* **Chronological Commit Processing**: Processes commits in `--date-order --reverse` (oldest first) to build the graph logically.
* **Error Handling**: Includes basic error handling for `subprocess` calls (e.g., `git` not found, errors during `git` command execution) and file I/O.

### Design Patterns (Git Branch Visualizer)

* **Command Pattern (Implicit)**: The script encapsulates requests to the Git system as `subprocess.run()` calls.
* **Interpreter Pattern (Conceptual)**: The script parses the output of Git commands (a form of "language") and interprets it to build a new representation (Mermaid code).
* **Builder Pattern (Conceptual)**: The `generate_mermaid_code` function incrementally builds the Mermaid string line by line.
* **Data Transformation**: Converts structured data from `git log` into a specific textual format for Mermaid.

## Cline's Operational System Patterns

My core operational directives, which define my behavior and collaboration, are documented as system patterns in `../../Cline/Rules/00-primary-directive.md`. These include:

* **Proactive Partnership**: Embodying an expert, pragmatic, proactive, and efficient coding partner.
* **Quality-Driven Delivery**: Consistently delivering clean, maintainable, secure, and idiomatic code.
* **Profound User Intent Understanding**: Rigorously prioritizing explicit instructions while proactively seeking clarification for ambiguity.
* **Continuous Learning & Knowledge Persistence**: Actively learning from interactions and maintaining the Memory Bank (`.clinerules`) for continuity and efficiency.
* **Principled Development & Quality Assurance**: Applying established software engineering principles, including comprehensive documentation, robust testing, and integrated security.

## MCP Server Usage Patterns

### Git MCP Server (`github.com/modelcontextprotocol/servers/tree/main/src/git`)

*   **Pathing for `repo_path`**: To ensure reliable operation, all tools from this server that accept a `repo_path` parameter (e.g., `git_status`, `git_add`, `git_commit`) should be provided with an **absolute path** to the target repository. Using relative paths (like ".") can lead to errors if the server's internal working directory context differs from the user's current working directory. This was confirmed by testing `git_status` with an absolute path after a relative path failed for `git_add`.
