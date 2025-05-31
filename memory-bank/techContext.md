# Tech Context

This document covers the technologies used in the project, the development setup, technical constraints, dependencies, and tool usage patterns for each component.

## Text Analyzer (`analyzer.py`)

### Technologies Used (Text Analyzer)

* **Python**: Version 3.7 or higher is required.
* **Standard Library**:
  * `os`, `pathlib`: For file system interactions.
  * `collections`: `Counter` for frequency counting, `defaultdict` for NER results.
  * `string`: For punctuation constants.
  * `re`: For regex-based cleaning and splitting.
  * `csv`: For reading CSV files.
  * `json`: For reading JSON files.
* **NLTK (Natural Language Toolkit)**:
    * VADER for sentiment analysis.
    * `rake-nltk` for RAKE keyword extraction.
    * `stopwords` corpus for various languages.
    * `punkt` for tokenization (used by some NLTK components).
* **spaCy**: For Part-of-Speech (POS) tagging and Named Entity Recognition (NER), using the `en_core_web_sm` model.
* **matplotlib**: For generating plots (word frequencies, sentiment distribution, word length distribution).
* **textstat**: For calculating various standard readability indices.
* **pyspellchecker**: For typo correction.

### Development Setup (Text Analyzer)

* **Python Installation**: Ensure Python 3.7+ is installed and accessible from the command line.
* **Text Editor/IDE**: VS Code, PyCharm, Sublime Text, Atom, etc.
* **Virtual Environment**: Recommended as per Module 3A of the lesson plan.

### Technical Constraints (Text Analyzer)

* **Simple Design**: Intentionally simple for beginners; does not handle very large datasets or highly complex NLP tasks.
* **Basic Tokenization**: Uses `.split()`, which is a simplification and doesn't handle all linguistic nuances.

### Dependencies (Text Analyzer)

* Primarily relies on Python's standard library for core Module 1-3 functionalities.
* **NLTK**: External dependency. Requires data packages like `punkt`, `stopwords`, `vader_lexicon`.
* **spaCy**: External dependency. Requires language models like `en_core_web_sm`.
* **matplotlib**: External dependency for plotting.
* **textstat**: External dependency for readability scores.
* **pyspellchecker**: External dependency for typo correction.
* **rake-nltk**: External dependency for keyword extraction.
* **NumPy**: Pinned to `<2.0` in `requirements.txt` to avoid binary incompatibility issues with `thinc` (a spaCy dependency) during deployment on platforms like Render. (Note: Check if this is still the case or if newer spaCy/thinc versions have resolved this).

### Tool Usage Patterns (Text Analyzer)

* Executed via `python -m text_analyzer.analyzer` (as a module to handle relative imports).
* Reads from user-specified input files (.txt, .csv, .json) or a fixed default file.
* Prompts for configurations (top words, stop word strategy, plot generation).
* Outputs analysis results to the console, including textual reports and optionally saves graphical plots to an `analysis_plots` directory.
* Can save textual analysis summary to a user-specified file.

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

### Memory MCP Server (`github.com/modelcontextprotocol/servers/tree/main/src/memory`)

*   **Tool Usage Pattern**: This server provides knowledge graph functionality over stdio transport.
*   **Dependencies**: Requires Node.js and NPM for package installation and execution.
*   **Configuration Notes**: 
    - Use `cmd` instead of `powershell` for more reliable execution
    - Direct `npx` command is preferred over PowerShell script execution
    - Recommended timeout of 120 seconds or higher to ensure stable connection
*   **Troubleshooting**:
    - If encountering "MCP error -1: Connection closed", try:
      1. Using `cmd` as the command executor
      2. Simplifying command args to `["/c", "npx", "-y", "@modelcontextprotocol/server-memory"]`
      3. Increasing the timeout value in MCP settings

## Self-Directed AI Engineering Education

### Key Learning Resources
The primary learning resources, including Sebastian Raschka's "Build a Large Language Model (From Scratch)," the "Generative AI with Python and PyTorch, Second Edition" PDF, and the "AI Engineering Master Curriculum," are detailed in `memory-bank/projectbrief.md`. This section focuses on the technologies associated with these resources and the overall learning process.

*   **Technologies associated with Primary Technical Guide (Raschka):** Python, PyTorch, Jupyter Notebooks. Focuses on building Transformer components, attention mechanisms, GPT-like models, pretraining, and finetuning.
*   **Technologies associated with Comprehensive Textbook (GenAI PDF):** Python, PyTorch. Covers a wide range of topics from deep learning fundamentals to advanced LLM applications and optimization.
*   **Technologies associated with Inspirational Curriculum (AI Engineering Master Curriculum):** Broad overview, implies various technologies depending on the specific area of AI engineering.
*   **Foundational Practical Exercise:**
    *   The `text_analyzer` project (details above).

### Development Setup (Self-Directed Learning)
*   **Primary Language:** Python.
*   **Core Libraries:** PyTorch, Hugging Face Transformers, NLTK, spaCy, Pandas, NumPy.
*   **LLM Tooling:** LangChain, LangSmith.
*   **Version Control:** Git, with `LLMs-from-scratch-main/` as a Git submodule.
*   **Environment:** VS Code, with access to relevant files and ability to run Python scripts and Jupyter Notebooks.
*   **MCP Servers:** Git MCP Server and Memory MCP Server for enhanced workflow and knowledge persistence.

### Technical Constraints (Self-Directed Learning)
*   Learning is self-paced and iterative.
*   Computational resources for training very large models from scratch may be a constraint, leading to focus on understanding concepts, implementing smaller-scale versions, or leveraging pre-trained models for certain aspects.

### Dependencies (Self-Directed Learning)
*   Python 3.7+
*   Specific Python packages as listed in `requirements.txt` for the `text_analyzer` and `LLMs-from-scratch-main/` projects.
*   Additional packages as introduced by the "GenAI PDF" examples (e.g., `transformers`, `datasets`, `trl`, `langchain`).

### Tool Usage Patterns (Self-Directed Learning)
*   Reading and working through code examples from Raschka's book and the "GenAI PDF."
*   Modifying and extending the `text_analyzer` project.
*   Conceptually designing and planning components of "SAI."
*   Using Cline (this AI assistant) for discussion, clarification, code assistance, and updating memory systems.
*   Utilizing the MCP Knowledge Graph to structure and persist learned concepts.
