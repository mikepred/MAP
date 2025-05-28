# Module F: Main Orchestration and Testing (`analyzer.py`)

**Welcome to Module F!** This is where all the pieces come together. We'll explore `analyzer.py`, the main script that you execute. It handles user interaction, orchestrates the calls to various modules we've already discussed, and even includes a basic testing function.

**Prerequisites:**
*   Completion of [Module E: Displaying Results](comprehending-E-display.md).
*   Understanding of how functions from different files (modules) can be imported and used in Python.

**Learning Objectives:**
*   Understand the role of `analyzer.py` as the main entry point and controller of the application.
*   Learn how the main menu and user choices are handled.
*   See how `analyzer.py` integrates functions from `file_io.py`, `text_processing.py`, `analysis.py`, and `display.py`.
*   Understand the purpose of helper functions like `_perform_analysis_and_display`.
*   Learn how user-defined configurations (like top words count, stop word usage) are obtained and passed through the system.
*   Understand the functionality of the built-in `run_comprehensive_test` feature.

---

## 1. The Conductor: `analyzer.py`

Think of `analyzer.py` as the conductor of an orchestra. The other modules (`file_io.py`, `text_processing.py`, `analysis.py`, `display.py`, `config.py`) are like different sections of the orchestra, each proficient with their instruments (functions). `analyzer.py` tells them when and what to play.

Open `text_analyzer/analyzer.py` in your editor.

**Key Imports:**
At the top, you'll see imports from all the other modules in the package:
```python
from . import config as cfg
from . import file_io
from . import text_processing as tp
from . import analysis
from . import display
```
The `.` indicates a relative import from the current package (`text_analyzer`).

---

## 2. The Main Menu: `main()` Function

The `main()` function is the heart of the user interaction.

*   **Loop:** It runs a `while True` loop to continuously display the menu until the user chooses to exit.
*   **Menu Display:** Prints the options (Analyze Fixed File, Analyze Custom File, Run Tests, Help, Exit).
*   **User Input:** Prompts the user for `choice = input(...)`.
*   **Conditional Logic:** Uses `if/elif/else` statements to call different functions based on the user's choice.
    *   `_handle_analyze_file_option()` for fixed file.
    *   `_handle_custom_file_option()` for custom file.
    *   `run_comprehensive_test()` for tests.
    *   Prints help directly or exits.
*   **Error Handling:** Includes a `try-except KeyboardInterrupt` to gracefully exit on Ctrl+C and a generic `except Exception` to catch other unexpected errors in the menu logic.

---

## 3. Core Workflow: `_handle_analyze_file_option()` and `_handle_custom_file_option()`

These are internal helper functions called by `main()`.

*   **`_handle_analyze_file_option()`**:
    1.  Gets the fixed file path from `cfg.FIXED_TARGET_FILEPATH`.
    2.  Validates it using `file_io.validate_file_path`.
    3.  Reads the file content using `file_io.read_file`.
    4.  If content is loaded, calls `_perform_analysis_and_display`.
*   **`_handle_custom_file_option()`**:
    1.  Calls `file_io.load_text_file()` which handles prompting the user for a filename and reading it.
    2.  If content is loaded, calls `_perform_analysis_and_display`.

---

## 4. Central Analysis & Display Logic: `_perform_analysis_and_display(...)`

This internal helper function is crucial as it centralizes the sequence of operations once file content is available.

*   **Inputs:** `file_content: str`, `source_filename_hint: str`.
*   **Steps:**
    1.  **Get User Configuration:** Calls `get_user_input_config()` to ask the user how many top words to display and whether to use stop words.
    2.  **Run Analysis:** Calls `analysis.analyze_text_complete()`, passing the file content and user configurations. This is where the core analysis happens. It also times this operation using `time_function`.
    3.  **Display Results:**
        *   Prompts the user to choose a display format (Complete, Quick Summary, Both).
        *   Calls the appropriate functions from `display.py` (`display_complete_analysis`, `display_summary`).
    4.  **Word Length Analysis Display:** Calls `analysis.analyze_word_lengths` (to get the Counter) and then `display.display_word_length_analysis`.
    5.  **Save Results (Optional):** Asks the user if they want to save the results and, if yes, calls `file_io.save_results_to_file()`.

---

## 5. User Configuration: `get_user_input_config() -> Tuple[int, bool]`

This function is responsible for interactively asking the user for analysis parameters:

*   Number of top words to display (with a default from `cfg.DEFAULT_TOP_WORDS_DISPLAY`).
*   Whether to remove stop words (defaults to `True`).
*   Includes input validation and retry logic for these questions.
*   Returns the chosen number of words and a boolean for stop word usage.

---

## 6. System Testing: `run_comprehensive_test() -> bool`

This function provides a way to perform a basic sanity check on the various components of the `text_analyzer`.

*   **Structure:** It's organized into sections testing File I/O, Text Processing, Analysis, and Display.
*   **Assertions:** Uses `assert` statements to check if functions produce expected outputs for given inputs. For example:
    *   `assert cleaned_for_words == "expected output"`
    *   `assert num_sentences == 2`
*   **Limitations:** While useful, these tests are not exhaustive and are part of the script itself. For more rigorous testing, dedicated frameworks like `pytest` are typically used in larger projects.
*   **Output:** Prints whether each component test passed or failed and an overall summary.

---

## 7. Utility: `time_function(func: callable, *args: Any, **kwargs: Any) -> Tuple[Any, float]`

A simple utility function that takes another function (`func`) and its arguments, executes it, and measures the execution time.

*   Returns a tuple: the result of the function call and the duration in seconds.
*   This is used in `_perform_analysis_and_display` to time the `analysis.analyze_text_complete` call.

**AI Copilot Interaction Prompts:**

*   "In `analyzer.py`, trace the execution flow if a user chooses option '1' from the main menu. Which functions are called in what order?"
*   "Explain the purpose of `*args` and `**kwargs` in the `time_function` signature in `analyzer.py`."
*   "How could the `run_comprehensive_test` function be improved to provide more detailed feedback on test failures?"
*   "If I wanted to add a new main menu option to `analyzer.py`, what parts of the `main()` function would I need to modify?"
*   "Where in `_perform_analysis_and_display` is the decision made whether to remove stop words or not, and how is that decision passed to the analysis functions?"

---

## Next Steps

We've now seen how all the modules are orchestrated by `analyzer.py`. The final module will focus on how you can use this understanding to extend the `text_analyzer`, and how an AI copilot can assist in that process.

➡️ **Continue to [Module G: Extending the Analyzer and AI Copilot Usage (Conceptual)](comprehending-G-extending.md)**
