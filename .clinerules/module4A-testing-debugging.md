# 🧪 Module 4A: Testing and Debugging Fundamentals

**Overview:** This module focuses on validating the script developed in Module 3, learning fundamental debugging skills, and ensuring your text analyzer is running correctly before adding enhancements.

**Estimated Time:** 30-45 minutes

---

## 4.1 Running Your Script

### Initial Test Setup

#### Step 1: Verify Your Files
Make sure you have these files in your project directory:
```
text_analyzer/
├── analyzer.py        # Your complete script from Module 3
└── sample.txt         # Test data file
```

#### Step 2: Test Data Preparation
If you haven't already, create a `sample.txt` file with varied content. Here's a suggestion if you need one:

```text
The quick brown fox jumps over the lazy dog. This sentence contains every letter of the alphabet at least once. Text processing is fascinating! It helps us understand how computers can make sense of human language. From simple word counting to complex language models, everything starts with basic text manipulation. The future of AI depends on our ability to process and understand text data effectively.

Natural Language Processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans through natural language. The ultimate objective of NLP is to read, decipher, understand, and make sense of human languages in a manner that is valuable.

Machine learning and deep learning have revolutionized NLP. Modern applications include chatbots, language translation, sentiment analysis, and text summarization. The processing pipeline we're building mirrors the initial steps used in these advanced systems.
```

#### Step 3: Run the Script
Execute your script from the command line:
```bash
python analyzer.py
```

### Expected Successful Output
Your script's output should look something like this (exact numbers may vary based on your `sample.txt` and Module 3 implementation):
```
Text Analysis Script
==================================================
Reading file: sample.txt
File read successfully. Length: 892 characters
Cleaning text...
Text cleaned. Length: 780 characters
Tokenizing text...
Found 135 total words
Counting word frequencies...

Top 10 most common words:
------------------------------
the             :  10
and             :   8
of              :   6
text            :   4
language        :   4
to              :   4
processing      :   3
nlp             :   3
is              :   3
in              :   3
------------------------------
Total unique words: 89

Analysis complete!
```
If your output matches this, great! If not, the next section on debugging will help.

---

## 4.2 Debugging 🐞

### Common Issues and Solutions

#### Issue 1: File Not Found Error
**Symptoms:**
```
Error: File not found at sample.txt
Failed to read file. Exiting.
```

**Solutions:**
1.  **Check file existence:** Ensure `sample.txt` is in the same directory as `analyzer.py`.
2.  **Check file name:** Verify exact spelling and case sensitivity (e.g., `sample.txt` vs `Sample.txt`).
3.  **Use absolute path (for testing):** Try providing the full path to the file to see if that works.
4.  **Check permissions:** Ensure your user account has permission to read the file.

**Debug technique:**
Add this to the top of your `analyzer.py` (if not already present) or run in a Python interpreter in your project directory:
```python
import os
print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))
```
This helps confirm if Python is looking in the right place and if the file is visible.

#### Issue 2: Empty or No Output for Word Frequencies
**Symptoms:**
- Script runs without errors but shows no word frequencies.
- You might see "No frequencies to display." or an empty list of common words.

**Possible causes:**
1.  **Empty `sample.txt`:** The file might be empty or contain only whitespace.
2.  **Overly aggressive cleaning:** Your `clean_text` function might be removing all characters.
3.  **Encoding issues:** The file might not be read correctly, resulting in empty content after decoding.
4.  **Logic error in tokenization/counting:** Tokens might be empty or the counter might not be updated.

**Debug technique:**
Add temporary `print()` statements at various stages in your `analyzer.py`'s `if __name__ == "__main__":` block:
```python
# Inside if __name__ == "__main__":
# ...
raw_text = read_file(filepath)
print(f"Raw text preview (first 100 chars): {repr(raw_text[:100])}") # repr() shows hidden characters

cleaned_text = clean_text(raw_text)
print(f"Cleaned text preview (first 100 chars): {repr(cleaned_text[:100])}")

tokens = tokenize_text(cleaned_text)
print(f"First 10 tokens: {tokens[:10]}")
print(f"Total tokens: {len(tokens)}")

frequencies = count_frequencies(tokens)
print(f"Frequency counter object: {frequencies}")
print(f"Top 3 from counter: {frequencies.most_common(3)}")
# ...
```

#### Issue 3: Encoding Errors
**Symptoms:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xXX in position YY: invalid start byte
```
Or similar messages indicating an encoding problem.

**Solutions:**
1.  **Verify file encoding:** Ensure `sample.txt` is saved as UTF-8. Most modern text editors do this by default.
2.  **Specify encoding during open (already in Module 3):** Your `read_file` function should use `open(filepath, 'r', encoding='utf-8')`.
3.  **Try alternative encodings (if UTF-8 fails and you suspect a different encoding):**
    ```python
    # In read_file function, for testing:
    # try:
    #     with open(filepath, 'r', encoding='latin-1') as f:
    #         return f.read()
    # except ...
    ```
4.  **Use `errors='ignore'` or `errors='replace'` (use with caution):**
    ```python
    # In read_file function:
    # with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    #     return f.read()
    ```
    This can lead to data loss or corruption, so it's better to fix the file's encoding if possible.

### Interactive Debugging Exercise

To get comfortable with debugging, try intentionally introducing some errors into your `analyzer.py` script and then fixing them:

1.  **Misspell the filename in `analyzer.py`:**
    Change `filepath = "sample.txt"` to `filepath = "sampl.txt"` (missing 'e'). Run the script and observe the `FileNotFoundError`. Use the debugging techniques to identify it.

2.  **Create an empty `sample.txt`:**
    Delete the content of `sample.txt` (or create a new empty file and point your script to it). Run the script. How does it behave? Does it fail gracefully or produce strange output? Ensure it handles this case (e.g., prints "No frequencies to display").

3.  **Problematic content in `sample.txt`:**
    Add a line with only punctuation like `!!!!!!!!!!!!` or a very long string without spaces. Does your `clean_text` and `tokenize_text` handle this as expected?

4.  **Introduce a `TypeError`:**
    Temporarily change a line in `tokenize_text` to something like `return text.split(123)` (passing an integer where a string or None is expected for the separator). Observe the `TypeError` and traceback.

---

## Quick Reference: Common Debugging Commands & Techniques

-   **`print()` statements:** The simplest way to inspect variable values at different points in your code.
    ```python
    print(f"Value of my_variable: {my_variable}")
    print(f"Type of my_variable: {type(my_variable)}")
    print(f"Length of my_list: {len(my_list)}")
    ```
-   **`repr()`:** Use `repr(variable)` to get a string representation that's often more detailed for debugging (e.g., shows quotes around strings, escape characters).
    ```python
    my_string = "Hello\nWorld"
    print(my_string)       # Prints on two lines
    print(repr(my_string)) # Prints 'Hello\\nWorld'
    ```
-   **Python Debugger (`pdb`):** For more advanced, interactive debugging.
    ```python
    import pdb

    # ... your code ...
    pdb.set_trace() # Execution will pause here, and you'll enter the pdb debugger
    # ... more code ...
    ```
    Common `pdb` commands:
    -   `n` (next line)
    -   `c` (continue execution)
    -   `s` (step into function)
    -   `p variable_name` (print variable)
    -   `q` (quit debugger)

-   **Read Tracebacks Carefully:** When an error occurs, Python prints a traceback. Start from the bottom (the most recent call) and work your way up. It tells you the file, line number, and the type of error.

---

By the end of this module, you should be more confident in running your script, identifying potential issues, and using basic debugging strategies to fix them. This is a crucial skill for any programmer!

**Next Up:** [Module 4B: Core Script Enhancements](module4B-core-enhancements.md)
