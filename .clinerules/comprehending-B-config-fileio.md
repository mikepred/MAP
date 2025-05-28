# Module B: Configuration and File Handling

**Welcome to Module B!** In this section, we'll explore how the `text_analyzer` is configured and how it manages file input/output operations. We'll focus on two key files: `config.py` and `file_io.py`.

**Prerequisites:**
*   Completion of [Module A: Project Overview and Setup](comprehending-A-overview-setup.md).
*   Basic understanding of Python variables, constants, functions, and file operations.

**Learning Objectives:**
*   Understand the role of `config.py` in managing application settings.
*   Identify different types of configurations stored (e.g., paths, stop words, regex).
*   Learn how `file_io.py` handles reading text files, including path validation and error handling.
*   Understand the process of getting user input for filenames.
*   Learn how analysis results are saved to a file.

---

## 1. Centralized Configuration: `config.py`

Good software design often involves separating configuration from the application logic. This makes the application easier to maintain and modify. In `text_analyzer`, `config.py` serves this purpose.

Open `text_analyzer/config.py` in your editor.

**Key Aspects of `config.py`:**

*   **Constants:** It defines various constants used throughout the application. Using uppercase names (e.g., `MAX_FILE_SIZE_BYTES`) is a Python convention for constants.
*   **Path Definitions:**
    *   `SCRIPT_DIRECTORY = Path(__file__).resolve().parent`: This is a robust way to get the directory where `config.py` itself is located. Other paths (like `DEFAULT_SAMPLE_FILEPATH`, `FIXED_TARGET_FILEPATH`) are then defined relative to this.
    *   `Path` from `pathlib` is used for object-oriented path manipulations, making path operations more reliable across different operating systems.
*   **Stop Words:**
    *   `STOP_WORDS: Set[str] = {...}`: A `set` data structure is used for stop words. Sets provide fast membership testing (checking if a word is a stop word).
*   **Regular Expressions (Regex):**
    *   `URL_REGEX: re.Pattern = re.compile(...)`: Commonly used regex patterns are pre-compiled using `re.compile()`. This improves performance if a regex is used multiple times, as the compilation step is done only once.
*   **Numerical Limits and Defaults:**
    *   Constants like `DEFAULT_TOP_WORDS_DISPLAY`, `MAX_FILE_SIZE_BYTES`, `PREVIEW_LENGTH`, and various `DEFAULT_..._LIMIT` values for display ensure consistent behavior and provide easy points for tuning.

**How `config.py` is Used:**

Other modules import values from `config.py`. For example, in `file_io.py`, you might see:
```python
from . import config as cfg
# ...
# if file_size > cfg.MAX_FILE_SIZE_BYTES:
# ...
```
Or in `text_processing.py`:
```python
from . import config as cfg
# ...
# filtered_tokens = [token for token in tokens if token not in cfg.STOP_WORDS]
# ...
```

**AI Copilot Interaction Prompts:**

*   "Explain `Path(__file__).resolve().parent` in `config.py`."
*   "Why is using a `set` for `STOP_WORDS` more efficient than a `list` in `config.py`?"
*   "Show me an example of a pre-compiled regular expression from `config.py` being used in `text_processing.py`."
*   "If I wanted to change the default number of top words displayed, which constant in `config.py` should I modify?"

---

## 2. Managing Files: `file_io.py`

The `file_io.py` module is responsible for all interactions with the file system. This includes reading input files, validating their paths, and writing output files.

Open `text_analyzer/file_io.py` in your editor.

**Key Functions and Their Roles:**

*   **`validate_file_path(filename: Union[str, Path]) -> Tuple[bool, str]`:**
    *   Checks if a given `filename` (which can be a string or a `Path` object) is valid.
    *   Ensures the file exists, is actually a file (not a directory), and doesn't exceed `cfg.MAX_FILE_SIZE_BYTES`.
    *   Returns a tuple: a boolean indicating validity and a message.
*   **`read_file(filename: Union[str, Path]) -> str`:**
    *   Reads the content of the validated file.
    *   Uses `try-except` blocks to handle potential errors like `FileNotFoundError`, `PermissionError`, `UnicodeDecodeError`, etc.
    *   Returns the file content as a string or an empty string if an error occurs.
*   **`get_filename_from_user() -> str`:**
    *   Interactively prompts the user to enter a filename.
    *   Provides retry logic (`cfg.MAX_INPUT_ATTEMPTS`).
    *   Attempts to resolve relative paths against both the Current Working Directory (CWD) and the script's directory.
    *   Uses `validate_file_path` to check the user's input.
*   **`load_text_file() -> str`:**
    *   A workflow function that calls `get_filename_from_user()` and then `read_file()`.
    *   It also prints a preview of the loaded content.
*   **`save_results_to_file(...)`:**
    *   Takes analysis results (like word frequencies) and saves them to a specified output file.
    *   Formats the output before writing.
    *   The default output filename is `cfg.DEFAULT_RESULTS_FILENAME`.

**Error Handling:**

Notice the extensive use of `try-except` blocks in `read_file`. This is crucial for robust applications, as file operations can fail for many reasons outside the program's control.

**Path Resolution in `get_filename_from_user()`:**

This function tries to be smart about finding files:
1.  If an absolute path is given, it's used directly.
2.  If a relative path is given, it first checks relative to the current working directory (where you ran the script from).
3.  If not found there, it checks relative to the script's own directory (`cfg.SCRIPT_DIRECTORY`).
This behavior makes the tool more flexible for the user.

**AI Copilot Interaction Prompts:**

*   "Explain the error handling in the `read_file` function in `file_io.py`. What kind of errors does it catch?"
*   "In `get_filename_from_user`, what is the difference between `Path.cwd()` and `cfg.SCRIPT_DIRECTORY`?"
*   "How does `save_results_to_file` format the output before writing to the file?"
*   "What would happen if `validate_file_path` was not used before trying to read a file in `file_io.py`?"

---

## Next Steps

With an understanding of configuration and file I/O, we're ready to look at how the text data itself is processed. The next module focuses on `text_processing.py`.

➡️ **Continue to [Module C: Text Processing Logic (`text_processing.py`)](comprehending-C-text-processing.md)**
