# Module A: Project Overview and Setup

**Welcome to Module A!** This module provides a high-level introduction to the `text_analyzer` tool, shows you how to run it, and gives a brief map of its codebase.

**Prerequisites:**
*   Basic understanding of Python.
*   Ability to run Python scripts from a terminal.
*   An environment where the `text_analyzer` project code is available.

**Learning Objectives:**
*   Understand the main purpose and capabilities of the `text_analyzer` tool.
*   Learn how to start the `text_analyzer` application.
*   Become familiar with the main menu options of the application.
*   Get a high-level overview of the different Python files that make up the project and their roles.

## 1. What is the Text Analyzer?

The `text_analyzer` is a Python application designed to perform various analyses on text data. As highlighted in the project's `README.md` and `memory-bank` documentation (e.g., `productContext.md`), its primary goal is to serve as an educational tool. It demonstrates a practical, modular approach to text processing, similar to the initial stages of data handling in Natural Language Processing (NLP) and for Large Language Models (LLMs).

**Key Capabilities:**

*   **Input:** Reads text from files (either a fixed file `s.txt` or a custom file you specify).
*   **Processing:** Cleans text (lowercase, punctuation removal), tokenizes it into words, and can filter out common "stop words."
*   **Analysis:**
    *   Calculates word frequencies.
    *   Analyzes sentence structures (counts, average lengths, identifies longest/shortest).
    *   Assesses text readability.
    *   Identifies interesting patterns (like frequently repeated words or very long words).
*   **Output:** Displays comprehensive analysis reports or summaries directly in your console and can save a summary to a file.

The tool is intentionally built with clear, separated modules for different tasks like file input/output, text processing, analysis logic, display formatting, and configuration. This modular design is a key aspect we'll be exploring.

For more details on the project's features, refer to the main project documentation:
*   **Main Lesson Plan:** [`comprehending-text-analyzer.md`](comprehending-text-analyzer.md)
*   **Project README:** [`../text_analyzer/README.md`](../text_analyzer/README.md)

## 2. Running the Text Analyzer

The `text_analyzer` application is run from its main script, `analyzer.py`.

**Steps to Run:**

1.  **Navigate to the Project Directory:**
    Open your terminal or command prompt. Change your current directory to the root of the `MAP` project, then into the `text_analyzer` folder.
    ```bash
    cd path/to/MAP/text_analyzer
    ```

2.  **Run the Script:**
    Execute the `analyzer.py` script using Python.
    ```bash
    python analyzer.py
    ```
    (Note: If you have multiple Python versions, you might need to use `python3 analyzer.py`)

**Expected Output:**

Upon running the script, you should see a welcome message and the main menu:

```text
TEXT ANALYZER - COMPLETE VERSION
Welcome to the comprehensive text analysis tool!
Built through Modules 3A-3E. Now enhancing with Module 4B features.

==================================================
Main Menu
==================================================
1. Analyze Fixed Text File (s.txt)
2. Analyze Custom Text File
3. Run System Tests
4. Help & Information
5. Exit
==================================================
Enter your choice (1-5):
```

## 3. Navigating the Main Menu

The application is interactive. You'll be prompted to enter a choice:

*   **Choice `1` (Analyze Fixed Text File):**
    *   Automatically analyzes the content of `text_analyzer/s.txt`.
    *   You'll then be asked for configuration (number of top words, stop word removal) and display preferences.
*   **Choice `2` (Analyze Custom Text File):**
    *   Prompts you to enter the path to a text file you want to analyze.
    *   Then asks for configuration and display preferences.
*   **Choice `3` (Run System Tests):**
    *   Executes a series of internal tests to check the basic functionality of different components. This is useful for developers.
*   **Choice `4` (Help & Information):**
    *   Displays a brief help message about the tool.
*   **Choice `5` (Exit):**
    *   Closes the application.

**Activity:**

*   Try running the `text_analyzer`.
*   Experiment with options 1 and 2. Use `s.txt` or `sample.txt` (both in the `text_analyzer` directory) as input for option 2.
*   Observe the prompts for configuration (number of top words, stop words) and display choices.
*   Explore option 4 for help.
*   Use option 5 to exit.

## 4. Codebase Overview: The Python Files

The `text_analyzer` project is organized into several Python files, each with a specific responsibility. This separation of concerns makes the code easier to understand, manage, and extend.

Here's a brief overview (we'll dive deeper into each in subsequent modules):

*   **`analyzer.py`:**
    *   The main executable script and entry point of the application.
    *   Contains the user interface logic (the menu system).
    *   Orchestrates the overall workflow by calling functions from other modules.
*   **`config.py`:**
    *   Stores global configuration settings and constants.
    *   Examples: default file paths, stop word lists, regular expressions for cleaning, limits for display.
*   **`file_io.py`:**
    *   Manages all file input and output operations.
    *   Functions for reading files, validating user-provided file paths, and saving analysis results.
*   **`text_processing.py`:**
    *   Focuses on preparing the text data for analysis.
    *   Includes functions for cleaning text (e.g., lowercasing, removing punctuation, URLs, emails), tokenizing text into words, and removing stop words.
*   **`analysis.py`:**
    *   The core analysis engine.
    *   Contains functions that perform the actual calculations and derive insights from the processed text (e.g., word counts, sentence statistics, readability scores, pattern identification).
*   **`display.py`:**
    *   Handles the presentation of analysis results to the user.
    *   Formats the data from the `analysis.py` module into readable console output (e.g., tables, summaries).
*   **`__init__.py`:**
    *   An empty file that tells Python to treat the `text_analyzer` directory as a package, allowing for organized imports between the modules.

**AI Copilot Interaction Prompts:**

*   "Can you explain the concept of a 'main execution block' in `analyzer.py` (i.e., `if __name__ == '__main__':`)?"
*   "What does it mean for `__init__.py` to make a directory a 'Python package'?"
*   "Show me where `config.py` is imported and used in one of the other files."

## Next Steps

You've now had a first look at the `text_analyzer` tool, how to run it, and the layout of its code. In the next module, we'll explore how the application is configured and how it handles file operations.

**Continue to [Module B: Configuration and File Handling (`config.py`, `file_io.py`)](comprehending-B-config-fileio.md)**
