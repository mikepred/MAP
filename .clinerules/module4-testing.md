---
## File: `.clinerules/module4-testing.md`
---
# 🏁 Module 4: Testing and Refinement

**Overview:** This module guides you through testing your script, handling edge cases, and exploring potential improvements to make your text analyzer more robust and feature-rich.

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
If you haven't already, create a `sample.txt` file with varied content:

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
1. **Check file existence:** Ensure `sample.txt` is in the same directory as `analyzer.py`
2. **Check file name:** Verify exact spelling and case sensitivity
3. **Use absolute path:** Try using the full path to the file
4. **Check permissions:** Ensure the file is readable

**Debug technique:**
```python
import os
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir('.'))
```

#### Issue 2: Empty or No Output
**Symptoms:**
- Script runs but shows no word frequencies
- "No frequencies to display" message

**Possible causes:**
1. Empty text file
2. File contains only punctuation/whitespace
3. Encoding issues

**Debug technique:**
Add temporary print statements:
```python
print(f"Raw text preview: {repr(raw_text[:100])}")
print(f"Cleaned text preview: {repr(cleaned_text[:100])}")
print(f"First 10 tokens: {tokens[:10]}")
```

#### Issue 3: Encoding Errors
**Symptoms:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

**Solutions:**
1. Try different encoding: `encoding='latin-1'` or `encoding='cp1252'`
2. Use `errors='ignore'` parameter: `encoding='utf-8', errors='ignore'`
3. Check the source of your text file

### Interactive Debugging Exercise

Intentionally introduce errors to practice debugging:

1. **Misspell the filename:**
   ```python
   filepath = "sampl.txt"  # Missing 'e'
   ```
   
2. **Create an empty file:**
   Create an empty `sample.txt` and observe the behavior

3. **Add some problematic content:**
   Include special characters or very long words to see how your script handles them

---

## 4.3 Potential Improvements & Enhancements

### Enhancement 1: Stop Word Removal 🚫

Stop words are common words that often don't carry significant meaning for analysis.

#### Implementation
```python
def remove_stop_words(tokens):
    """
    Removes common stop words from a list of tokens.
    
    Args:
        tokens (list): List of word tokens
        
    Returns:
        list: Filtered list without stop words
    """
    # Common English stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 
        'her', 'us', 'them'
    }
    
    return [token for token in tokens if token not in stop_words]
```

#### Integration
Add this step after tokenization:
```python
tokens = tokenize_text(cleaned_text)
tokens = remove_stop_words(tokens)  # Add this line
frequencies = count_frequencies(tokens)
```

### Enhancement 2: User Input 👤

Make your script interactive by asking for user input.

#### Implementation
```python
def get_user_input():
    """
    Gets configuration from user input.
    
    Returns:
        tuple: (filepath, num_words)
    """
    print("Text Analysis Configuration")
    print("-" * 30)
    
    filepath = input("Enter path to text file (default: sample.txt): ").strip()
    if not filepath:
        filepath = "sample.txt"
    
    try:
        num_words = int(input("Number of top words to display (default: 10): ") or 10)
    except ValueError:
        num_words = 10
        print("Invalid number, using default: 10")
    
    return filepath, num_words
```

#### Integration
Replace the configuration section:
```python
if __name__ == "__main__":
    filepath, num_common_words = get_user_input()
    # ... rest of the script
```

### Enhancement 3: Output to File 💾

Save results instead of just printing them.

#### Implementation
```python
def save_results(frequencies, n, output_file="results.txt"):
    """
    Saves analysis results to a file.
    
    Args:
        frequencies (Counter): Word frequency data
        n (int): Number of top words to save
        output_file (str): Output filename
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Text Analysis Results\n")
        f.write("=" * 50 + "\n\n")
        
        most_common = frequencies.most_common(n)
        f.write(f"Top {n} most common words:\n")
        f.write("-" * 30 + "\n")
        
        for word, count in most_common:
            f.write(f"{word:15} : {count:3d}\n")
        
        f.write("-" * 30 + "\n")
        f.write(f"Total unique words: {len(frequencies)}\n")
    
    print(f"Results saved to {output_file}")
```

### Enhancement 4: Advanced Text Cleaning 🧽

More sophisticated cleaning for real-world text.

#### Implementation
```python
import re

def advanced_clean_text(text):
    """
    Advanced text cleaning with additional preprocessing.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
    """
    if text is None:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove numbers (optional - depends on your needs)
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    
    return text.strip()
```

### Enhancement 5: Word Length Analysis 📏

Analyze word length distribution.

#### Implementation
```python
def analyze_word_lengths(tokens):
    """
    Analyzes the distribution of word lengths.
    
    Args:
        tokens (list): List of word tokens
        
    Returns:
        dict: Length distribution data
    """
    length_counts = Counter(len(word) for word in tokens)
    
    print("\nWord Length Analysis:")
    print("-" * 25)
    for length in sorted(length_counts.keys()):
        count = length_counts[length]
        percentage = (count / len(tokens)) * 100
        print(f"{length:2d} letters: {count:3d} words ({percentage:5.1f}%)")
    
    avg_length = sum(len(word) for word in tokens) / len(tokens)
    print(f"\nAverage word length: {avg_length:.1f} letters")
    
    return length_counts
```

---

## 4.4 Performance Considerations

### Measuring Performance 📊

Add timing to see how fast your script runs:

```python
import time

def time_function(func, *args, **kwargs):
    """Times the execution of a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"{func.__name__} took {end_time - start_time:.3f} seconds")
    return result

# Usage in main block:
tokens = time_function(tokenize_text, cleaned_text)
frequencies = time_function(count_frequencies, tokens)
```

### Memory Usage Tips

For large files, consider:
1. **Streaming:** Read files in chunks instead of all at once
2. **Generator expressions:** Use generators for memory efficiency
3. **Selective processing:** Only process parts of very large files

---

## 4.5 Complete Enhanced Script

Here's a version with multiple enhancements:

```python
"""
Enhanced Text Analysis Script
Includes stop word removal, user input, and file output options.
"""

from collections import Counter
import string
import re
import time

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

def clean_text(text, advanced=False):
    """Converts text to lowercase and removes punctuation."""
    if text is None:
        return ""
    
    text = text.lower()
    
    if advanced:
        # Remove URLs and emails
        text = re.sub(r'http[s]?://\S+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'\s+', ' ', text)
    
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    
    return text.strip()

def tokenize_text(text):
    """Splits text into a list of words (tokens)."""
    if not text:
        return []
    return text.split()

def remove_stop_words(tokens):
    """Removes common stop words from a list of tokens."""
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 
        'her', 'us', 'them'
    }
    return [token for token in tokens if token not in stop_words]

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
    print("Enhanced Text Analysis Script")
    print("=" * 50)
    
    # Configuration (you can make this interactive)
    filepath = "sample.txt"
    num_common_words = 10
    use_stop_words = True
    
    # Execute the pipeline
    start_time = time.time()
    
    raw_text = read_file(filepath)
    if raw_text is None:
        exit(1)
    
    cleaned_text = clean_text(raw_text, advanced=True)
    tokens = tokenize_text(cleaned_text)
    
    if use_stop_words:
        print("Removing stop words...")
        tokens = remove_stop_words(tokens)
    
    frequencies = count_frequencies(tokens)
    display_most_common(frequencies, num_common_words)
    
    end_time = time.time()
    print(f"\nTotal processing time: {end_time - start_time:.3f} seconds")
```

---

## Module 4 Summary

### Testing Skills Developed
- ✅ **Systematic testing** approach for scripts
- ✅ **Debugging techniques** for common issues
- ✅ **Error handling** and graceful failure
- ✅ **Performance measurement** and optimization awareness

### Enhancement Capabilities
- ✅ **Stop word removal** for better analysis
- ✅ **User input handling** for interactivity
- ✅ **File output** for saving results
- ✅ **Advanced text cleaning** for real-world data
- ✅ **Performance timing** for optimization

### Professional Development
- ✅ **Code organization** with modular enhancements
- ✅ **Documentation** with clear docstrings
- ✅ **Configuration options** for flexibility
- ✅ **Error handling** for robust operation

---

## Next Steps

Ready to understand how this connects to the bigger picture? Continue to **[Module 5: Connecting to the Bigger World of LLMs](module5-llm-connections.md)** where we'll explore how your text processing skills relate to modern AI and machine learning systems.

---

## Quick Reference: Common Debugging Commands

```python
# Check current directory and files
import os
print("Current directory:", os.getcwd())
print("Files:", os.listdir('.'))

# Preview text data
print("Raw text:", repr(raw_text[:100]))
print("Cleaned text:", repr(cleaned_text[:100]))
print("Tokens:", tokens[:10])

# Check data types and lengths
print("Type:", type(frequencies))
print("Length:", len(frequencies))
print("Empty?", len(frequencies) == 0)
```
