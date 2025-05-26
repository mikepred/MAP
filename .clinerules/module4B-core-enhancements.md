# 🛠️ Module 4B: Core Script Enhancements

**Overview:** This module focuses on implementing foundational enhancements to add significant new capabilities to the text analyzer. We'll cover stop word removal, user input for configuration, and saving analysis results to a file.

**Estimated Time:** 45-60 minutes

---

## Enhancement 1: Stop Word Removal 🚫

Stop words are common words (e.g., "the", "is", "in") that often don't carry significant meaning for certain types of text analysis. Removing them can help highlight more important terms.

### Implementation

Add the following function to your `analyzer.py`:

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
    
    filtered_tokens = [token for token in tokens if token not in stop_words]
    print(f"Removed {len(tokens) - len(filtered_tokens)} stop words.")
    return filtered_tokens
```

### Integration

Modify the `if __name__ == "__main__":` block in `analyzer.py` to include this step. You might want to make it configurable.

```python
# Inside if __name__ == "__main__":
# ...
    tokens = tokenize_text(cleaned_text)
    
    # Add a flag for stop word removal, e.g., at the top of the main block
    # use_stop_word_removal = True # or get from user input later
    
    if use_stop_word_removal: # Example: make this configurable
        tokens = remove_stop_words(tokens)
        
    frequencies = count_frequencies(tokens)
# ...
```
**Note:** Remember to define `use_stop_word_removal` or integrate it with user input (covered next).

---

## Enhancement 2: User Input for Configuration 👤

Make your script more flexible by allowing users to specify the input file and the number of top words to display.

### Implementation

Add this function to `analyzer.py`:

```python
def get_user_input_config():
    """
    Gets configuration from user input.
    
    Returns:
        tuple: (filepath, num_words, enable_stop_words)
    """
    print("\n--- Text Analysis Configuration ---")
    
    filepath = input("Enter path to text file (default: sample.txt): ").strip()
    if not filepath:
        filepath = "sample.txt"
    
    while True:
        try:
            num_words_str = input("Number of top words to display (default: 10): ").strip()
            if not num_words_str:
                num_words = 10
            else:
                num_words = int(num_words_str)
            if num_words <= 0:
                print("Please enter a positive number for top words.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    while True:
        stop_words_choice = input("Remove stop words? (yes/no, default: yes): ").strip().lower()
        if not stop_words_choice or stop_words_choice == 'yes':
            enable_stop_words = True
            break
        elif stop_words_choice == 'no':
            enable_stop_words = False
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
            
    return filepath, num_words, enable_stop_words
```

### Integration

In the `if __name__ == "__main__":` block, replace the hardcoded configuration:

```python
# Inside if __name__ == "__main__":
    print("Enhanced Text Analysis Script")
    print("=" * 50)
    
    filepath, num_common_words, use_stop_word_removal = get_user_input_config()
    
    # ... rest of the script
    # Ensure 'use_stop_word_removal' is used as shown in Enhancement 1
    # And 'num_common_words' is passed to display_most_common
    # e.g., display_most_common(frequencies, num_common_words)
```

---

## Enhancement 3: Output to File 💾

Allow users to save the analysis results to a text file.

### Implementation

Add this function to `analyzer.py`:

```python
def save_results_to_file(frequencies, n, unique_word_count, output_filename="analysis_results.txt"):
    """
    Saves analysis results to a file.
    
    Args:
        frequencies (Counter): Word frequency data
        n (int): Number of top words to save
        unique_word_count (int): Total number of unique words
        output_filename (str): Name of the file to save results
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("Text Analysis Results\n")
            f.write("=" * 30 + "\n\n")
            
            most_common = frequencies.most_common(n)
            f.write(f"Top {n} most common words:\n")
            f.write("-" * 30 + "\n")
            
            for word, count in most_common:
                f.write(f"{word:15} : {count:3d}\n")
            
            f.write("-" * 30 + "\n")
            f.write(f"Total unique words: {unique_word_count}\n\n")
            f.write("Analysis complete.\n")
        
        print(f"\nResults successfully saved to {output_filename}")
    except IOError:
        print(f"\nError: Could not write results to {output_filename}.")
```

### Integration

In the `if __name__ == "__main__":` block, after displaying results, ask the user if they want to save:

```python
# Inside if __name__ == "__main__":
# ... (after display_most_common)

    if frequencies: # Check if there are frequencies to save
        while True:
            save_choice = input("\nSave results to file? (yes/no, default: no): ").strip().lower()
            if not save_choice or save_choice == 'no':
                break
            elif save_choice == 'yes':
                output_filename = input("Enter output filename (default: analysis_results.txt): ").strip()
                if not output_filename:
                    output_filename = "analysis_results.txt"
                save_results_to_file(frequencies, num_common_words, len(frequencies), output_filename)
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
    
    # ... (end of script)
```

---

By implementing these three enhancements, your text analyzer will be significantly more versatile and user-friendly. Remember to test each enhancement thoroughly after integrating it.

**Next Up:** [Module 4C: Advanced Refinements and Performance](module4C-advanced-refinements.md)
