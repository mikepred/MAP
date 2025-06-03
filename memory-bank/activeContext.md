# Active Context

This document outlines the current work focus, recent changes, and next steps for the MAP project, specifically concerning the `text_analyzer`.

## Current Work Focus

The primary focus has been on **enhancing the `text_analyzer` project** with several new features, moving beyond its initial scope as a basic educational tool.

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

## Pending Tasks & Next Steps

1.  **Finalize Current `text_analyzer` Enhancements**:
    *   Ensure all tests for the new features are robust (e.g., testing NLTK language stop word selection).
    *   Consider if `FIXED_TARGET_FILENAME` in `config.py` should be reverted from `test_plot_sample.txt` to a more general default sample file.
    *   Commit all recent changes to the `text_analyzer` project.

2.  **Future `text_analyzer` Considerations (Lower Priority for now)**:
    *   Address any remaining items from Module G's extension ideas if desired (e.g., full TF-IDF, more advanced GUI).
    *   Expand automated tests in `run_comprehensive_test()` to cover new features more thoroughly.
