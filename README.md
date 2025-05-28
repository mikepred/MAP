# 🐍 Python Text Analyzer: Your First Step into NLP and LLMs

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Difficulty](https://img.shields.io/badge/difficulty-beginner_to_intermediate-orange.svg)
![Learning](https://img.shields.io/badge/learning-NLP%20foundations%2C%20Python%20scripting-blueviolet.svg)

> **"Every journey into AI begins with understanding text."**  
> *Transform raw text into insights with Python*

## 📊 What You'll Build

This project guides you through building a command-line Python application that performs a comprehensive analysis of a given text file. It demonstrates key concepts in text processing and Natural Language Processing (NLP).

```text
Input Text File → Load & Validate → User Configuration → Clean & Process → Analyze → Display & Save Results
      ↑                                                                           ↓
  (s.txt / sample.txt)                                                (Console Output / analysis_results.txt)
```

**Example Output:**

(The following is a sample run with `text_analyzer/sample.txt` containing "This is a sample text for testing. Testing is fun.", stop words enabled, and display format "Both".)
```text
============================================================
🚀 TEXT ANALYZER - COMPLETE VERSION 🚀
============================================================
Welcome to the comprehensive text analysis tool!
Built through Modules 3A-3E. Now enhancing with Module 4B features.

==================================================
📋 Main Menu
==================================================
1. 📊 Analyze Fixed Text File (s.txt)
2. 📂 Analyze Custom Text File
3. 🧪 Run System Tests
4. ❓ Help & Information
5. 🚪 Exit
==================================================
Enter your choice (1-5): 2

🚀 Text File Loader
==============================

📂 Enter filename (attempt 1/3):
💡 Tip: Use 'sample.txt' for testing (located in script directory)
💡 Type 'quit' to exit
Filename: text_analyzer/sample.txt
✅ Validated relative path (in CWD): /path/to/your/project/text_analyzer/sample.txt
✅ Successfully read file: /path/to/your/project/text_analyzer/sample.txt
📄 File size: 51 characters

📖 File Preview:
--------------------
This is a sample text for testing. Testing is fun.
--------------------

--- ⚙️ Text Analysis Configuration ---
Number of top words to display (default: 10): 
Remove stop words? (yes/no, default: yes): yes

🔄 Running complete analysis...
------------------------------
ℹ️ Removed 5 stop words.

⏱️ Text analysis pipeline took: 0.0012 seconds

📊 Analysis complete! Choose display format:
1. Complete Report
2. Quick Summary
3. Both
Enter choice (1-3): 3

========================================
📊 QUICK SUMMARY
========================================
📄 Characters (raw): 51
📝 Words (analyzed): 5
📋 Sentences: 2
🎯 Unique Words (analyzed): 4
🏆 Most Common Word: 'testing' (2 times)
========================================

============================================================
                  📊 TEXT ANALYSIS REPORT 📊                  
============================================================

📊 General Statistics
--------------------
📄 Total Characters (raw): 51
🔤 Characters (raw, no spaces): 42
📝 Total Words (after cleaning/stop words): 5
📋 Total Sentences: 2
📄 Paragraphs: 1
📏 Average Words per Sentence: 2.5

🔤 Word Frequency Analysis
-------------------------
🎯 Unique Words: 4
📊 Total Word Count (in analysis): 5

🏆 Top 4 Most Common Words:
   1. 'testing' - 2 times (40.0%)
   2. 'sample' - 1 times (20.0%)
   3. 'text' - 1 times (20.0%)
   4. 'fun' - 1 times (20.0%)

📋 Sentence Analysis
-------------------
📊 Total Sentences: 2
📏 Average Words per Sentence: 5.0

📏 Longest Sentence:
   "this is a sample text for testing"

📏 Shortest Sentence:
   "testing is fun"

📖 Readability Analysis
----------------------
📐 Average Word Length (of analyzed words): 5.4 characters
🎯 Complexity Score: 5.2
📚 Readability Level: Easy
   💡 This text is easy to read and understand.

🔍 Interesting Patterns
----------------------
🎨 Word Variety (analyzed words): 80.0% (unique words / total analyzed words)

🔄 Most Repeated Words (among analyzed):
   'testing' appears 2 times

📏 Long Words (7+ characters, among analyzed):
   testing

--- Word Length Analysis ---
 3 letter(s):    1 words ( 20.0%)
 4 letter(s):    1 words ( 20.0%)
 6 letter(s):    1 words ( 20.0%)
 7 letter(s):    2 words ( 40.0%)

Average word length: 5.4 letters
--------------------------

✅ Analysis Complete
-------------------
📝 Report generated successfully!

--- Word Length Analysis ---
 3 letter(s):    1 words ( 20.0%)
 4 letter(s):    1 words ( 20.0%)
 6 letter(s):    1 words ( 20.0%)
 7 letter(s):    2 words ( 40.0%)

Average word length: 5.4 letters
--------------------------

💾 Save analysis results to file? (yes/no, default: no): no
```

## 🎯 Learning Objectives

By completing this project and following the associated lesson plan, you will:

*   Understand the foundational steps of a text analysis pipeline.
*   Learn to read from and write to files using Python, including `pathlib` for path manipulation.
*   Master various string manipulation techniques for text cleaning and normalization.
*   Implement different tokenization strategies (basic split, regex-based for URLs/emails).
*   Utilize Python's `collections.Counter` for efficient frequency counting.
*   Develop skills in conditional logic for configurable behavior (e.g., stop word removal).
*   Gain experience in structuring a Python application with multiple modules (`analyzer.py`, `analysis.py`, `text_processing.py`, `file_io.py`, `display.py`, `config.py`).
*   Practice creating clear and informative user interfaces (CLI-based).
*   Understand how to perform comprehensive text analysis, including word frequencies, sentence analysis, readability, and pattern detection.
*   Learn to format and display complex data in a readable manner.
*   Appreciate the importance of error handling and user input validation.
*   See how basic text processing techniques form the building blocks for more advanced NLP tasks and LLMs.

## 🎓 Prerequisites

**What you need to know:**

- [ ] Basic Python syntax (variables, functions, loops, conditional statements, data types like lists and dictionaries).
- [ ] How to run Python scripts from the command line.
- [ ] Basic understanding of text files and file paths.
- [ ] Familiarity with importing modules.

**What you'll learn (or reinforce):**

- [ ] Advanced File I/O operations, including `pathlib`.
- [ ] Effective string manipulation and regular expression usage.
- [ ] Proficient use of data structures like `collections.Counter`.
- [ ] Modular code organization and package structure in Python.
- [ ] Designing interactive command-line interfaces.
- [ ] Implementing error handling and input validation.
- [ ] Applying text analysis techniques to extract insights.

## 📂 Project Structure

The project is organized into several Python modules within the `text_analyzer` package:

- `text_analyzer/`: The main package directory.
    - `__init__.py`: Makes `text_analyzer` a Python package.
    - `analyzer.py`: The main executable script containing the primary application logic, menu handling, and orchestration of analysis tasks.
    - `analysis.py`: Contains functions for performing higher-level text analysis (e.g., sentence analysis, readability, pattern finding, word length distribution).
    - `config.py`: Stores configuration constants, such as file paths, default values, stop words, and pre-compiled regular expressions.
    - `display.py`: Handles the presentation and formatting of analysis results to the user.
    - `file_io.py`: Manages file input/output operations, including reading files, validating paths, and saving results.
    - `text_processing.py`: Includes core functions for cleaning text, tokenization, and stop word removal.
    - `sample.txt`: A sample text file for quick testing.
    - `s.txt`: A default, larger text file used for the fixed analysis option.
- `README.md`: This file – your guide to the project.
- `requirements.txt`: Lists project dependencies (currently, the project uses only the Python standard library).

## ⚡ Quick Start

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name> # e.g., cd python-text-analyzer
    ```
2.  **Run the analyzer:**
    ```bash
    python -m text_analyzer.analyzer
    ```
3.  Follow the on-screen prompts. For a quick test with the custom file option, you can use `text_analyzer/sample.txt`.

## ✨ Core Functionality

The `text_analyzer` package provides a comprehensive script to perform text analysis:

1.  **Interactive Menu:** Offers a user-friendly command-line interface to:
    *   Analyze a fixed default text file (`s.txt`).
    *   Analyze a custom text file specified by the user.
    *   Run a suite of internal system tests.
    *   Display help information.
2.  **File Loading:** Securely loads text content from user-specified or default files, with path validation and error handling.
3.  **Configuration:** Allows users to configure:
    *   The number of top words to display in frequency analysis.
    *   Whether to remove common English stop words.
4.  **Text Processing:**
    *   **Cleaning:** Normalizes text by converting to lowercase, removing punctuation, URLs, and emails (for word tokenization) or lightly cleaning while preserving sentence structure (for sentence analysis).
    *   **Tokenization:** Splits cleaned text into individual words (tokens).
    *   **Stop Word Removal:** Optionally filters out common stop words from the token list and reports the count of removed words.
5.  **Text Analysis:**
    *   **Word Frequency:** Calculates and displays the most common words and their frequencies (including percentages).
    *   **Word Length Distribution:** Analyzes and displays the distribution of word lengths.
    *   **Sentence Analysis:** Counts sentences, calculates average words per sentence, and identifies the longest and shortest sentences.
    *   **General Statistics:** Provides counts for characters (with/without spaces), words, sentences, and paragraphs.
    *   **Readability Assessment:** Calculates average word length and a complexity score, then provides a qualitative readability level (e.g., Easy, Moderate).
    *   **Pattern Detection:** Identifies word variety, most repeated words, and samples of long/short words.
6.  **Results Display:** Presents the analysis in a structured format, offering:
    *   A quick summary.
    *   A complete detailed report.
    *   Both summary and full report.
7.  **Save Results:** Optionally saves the word frequency analysis to a user-specified file.
8.  **Timing:** Measures and displays the duration of the analysis pipeline.

## 🚀 How to Run the Script

1.  **Prerequisites:** Ensure you have Python 3.7+ installed.
2.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name> # Navigate to the root of the project
    ```
3.  **Run from Project Root:** The script is designed to be run as a module from the project's root directory.
    ```bash
    python -m text_analyzer.analyzer
    ```
4.  **Follow Prompts:** The script will present a menu. Follow the on-screen prompts to:
    *   Choose an analysis option (fixed file, custom file, or run tests).
    *   If analyzing a custom file, provide the path (e.g., `text_analyzer/sample.txt`).
    *   Configure analysis parameters (top words, stop word removal).
    *   Select a display format for the results.
    *   Optionally save the results.

## 🐛 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| `python: command not found` or `python3: command not found` | Install Python 3.7+ and ensure it's added to your system's PATH. Use `python3` if `python` defaults to Python 2. |
| `FileNotFoundError` when providing a filename | Ensure the path to the file is correct. Relative paths are interpreted from the current working directory (usually the project root if you followed the run instructions). For files within the `text_analyzer` package, prefix with `text_analyzer/` (e.g., `text_analyzer/sample.txt`). |
| Script runs but no output or unexpected results | Check if your input text file has content and is plain text. Ensure it's UTF-8 encoded. |
| `ModuleNotFoundError: No module named 'text_analyzer'` | Make sure you are running the script from the **root directory** of the project (the one containing the `text_analyzer` folder and this `README.md`) using the `python -m text_analyzer.analyzer` command. |
| Encoding errors (e.g., `UnicodeDecodeError`) | Ensure your input text file is saved as UTF-8. |

## 🧠 Connecting to the World of LLMs

This text analyzer, while relatively simple, touches upon core principles vital to Large Language Models (LLMs) like GPT-4 or Claude:

- **Data Preprocessing:** LLMs are trained on vast amounts of text. This text must first be cleaned, normalized, and structured. Our script's cleaning functions (e.g., lowercasing, punctuation removal, URL/email stripping) mirror these essential initial steps, albeit on a much smaller scale.
- **Tokenization:** LLMs don't "see" words or sentences as humans do. They use sophisticated tokenizers (e.g., Byte Pair Encoding (BPE), WordPiece, SentencePiece) to break text into manageable pieces called tokens. Our `tokenize_text` function, using simple splitting, is a very basic form of this crucial step. Understanding this helps appreciate the complexity and importance of LLM tokenization.
- **Frequency Analysis & Statistical Patterns:** While our script counts raw word frequencies, LLMs learn complex statistical patterns and relationships between tokens to predict subsequent tokens. Frequency analysis is a basic way to start understanding the statistical nature of language, which underpins how LLMs learn to generate coherent and contextually relevant text.
- **Stop Word Removal:** In some NLP tasks (though not always for LLM pre-training directly), removing stop words helps focus on content-bearing words. Understanding this concept is useful for many downstream NLP applications.

This project provides a tangible entry point to demystify the initial data handling and analytical stages that every advanced NLP system, including LLMs, undergoes.

## 📚 Lesson Plan Modules Overview

This project is best understood by following an accompanying lesson plan (if provided) which might cover:

- **Module 1: Introduction & Setting the Stage** - Overview of text processing and project setup.
- **Module 2: Core Python Concepts for Text Processing** - File handling, text cleaning, tokenization, and frequency counting.
- **Module 3: Building the Script - Step-by-Step** - Implementation details for each module of the `text_analyzer`.
- **Module 4: Testing and Refinement** - Running, debugging, and improving the script with comprehensive tests.
- **Module 5: Connecting to the Bigger World of LLMs** - Understanding how this relates to LLM development.

## ✅ Success Criteria

You'll know you've mastered this project when you can:

*   Explain the role and interaction of each module in the `text_analyzer` package.
*   Successfully run the script to analyze both the default (`s.txt`) and custom (`sample.txt`) files.
*   Understand and interpret all sections of the generated analysis report.
*   Modify the `STOP_WORDS` set in `config.py` and observe its effect on the analysis.
*   Explain how the script handles potential errors like file not found or invalid user input.
*   Trace the flow of data from file input, through processing and analysis, to display and optional saving.
*   Articulate how configurable options (top words, stop words) affect the outcome.
*   Relate at least three functions in the codebase to preprocessing steps in a typical LLM pipeline.
*   Implement a small new feature or enhancement from the "Further Exploration" list.

## 💡 Further Exploration

Once you've mastered the current functionalities, consider these enhancements:

*   **Advanced Tokenization:** Explore more sophisticated tokenization methods (e.g., using regular expressions for hyphenated words, contractions).
*   **N-gram Analysis:** Extend frequency analysis to include bigrams (two-word phrases) or trigrams.
*   **Sentiment Analysis:** Implement a basic sentiment scoring mechanism (e.g., based on a predefined list of positive/negative words).
*   **Part-of-Speech (POS) Tagging:** Integrate a simple POS tagger to identify nouns, verbs, adjectives, etc.
*   **File Input Flexibility:** Allow users to paste text directly instead of only providing a file path.
*   **Output Formats:** Offer different output formats for saved results (e.g., CSV, JSON).
*   **Configuration File:** Load default settings from a configuration file (e.g., `config.ini` or `config.json`).
*   **GUI:** Develop a simple graphical user interface (e.g., using Tkinter, PyQt, or a web framework like Flask/Django).
*   **More Sophisticated Readability Scores:** Implement established readability formulas like Flesch-Kincaid or Gunning Fog.
*   **Explore NLP Libraries:** Experiment with libraries like NLTK, spaCy, or TextBlob to see how they handle these tasks more robustly.

Happy analyzing!
