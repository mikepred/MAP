# 🐍 Python Text Analyzer: A Modular Tool for Text Analysis

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellowgreen.svg)
![Learning](https://img.shields.io/badge/learning-Applied%20NLP-orange.svg)

> **"Unlock the stories hidden in your text."**  
> *Gain comprehensive insights from text data using a modular Python toolkit.*

This project provides a robust, modular Python package for comprehensive text analysis. It moves beyond a simple script to offer a structured approach to processing and understanding textual data.

## 📊 What This Tool Does

The `text_analyzer` package offers a pipeline for in-depth text analysis:

```text
Input Text → Advanced Cleaning & Preprocessing → Tokenization → Optional Stop Word Removal → Multiple Analyses → Formatted Output & Optional File Saving
    ↓                      ↓                       ↓                    ↓                        ↓                     ↓
Raw Text  → Lowercasing, Punctuation & Regex Cleaning → Word/Sentence Tokens → Filtered Tokens → Word Frequencies,  → Console Display / File
                                                                                              Sentence Analysis,
                                                                                              Readability Scores,
                                                                                              Pattern Matching
```

**Example Output Snippet:**

```text
--- Word Frequencies (Top 5) ---
1. text: 3 occurrences
2. analysis: 2 occurrences
3. tool: 1 occurrence
4. provides: 1 occurrence
5. insights: 1 occurrence

--- Sentence Analysis ---
Total Sentences: 3
Average Sentence Length: 10.3 words
Longest Sentence: "This tool provides comprehensive insights from textual data through multiple analysis modules." (13 words)

--- Readability (Flesch-Kincaid Grade Level) ---
Grade Level: 8.5
```

## 🎯 Learning Objectives

By exploring and utilizing this `text_analyzer` tool, you will:

- Understand the architecture of a modular text analysis application in Python.
- Learn how different components (file I/O, processing, analysis, display, configuration) interact within a package.
- Gain proficiency in interpreting various text analysis outputs, including word frequencies, sentence metrics, and readability scores.
- Understand how to effectively use the tool's features, including configuration options for customized analysis.
- Appreciate the connection between these text analysis techniques and the preprocessing pipelines used in Large Language Models (LLMs).
- Learn how to navigate and understand a well-structured Python package.

## 🎓 Prerequisites

**What you need to know:**

- [ ] Basic Python syntax (variables, functions, loops, data structures)
- [ ] How to run Python scripts from the command line
- [ ] Basic understanding of text files and encodings

**What you'll learn by exploring this tool:**

- [ ] How modules in a Python package collaborate to deliver functionality.
- [ ] The data flow within a text analysis pipeline, from input to output.
- [ ] How to use configuration files to customize application behavior.
- [ ] Practical application of text processing and analysis techniques.
- [ ] How to leverage different analysis modules for comprehensive text understanding.

## 📂 Project Structure

The `text_analyzer` package is organized as follows:

- `analyzer.py`: The main executable script. It provides a menu-driven command-line interface (CLI) and orchestrates the different analysis modules based on user choices.
- `config.py`: Stores all configuration settings for the application. This includes default file paths, lists of stop words, regular expressions for text cleaning and pattern matching, and limits for displaying results (e.g., number of top words).
- `file_io.py`: Handles all file input and output operations. This includes reading text from specified files, validating file existence, prompting the user for file paths if needed, and saving analysis results to a new file.
- `text_processing.py`: Contains functions dedicated to preparing text for analysis. This involves text cleaning (e.g., lowercasing, removing punctuation, custom regex cleaning), tokenization (splitting text into words or sentences), and removing stop words.
- `analysis.py`: Includes the core functions for performing various text analyses. This module calculates word frequencies, provides sentence statistics (like count, average length, longest/shortest sentences), computes readability scores (e.g., Flesch-Kincaid), and identifies common text patterns.
- `display.py`: Responsible for formatting and presenting the analysis results to the console in a clear, human-readable format.
- `__init__.py`: An empty file that signals to Python that the `text_analyzer` directory should be treated as a package, allowing for modular imports.
- `requirements.txt`: Lists the external Python libraries and dependencies required for the project to run correctly (e.g., `nltk` for readability scores).
- `sample.txt` (or `s.txt`): A sample text file provided for quick analysis and demonstration of the tool's capabilities.
- `.clinerules/`: This directory contains lesson plans and guides designed to help understand the project's structure, functionality, and how to explore it effectively, potentially with an AI copilot.

## ⚡ Quick Start

### Option 1: Follow the Comprehension Lesson Plan (Recommended)

For a deep dive into the tool's architecture and functionality:
1. Navigate to the `.clinerules/` directory.
2. Start with the main lesson plan (e.g., `comprehending_the_text_analyzer.md`) to systematically understand each component of the `text_analyzer` package.

### Option 2: Jump Right In

1. Ensure you have Python 3.7+ and the dependencies from `requirements.txt` installed.
   ```bash
   pip install -r requirements.txt 
   ```
2. Navigate to the `text_analyzer` project directory.
3. Run the main analyzer script:
   ```bash
   python analyzer.py
   ```
4. Follow the on-screen menu prompts to load a file and select analyses.

## ✨ Core Functionality

The `text_analyzer` package offers a comprehensive suite of features:

1.  **Flexible File Input:** Load text from a default sample file or provide a path to a custom text file.
2.  **Configurable Analysis:**
    *   Specify the number of top words to display.
    *   Utilize a configurable list of stop words, which can be customized in `config.py`.
3.  **Multiple Analysis Types:**
    *   **Word Frequency Analysis:** Identify the most common words.
    *   **Sentence Analysis:** Get total sentence count, average sentence length, and identify the longest and shortest sentences.
    *   **Readability Scores:** Calculate metrics like the Flesch-Kincaid Grade Level to assess text complexity.
    *   **Common Text Patterns:** Extract predefined patterns (e.g., dates, emails - configurable via `config.py`).
4.  **Save Results:** Option to save the detailed analysis output to a text file for later review.
5.  **Modular Design:** Each part of the analysis pipeline (I/O, processing, analysis, display) is handled by a separate module, making the codebase easy to understand, maintain, and extend.

## 🚀 How to Run the Script

1.  Ensure you have Python 3.7+ installed.
2.  Install necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Navigate to the `text_analyzer` directory in your terminal.
4.  Run the application using:
    ```bash
    python analyzer.py
    ```
    Alternatively, if you are outside the `text_analyzer` directory but it's in your Python path, you might run it as a module (though direct script execution is more common for this setup):
    ```bash
    python -m text_analyzer.analyzer
    ```
5.  The application will start, presenting you with a menu to guide you through loading a file and selecting analysis options.

## 🧠 Connecting to the World of LLMs

This text analyzer, while simpler than the sophisticated systems used for Large Language Models (LLMs), demonstrates several core principles crucial in the LLM lifecycle:

-   **Data Preprocessing:** LLMs are trained on vast quantities of text. This text undergoes extensive cleaning and normalization, similar to the functions in `text_processing.py`, but on a much larger and more complex scale. This includes lowercasing, punctuation removal, and often more advanced techniques like Unicode normalization and HTML stripping.
-   **Tokenization:** LLMs don't process raw text directly. They use advanced tokenizers (e.g., Byte Pair Encoding (BPE), WordPiece, SentencePiece) to break text into tokens (words, sub-words, or characters). Our `tokenize_text` function using `.split()` is a basic illustration of this vital step. Understanding this helps appreciate the nuances of how LLMs "see" and process language.
-   **Feature Extraction & Analysis:** While we perform explicit analyses like frequency counts and readability scores, LLMs learn to extract complex features and patterns from token sequences through their neural network layers. The statistical properties of text that our tool highlights (like word distributions and sentence structures) are foundational to what LLMs implicitly learn.
-   **Stop Word Removal:** Often, common words (stop words) are removed in NLP tasks to focus on more meaningful terms. This is a common preprocessing step that our tool also supports, reflecting practices in some NLP pipelines.

By understanding the operations in this `text_analyzer`, you get a tangible insight into the initial data handling and analytical concepts that underpin the development and functioning of advanced LLMs.

## 📚 Understanding the Text Analyzer: A Guided Tour

To help you explore and understand this `text_analyzer` package, a set of lesson plans is available in the `.clinerules/` directory. These are designed to be used ideally with an AI copilot to guide your learning.

The main guide, "Comprehending the Text Analyzer," is structured into modules:

-   **Module A: Project Overview & Setup** - High-level introduction to the tool's purpose, features, and how to get it running.
-   **Module B: Configuration & File I/O (`config.py`, `file_io.py`)** - Understanding how the tool is configured and how it handles file operations.
-   **Module C: Text Processing (`text_processing.py`)** - Diving into text cleaning, tokenization, and stop word removal.
-   **Module D: The Analysis Engine (`analysis.py`)** - Exploring how different text analyses (frequencies, sentence stats, readability, patterns) are performed.
-   **Module E: Displaying Results (`display.py`)** - How the analysis output is formatted and presented to the user.
-   **Module F: Orchestration & Main Application (`analyzer.py`)** - Understanding how the main script ties all modules together and manages user interaction.
-   **Module G: Extending the Analyzer & AI Copilot Collaboration** - Guidance on how you might extend the tool and effectively use an AI copilot for development and comprehension.

These modules aim to provide a clear path to understanding the existing codebase, its design choices, and how each part contributes to the overall functionality.

## ✅ Success Criteria

You'll know you've successfully understood this `text_analyzer` tool when you can:

-   [ ] Explain the primary role and responsibilities of each Python module (`analyzer.py`, `config.py`, `file_io.py`, `text_processing.py`, `analysis.py`, `display.py`) in the package.
-   [ ] Run the text analyzer with different input files and configuration settings (e.g., changing the number of top words, modifying stop words) and accurately interpret the various analysis outputs.
-   [ ] Describe the general data flow: how text is read, processed, analyzed, and finally displayed by the tool.
-   [ ] Identify which module(s) you would need to investigate or modify to implement a specific enhancement (e.g., adding a new type of text analysis, changing an existing cleaning rule).

## 💡 Further Exploration

Once you have a solid understanding of the `text_analyzer` package, you might consider these enhancements:

-   **Add New Analysis Modules:** Implement new types of text analysis in `analysis.py`, such as:
    *   Part-of-speech tagging.
    *   Named entity recognition.
    *   Sentiment analysis (basic keyword-based or using a simple library).
    *   N-gram frequency analysis (bigrams, trigrams).
-   **Improve Existing Algorithms:** Refine the algorithms in `analysis.py` or `text_processing.py`. For example, improve the readability formula or add more sophisticated cleaning options.
-   **Integrate Other Data Sources:** Modify `file_io.py` to support reading from URLs or other text-based formats.
-   **Enhance Configuration:** Allow more configurations to be set via command-line arguments or a more interactive configuration process.
-   **Develop a Simple GUI:** Use a library like Tkinter or PyQt to create a graphical user interface for the tool.
-   **Output to Different Formats:** Extend `file_io.py` and `display.py` to allow saving results in formats like CSV or JSON.

This tool provides a solid foundation for experimenting with various text analysis techniques. Happy analyzing!
