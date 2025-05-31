# Module D: Core Analysis Engine

**Welcome to Module D!** Now that we've seen how text is preprocessed, let's explore how the `text_analyzer` actually derives insights from that text. This module focuses on `analysis.py`, the script's analytical powerhouse.

**Prerequisites:**
*   Completion of [Module C: Text Processing Logic](comprehending-C-text-processing.md).
*   Basic understanding of Python data structures (lists, dictionaries, Counters) and functions.

**Learning Objectives:**
*   Understand how word count statistics are generated.
*   Learn the methods used for sentence analysis (counting, length analysis).
*   Discover how readability metrics and text complexity are calculated.
*   See how various text patterns (like repeated words or word lengths) are identified.
*   Understand the role of `analyze_text_complete` as the central function that orchestrates all analysis tasks.

## 1. The Analysis Hub: `analysis.py`

The `analysis.py` file contains functions that take the preprocessed text (or tokens) and perform various calculations and data extractions to provide meaningful insights.

Open `text_analyzer/analysis.py` in your editor.

## 2. Word-Level Statistics: `get_word_count_stats(word_counts: Counter[str]) -> Dict[str, Any]`

This function takes a `Counter` object (like the one produced by `tp.count_words` in `text_processing.py`) and calculates several key statistics about the word frequencies.

*   **Inputs:** A `Counter` object where keys are words and values are their counts.
*   **Calculations:**
    *   `total_words`: Sum of all counts in the `Counter`.
    *   `unique_words`: Number of unique items (words) in the `Counter`.
    *   `most_common`: Uses `word_counts.most_common(cfg.DEFAULT_SUMMARY_MOST_COMMON_WORDS_COUNT)` to get a list of the most frequent words (the number is configurable via `config.py`).
    *   `average_frequency`: Calculated as `total_words / unique_words`.
*   **Output:** Returns a dictionary containing these statistics.

## 3. Sentence Analysis

Analyzing sentence structure can provide insights into text complexity and style.

*   **`count_sentences(text: Optional[str]) -> int`**:
    *   A relatively simple function that uses `re.split(r'[.!?]+', text)` to split the text by common sentence terminators.
    *   It then counts the number of resulting non-empty strings.
*   **`analyze_sentences(text: Optional[str]) -> Dict[str, Any]`**:
    *   This function provides more detailed sentence analysis.
    *   **Sentence Splitting:** It also uses `re.split(r'[.!?]+', text)` for initial splitting.
    *   **Word Counting per Sentence:** For each sentence, it re-tokenizes and counts words (using `tp.clean_text_for_word_tokenization` for consistency in word definition).
    *   **Metrics Calculated:**
        *   `sentence_count`.
        *   `average_words_per_sentence`.
        *   `longest_sentence` (the actual sentence string).
        *   `shortest_sentence` (the actual sentence string).
    *   **Output:** Returns a dictionary with these metrics.

**Note on Text Used for Sentence Analysis:** The `analyze_text_complete` function (discussed later) uses `tp.preprocess_text_for_sentence_analysis` to prepare the text before calling these sentence analysis functions. This ensures that sentence structures are reasonably preserved.

## 4. Word Length Analysis: `analyze_word_lengths(tokens: List[str]) -> Counter[int]`

This function analyzes the distribution of word lengths from a list of tokens.

*   **Input:** A list of word tokens (e.g., after cleaning and stop word removal).
*   **Process:** Uses a `Counter` to count the occurrences of each word length: `Counter(len(word) for word in tokens)`.
*   **Output:** A `Counter` object where keys are word lengths (integers) and values are the number of words having that length.

## 5. Readability and Complexity: `calculate_readability_stats(...) -> Dict[str, Any]`

This function attempts to quantify how easy or difficult a text is to read.

*   **Inputs:** The raw text, the `word_counts` Counter, and the `sentence_analysis` dictionary.
*   **Metrics Calculated:**
    *   `avg_word_length`: Average length of the words (based on `word_counts`).
    *   `avg_sentence_length`: Taken from `sentence_analysis`.
    *   `complexity_score`: A weighted average of `avg_word_length` and `avg_sentence_length`. This is a simplified custom metric for this project.
    *   `readability_level`: A qualitative assessment ('Easy', 'Moderate', 'Difficult', 'Very Difficult') based on the `complexity_score`.
*   **Output:** A dictionary containing these readability metrics.

## 6. Finding Patterns: `find_interesting_patterns(...) -> Dict[str, Any]`

This function looks for specific patterns in the text based on word counts.

*   **Inputs:** The `word_counts` Counter and the raw text (though the text parameter is currently noted for potential future use, the logic primarily uses `word_counts`).
*   **Patterns Identified:**
    *   `repeated_words`: Most common words that appear more than once (configurable limit).
    *   `long_words`: A sample of words with 7 or more characters (configurable limit).
    *   `short_words`: A sample of words with 2 or fewer characters (configurable limit).
    *   `word_variety`: A percentage representing `unique_words / total_words`, indicating lexical diversity.
*   **Output:** A dictionary containing these identified patterns.

## 7. The Orchestrator: `analyze_text_complete(...) -> Dict[str, Any]`

This is the main analysis pipeline function in `analysis.py`. It calls many of the other processing and analysis functions to generate a comprehensive set of results.

**Key Steps:**

1.  **Initial Check:** Returns an error structure if no text is provided.
2.  **Sentence Analysis Preparation:** Calls `tp.preprocess_text_for_sentence_analysis` on the input text.
3.  **Sentence Stats:** Calls `analyze_sentences` with the prepared text.
4.  **Word Analysis Preparation:** Calls `tp.clean_text_for_word_tokenization` (with `advanced=True`) on the input text.
5.  **Tokenization:** Calls `tp.tokenize_text` on the cleaned text for words.
6.  **Stop Word Removal (Optional):** If `use_stop_words` is true, calls `tp.remove_stop_words`. It captures the count of removed stop words.
7.  **Final Word Counts:** Creates a `Counter` from the (potentially filtered) tokens.
8.  **Word Count Stats:** Calls `get_word_count_stats` with the final word counts.
9.  **General Stats Calculation:** Computes character counts, paragraph counts, etc.
10. **Readability & Pattern Analysis:** Calls `calculate_readability_stats` and `find_interesting_patterns` if words were found.
11. **Word Length Analysis:** Calls `analyze_word_lengths` on the processed tokens.
12. **Result Aggregation:** Compiles all these results into a single, structured dictionary. This dictionary includes sections for `word_analysis` (with frequencies, stats, and the count of removed stop words), `sentence_analysis`, `general_stats`, `readability_stats`, `interesting_patterns`, the processed tokens themselves, and the word length counts.

**AI Copilot Interaction Prompts:**

*   "In `analysis.py`, trace the arguments passed to `calculate_readability_stats` back to their origins in `analyze_text_complete`. Where does the data for `word_counts` and `sentence_analysis` come from?"
*   "Explain the purpose of the `removed_stop_words_count` being included in the results of `analyze_text_complete`."
*   "If I wanted to add a new analysis, for example, counting the frequency of specific punctuation marks, which functions in `analysis.py` and `text_processing.py` might I need to modify or add to?"
*   "What is the role of `cfg.DEFAULT_SUMMARY_MOST_COMMON_WORDS_COUNT` in `get_word_count_stats` and where is this constant defined?"

## Next Steps

We've now covered how the `text_analyzer` processes text and performs its core analyses. The next step is to see how these rich analytical results are presented to the user.

**Continue to [Module E: Displaying Results (`display.py`)](comprehending-E-display.md)**
