# 🚀 Module 4C: Advanced Refinements and Performance

**Overview:** This module focuses on adding more sophisticated text processing features, considering performance aspects, and integrating all enhancements into a final polished script.

**Estimated Time:** 45-60 minutes

---

## Enhancement 4: Advanced Text Cleaning 🧽

More sophisticated cleaning for real-world text, such as removing URLs, email addresses, and optionally numbers.

### Implementation

Add or update the `clean_text` function in `analyzer.py` (or create a new `advanced_clean_text` function if you prefer to keep the simpler one). The example below enhances the existing `clean_text` by adding an `advanced` flag.

```python
import re # Ensure re is imported at the top of your file

def clean_text(text, advanced=False): # Modified to accept an 'advanced' flag
    """
    Converts text to lowercase and removes punctuation.
    If advanced is True, also removes URLs, emails, and optionally numbers.
    
    Args:
        text (str): Input text
        advanced (bool): Flag to enable advanced cleaning
        
    Returns:
        str: Cleaned text
    """
    if text is None:
        return ""
    
    text = text.lower()
    
    if advanced:
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Remove numbers (optional - you might want to keep them for some analyses)
        # text = re.sub(r'\d+', '', text) 
        # Remove extra whitespace that might have been introduced
        text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove punctuation (this should be standard for word tokenization)
    # Ensure string module is imported: import string
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    
    # Final whitespace cleanup
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
```

### Integration

In the `if __name__ == "__main__":` block, you can decide whether to use advanced cleaning, perhaps based on user input or a fixed setting.

```python
# Inside if __name__ == "__main__":
# ...
    # Example: always use advanced cleaning for this version
    cleaned_text = clean_text(raw_text, advanced=True) 
# ...
```

---

## Enhancement 5: Word Length Analysis 📏

Analyze and display the distribution of word lengths in the text.

### Implementation

Add this function to `analyzer.py`:

```python
from collections import Counter # Ensure Counter is imported

def analyze_word_lengths(tokens):
    """
    Analyzes the distribution of word lengths and prints the analysis.
    
    Args:
        tokens (list): List of word tokens
        
    Returns:
        Counter: Counter object with word lengths as keys and counts as values
    """
    if not tokens:
        print("\nNo tokens to analyze for word lengths.")
        return Counter()

    length_counts = Counter(len(word) for word in tokens)
    
    print("\n--- Word Length Analysis ---")
    # Sort by length for display
    for length in sorted(length_counts.keys()):
        count = length_counts[length]
        percentage = (count / len(tokens)) * 100 if len(tokens) > 0 else 0
        print(f"{length:2d} letter(s): {count:4d} words ({percentage:5.1f}%)")
    
    if len(tokens) > 0:
        avg_length = sum(len(word) for word in tokens) / len(tokens)
        print(f"\nAverage word length: {avg_length:.1f} letters")
    else:
        print("\nAverage word length: N/A (no tokens)")
    print("--------------------------")
    
    return length_counts
```

### Integration

Call this function in the `if __name__ == "__main__":` block, after tokenization and possibly after stop word removal.

```python
# Inside if __name__ == "__main__":
# ...
    if use_stop_word_removal:
        tokens = remove_stop_words(tokens)
        
    frequencies = count_frequencies(tokens)
    display_most_common(frequencies, num_common_words)
    
    # Add word length analysis
    if tokens: # Only analyze if there are tokens
        analyze_word_lengths(tokens)
# ...
```

---

## 4.4 Performance Considerations

### Measuring Performance 📊

It's useful to know how long your script takes to run, especially as you add more features or process larger files.

#### Implementation

Add this utility function (if not already present) and use it to time key operations:

```python
import time # Ensure time is imported

def time_function(func, *args, **kwargs):
    """Times the execution of a function and prints the duration."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds.")
    return result

# Example Usage in the main block:
# raw_text = time_function(read_file, filepath)
# cleaned_text = time_function(clean_text, raw_text, advanced=True)
# tokens = time_function(tokenize_text, cleaned_text)
# if use_stop_word_removal:
#     tokens = time_function(remove_stop_words, tokens)
# frequencies = time_function(count_frequencies, tokens)
```
You can also time the entire pipeline:
```python
# Inside if __name__ == "__main__":
    pipeline_start_time = time.time()
    
    # ... all your processing steps ...
    
    pipeline_end_time = time.time()
    print(f"\nTotal processing pipeline took: {pipeline_end_time - pipeline_start_time:.4f} seconds")
```

### Memory Usage Tips

For very large files, your current script might consume a lot of memory because it reads the entire file content at once. Consider these strategies for larger-scale applications (implementation details are beyond this module's scope but good to be aware of):

1.  **Streaming/Chunking:** Read and process the file in smaller chunks instead of loading it all into memory.
    ```python
    # Conceptual example for reading in chunks
    # with open(filepath, 'r', encoding='utf-8') as f:
    #     while True:
    #         chunk = f.read(4096) # Read 4KB at a time
    #         if not chunk:
    #             break
    #         # Process the chunk
    ```
2.  **Generator Expressions:** Use generator expressions `(expression for item in iterable)` instead of list comprehensions `[expression for item in iterable]` for intermediate steps if memory is a concern, as they produce items one at a time.
3.  **Efficient Data Structures:** `collections.Counter` is already quite efficient for frequency counting. For other tasks, choose data structures wisely.

---

## 4.5 Complete Enhanced Script

This section would typically show the fully integrated `analyzer.py` script incorporating all enhancements from Modules 4A, 4B, and 4C. For brevity here, ensure your `analyzer.py` now includes:
- All functions from Module 3.
- `remove_stop_words()` from Module 4B.
- `get_user_input_config()` from Module 4B.
- `save_results_to_file()` from Module 4B.
- The updated `clean_text()` (or `advanced_clean_text()`) from this module (4C).
- `analyze_word_lengths()` from this module (4C).
- Performance timing (optional, but good practice).
- All integrated into the `if __name__ == "__main__":` block logically.

**Key integration points in `if __name__ == "__main__":`:**
1. Call `get_user_input_config()` to get `filepath`, `num_common_words`, `use_stop_word_removal`.
2. Call `read_file(filepath)`.
3. Call `clean_text(raw_text, advanced=True)`.
4. Call `tokenize_text(cleaned_text)`.
5. If `use_stop_word_removal`, call `remove_stop_words(tokens)`.
6. Call `count_frequencies(tokens)`.
7. Call `display_most_common(frequencies, num_common_words)`.
8. Call `analyze_word_lengths(tokens)`.
9. Ask user if they want to save results and call `save_results_to_file()` if yes.
10. Include overall pipeline timing.

---

## Module 4 Summary (Consolidated)

### Testing Skills Developed
- ✅ **Systematic testing** approach for scripts.
- ✅ **Debugging techniques** for common issues (covered in 4A).
- ✅ **Error handling** and graceful failure throughout enhancements.
- ✅ **Performance measurement** awareness.

### Enhancement Capabilities Added
- ✅ **Stop word removal** for more focused analysis (Module 4B).
- ✅ **User input handling** for script interactivity and configuration (Module 4B).
- ✅ **File output** for saving analysis results (Module 4B).
- ✅ **Advanced text cleaning** for handling more diverse real-world text (Module 4C).
- ✅ **Word length analysis** for additional textual insights (Module 4C).
- ✅ **Performance timing** for optimization awareness (Module 4C).

### Professional Development
- ✅ **Code organization** with modular functions for each enhancement.
- ✅ **Documentation** (docstrings) for new functions.
- ✅ **Configuration options** for script flexibility.
- ✅ **Robustness** through handling more varied inputs and providing more analysis.

---

## Next Steps

Ready to understand how this connects to the bigger picture? Continue to **[Module 5: Connecting to the Bigger World of LLMs](module5-llm-connections.md)** where we'll explore how your text processing skills relate to modern AI and machine learning systems.
