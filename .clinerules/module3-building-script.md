---
## File: `.clinerules/module3-building-script.md`
---

# 🚀 Module 3: Building the Script - Step-by-Step

**Overview:** This module provides complete implementations for each function and shows how to assemble them into a working text analysis script.

---

## 3.1 Structuring Your `analyzer.py`

### Recommended File Layout for `analyzer.py`

```python
# analyzer.py - Text Processing Script

# Import required modules
from collections import Counter
import string

# Define all your functions here
def read_file(filepath):
    # Implementation here
    pass

def clean_text(text):
    # Implementation here
    pass

def tokenize_text(text):
    # Implementation here
    pass

def count_frequencies(tokens):
    # Implementation here
    pass

def display_most_common(frequencies, n):
    # Implementation here
    pass

# Main execution block
if __name__ == "__main__":
    # Your main logic will go here
    filepath = "sample.txt"
    num_common_words = 10

    # Call your functions in sequence
    # text_content = read_file(filepath)
    # cleaned_content = clean_text(text_content)
    # ... and so on
```

### Why This Structure is Recommended

- **Imports at top:** All dependencies clearly visible
- **Functions before main:** Define tools before using them
- **`if __name__ == "__main__"`:** Makes script runnable but also importable
- **Clear variable names:** Easy to follow the data flow

---

## 3.2 Implementing `read_file(filepath)`

### Goal for `read_file`

Takes a filepath string, returns the content of the file as a string.

### Complete `read_file` Implementation

```python
def read_file(filepath):
    """
    Reads a file and returns its content as a string.
    
    Args:
        filepath (str): Path to the file to read
        
    Returns:
        str or None: File content as string, or None if error occurs
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
```

### Key Features of `read_file`

- **Error handling:** Gracefully handles missing files and other errors
- **UTF-8 encoding:** Handles international characters properly
- **Return None on error:** Allows calling code to check for success
- **Informative error messages:** Helps with debugging

---

## 3.3 Implementing `clean_text(text)`

### Goal for `clean_text`

Takes a string, returns a cleaned string (lowercase, no punctuation).

### Complete `clean_text` Implementation

```python
def clean_text(text):
    """
    Converts text to lowercase and removes punctuation.
    
    Args:
        text (str or None): The input text to clean
        
    Returns:
        str: The cleaned text (empty string if input was None)
    """
    if text is None:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation using translation table
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    
    return text
```

### Why This Approach for `clean_text`?

- **Null safety:** Handles None input gracefully
- **Efficient punctuation removal:** `str.maketrans()` is faster than multiple `.replace()` calls
- **Standard library:** Uses `string.punctuation` for comprehensive coverage

### What `string.punctuation` Includes

```python
import string
print(string.punctuation)
# Output: !"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
```

---

## 3.4 Implementing `tokenize_text(text)`

### Goal for `tokenize_text`

Takes a cleaned string, returns a list of words.

### Complete `tokenize_text` Implementation

```python
def tokenize_text(text):
    """
    Splits text into a list of words (tokens).
    
    Args:
        text (str): The input text to tokenize
        
    Returns:
        list: List of word tokens
    """
    if not text:  # Handle empty or None text
        return []
    
    # split() handles multiple spaces, tabs, newlines automatically
    return text.split()
```

### Why `.split()` Is Perfect Here for `tokenize_text`

- **Handles whitespace:** Automatically deals with multiple spaces, tabs, newlines
- **No empty strings:** Unlike `text.split(' ')`, it won't create empty list elements
- **Simple and reliable:** Built-in method optimized for this exact use case

### `tokenize_text` Example Usage

```python
text = "hello    world\\n\\tpython   programming"
tokens = tokenize_text(text)
print(tokens)
# Output: ['hello', 'world', 'python', 'programming']
```

---

## 3.5 Implementing `count_frequencies(tokens)`

### Goal for `count_frequencies`

Takes a list of tokens, returns a `collections.Counter` of word frequencies.

### Complete `count_frequencies` Implementation

```python
def count_frequencies(tokens):
    """
    Counts the frequency of each token in a list.
    
    Args:
        tokens (list): List of word tokens
        
    Returns:
        Counter: Counter object with word frequencies
    """
    return Counter(tokens)
```

### Why `Counter` is Simple for `count_frequencies`?

`Counter` is designed exactly for this purpose! It:

- Counts all items in an iterable automatically
- Handles missing keys gracefully
- Provides useful methods like `.most_common()`

### `count_frequencies` Example Usage

```python
tokens = ['apple', 'banana', 'apple', 'cherry', 'apple', 'banana']
frequencies = count_frequencies(tokens)
print(frequencies)
# Output: Counter({'apple': 3, 'banana': 2, 'cherry': 1})
```

---

## 3.6 Implementing `display_most_common(frequencies, n)`

### Goal for `display_most_common`

Takes a `Counter` object and an integer `n`, prints the `n` most common words.

### Complete `display_most_common` Implementation

```python
def display_most_common(frequencies, n):
    """
    Displays the n most common words and their frequencies.
    
    Args:
        frequencies (Counter): Counter object with word frequencies
        n (int): Number of top words to display
    """
    if not frequencies:
        print("No frequencies to display.")
        return
    
    most_common = frequencies.most_common(n)
    
    print(f"\nTop {n} most common words:")
    print("-" * 30)
    for word, count in most_common:
        print(f"{word:15} : {count:3d}")
    print("-" * 30)
    print(f"Total unique words: {len(frequencies)}")
```

### Enhanced Features of `display_most_common`

- **Empty check:** Handles case where no words were found
- **Formatted output:** Nice alignment and visual separators
- **Additional info:** Shows total unique word count
- **Professional appearance:** Looks clean and informative

### `display_most_common` Example Output

```text
Top 5 most common words:
------------------------------
the             :  12
and             :   8
of              :   7
to              :   6
a               :   5
------------------------------
Total unique words: 45
```

---

## 3.7 The `if __name__ == "__main__":` Block

### Concept of `__name__ == "__main__"`

This Python idiom allows your script to be both runnable and importable.

### Complete Main Block Implementation

```python
if __name__ == "__main__":
    # Configuration
    filepath = "sample.txt"
    num_common_words = 10
    
    print("Text Analysis Script")
    print("=" * 50)
    
    # Step 1: Read the file
    print(f"Reading file: {filepath}")
    raw_text = read_file(filepath)
    
    if raw_text is None:
        print("Failed to read file. Exiting.")
        exit(1)
    
    print(f"File read successfully. Length: {len(raw_text)} characters")
    
    # Step 2: Clean the text
    print("Cleaning text...")
    cleaned_text = clean_text(raw_text)
    print(f"Text cleaned. Length: {len(cleaned_text)} characters")
    
    # Step 3: Tokenize
    print("Tokenizing text...")
    tokens = tokenize_text(cleaned_text)
    print(f"Found {len(tokens)} total words")
    
    # Step 4: Count frequencies
    print("Counting word frequencies...")
    frequencies = count_frequencies(tokens)
    
    # Step 5: Display results
    display_most_common(frequencies, num_common_words)
    
    print("\nAnalysis complete!")
```

### Key Features of the Main Block

- **Progress updates:** Shows what's happening at each step
- **Error handling:** Exits gracefully if file reading fails
- **Informative output:** Shows statistics about the processing
- **Clear structure:** Easy to follow the data flow

---

## 3.8 Complete Script Assembly

### Your Final `analyzer.py`

Here's how all the pieces fit together:

```python
"""
Text Analysis Script - A Foundation for Understanding LLM Preprocessing

This script demonstrates the basic text processing pipeline used in
natural language processing and machine learning applications.
"""

from collections import Counter
import string

def read_file(filepath):
    """Reads a file and returns its content as a string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def clean_text(text):
    """Converts text to lowercase and removes punctuation."""
    if text is None:
        return ""
    
    text = text.lower()
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    
    return text

def tokenize_text(text):
    """Splits text into a list of words (tokens)."""
    if not text:
        return []
    return text.split()

def count_frequencies(tokens):
    """Counts the frequency of each token in a list."""
    return Counter(tokens)

def display_most_common(frequencies, n):
    """Displays the n most common words and their frequencies."""
    if not frequencies:
        print("No frequencies to display.")
        return
    
    most_common = frequencies.most_common(n)
    
    print(f"\nTop {n} most common words:")
    print("-" * 30)
    for word, count in most_common:
        print(f"{word:15} : {count:3d}")
    print("-" * 30)
    print(f"Total unique words: {len(frequencies)}")

if __name__ == "__main__":
    # Configuration
    filepath = "sample.txt"
    num_common_words = 10
    
    print("Text Analysis Script")
    print("=" * 50)
    
    # Execute the pipeline
    print(f"Reading file: {filepath}")
    raw_text = read_file(filepath)
    
    if raw_text is None:
        print("Failed to read file. Exiting.")
        exit(1)
    
    print(f"File read successfully. Length: {len(raw_text)} characters")
    
    print("Cleaning text...")
    cleaned_text = clean_text(raw_text)
    print(f"Text cleaned. Length: {len(cleaned_text)} characters")
    
    print("Tokenizing text...")
    tokens = tokenize_text(cleaned_text)
    print(f"Found {len(tokens)} total words")
    
    print("Counting word frequencies...")
    frequencies = count_frequencies(tokens)
    
    display_most_common(frequencies, num_common_words)
    
    print("\nAnalysis complete!")
```

---

## Testing Your Script

### Running the Script

1. Save the complete code as `analyzer.py`
2. Make sure `sample.txt` exists in the same directory
3. Run from command line:

   ```bash
   python analyzer.py
   ```

### Expected Output Format from `analyzer.py`

```text
Text Analysis Script
==================================================
Reading file: sample.txt
File read successfully. Length: 487 characters
Cleaning text...
Text cleaned. Length: 429 characters
Tokenizing text...
Found 78 total words
Counting word frequencies...

Top 10 most common words:
------------------------------
the             :   6
and             :   4
of              :   3
text            :   3
to              :   3
...
------------------------------
Total unique words: 65

Analysis complete!
```

---

## Module 3 Summary

### What You've Built in Module 3

A complete text processing pipeline that:

- ✅ Safely reads text files
- ✅ Cleans and normalizes text data
- ✅ Tokenizes text into words
- ✅ Counts word frequencies
- ✅ Displays results in a professional format

### Key Programming Concepts Applied in Module 3

- **Error handling** with try/except blocks
- **Modular design** with focused functions
- **Professional output** formatting
- **Script vs. module** design with `if __name__ == "__main__"`

---

## Next Steps

Ready to test and refine your script? Continue to **[Module 4: Testing and Refinement](module4-testing.md)** where we'll run the script, handle edge cases, and explore potential improvements.

*Note: The core implementation concepts in this module are covered in **[Module 2A: Core Text Processing Pipeline](../module2A-core-pipeline.md)**. For deeper insights into code quality and professional practices, refer to **[Module 2B: Code Design & Quality Practices](../module2B-code-quality.md)** and **[Module 2C: Professional Development Practices](../module2C-professional-dev.md)**.*

---

## Quick Debugging Tips

**Common Issues:**

- **File not found:** Check that `sample.txt` exists in the same directory
- **Import errors:** Make sure you have the imports at the top of your file
- **Encoding issues:** The `encoding='utf-8'` parameter should handle most text files
- **Empty output:** Check that your `sample.txt` file has content
