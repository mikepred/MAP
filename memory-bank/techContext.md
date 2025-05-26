# Tech Context

This document covers the technologies used in the project, the development setup, technical constraints, dependencies, and tool usage patterns.

## Technologies Used

*   **Python**: Version 3.7 or higher is required to run the `analyzer.py` script.
*   **Standard Library**: The current implementation (Module 3B) uses `os` and `pathlib`. Future modules will incorporate:
    *   `collections`: The `Counter` class will be used for efficient word frequency counting (Module 3C).
    *   `string`: The `string.punctuation` constant and `str.maketrans()` method will be used for text cleaning (Module 3C).
    *   `re`: The regular expression module will be used for more advanced text cleaning and sentence splitting (Module 3C).
*   **(Optional) NLTK/spaCy**: If enhancements from Module 4 are implemented (e.g., stop word removal, advanced cleaning), the Natural Language Toolkit (NLTK) or spaCy libraries may be used.

## Development Setup

*   **Python Installation**: Ensure Python 3.7+ is installed and accessible from the command line.
*   **Text Editor/IDE**: A text editor or Integrated Development Environment (IDE) is needed to view and modify the `analyzer.py` script and other project files. Popular options include VS Code, PyCharm, Sublime Text, and Atom.
*   **Virtual Environment**: Module 3A of the lesson plan recommends creating and activating a virtual environment as a professional development practice. This helps isolate project dependencies and is good practice even if no external libraries are immediately added.

## Technical Constraints

*   **Simple Design**: The project is intentionally designed to be simple and accessible for beginners. It does not address the complexities of real-world text processing, such as handling very large datasets, dealing with noisy or unstructured text, or implementing advanced linguistic features.
*   **Basic Tokenization**: The use of `.split()` for tokenization is a simplification. It does not handle contractions, hyphenated words, or other complex tokenization scenarios effectively.

## Dependencies

*   The current functionality of `analyzer.py` (up to Module 3B) relies only on Python's standard library (`os`, `pathlib`). No external dependencies are currently required.
*   Future modules (3C onwards) will continue to primarily use the standard library (`collections`, `string`, `re`).
*   If enhancements from Module 4 are implemented, the following external dependencies may be required:
    *   `nltk`: Natural Language Toolkit (if stop word removal or other advanced features are added). Install with `pip install nltk`.
    *   `spacy`: Industrial-strength NLP library (if more sophisticated NLP tasks are implemented). Install with `pip install spacy`.

## Tool Usage Patterns

*   The `analyzer.py` script is executed from the command line using the `python analyzer.py` command.
*   The script reads text data from a specified input file (default: `sample.txt`). The user may modify this file or provide a different file path.
*   The script outputs the analysis results (the most common words and their counts) to the console.
