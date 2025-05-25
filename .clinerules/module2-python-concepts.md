---
## File: `.clinerules/module2-python-concepts.md`
---
# 🛠️ Module 2: Core Python Concepts for Text Processing

**Overview:** This module covers the essential Python concepts and techniques needed to build our text processing pipeline.

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
