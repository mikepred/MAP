# 🐍 Python Text Analyzer: Your First Step into NLP and LLMs

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-brightgreen.svg)
![Learning](https://img.shields.io/badge/learning-NLP%20foundations-orange.svg)

> **"Every journey into AI begins with understanding text."**  
> *Transform raw text into insights with Python*

## 📊 What You'll Build

```
Input Text → Clean → Tokenize → Count → Display Results
    ↓         ↓        ↓        ↓         ↓
"Hello!"  → "hello"  → ["hello"] → {hello: 1} → Top Words
```

**Example Output:**
```
Top 5 most common words:
1. the: 42 occurrences
2. and: 28 occurrences  
3. to: 21 occurrences
4. of: 19 occurrences
5. in: 15 occurrences
```

## 🎯 Learning Objectives

By completing this project and following the associated lesson plan, you will:
- Understand the importance of text processing in the modern world of data.
- Learn how to read text data from files using Python.
- Master basic text cleaning techniques, such as lowercasing and punctuation removal.
- Grasp the concept of tokenization and implement a simple word tokenizer.
- Utilize Python's `collections.Counter` to efficiently count word frequencies.
- Be able to display analytical results in a clear and readable format.
- Appreciate how these foundational techniques relate to the preprocessing pipelines in Large Language Models (LLMs).
- Gain experience in structuring a Python script with modular functions.

## 🎓 Prerequisites

**What you need to know:**
- [ ] Basic Python syntax (variables, functions, loops)
- [ ] How to run Python scripts from command line
- [ ] Basic understanding of text files

**What you'll learn:**
- [ ] File I/O operations
- [ ] String manipulation techniques
- [ ] Data structure usage (dictionaries, lists)
- [ ] Code organization with functions

## 📂 Project Structure

The project is organized as follows:

-   `analyzer.py`: The main Python script where you'll implement the text analysis logic.
-   `sample.txt`: A sample text file provided as input for your analyzer. Feel free to experiment with your own text files too!
-   `README.md`: This file – your guide to the project.

## ⚡ Quick Start

### Option 1: Follow the Full Lesson Plan (Recommended)
```bash
# Start with Module 1 for complete understanding
# Then work through each module systematically
```

### Option 2: Jump Right In
```bash
git clone [repository-url]
cd text_analyzer
python analyzer.py
# Follow prompts or modify sample.txt
```

## ✨ Core Functionality

The `analyzer.py` script you will build (or enhance) performs a sequence of text processing tasks:

1.  **Read File:** Loads text content from the specified input file (e.g., `sample.txt`).
2.  **Clean Text:** Normalizes the text by:
    *   Converting all characters to lowercase to ensure case-insensitive analysis.
    *   Removing punctuation marks to focus on word content.
3.  **Tokenize Text:** Splits the cleaned text into a list of individual words (tokens).
4.  **Count Frequencies:** Calculates how many times each unique word appears in the token list.
5.  **Display Results:** Shows the most frequently occurring words, providing insights into the text's content.

## 🐛 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| `python: command not found` | Install Python 3.7+ or use `python3` |
| `FileNotFoundError` | Ensure `sample.txt` exists in the same directory |
| Script runs but no output | Check if your text file has content |
| Encoding errors | Save your text file as UTF-8 |

**Need help?** Check Module 4 for detailed troubleshooting steps.

## 🚀 How to Run the Script

1.  Ensure you have Python 3.7+ installed on your system.
2.  Make sure the `analyzer.py` script and `sample.txt` (or your chosen text file) are in the same directory.
3.  Open your terminal or command prompt.
4.  Navigate to the `text_analyzer` project directory.
5.  Run the script using the command:
    ```bash
    python analyzer.py
    ```
6.  The script will output the analysis, including the most common words found in `sample.txt`.

*(Note: The `analyzer.py` script in its final form, as per Module 3 and 4 of the lesson plan, may include interactive prompts for filename and number of top words, or options for stop-word removal.)*

## 🧠 Connecting to the World of LLMs

This seemingly simple text analyzer touches upon core principles vital to Large Language Models (LLMs) like GPT-4 or Claude:

*   **Data Preprocessing:** LLMs are trained on vast amounts of text. This text must first be cleaned and normalized, much like our `clean_text` function, though on a much larger and more complex scale.
*   **Tokenization:** LLMs don't see words as we do. They use sophisticated tokenizers (e.g., Byte Pair Encoding (BPE), WordPiece, SentencePiece) to break text into manageable pieces (tokens). Our `tokenize_text` function using `.split()` is a very basic form of this crucial step. Understanding this helps appreciate the complexity involved in LLM tokenization (see `llms-from-scratch` Ch02 for advanced techniques).
*   **Frequency Analysis & Embeddings:** While we count raw word frequencies, LLMs learn dense vector representations (embeddings) for tokens. These embeddings capture semantic meaning. However, the underlying statistical patterns in language, which frequency analysis begins to reveal, are fundamental to how these embeddings are learned.

**Fun Fact:** The text cleaning you're doing is similar to what happened to prepare the training data for this very conversation!

This project provides a tangible entry point to demystify the initial data handling stages that every LLM undergoes.

## 📚 Lesson Plan Modules Overview

This project is best understood by following the accompanying lesson plan:

-   **Module 1: Introduction & Setting the Stage** - Overview of text processing and project setup.
-   **Module 2: Core Python Concepts for Text Processing** - File handling, text cleaning, tokenization, and frequency counting.
-   **Module 3: Building the Script - Step-by-Step** - Implementation details and code examples.
-   **Module 4: Testing and Refinement** - Running, debugging, and improving the script.
-   **Module 5: Connecting to the Bigger World of LLMs** - Understanding how this relates to LLM development.

## ✅ Success Criteria

You'll know you've mastered this project when you can:

- [ ] Explain why text cleaning is important
- [ ] Modify the script to handle different file formats
- [ ] Predict which words will be most common before running analysis
- [ ] Connect each function to a real-world NLP application
- [ ] Explain how this relates to LLM preprocessing

**Bonus Achievement:** Implement one enhancement from Module 4!

## 💡 Further Exploration

Once you've mastered the basics with this project, consider these enhancements (some are covered in Module 4):

*   Implement stop-word removal.
*   Allow the user to specify the input file and the number of top words to display.
*   Output the results to a new file instead of just printing to the console.
*   Experiment with different text sources.
*   Explore more advanced NLP libraries like NLTK or spaCy.
*   Dive deeper into the `llms-from-scratch` repository to see how these concepts scale up.

Happy analyzing!
