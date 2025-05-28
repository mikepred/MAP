# Module E: Displaying Results

**Welcome to Module E!** After processing text and performing detailed analyses, the final step for the `text_analyzer` is to present these findings to the user in a clear and understandable way. This module explores `display.py`, which is responsible for all console output formatting.

**Prerequisites:**
*   Completion of [Module D: Core Analysis Engine](comprehending-D-analysis-engine.md).
*   Basic understanding of Python f-strings and print formatting.

**Learning Objectives:**
*   Understand the role of `display.py` in the application.
*   Learn how different parts of the analysis results are formatted and displayed.
*   Recognize how helper functions are used for consistent output styling.
*   See how configuration constants influence the displayed output.
*   Differentiate between the complete report and the summary display.

---

## 1. The Presentation Layer: `display.py`

Effective presentation of data is just as important as the analysis itself. If users can't understand the output, the analysis loses its value. The `display.py` module handles this "presentation layer" for the `text_analyzer`.

Open `text_analyzer/display.py` in your editor.

---

## 2. Styling Helpers

Consistent formatting makes the output look professional and easier to read.

*   **`print_header(title: str, width: int = 60) -> None`**:
    *   Prints a prominent header with a title, typically used for the main report title.
    *   Example: `📊 TEXT ANALYSIS REPORT 📊`
*   **`print_section(title: str, width: int = 60) -> None`**:
    *   Prints a section header, used to demarcate different parts of the analysis report.
    *   Example: `🔤 Word Frequency Analysis`

---

## 3. Displaying Specific Analysis Components

Most functions in `display.py` are designed to format and print a specific slice of the overall analysis results dictionary produced by `analysis.analyze_text_complete`.

*   **`display_general_statistics(stats: Dict[str, Any]) -> None`**:
    *   Displays overall metrics like character counts, word counts, sentence counts, and paragraph counts.
*   **`display_word_analysis(word_analysis_data: Dict[str, Any]) -> None`**:
    *   Shows unique word count, total analyzed words.
    *   Lists the top N most common words with their counts and percentages. The actual data for this comes from `word_analysis_data['word_frequencies']` and `word_analysis_data['statistics']`.
*   **`display_sentence_analysis(sentence_analysis_data: Dict[str, Any]) -> None`**:
    *   Prints total sentence count, average words per sentence.
    *   Displays the longest and shortest sentences (potentially truncated using `cfg.PREVIEW_LENGTH` from `config.py`).
*   **`display_readability_analysis(readability_stats_data: Dict[str, Any]) -> None`**:
    *   Shows average word length, the calculated complexity score, and the assigned readability level (e.g., 'Easy', 'Moderate').
    *   Includes a small interpretation of the readability level.
*   **`display_interesting_patterns(patterns_data: Dict[str, Any]) -> None`**:
    *   Displays word variety percentage.
    *   Lists most repeated words, a sample of long words, and a sample of short words. The number of items displayed for these lists is often controlled by constants in `config.py` (e.g., `cfg.DEFAULT_DISPLAY_REPEATED_WORDS_LIMIT`).
*   **`display_word_length_analysis(length_counts: Counter[int], total_tokens: int) -> None`**:
    *   Shows the distribution of word lengths: how many words of 1 letter, 2 letters, etc., were found, along with percentages.
    *   Calculates and displays the average word length based on this distribution.

**Data Flow:** Each of these functions expects a dictionary (or a `Counter` and an `int` for `display_word_length_analysis`) containing the specific data it needs to display. This data is typically a sub-dictionary from the main results object created by `analysis.analyze_text_complete`.

---

## 4. Main Display Orchestrators

Two functions orchestrate the calling of the more specific display functions:

*   **`display_complete_analysis(analysis_results: Dict[str, Any]) -> None`**:
    *   This function is responsible for printing the full, detailed report.
    *   It calls `print_header` once.
    *   Then, it sequentially calls the various specific display functions (`display_general_statistics`, `display_word_analysis`, etc.) for each relevant section of the `analysis_results` dictionary.
    *   It includes checks to see if data for a particular section is available before trying to display it (e.g., "Readability stats not available").
*   **`display_summary(analysis_results: Dict[str, Any]) -> None`**:
    *   This function prints a much shorter, quick overview of the key findings.
    *   It typically includes total characters, total analyzed words, total sentences, unique words, and the single most common word.

**User Choice:** In `analyzer.py` (the main script), the user is prompted to choose whether they want to see the "Complete Report," "Quick Summary," or "Both." This choice determines which of these orchestrator functions (or both) are called.

**AI Copilot Interaction Prompts:**

*   "In `display.py`, how is `cfg.PREVIEW_LENGTH` used in `display_sentence_analysis`?"
*   "Find an example in `display_interesting_patterns` where a constant from `config.py` is used to limit the number of items shown."
*   "What would happen if the `analysis_results` dictionary passed to `display_complete_analysis` was missing the `'sentence_analysis'` key?"
*   "Explain the f-string formatting used in `display_word_analysis` to show the word, count, and percentage."
*   "If I wanted to add a new section to the `display_complete_analysis` report, what steps would I need to take in `display.py`?"

---

## Next Steps

We've now seen how data is ingested, configured, processed, analyzed, and finally displayed. The next module ties everything together by looking at `analyzer.py`, the main script that orchestrates all these operations and handles user interaction.

➡️ **Continue to [Module F: Main Orchestration and Testing (`analyzer.py`)](comprehending-F-orchestration-testing.md)**
