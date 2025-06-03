# Tech Context

This document covers the technologies used in the project, the development setup, technical constraints, dependencies, and tool usage patterns for each component.

## Text Analyzer (CLI & Core Logic - `text_analyzer/`)

### Technologies Used (Text Analyzer)

* **Python**: Version 3.7 or higher is required.
* **Standard Library**:
  * `os`, `pathlib`: For file system interactions.
  * `collections`: `Counter` for frequency counting, `defaultdict` for NER results.
  * `string`: For punctuation constants.
  * `re`: For regex-based cleaning and splitting.
  * `csv`: For reading CSV files.
  * `json`: For reading JSON files.
* **NLTK (Natural Language Toolkit)**:
    * VADER for sentiment analysis.
    * `rake-nltk` for RAKE keyword extraction.
    * `stopwords` corpus for various languages.
    * `punkt` for tokenization (used by some NLTK components).
* **spaCy**: For Part-of-Speech (POS) tagging and Named Entity Recognition (NER), using the `en_core_web_sm` model.
* **matplotlib**: For generating plots (word frequencies, sentiment distribution, word length distribution).
* **textstat**: For calculating various standard readability indices.
* **pyspellchecker**: For typo correction.

### Development Setup (Text Analyzer)

* **Python Installation**: Ensure Python 3.7+ is installed and accessible from the command line.
* **Text Editor/IDE**: VS Code, PyCharm, Sublime Text, Atom, etc.
* **Virtual Environment**: Recommended.

### Technical Constraints (Text Analyzer)

* **Simple Design**: Intentionally simple for beginners; does not handle very large datasets or highly complex NLP tasks.
* **Basic Tokenization**: Uses `.split()`, which is a simplification and doesn't handle all linguistic nuances.

### Dependencies (Text Analyzer)

* Primarily relies on Python's standard library for core functionalities.
* **NLTK**: External dependency. Requires data packages like `punkt`, `stopwords`, `vader_lexicon`.
* **spaCy**: External dependency. Requires language models like `en_core_web_sm`.
* **matplotlib**: External dependency for plotting.
* **textstat**: External dependency for readability scores.
* **pyspellchecker**: External dependency for typo correction.
* **rake-nltk**: External dependency for keyword extraction.
* **NumPy**: Pinned to `<2.0` in `requirements.txt` to avoid binary incompatibility issues with `thinc` (a spaCy dependency) during deployment on platforms like Render. (Note: This might need review based on current library versions).
* All dependencies are managed in the root `requirements.txt`.

### Tool Usage Patterns (Text Analyzer CLI - `text_analyzer/analyzer.py`)

* Executed via `python -m text_analyzer.analyzer` (as a module to handle relative imports).
* Reads from user-specified input files (.txt, .csv, .json) or a fixed default file.
* Prompts for configurations (top words, stop word strategy, plot generation).
* Outputs analysis results to the console, including textual reports and optionally saves graphical plots to an `analysis_plots` directory (which should be gitignored).
* Can save textual analysis summary to a user-specified file.

### Tool Usage Patterns (Text Analyzer Desktop GUI - `text_analyzer/gui.py`)
* Executed via `python text_analyzer/gui.py`.
* Provides a Tkinter-based graphical interface for the text analyzer functionalities.

## Web Application (`web_application/`)

### Technologies Used (Web Application)

* **Python**: Version 3.7 or higher.
* **Flask**: Web framework for building the application.
* **HTML/CSS**: For structuring and styling the web pages (located in `web_application/templates/` and `web_application/static/`).
* Utilizes the core logic from the `text_analyzer` package for analysis.

### Development Setup (Web Application)

* **Python Installation**: Python 3.7+
* **Virtual Environment**: Strongly recommended.
* Dependencies listed in the root `requirements.txt`.

### Technical Constraints (Web Application)

* Relies on the `text_analyzer` package for its core functionality.
* Designed as a relatively simple web interface for the analyzer.

### Dependencies (Web Application)

* **Flask**: Core web framework.
* Other dependencies are inherited from the `text_analyzer` core logic as needed (NLTK, spaCy, etc.), all managed in the root `requirements.txt`.

### Tool Usage Patterns (Web Application - `web_application/app.py`)

* Run via `python web_application/app.py` for local development.
* Deployed using a WSGI server like Gunicorn (see `Procfile`, `wsgi.py`).
* Provides a web-based GUI for text analysis, allowing file uploads and displaying results, including interactive charts.
