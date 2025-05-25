---
## File: `.clinerules/module2-python-concepts.md`
---
# 🛠️ Module 2: Core Python Concepts for Text Processing

**Overview:** This module covers the essential Python concepts and techniques needed to build our text processing pipeline.

**Table of Contents**
- [2.1 File Handling in Python 📁](#21-file-handling-in-python-️)
- [2.2 Text Cleaning: The Janitor's Work 🧹](#22-text-cleaning-the-janitors-work-🧹)
- [2.3 Tokenization: Breaking Down Words 🧩](#23-tokenization-breaking-down-words-🧩)
- [2.4 Counting Frequencies: Who's Most Popular? 📊](#24-counting-frequencies-whos-most-popular-📊)
- [2.5 Displaying Results: Show Me the Data! ✨](#25-displaying-results-show-me-the-data-✨)
- [2.6 Modular Design with Functions 🧱](#26-modular-design-with-functions-🧱)
- [2.7 Input Validation &amp; Error Handling 🛡️](#27-input-validation--error-handling-🛡️)
- [2.8 Performance Considerations ⚡](#28-performance-considerations-⚡)
- [2.9 Code Style &amp; Consistency 📏](#29-code-style--consistency-📏)
- [2.10 Testing Mindset 🧪](#210-testing-mindset-🧪)
- [2.11 Configuration &amp; Flexibility 🔧](#211-configuration--flexibility-🔧)
- [2.12 Documentation Standards 📚](#212-documentation-standards-📚)
- [2.13 Debugging Tips 🐛](#213-debugging-tips-🐛)
- [2.14 Future-Proofing 🔮](#214-future-proofing-🔮)
- [2.15 Code Organization 📁](#215-code-organization-📁)
- [2.16 Real-World Considerations 🌍](#216-real-world-considerations-🌍)
- [Module 2 Summary](#module-2-summary)
- [Quick Reference](#quick-reference)

---

## 2.1 File Handling in Python 📁

### Concept
Reading data from external files safely and efficiently.

### Key Syntax
Using `with open(...) as f:` for safe file operations:
- `f.read()` - reads entire file as a string
- `f.readlines()` - reads file as a list of lines

### Best Practices
- Always use `with` statements for automatic file closing
- Specify encoding explicitly (usually `utf-8`)
- Handle potential errors gracefully

### Activity
Write a simple function to read the content of `sample.txt` and print it to the console.

**Starting point:**
```python
def read_file(filepath):
    """Reads a file and returns its content as a string."""
    # Your code here
    pass
```

**Key takeaway:** Error handling (e.g., `FileNotFoundError`) is important in real-world scenarios, though we might keep it simple for this project.

---

## 2.2 Text Cleaning: The Janitor's Work 🧹

### Concept
Why cleaning is essential for consistent analysis:
- **Consistency:** "The" and "the" should be treated as the same word
- **Noise reduction:** Remove irrelevant characters that don't contribute to meaning

### Common Cleaning Steps

#### Lowercase Everything
"The" and "the" are the same word for our analysis.
```python
text = text.lower()
```

#### Remove Punctuation
Often, punctuation isn't needed for basic frequency analysis.
```python
import string
text = text.translate(str.maketrans('', '', string.punctuation))
```

#### (Optional Advanced Topic) Stop Word Removal
Common words like "is", "an", "the" might be filtered out. This is conceptual for now - we might implement as a bonus feature.

### Python String Methods to Know
- `.lower()` - converts to lowercase
- `.replace(old, new)` - replaces substrings
- `.isalpha()` - checks if character is alphabetic
- `str.maketrans()` - creates translation table for character replacement

### Activity
Write a function that takes a string, converts it to lowercase, and removes common punctuation (`.`, `,`, `!`, `?`, etc.).

**Starting point:**
```python
def clean_text(text):
    """Converts text to lowercase and removes punctuation."""
    # Your code here
    pass
```

---

## 2.3 Tokenization: Breaking Down Words 🧩

### Concept
**What is tokenization?** Splitting text into individual words or "tokens".

**Why is it important?** 
- Enables word-by-word analysis
- Creates standardized units for processing
- Foundation for all further text analysis

### Simple Tokenization
Using string's `.split()` method:
```python
words = text.split()  # Splits on whitespace
```

The `.split()` method is smart - it handles multiple spaces, tabs, and newlines automatically.

### Connection to LLMs
LLMs use much more sophisticated tokenizers:
- **Byte Pair Encoding (BPE):** Handles unknown words by breaking them into subword units
- **WordPiece:** Similar to BPE, used by models like BERT
- **SentencePiece:** Used by T5 and other models

These advanced tokenizers build fixed-size vocabularies and handle the complexity of real-world text. The `llms-from-scratch` repository (Chapter 2) explores these techniques in detail. Our project uses the basic form to understand the fundamentals.

### Activity
Write a function that takes the cleaned text string and returns a list of words (tokens).

**Starting point:**
```python
def tokenize_text(text):
    """Splits text into a list of words (tokens)."""
    # Your code here
    pass
```

---

## 2.4 Counting Frequencies: Who's Most Popular? 📊

### Concept
How to count occurrences of each word to understand which words appear most frequently in our text.

### Data Structures

#### Dictionaries
A natural fit for word-count pairs:
```python
word_counts = {'word': count, 'another': count}
```

#### `collections.Counter`
A specialized dictionary subclass for counting hashable objects. This is the preferred, more Pythonic way:
```python
from collections import Counter
word_counts = Counter(['word', 'word', 'another', 'word'])
# Result: Counter({'word': 3, 'another': 1})
```

### Why Use Counter?
- Handles missing keys automatically (no KeyError)
- Provides useful methods like `.most_common()`
- More readable and less error-prone than manual dictionary management

### Activity
Write a function that takes a list of tokens and returns a `Counter` object mapping each word to its frequency.

**Starting point:**
```python
from collections import Counter

def count_frequencies(tokens):
    """Counts the frequency of each token in a list."""
    # Your code here
    pass
```

---

## 2.5 Displaying Results: Show Me the Data! ✨

### Concept
Presenting the most common words in a readable, user-friendly format.

### `Counter` Methods
`.most_common(n)` returns a list of (word, count) tuples for the n most frequent items:
```python
counter = Counter(['apple', 'banana', 'apple', 'cherry', 'apple'])
top_2 = counter.most_common(2)
# Result: [('apple', 3), ('banana', 1)]
```

### Activity
Write a function that takes the word frequency `Counter` and a number `N`, then prints the `N` most common words and their counts in a nice format.

**Starting point:**
```python
def display_most_common(frequencies, n):
    """Displays the n most common words and their frequencies."""
    # Your code here
    pass
```

**Example output format:**
```
Top 5 most common words:
- the: 12
- and: 8
- of: 7
- to: 6
- a: 5
```

---

## 2.6 Modular Design with Functions 🧱

### Concept
Why use functions for our text processing pipeline?
- **Readability:** Each function has a clear, single purpose
- **Reusability:** Functions can be used multiple times with different inputs
- **Organization:** Logical separation of concerns
- **Easier debugging:** Isolate and test individual components

### Best Practices

#### Single Responsibility
Each function should do one thing well:
- ✅ `read_file()` - only reads files
- ✅ `clean_text()` - only cleans text
- ❌ `read_and_clean_file()` - does too many things

#### Clear Naming
Use descriptive function and variable names:
- ✅ `count_frequencies()` instead of `count_stuff()`
- ✅ `cleaned_text` instead of `ct`

#### Documentation
Use docstrings to explain what functions do:
```python
def clean_text(text):
    """
    Converts text to lowercase and removes punctuation.
    
    Args:
        text (str): The input text to clean
        
    Returns:
        str: The cleaned text
    """
    # Function implementation here
```

### Activity
Review the functions written so far. Ensure they are:
1. Well-named and focused on a single task
2. Properly documented with docstrings
3. Following consistent coding style

---

## Additional Best Practices & Guidelines

### 2.7 Input Validation & Error Handling 🛡️

**File Operations:**
```python
def read_file(filepath):
    """Reads a file and returns its content as a string."""
    if not filepath:
        raise ValueError("Filepath cannot be empty")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return ""
    except UnicodeDecodeError:
        print(f"Error: Cannot decode file '{filepath}'. Try different encoding")
        return ""
```

**Input Type Checking:**
```python
def clean_text(text):
    """Converts text to lowercase and removes punctuation."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    if not text.strip():  # Handle empty or whitespace-only strings
        return ""
    # Rest of implementation...
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation using translation table
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    return text
```

### 2.8 Performance Considerations ⚡

**Memory Efficiency:**
- For large files, consider reading line-by-line instead of loading entire file
- Use generators for processing large datasets

**String Operations:**
```python
# ❌ Inefficient for large texts
def clean_text_slow(text):
    for char in string.punctuation:
        text = text.replace(char, ' ')
    return text.lower()

# ✅ More efficient using translate
def clean_text_fast(text):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return text.translate(translator).lower()
```

### 2.9 Code Style & Consistency 📏

**Variable Naming Conventions:**
```python
# ✅ Good naming
file_content = read_file(input_filepath)
cleaned_text = clean_text(file_content)
word_tokens = tokenize_text(cleaned_text)
frequency_counter = count_frequencies(word_tokens)

# ❌ Poor naming
data = read_file(fp)
x = clean_text(data)
lst = tokenize_text(x)
```

**Function Length Guidelines:**
- Keep functions under 20-25 lines when possible
- If longer, consider breaking into smaller helper functions

**Import Organization:**
```python
# Standard library imports first
import string
from collections import Counter
from pathlib import Path

# Third-party imports (if any)
# import requests

# Local imports (if any)
# from utils import helper_function
```

### 2.10 Testing Mindset 🧪

**Write Testable Functions:**
```python
def clean_text(text):
    """
    Example with edge cases to consider:
    - Empty strings
    - Strings with only punctuation
    - Strings with mixed case
    - Unicode characters
    """
    if not text: # Added basic check based on previous section
        return ""
    if not isinstance(text, str): # Added from 2.7
        raise TypeError("Input must be a string")
    if not text.strip():
        return ""

    # Remove punctuation and convert to lowercase
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator).lower()

# Test cases to think about:
# clean_text("Hello, World!") → "hello world"
# clean_text("") → ""
# clean_text("!!!") → ""
# clean_text("Hello123") → "hello123"
```

### 2.11 Configuration & Flexibility 🔧

**Make Functions Configurable:**
```python
def display_most_common(frequencies, n=10, show_count=True):
    """Displays the n most common words with optional count display."""
    if not isinstance(frequencies, Counter): # Added type check
        raise TypeError("Frequencies must be a Counter object")
    if not isinstance(n, int) or n <= 0: # Enhanced n validation
        raise ValueError("Number of words to display (n) must be a positive integer")

    print(f"Top {n} most common words:")
    for word, count in frequencies.most_common(n):
        if show_count:
            print(f"- {word}: {count}")
        else:
            print(f"- {word}")
```

**Use Constants for Magic Numbers:**
```python
# At the top of your file
DEFAULT_TOP_WORDS = 10
DEFAULT_ENCODING = 'utf-8'
PUNCTUATION_REPLACEMENT = ' ' # This constant isn't used in clean_text_fast, consider if needed

def read_file(filepath, encoding=DEFAULT_ENCODING):
    # Implementation using the constant
    if not filepath:
        raise ValueError("Filepath cannot be empty")
    try:
        with open(filepath, 'r', encoding=encoding) as f: # Used encoding parameter
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return ""
    except UnicodeDecodeError:
        print(f"Error: Cannot decode file '{filepath}' with encoding '{encoding}'.")
        return ""
    except Exception as e: # General exception for other open/read errors
        print(f"An unexpected error occurred with '{filepath}' and encoding '{encoding}': {e}")
        return ""
```

### 2.12 Documentation Standards 📚

**Enhanced Docstring Format:**
```python
def count_frequencies(tokens):
    """
    Counts the frequency of each token in a list.

    Args:
        tokens (list[str]): List of word tokens to count.
                            Expected to be a list of strings.

    Returns:
        collections.Counter: A Counter object mapping each word to its frequency.
                             Returns an empty Counter if input is not a list
                             or if the list is empty.

    Raises:
        TypeError: If tokens is not a list.

    Example:
        >>> from collections import Counter
        >>> count_frequencies(['the', 'cat', 'the'])
        Counter({'the': 2, 'cat': 1})
        >>> count_frequencies([])
        Counter()
        >>> count_frequencies("not a list") # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        TypeError: Input must be a list of strings
    """
    if not isinstance(tokens, list):
        raise TypeError("Input must be a list of strings")
    # Further validation could check if all elements are strings
    return Counter(tokens)
```

### 2.13 Debugging Tips 🐛

**Add Helpful Print Statements During Development:**
```python
def tokenize_text(text, debug=False):
    """Splits text into a list of words (tokens)."""
    if not isinstance(text, str): # Added type check
        if debug:
            print(f"Error: Input text is not a string. Received type: {type(text)}")
        return [] # Or raise TypeError

    if debug:
        print(f"Input text length: {len(text)}")
        print(f"First 50 chars: '{text[:50]}...'"

    tokens = text.split()

    if debug:
        print(f"Number of tokens: {len(tokens)}")
        print(f"First 5 tokens: {tokens[:5]}")

    return tokens
```

### 2.14 Future-Proofing 🔮

**Design for Extension:**
```python
def clean_text(text, remove_numbers=False, custom_punctuation=None):
    """
    Flexible text cleaning with optional features.

    Args:
        text (str): Input text to clean.
        remove_numbers (bool): If True, removes digits from the text.
                               Defaults to False.
        custom_punctuation (str | None): A string of custom punctuation characters
                                         to remove. If None, `string.punctuation`
                                         is used. Defaults to None.

    Returns:
        str: The cleaned text.

    Raises:
        TypeError: If text is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    if not text.strip():
        return ""

    text = text.lower()

    if remove_numbers:
        text = ''.join(char for char in text if not char.isdigit())

    punctuation_to_remove = custom_punctuation if custom_punctuation is not None else string.punctuation
    translator = str.maketrans('', '', punctuation_to_remove)
    text = text.translate(translator)

    return text
```

### 2.15 Code Organization 📁

**Suggested File Structure:**
This section describes a potential project structure. It's good for context but doesn't directly modify the concepts within Module 2 itself. We can keep it as is.
```
text_analyzer/
├── main.py              # Main script that ties everything together
├── text_processor.py    # Core text processing functions
├── file_utils.py        # File handling utilities
├── display_utils.py     # Output formatting functions
└── config.py           # Configuration constants
```

### 2.16 Real-World Considerations 🌍

**Encoding Awareness:**
```python
def read_file_robust(filepath): # Renamed to avoid conflict with earlier simple read_file
    """Reads file with fallback encoding options."""
    if not filepath:
        raise ValueError("Filepath cannot be empty")

    encodings_to_try = ['utf-8', 'latin-1', 'cp1252'] # More descriptive name

    for encoding in encodings_to_try:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                print(f"Successfully read '{filepath}' with encoding '{encoding}'") # Added success message
                return f.read()
        except FileNotFoundError: # Moved FileNotFoundError outside loop
            print(f"Error: File '{filepath}' not found.")
            return "" # Or raise
        except UnicodeDecodeError:
            print(f"Warning: Could not decode '{filepath}' with encoding '{encoding}'. Trying next...")
            continue
        except Exception as e: # General exception for other open/read errors
            print(f"An unexpected error occurred with '{filepath}' and encoding '{encoding}': {e}")
            continue # Try next encoding

    # If all encodings fail
    print(f"Error: Could not decode file '{filepath}' with any of the attempted encodings: {encodings_to_try}")
    return "" # Or raise a custom error
```

**Large File Handling:**
```python
from collections import Counter # Ensure Counter is imported

def process_large_file(filepath, chunk_size=1024*1024): # Increased default chunk_size to 1MB
    """
    Process large files in chunks to manage memory usage.

    Args:
        filepath (str): Path to the large text file.
        chunk_size (int): Size of chunks to read in bytes. Defaults to 1MB.

    Returns:
        collections.Counter: A Counter object with word frequencies from the file.

    Raises:
        ValueError: If filepath is empty.
        FileNotFoundError: If the file does not exist.
    """
    if not filepath:
        raise ValueError("Filepath cannot be empty")

    word_counter = Counter()
    processed_chunks = 0

    try:
        with open(filepath, 'r', encoding='utf-8') as f: # Assuming utf-8, could be made more robust
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break # End of file

                # Process chunk (ensure clean_text and tokenize_text are defined)
                cleaned_chunk = clean_text(chunk) # Assuming clean_text is available
                tokens_in_chunk = tokenize_text(cleaned_chunk) # Assuming tokenize_text is available
                word_counter.update(tokens_in_chunk)
                processed_chunks += 1
                print(f"Processed chunk {processed_chunks}...") # Progress update

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        raise # Re-raise the exception or handle as appropriate
    except Exception as e:
        print(f"An error occurred while processing '{filepath}': {e}")
        raise # Re-raise or handle

    if processed_chunks == 0:
        print(f"Warning: File '{filepath}' was empty or could not be processed.")

    print(f"Finished processing. Total chunks: {processed_chunks}")
    return word_counter
```

---

## Module 2 Summary

### Functions You Should Have
By the end of this module, you should have drafted these functions:

1. `read_file(filepath)` - Reads a text file
2. `clean_text(text)` - Cleans and normalizes text
3. `tokenize_text(text)` - Splits text into word tokens
4. `count_frequencies(tokens)` - Counts word frequencies
5. `display_most_common(frequencies, n)` - Shows top N words

### Key Concepts Mastered
- ✅ Safe file handling with `with` statements
- ✅ Text cleaning techniques (lowercase, punctuation removal)
- ✅ Basic tokenization using `.split()`
- ✅ Frequency counting with `collections.Counter`
- ✅ Modular programming with focused functions

---

## Next Steps

Ready to put it all together? Continue to **[Module 3: Building the Script - Step-by-Step](module3-building-script.md)** where we'll implement each function with complete code examples and assemble them into a working script.

---

## Quick Reference

**Essential Imports:**
```python
from collections import Counter
import string
```

**Key Methods:**
- `text.lower()` - convert to lowercase
- `text.split()` - split into words
- `Counter(list)` - count frequencies
- `counter.most_common(n)` - get top n items
