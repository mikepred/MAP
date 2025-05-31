# Active Context

This document outlines the current work focus, recent changes, and next steps for the MAP project.

## Current Work Focus

The primary focus has been on **enhancing the `text_analyzer` project** with several new features, moving beyond its initial scope as a basic educational tool. This also serves as practical application while progressing with the broader self-directed AI engineering education plan.

**Current Learning Phase:** Practical application of NLP concepts through `text_analyzer` enhancements, while preparing to dive deeper into "Text representation/early NLP" (Chapter 3 of "GenAI PDF") and Raschka's "Build an LLM (From Scratch)" (Chapter 2).

## Recent Changes

*   **`text_analyzer` Enhancements (Current Session):**
    *   **CSV and JSON Input Support**: Implemented functionality to read and extract text from specified columns in CSV files and specified keys in JSON files. This involved updates to `file_io.py` and `analyzer.py`.
    *   **Graphical Output/Visualization**: Added support for generating `matplotlib` plots for:
        *   Top N Word Frequencies.
        *   Sentiment Score Distribution (VADER).
        *   Word Length Distribution.
        This involved updates to `display.py`, `config.py` (for plot settings), `analyzer.py` (for user prompts and plot generation calls), and `text_analyzer/requirements.txt` (adding `matplotlib`).
    *   **Full Keyword Extraction (RAKE)**: Implemented keyword extraction using the RAKE algorithm via `rake-nltk`. This involved updates to `analysis.py`, `display.py`, `config.py`, `analyzer.py`, and `text_analyzer/requirements.txt`. NLTK `stopwords` resource dependency was addressed.
    *   **Dynamic Stop Word Management**: Enhanced stop word handling to allow users to:
        *   Use the default English list.
        *   Select NLTK stop words for other supported languages.
        *   Provide a path to a custom stop word file.
        *   Opt out of stop word removal.
        This involved updates to `text_processing.py`, `file_io.py`, `analysis.py`, `analyzer.py`, and `config.py`.

*   **Previous Learning Strategy Refinement:**
    *   Clarified roles of key learning resources (Raschka's book, GenAI PDF, AI Engineering Master Curriculum).
    *   Affirmed "SAI" as the conceptual learning framework.
    *   Updated core memory bank files (`projectbrief.md`, `productContext.md`, etc.) to reflect this strategy.
    *   **New Global Rules & Workflows Created**:
        *   Added global rules for proactive feature development, defaulting to `pytest`, and prioritizing modularity/extensibility.
        *   Created global workflows for envisioning NLP features, refactoring for plugin architectures, and adding `matplotlib` visualizations.

## Pending Tasks & Next Steps

*This Memory Bank update (reflecting new global rules/workflows and `.clinerules` changes) is now complete. The next steps are:*

1.  **Finalize Current `text_analyzer` Enhancements**:
    *   Ensure all tests for the new features are robust (e.g., testing NLTK language stop word selection).
    *   Consider if `FIXED_TARGET_FILENAME` in `config.py` should be reverted from `test_plot_sample.txt` to `../dict-sample.txt` or another default.
    *   Commit all recent changes to the `text_analyzer` project.

3.  **Continue Learning (Self-Directed AI Engineering Education)**:
    *   **Immediate Focus:** "Text representation/early NLP."
        *   Deep dive into Chapter 3 of the "GenAI PDF."
        *   Begin Chapter 2 of Raschka's "Build an LLM (From Scratch)" (Data Processing and Tokenization).
        *   Relate concepts from these resources to the functionalities now present in the enhanced `text_analyzer`.
    *   **Ongoing:** Populate MCP Knowledge Graph with learned concepts.

4.  **Future `text_analyzer` Considerations (Lower Priority for now)**:
    *   Address any remaining items from Module G's extension ideas if desired (e.g., full TF-IDF, more advanced GUI).
    *   Expand automated tests in `run_comprehensive_test()` to cover new features more thoroughly.
