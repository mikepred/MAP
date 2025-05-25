# File: text_analyzer/analyzer.py
"""
Text Analysis Script - A Foundation for Understanding LLM Preprocessing

This script will contain functions to read, clean, tokenize,
and analyze text to count word frequencies.
It forms the basis of the project outlined in the lesson plan.
"""

import string
from collections import Counter
from typing import List, Optional, Counter as CounterType # For type hinting

import re # For advanced cleaning in clean_text
from typing import Tuple # For read_file_robust return type

# Configuration constants
DEFAULT_TOP_WORDS: int = 10
DEFAULT_ENCODING: str = 'utf-8'
CHUNK_SIZE_BYTES: int = 1024 * 1024 # 1MB for process_large_file

def read_file_robust(filepath: str, encodings: List[str] = [DEFAULT_ENCODING, 'latin-1', 'cp1252']) -> Optional[Tuple[str, str]]:
    """
    Reads a file and returns its content as a string, trying multiple encodings.
    
    Args:
        filepath (str): Path to the file to read.
        encodings (List[str], optional): A list of encodings to try in order. 
                                         Defaults to [DEFAULT_ENCODING, 'latin-1', 'cp1252'].
        
    Returns:
        Optional[Tuple[str, str]]: A tuple containing the file content and the successful encoding, 
                                   or (None, None) if all attempts fail or an error occurs.
        
    Raises:
        # Note: Specific errors like FileNotFoundError, UnicodeDecodeError, PermissionError
        # are handled internally by printing a message and returning (None, None).
        # ValueError for empty filepath is also handled this way for consistency here,
        # though typically it might be raised.
    """
    if not filepath:
        # According to Module 2B, this should raise ValueError.
        # However, the original implementation prints and returns None for other errors.
        # For consistency within this function's error handling style, we'll print and return (None, None).
        print("Error: Filepath cannot be empty.")
        return None, None

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                content = file.read()
                print(f"✅ Successfully read '{filepath}' with {encoding} encoding.")
                return content, encoding
        except FileNotFoundError:
            print(f"Error: File not found at '{filepath}'")
            return None, None # File not found, no need to try other encodings
        except UnicodeDecodeError:
            print(f"⚠️ Failed to decode '{filepath}' with {encoding}, trying next...")
            continue
        except PermissionError:
            print(f"Error: Permission denied for '{filepath}'")
            return None, None # Permission error, no need to try other encodings
        except Exception as e:
            print(f"❌ Unexpected error with {encoding} for '{filepath}': {e}")
            continue
            
    print(f"❌ Could not decode file '{filepath}' with any of the specified encodings: {encodings}")
    return None, None

def clean_text(
    text: Optional[str],
    lowercase: bool = True,
    remove_punctuation: bool = True,
    remove_numbers: bool = False,
    custom_punctuation: Optional[str] = None,
    preserve_spaces: bool = True
) -> str:
    """
    Converts text to lowercase and removes punctuation.
    
    Args:
        text (Optional[str]): Input text to clean.
        lowercase (bool, optional): Convert to lowercase if True. Defaults to True.
        remove_punctuation (bool, optional): Remove punctuation if True. Defaults to True.
        remove_numbers (bool, optional): Remove digits if True. Defaults to False.
        custom_punctuation (Optional[str], optional): Custom punctuation characters to remove. 
                                                     Defaults to None (uses string.punctuation).
        preserve_spaces (bool, optional): Keep single spaces between words if True. Defaults to True.
        
    Returns:
        str: Cleaned text according to specified options.
             Returns an empty string if input is None or whitespace-only after initial checks.
        
    Raises:
        TypeError: If the input `text` is not a string or None.

    Example:
        >>> clean_text("Hello, World! 123")
        'hello world 123'
        >>> clean_text("Hello, World! 123", remove_numbers=True)
        'hello world '
        >>> clean_text("Test...Test", custom_punctuation=".")
        'testtest'
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        raise TypeError(f"Expected string or None, got {type(text)}")
    
    if not text.strip(): # Handle empty or whitespace-only strings
        return ""
    
    result = text
    
    if lowercase:
        result = result.lower()
    
    if remove_numbers:
        result = re.sub(r'\d+', '', result) # Using re.sub for potentially better handling of numbers
    
    if remove_punctuation:
        punctuation_to_remove = custom_punctuation if custom_punctuation is not None else string.punctuation
        if preserve_spaces:
            # Replace each punctuation char with a space
            translator = str.maketrans(punctuation_to_remove, ' ' * len(punctuation_to_remove))
        else:
            # Remove punctuation chars entirely
            translator = str.maketrans('', '', punctuation_to_remove)
        result = result.translate(translator)
    
    # Clean up multiple spaces if spaces were preserved or introduced
    if preserve_spaces: # This applies if punctuation was replaced by spaces or original text had multiple spaces
        result = ' '.join(result.split()) # Normalizes multiple spaces to single space
    
    return result.strip() # Final strip to remove leading/trailing spaces

def tokenize_text(text: Optional[str], debug: bool = False) -> List[str]:
    """
    Splits text into a list of words (tokens).
    
    Args:
        text (Optional[str]): Input text to tokenize.
        debug (bool, optional): If True, prints debugging information. Defaults to False.
        
    Returns:
        List[str]: List of word tokens. Returns an empty list if input is None or empty.
        
    Example:
        >>> tokenize_text("hello world")
        ['hello', 'world']
    """
    if debug and text is not None:
        print(f"🔍 Input text length for tokenization: {len(text)}")
        print(f"🔍 First 50 chars for tokenization: '{text[:50]}...'")
        print(f"🔍 Input text contains newlines: {'\\n' in text}")

    if not text: # Handles None or empty string
        return []
    
    tokens = text.split()

    if debug:
        print(f"✅ Generated {len(tokens)} tokens.")
        print(f"✅ Sample tokens: {tokens[:5]}")
        print(f"✅ Unique tokens in this batch: {len(set(tokens))}")
    
    return tokens

def count_frequencies(tokens: Optional[List[str]], debug: bool = False) -> CounterType[str]:
    """
    Counts the frequency of each token in a list.
    
    Args:
        tokens (Optional[List[str]]): List of word tokens.
        debug (bool, optional): If True, prints debugging information. Defaults to False.
        
    Returns:
        CounterType[str]: A Counter object mapping each unique word to its frequency.
                          Returns an empty Counter if tokens list is None, empty.
    
    Raises:
        TypeError: If `tokens` is not a list or if any element in `tokens` is not a string.

    Example:
        >>> count_frequencies(['cat', 'dog', 'cat'])
        Counter({'cat': 2, 'dog': 1})
    """
    if tokens is None: # Handles None case
        if debug: print("⚠️ count_frequencies received None, returning empty Counter.")
        return Counter()
        
    if not isinstance(tokens, list):
        raise TypeError("Input 'tokens' must be a list.")
    
    # Check for non-string elements only if the list is not empty
    if tokens and not all(isinstance(token, str) for token in tokens):
        raise TypeError("All elements in 'tokens' must be strings.")
    
    if debug:
        print(f"📊 Counting frequencies for {len(tokens)} tokens.")

    word_counts = Counter(tokens)

    if debug:
        print(f"📊 Found {len(word_counts)} unique words from this token list.")
    return word_counts

def process_large_file(filepath: str, chunk_size: int = CHUNK_SIZE_BYTES, debug: bool = False) -> CounterType[str]:
    """
    Processes large files efficiently using chunked reading and returns word frequencies.
    
    Args:
        filepath (str): Path to the large text file.
        chunk_size (int, optional): Size of chunks in bytes. Defaults to CHUNK_SIZE_BYTES.
        debug (bool, optional): If True, prints debugging information. Defaults to False.
        
    Returns:
        CounterType[str]: Word frequencies from the entire file.
        
    Note:
        Uses constant memory relative to chunk_size, not total file size.
    """
    word_counter: CounterType[str] = Counter()
    
    try:
        with open(filepath, 'r', encoding=DEFAULT_ENCODING) as f: # Assuming default encoding for simplicity here
            chunk_number = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break # End of file
                
                if debug: print(f"🔄 Processing chunk {chunk_number + 1} of size {len(chunk)} bytes.")
                
                # Process chunk
                cleaned_chunk = clean_text(chunk) # Using default clean_text options
                tokens_chunk = tokenize_text(cleaned_chunk, debug=debug) # Pass debug flag
                word_counter.update(tokens_chunk)
                
                chunk_number += 1
                if debug and chunk_number % 10 == 0: # Progress update every 10 chunks in debug mode
                    print(f"📈 Processed {chunk_number} chunks so far...")
                    
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return Counter() # Return empty counter on error
    except Exception as e:
        print(f"❌ Error processing large file '{filepath}': {e}")
        return Counter() # Return empty counter on error
    
    if debug: print(f"✅ Completed processing {chunk_number} chunks from '{filepath}'.")
    return word_counter

def display_most_common(
    frequencies: CounterType[str], 
    n: int = DEFAULT_TOP_WORDS, 
    show_count: bool = True, 
    format_style: str = 'list'
) -> None:
    """
    Displays the n most common words and their frequencies.
    
    Args:
        frequencies (CounterType[str]): Word frequency counter.
        n (int, optional): Number of top words to display. Defaults to DEFAULT_TOP_WORDS.
        show_count (bool, optional): Whether to display the count alongside the word. Defaults to True.
        format_style (str, optional): Style of display ('list' or 'table'). Defaults to 'list'.
        
    Raises:
        TypeError: If `frequencies` is not a Counter object.
        ValueError: If `format_style` is not 'list' or 'table'.

    Example output (list style):
        Top 3 most common words:
        - the: 12
        - and: 8
        - of: 7
    """
    if not isinstance(frequencies, Counter):
        raise TypeError("Input 'frequencies' must be a Counter object.")
    if not frequencies:
        print("No frequencies to display.")
        return
    if format_style not in ['list', 'table']:
        raise ValueError("format_style must be 'list' or 'table'.")

    print(f"\nTop {n} most common words:")
    
    for word, count in frequencies.most_common(n):
        if format_style == 'list':
            if show_count:
                print(f"- {word}: {count}")
            else:
                print(f"- {word}")
        elif format_style == 'table':
            if show_count:
                # Basic table formatting, can be improved with libraries like tabulate
                print(f"{word:<20} {count:>5}") 
            else:
                print(f"{word}")
    
    print(f"Total unique words: {len(frequencies)}")


if __name__ == "__main__":
    # Configuration
    # Note: Module 3 uses "sample.txt". We'll use "text_analyzer/sample.txt"
    # as that's the correct path relative to the project root where the script is likely run from.
    filepath_to_analyze: str = "text_analyzer/sample.txt"
    num_common_words_to_display: int = DEFAULT_TOP_WORDS # Use constant
    # For Module 3, we'll use default cleaning and no debug for the main pipeline.
    # Debug mode and advanced cleaning were tested in Module 2C's main block.
    
    print("Text Analysis Script - Module 3 Execution")
    print("=" * 50)
    
    # Step 1: Read the file
    # Using read_file_robust as it's the enhanced version from Module 2C
    print(f"Reading file: {filepath_to_analyze}")
    raw_text_tuple = read_file_robust(filepath_to_analyze)
    
    if raw_text_tuple is None or raw_text_tuple[0] is None:
        print("Failed to read file. Exiting.")
        exit(1) # Exit script if file reading fails
    
    raw_text, used_encoding = raw_text_tuple
    print(f"File read successfully using {used_encoding} encoding. Length: {len(raw_text)} characters")
    
    # Step 2: Clean the text
    # Using the flexible clean_text with default parameters as per Module 3's simpler clean_text
    print("Cleaning text (default settings)...")
    cleaned_text_content: str = clean_text(raw_text) # Default cleaning options
    print(f"Text cleaned. Length: {len(cleaned_text_content)} characters")
    
    # Step 3: Tokenize
    print("Tokenizing text...")
    word_tokens: List[str] = tokenize_text(cleaned_text_content) # Default debug=False
    print(f"Found {len(word_tokens)} total words (tokens).")
    
    # Step 4: Count frequencies
    if not word_tokens:
        print("No tokens to count. Exiting.")
        frequencies_data: CounterType[str] = Counter()
    else:
        print("Counting word frequencies...")
        try:
            frequencies_data = count_frequencies(word_tokens) # Default debug=False
        except TypeError as e:
            print(f"Error counting frequencies: {e}. Exiting.")
            exit(1)
            
    # Step 5: Display results
    # Using the flexible display_most_common with default parameters
    if frequencies_data:
        display_most_common(frequencies_data, num_common_words_to_display)
    else:
        print("No frequencies were counted to display.")
        
    print("\nAnalysis complete!")
    pass
