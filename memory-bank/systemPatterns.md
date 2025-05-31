# System Patterns

This document outlines the system architecture, key technical decisions, and design patterns employed in the project.

## Text Analyzer Project

### System Architecture (Text Analyzer)

The `analyzer.py` script follows an enhanced linear data processing pipeline:

1.  **User Configuration Input (`analyzer.py`)**:
    *   `get_user_input_config()`: Prompts user for analysis parameters, including top words count and stop word management preferences (default, NLTK language, custom file, none).
2.  **Data Input & Validation (`file_io.py`, `analyzer.py`)**:
    *   User selects fixed file or provides a custom file path.
    *   `load_text_file()`: Handles file path input, validation (`validate_file_path()`).
    *   Detects file type (.txt, .csv, .json).
    *   For CSV/JSON: Prompts for column/key, then calls `read_csv_file()` or `read_json_file()` to extract text.
    *   For .txt: Calls `read_file()`.
    *   `load_custom_stop_words()`: If user chose custom stop words, this function is called to load them.
3.  **Stop Word Set Preparation (`analyzer.py`)**:
    *   Based on user configuration, the `active_stop_words_set` is prepared (default, NLTK language-specific, custom loaded, or empty set for no removal).
4.  **Core Text Processing & Analysis (`analysis.py`, `text_processing.py`)**:
    *   `analyze_text_complete()`: Orchestrates all analyses. Receives raw text and the `active_stop_words_set`.
        *   `preprocess_text_for_sentence_analysis()`: Light cleaning for sentence-based tasks.
        *   Sentence Analysis (`analyze_sentences`).
        *   Sentiment Analysis (`analyze_sentiment_vader`).
        *   POS Tagging & Lexical Density (`analyze_pos_tags_spacy`, `calculate_lexical_density`).
        *   Named Entity Recognition (`analyze_ner_spacy`).
        *   Keyword Extraction (`extract_keywords_rake` using RAKE algorithm).
        *   `clean_text_for_word_tokenization()`: Heavier cleaning for word-based tasks.
        *   `tokenize_text()`.
        *   `remove_stop_words()`: Called by `count_words` using the `active_stop_words_set`.
        *   Word Frequency Counting (`count_words` using `collections.Counter`).
        *   N-gram Analysis (`generate_ngrams`, `calculate_ngram_frequencies`).
        *   Readability Assessment (`calculate_readability_stats`).
        *   Pattern Detection (`find_interesting_patterns`).
        *   Word Length Analysis (`analyze_word_lengths`).
5.  **Results Display (`display.py`, `analyzer.py`)**:
    *   User chooses display format (complete, summary, both).
    *   `display_complete_analysis()` / `display_summary()`: Format and print textual analysis results. Includes sections for all new analyses (keywords, etc.).
    *   Plotting (Optional):
        *   User prompted if plots are desired.
        *   `plot_word_frequencies()`, `plot_sentiment_distribution()`, `plot_word_length_distribution()`: Generate and save/display `matplotlib` charts.
6.  **Save Results (Optional) (`file_io.py`)**:
    *   User prompted to save textual summary to a file.

This pipeline allows for flexible configuration and a comprehensive set of analyses.

### Key Technical Decisions (Text Analyzer)

* **Use of Standard Library & Key NLP Libraries**: Leverages Python's standard library, supplemented by NLTK (VADER, RAKE, stopwords), spaCy (POS, NER), `matplotlib` (plotting), and `textstat` (readability).
* **Modular Design**: Maintained and extended with single-responsibility functions.
* **Dynamic Configuration**: User can configure stop words, input file types, and output preferences at runtime.
* **Progressive Enhancement**: Features added incrementally, building upon the core structure.

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

### Memory MCP Server (`github.com/modelcontextprotocol/servers/tree/main/src/memory`)

*   **Self-Learning Process**: The memory server updates its knowledge through:
    - Monitoring stdio communication for new information
    - Analyzing patterns in user-agent interactions
    - Processing command results and outcomes
    - Learning from error cases and their resolutions

*   **Knowledge Integration**:
    - Automatically captures successful command patterns
    - Records error scenarios and their solutions
    - Updates its understanding based on user feedback
    - Integrates new knowledge with existing patterns

*   **Knowledge Application**:
    - Uses learned patterns to improve future interactions
    - Applies past solutions to similar problems
    - Adapts behavior based on accumulated experience
    - Provides context-aware suggestions
