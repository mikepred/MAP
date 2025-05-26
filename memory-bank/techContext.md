# Tech Context

This document covers the technologies used in the project, the development setup, technical constraints, dependencies, and tool usage patterns for each component.

## Text Analyzer (`analyzer.py`)

### Technologies Used (Text Analyzer)

* **Python**: Version 3.7 or higher is required.
* **Standard Library**:
  * `os`, `pathlib`: For file system interactions (Module 3B onwards).
  * `collections`: The `Counter` class for efficient word frequency counting (Module 3C onwards).
  * `string`: The `string.punctuation` constant and `str.maketrans()` method for text cleaning (Module 3C onwards).
  * `re`: The regular expression module for advanced text cleaning and sentence splitting (Module 3C onwards).
* **NLTK (Natural Language Toolkit)**: Used for advanced tokenization, stop word removal, and other NLP tasks (Module 5C exploration).
* **spaCy**: Used for advanced tokenization, stop word removal, part-of-speech tagging, named entity recognition, and other NLP tasks (Module 5C exploration).

### Development Setup (Text Analyzer)

* **Python Installation**: Ensure Python 3.7+ is installed and accessible from the command line.
* **Text Editor/IDE**: VS Code, PyCharm, Sublime Text, Atom, etc.
* **Virtual Environment**: Recommended as per Module 3A of the lesson plan.

### Technical Constraints (Text Analyzer)

* **Simple Design**: Intentionally simple for beginners; does not handle very large datasets or highly complex NLP tasks.
* **Basic Tokenization**: Uses `.split()`, which is a simplification and doesn't handle all linguistic nuances.

### Dependencies (Text Analyzer)

* Primarily relies on Python's standard library for core Module 1-3 functionalities.
* **NLTK**: External dependency, installed and explored as part of Module 5C. Requires data packages like `punkt`, `stopwords`, `punkt_tab`.
* **spaCy**: External dependency, installed and explored as part of Module 5C. Requires language models like `en_core_web_sm`.

### Tool Usage Patterns (Text Analyzer)

* Executed via `python analyzer.py`.
* Reads from a specified input text file (default: `sample.txt`).
* Outputs analysis results to the console.

## Git Branch Visualizer (`branch_visualizer.py`)

### Technologies Used (Git Branch Visualizer)

* **Python**: Version 3.7 or higher.
* **Standard Library**:
  * `subprocess`: To execute external Git commands.
  * `re`: For parsing Git log output.
  * `os`: Used implicitly by `subprocess` for path context.
  * `pathlib`: For path manipulations if extended (currently uses string for REPO_PATH).
* **Git**: External command-line tool. The script assumes `git` is installed and in the system's PATH.
* **Mermaid**: The script generates `gitGraph` syntax, which is a domain-specific language for Mermaid.js to render diagrams.

### Development Setup (Git Branch Visualizer)

* **Python Installation**: Python 3.7+ installed.
* **Git Installation**: Git must be installed and configured in the system's PATH.
* **Text Editor/IDE**: For viewing/editing the script.
* **Mermaid Renderer (Optional, for viewing output)**:
  * Online editors (e.g., mermaid.live).
  * IDE extensions (e.g., Markdown Preview Mermaid Support for VS Code).
  * Command-line tools for Mermaid.

### Technical Constraints (Git Branch Visualizer)

* **Git Dependency**: Functionality is entirely dependent on the presence and correct operation of the `git` executable.
* **Local Branch Focus**: The current visualization primarily focuses on local branches. Representation of remote branches is limited.
* **Parsing Robustness**: The accuracy of the graph depends on the parsing logic for `git log` output, which might need adjustments for highly unusual Git histories or log formats.
* **Graph Complexity**: Very large repositories with numerous branches and complex merge histories might result in overly dense or hard-to-read Mermaid diagrams.

### Dependencies (Git Branch Visualizer)

* **External**: `git` command-line tool.
* **Python**: Relies only on Python's standard library (`subprocess`, `re`, `os`).

### Tool Usage Patterns (Git Branch Visualizer)

* Executed via `python branch_visualizer.py` from within a Git repository.
* The script automatically uses the current working directory as the `REPO_PATH`.
* Outputs the generated Mermaid `gitGraph` code to `branch_visualization.mermaid.txt`.
* The content of `branch_visualization.mermaid.txt` can be copied into a Mermaid renderer to view the graph.

## Overall Project/Repository Technical Context

### Dependency Management

* **Git Submodules**: The project utilizes Git submodules for managing external repository dependencies. For example, the `LLMs-from-scratch` directory is integrated as a submodule, allowing the project to track a specific version of this external code.

## MCP Servers

### Git MCP Server (`github.com/modelcontextprotocol/servers/tree/main/src/git`)

*   **Tool Usage Pattern**: When using tools from this server (e.g., `git_status`, `git_add`, `git_commit`), the `repo_path` parameter **must be an absolute path** to the target repository. Relative paths may lead to errors due to the server's execution context.
*   **Dependencies**: This server relies on the system's `git` command-line installation.
