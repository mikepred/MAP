# 🐍 Python Text Analyzer: A Modular Tool for Text Analysis

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellowgreen.svg)
![Learning](https://img.shields.io/badge/learning-Applied%20NLP-orange.svg)
![Deployment](https://img.shields.io/badge/deployment-render-blueviolet.svg)

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

## 🚀 How to Run the Text Analyzer

There are three primary ways to run the Text Analyzer:

### Option 1: Command-Line Interface (CLI)

This provides a menu-driven interface in your terminal.

1.  **Ensure Prerequisites:**
    *   Python 3.7+ installed.
    *   Navigate to the project's root directory (e.g., `MAP/`).
    *   Install dependencies from the root `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```

2.  **Run the CLI Script:**
    From the project's root directory, execute:
    ```bash
    python -m text_analyzer.analyzer
    ```

3.  **Interact:** Follow the on-screen menu prompts to load a file and select analyses. The CLI also includes an option to run built-in system tests.

### Option 2: Web Graphical User Interface (Web GUI)

This launches a web-based interface that you can access in your browser.

1.  **Set up a Virtual Environment (Recommended):**
    From the project's root directory (`MAP/`):
    ```bash
    # Create a virtual environment (e.g., named 'venv')
    python -m venv venv

    # Activate the virtual environment
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

2.  **Install Dependencies (inside the virtual environment):**
    Install dependencies from the root `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Web Application:**
    From the project's root directory:
    ```bash
    python web_application/app.py
    ```

4.  **Access in Browser:** Open your web browser and navigate to the URL provided in the terminal (usually `http://127.0.0.1:5000` or a similar address).
    The Web GUI now includes interactive charts and features to visualize and explore your text:
      * Word Frequencies (Top N words): A bar chart displaying the most common words. *Click on a word in this chart to see example sentences where it appears.*
      * Sentiment Score Distribution (Positive, Neutral, Negative): A pie chart.
      * Word Length Distribution: A bar chart.
      * User-Defined Pattern Matching: An option to specify one custom regular expression pattern (with a name) to find and display matches from the text.

5.  **Deactivate Virtual Environment (when done):**
    ```bash
    deactivate
    ```

### Option 3: Desktop Graphical User Interface (Desktop GUI)

This launches a local desktop application using Tkinter.

1.  **Ensure Prerequisites:**
    *   Python 3.7+ installed (Tkinter is usually included).
    *   Navigate to the project's root directory.
    *   Install dependencies from the root `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```

2.  **Run the Desktop GUI Script:**
    From the project's root directory:
    ```bash
    python text_analyzer/gui.py
    ```

### Quick Start Tip: Follow the Comprehension Lesson Plan

For a deep dive into the tool's architecture and functionality, especially for the CLI:
1. Navigate to the `.clinerules/` directory within `text_analyzer/`.
2. Start with the main lesson plan (e.g., `comprehending-text-analyzer.md`) to systematically understand each component.

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

The project is organized as follows:

- `web_application/`: Contains the Flask web application.
    - `app.py`: Main script for launching the Web GUI.
    - `templates/`: HTML templates for the web application.
    - `static/`: CSS and other static files for the web application.
    - `tests/`: Unit tests for the web application.
    - `wsgi.py`: WSGI entry point for deployment.
- `text_analyzer/`: Contains the core text analysis logic and CLI/Desktop GUI.
    - `analyzer.py`: Main executable script for the command-line interface (CLI).
    - `gui.py`: Script for launching the local Desktop GUI (Tkinter).
    - `config.py`: Stores all configuration settings.
    - `file_io.py`: Handles file input/output.
    - `text_processing.py`: Functions for text preparation.
    - `analysis.py`: Core analysis functions.
    * `display.py`: Formats and presents CLI results.
    * `__init__.py`: Makes `text_analyzer` a Python package.
    * `sample.txt`, `s.txt`, etc.: Sample text files.
    * `tests/`: Unit tests for the core analyzer.
- `requirements.txt` (in project root): Lists all Python dependencies for the entire project.
- `.clinerules/` (within `text_analyzer/`): Contains lesson plans and guides.

## ✨ Core Functionality (Common across interfaces)

The `text_analyzer` package offers a comprehensive suite of features:

1.  **Flexible File Input:** Load text from a default sample file or provide a path to a custom text file.
2.  **Configurable Analysis:**
    *   Specify the number of top words to display.
    *   Utilize a configurable list of stop words, which can be customized in `config.py`.
3.  **Multiple Analysis Types:**
    *   **Word Frequency Analysis:** Identify the most common words.
    *   **Sentence Analysis:** Get total sentence count, average sentence length, and identify the longest and shortest sentences.
    *   **Comprehensive Readability Assessment:** Calculates a custom complexity score and a suite of standardized readability indices.
    *   **Common Text Patterns:** Extract predefined patterns (e.g., dates, emails - configurable via `config.py`).
    *   **N-gram Frequencies:** Analyzes and displays common N-grams (Bigrams and Trigrams).
    *   **Sentiment Analysis:** Determines overall sentiment (Positive, Negative, Neutral) using VADER.
    *   **Part-of-Speech (POS) Tagging:** Identifies POS tags, lists the most common ones, and calculates Lexical Density.
    *   **Named Entity Recognition (NER):** Detects and categorizes named entities.
4.  **Save Results (CLI):** Option to save the detailed analysis output to a text file.

## 🧠 Connecting to the World of LLMs

This text analyzer, while simpler than the sophisticated systems used for Large Language Models (LLMs), demonstrates several core principles crucial in the LLM lifecycle:

-   **Data Preprocessing:** LLMs are trained on vast quantities of text. This text undergoes extensive cleaning and normalization, similar to the functions in `text_processing.py`.
-   **Tokenization:** LLMs use advanced tokenizers to break text into tokens. Our `tokenize_text` function is a basic illustration of this vital step.
-   **Feature Extraction & Analysis:** The statistical properties of text that our tool highlights are foundational to what LLMs implicitly learn.
-   **Stop Word Removal:** A common preprocessing step in some NLP pipelines, also supported by our tool.

By understanding the operations in this `text_analyzer`, you get a tangible insight into the initial data handling and analytical concepts that underpin the development and functioning of advanced LLMs.

## 📚 Understanding the Text Analyzer: A Guided Tour

To help you explore and understand this `text_analyzer` package, a set of lesson plans is available in the `text_analyzer/.clinerules/` directory. These are designed to be used ideally with an AI copilot to guide your learning.

The main guide, "Comprehending the Text Analyzer," is structured into modules:

-   **Module A: Project Overview & Setup**
-   **Module B: Configuration & File I/O (`config.py`, `file_io.py`)**
-   **Module C: Text Processing (`text_processing.py`)**
-   **Module D: The Analysis Engine (`analysis.py`)**
-   **Module E: Displaying Results (`display.py`)**
-   **Module F: Orchestration & Main Application (`analyzer.py`)**
-   **Module G: Extending the Analyzer & AI Copilot Collaboration**

## ✅ Success Criteria

You'll know you've successfully understood this `text_analyzer` tool when you can:

-   [ ] Explain the primary role of each Python module.
-   [ ] Run the text analyzer with different inputs and configurations.
-   [ ] Describe the general data flow.
-   [ ] Identify which module(s) to modify for specific enhancements.

## 💡 Further Exploration

-   Improve existing algorithms.
-   Integrate other data sources (URLs, PDFs).
-   Enhance configuration options.
-   Output to different formats (CSV, JSON).
-   Implement corpus-level analysis (TF-IDF, topic modeling).

This tool provides a solid foundation for experimenting with various text analysis techniques. Happy analyzing!

---

## 📋 Example Full Analysis Report (CLI Output)

The following is an example of the detailed report generated by the Command-Line Interface:

```text
============================================================
                  📊 TEXT ANALYSIS REPORT 📊
============================================================

📊 General Statistics
--------------------
📄 Total Characters (raw): 242,819
🔤 Characters (raw, no spaces): 202,251
📝 Total Words (after cleaning/stop words): 27,083
📋 Total Sentences: 2,890
📄 Paragraphs: 870
📏 Average Words per Sentence: 9.4

🔤 Word Frequency Analysis
-------------------------
🎯 Unique Words: 7,375
📊 Total Word Count (in analysis): 27,083

🏆 Top 25 Most Common Words:
   1. 'your' - 596 times (2.2%)
   2. 'etymology' - 311 times (1.1%)
   3. 'n' - 252 times (0.9%)
   4. 'as' - 246 times (0.9%)
   5. 'from' - 238 times (0.9%)
   6. 'pronounced' - 230 times (0.8%)
   7. 'all' - 226 times (0.8%)
   8. 'if' - 188 times (0.7%)
   9. 'life' - 157 times (0.6%)
  10. 'out' - 157 times (0.6%)
  11. 'which' - 152 times (0.6%)
  12. 'their' - 149 times (0.6%)
  13. 'how' - 146 times (0.5%)
  14. 'like' - 138 times (0.5%)
  15. 'just' - 137 times (0.5%)
  16. 'into' - 136 times (0.5%)
  17. 'up' - 128 times (0.5%)
  18. 'only' - 126 times (0.5%)
  19. 'when' - 125 times (0.5%)
  20. 'even' - 123 times (0.5%)
  21. 'time' - 122 times (0.5%)
  22. 'what' - 120 times (0.4%)
  23. 'so' - 119 times (0.4%)
  24. 'feel' - 117 times (0.4%)
  25. 'back' - 116 times (0.4%)

📋 Sentence Analysis
-------------------
📊 Total Sentences: 2890
📏 Average Words per Sentence: 14.1

📏 Longest Sentence:
   "the sorrow of imagining the wealth of knowledge forever lost to historyâ knowing weâll never hear th..."

📏 Shortest Sentence:
   "st"

📖 Readability Analysis
----------------------
📐 Average Word Length (of analyzed words): 5.9 characters
🎯 Complexity Score: 9.2
📚 Readability Level: Moderate
   💡 This text requires moderate reading skills.

  Standardized Readability Indices:
    - Flesch Reading Ease: 63.72
    - Flesch-Kincaid Grade Level: 8.51
    - Gunning Fog Index: 10.33
    - SMOG Index: 10.68
    - Coleman-Liau Index: 9.63
    - Dale-Chall Readability Score: 9.23
    - Automated Readability Index (ARI): 9.79

🔍 Interesting Patterns
----------------------
🎨 Word Variety (analyzed words): 27.2% (unique words / total analyzed words)

🔄 Most Repeated Words (among analyzed):
   'your' appears 596 times
   'etymology' appears 311 times
   'n' appears 252 times
   'as' appears 246 times
   'from' appears 238 times

📏 Long Words (7+ characters, among analyzed):
   achenia, maddening, complex, understand, whenever, trivial, question, quickly

🔤 Short Words (1-2 characters, among analyzed):
   n, up, 1, if, nd, so, as, st, no, o

--- Word Length Analysis ---
 1 letter(s):  339 words (  1.3%)
 2 letter(s):  944 words (  3.5%)
 3 letter(s): 2433 words (  9.0%)
 4 letter(s): 6212 words ( 22.9%)
 5 letter(s): 4310 words ( 15.9%)
 6 letter(s): 3454 words ( 12.8%)
 7 letter(s): 3167 words ( 11.7%)
 8 letter(s): 2164 words (  8.0%)
 9 letter(s): 1724 words (  6.4%)
10 letter(s): 1046 words (  3.9%)
11 letter(s):  436 words (  1.6%)
12 letter(s):  305 words (  1.1%)
13 letter(s):  176 words (  0.6%)
14 letter(s):  113 words (  0.4%)
15 letter(s):   77 words (  0.3%)
16 letter(s):   55 words (  0.2%)
17 letter(s):   45 words (  0.2%)
18 letter(s):   30 words (  0.1%)
19 letter(s):   21 words (  0.1%)
20 letter(s):   13 words (  0.0%)
21 letter(s):    9 words (  0.0%)
22 letter(s):    3 words (  0.0%)
23 letter(s):    4 words (  0.0%)
24 letter(s):    1 words (  0.0%)
28 letter(s):    1 words (  0.0%)
31 letter(s):    1 words (  0.0%)

Average word length: 5.9 letters
--------------------------

📊 Bigrams Frequencies
---------------------
   1. 'etymology from' - 117 times
   2. 'as if' - 50 times
   3. 'your life' - 48 times
   4. 'your own' - 47 times
   5. 'even if' - 27 times
   6. 'etymology ancient' - 22 times
   7. 'ancient greek' - 22 times
   8. 'etymology latin' - 22 times
   9. 'your head' - 22 times
  10. 'each other' - 21 times

📊 Trigrams Frequencies
----------------------
   1. 'etymology ancient greek' - 18 times
   2. 'etymology middle english' - 11 times
   3. 'as long as' - 8 times
   4. 'no matter how' - 8 times
   5. 'inside your head' - 7 times
   6. 'as if youâre' - 7 times
   7. 'makes wonder if' - 7 times
   8. 'no way knowing' - 6 times
   9. 'as if your' - 6 times
  10. 'life etymology latin' - 5 times

💖 Sentiment Analysis (VADER)
----------------------------
  Negative Score: 0.082
  Neutral Score:  0.806
  Positive Score: 0.112
  Compound Score: 1.000

  Overall Sentiment: Positive
  (Interpretation based on VADER's compound score thresholds)

🏷️ Part-of-Speech (POS) Tag Analysis (spaCy)
--------------------------------------------
Total POS Tags (excluding punctuation/spaces): 41,242

Most Common POS Tags:
   1. NOUN: 8912 times (21.6%)
   2. VERB: 6046 times (14.7%)
   3. ADP: 4845 times (11.7%)
   4. PRON: 4320 times (10.5%)
   5. DET: 3882 times (9.4%)
   6. ADJ: 3266 times (7.9%)
   7. ADV: 2975 times (7.2%)
   8. AUX: 1695 times (4.1%)
   9. PROPN: 1372 times (3.3%)
  10. CCONJ: 1237 times (3.0%)

Lexical Density: 51.40% (Percentage of content words)

🌍 Named Entity Recognition (NER) Analysis (spaCy)
-------------------------------------------------
Total Named Entity Mentions Found: 859

Most Common Entity Types:
   1. PERSON: 203 mentions (e.g., -lee-et.â, -lee-zee-uhm.â, a.a.... anachl)
   2. DATE: 173 mentions (e.g., 12000, 1609, 1982)
   3. NORP: 153 mentions (e.g., american, appalachian, armenian)
   4. CARDINAL: 139 mentions (e.g., 0, 1, 2)
   5. TIME: 56 mentions (e.g., 5 a.m., a dark morning, a few minutes)

✅ Analysis Complete
-------------------
📝 Report generated successfully!
