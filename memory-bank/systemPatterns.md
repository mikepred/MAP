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
