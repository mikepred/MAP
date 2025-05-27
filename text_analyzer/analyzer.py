"""
Text Analysis Script - Complete Version
A comprehensive text analysis tool for processing and analyzing text files.

Modules 3A-3E: Complete Integration. Enhanced with Module 4B features.
"""

import os
import re
import string
from pathlib import Path
from collections import Counter
import time # Added for Module 4C
from typing import Optional, List, Dict, Tuple, Set, Any, Union # For type hints

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================
MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB
MAX_INPUT_ATTEMPTS: int = 3
DEFAULT_TOP_WORDS_DISPLAY: int = 10
PREVIEW_LENGTH: int = 100

# Path constants
SCRIPT_DIRECTORY: Path = Path(__file__).resolve().parent
DEFAULT_SAMPLE_FILENAME: str = "sample.txt" # Relative to script directory
DEFAULT_RESULTS_FILENAME: str = "analysis_results.txt"
# Construct full default path for sample.txt, assuming it's in the same dir as the script
DEFAULT_SAMPLE_FILEPATH: Path = SCRIPT_DIRECTORY / DEFAULT_SAMPLE_FILENAME

# Fixed target file for automatic analysis as per user request
FIXED_TARGET_FILENAME: str = "s.txt"
FIXED_TARGET_FILEPATH: Path = SCRIPT_DIRECTORY / FIXED_TARGET_FILENAME

# Stop words set (moved from remove_stop_words function)
STOP_WORDS: Set[str] = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
    'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
    'her', 'us', 'them'
}

# Pre-compiled Regular Expressions for performance
URL_REGEX: re.Pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
EMAIL_REGEX: re.Pattern = re.compile(r'\S+@\S+')
NUMBERS_REGEX: re.Pattern = re.compile(r'\d+') # Optional, if number removal is desired
EXTRA_WHITESPACE_REGEX: re.Pattern = re.compile(r'\s+')
# For clean_text_for_sentence_analysis:
SENTENCE_CLEAN_REGEX: re.Pattern = re.compile(r'[^\w\s.,!?;:\'-]')


# =============================================================================
# FILE I/O FUNCTIONS (Module 3B from original structure)
# =============================================================================

def validate_file_path(filename: Union[str, Path]) -> Tuple[bool, str]:
    """Validate that a file path is safe and accessible."""
    try:
        file_path: Path = Path(filename).resolve() # Resolve the path to make it absolute and normalized
        
        # The previous security check for absolute paths outside CWD has been removed
        # to allow users to specify any valid absolute file path.
        # OS-level permissions will handle access control.
        
        if not file_path.exists():
            return False, f"File '{file_path}' does not exist"
        
        if not file_path.is_file():
            return False, f"'{file_path}' is not a file"
        
        file_size: int = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE_BYTES:
            return False, f"File too large ({file_size} bytes). Maximum: {MAX_FILE_SIZE_BYTES} bytes"
        
        return True, "File validation passed"
        
    except Exception as e:
        return False, f"Error validating file '{filename}': {e}"

def read_file(filename: Union[str, Path]) -> str: # Return empty string on error, not Optional[str] as per original logic
    """Read text from a file with comprehensive error handling."""
    try:
        # Ensure filename is a Path object for open()
        file_to_read: Path = Path(filename)
        with open(file_to_read, 'r', encoding='utf-8') as file:
            content: str = file.read()
            print(f"✅ Successfully read file: {file_to_read}")
            print(f"📄 File size: {len(content)} characters")
            return content
            
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        print("💡 Please check the filename and path.")
        return ""
        
    except PermissionError:
        print(f"❌ Error: No permission to read '{filename}'.")
        print("💡 Check file permissions or try running as administrator.")
        return ""
        
    except UnicodeDecodeError:
        print(f"❌ Error: Unable to decode '{filename}' as text.")
        print("💡 File might be binary or use different encoding.")
        return ""
        
    except IsADirectoryError:
        print(f"❌ Error: '{filename}' is a directory, not a file.")
        print("💡 Please specify a file, not a folder.")
        return ""
        
    except Exception as e:
        print(f"❌ Unexpected error reading '{filename}': {e}")
        print("💡 Please try again or contact support.")
        return ""

def get_filename_from_user() -> str: # Returns Path object as string or empty string
    """Get filename from user with input validation and retry logic."""
    attempts: int = 0
    
    while attempts < MAX_INPUT_ATTEMPTS:
        try:
            print(f"\n📂 Enter filename (attempt {attempts + 1}/{MAX_INPUT_ATTEMPTS}):")
            # Using str() for display if DEFAULT_SAMPLE_FILEPATH is Path
            print(f"💡 Tip: Use '{DEFAULT_SAMPLE_FILEPATH.name}' for testing (located in script directory)")
            print("💡 Type 'quit' to exit")
            
            filename_str: str = input("Filename: ").strip()
            
            if filename_str.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                return ""
            
            if not filename_str:
                print("⚠️  Please enter a filename.")
                attempts += 1
                continue
            
            # Construct path relative to script dir if not absolute, or use as is if absolute
            input_path: Path = Path(filename_str)
            path_to_validate: Path
            if input_path.is_absolute():
                path_to_validate = input_path
            else:
                # Assume relative to script directory if not absolute,
                # or could be relative to CWD. For consistency with DEFAULT_SAMPLE_FILEPATH,
                # let's assume relative to script dir if simple name, else CWD.
                # This logic can be tricky. For now, let's assume CWD for relative paths.
                path_to_validate = Path.cwd() / input_path


            is_valid, message = validate_file_path(path_to_validate)
            if is_valid:
                print(f"✅ {message}")
                return str(path_to_validate) # Return as string
            else:
                # If validation failed for CWD relative, try SCRIPT_DIRECTORY relative for simple names
                if not input_path.is_absolute() and not os.path.sep in filename_str : # simple filename
                    path_to_validate_script_dir = SCRIPT_DIRECTORY / input_path
                    is_valid_script_dir, message_script_dir = validate_file_path(path_to_validate_script_dir)
                    if is_valid_script_dir:
                        print(f"✅ {message_script_dir} (found in script directory)")
                        return str(path_to_validate_script_dir)
                    else:
                        print(f"❌ {message} (checked in CWD)")
                        # Optionally print message_script_dir if different and more informative
                        # print(f"❌ Also not valid in script directory: {message_script_dir}")
                else:
                     print(f"❌ {message}")
                attempts += 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            return ""
        except Exception as e:
            print(f"❌ Error getting input: {e}")
            attempts += 1
    
    print(f"\n❌ Maximum attempts ({MAX_INPUT_ATTEMPTS}) reached")
    return ""

def get_user_input_config() -> Tuple[int, bool]:
    """
    Gets configuration from user input for number of top words and stop word removal.
    (Enhancement 2 from Module 4B)
    Filepath is NOT asked here as it's handled differently by the caller.
    
    Returns:
        Tuple[int, bool]: (num_words_to_display, enable_stop_word_removal)
    """
    print("\n--- ⚙️ Text Analysis Configuration ---")
    
    # Filepath is no longer asked here, it will be fixed in main() for option 1.
    
    num_words: int = DEFAULT_TOP_WORDS_DISPLAY
    while True:
        try:
            num_words_str_input: str = input(f"Number of top words to display (default: {num_words}): ").strip()
            if not num_words_str_input:
                break
            else:
                num_words_val: int = int(num_words_str_input)
                if num_words_val <= 0:
                    print("⚠️ Please enter a positive number for top words.")
                    continue
                num_words = num_words_val
            break
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")
            
    enable_stop_words: bool = True # Default
    while True:
        default_sw_choice_str: str = 'yes' if enable_stop_words else 'no'
        stop_words_prompt: str = f"Remove stop words? (yes/no, default: {default_sw_choice_str}): "
        stop_words_choice: str = input(stop_words_prompt).strip().lower()
        if not stop_words_choice:
            break
        elif stop_words_choice == 'yes':
            enable_stop_words = True
            break
        elif stop_words_choice == 'no':
            enable_stop_words = False
            break
        else:
            print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")
            
    return num_words, enable_stop_words

def load_text_file() -> str: # Returns content as string or empty string
    """Complete file loading workflow with user interaction."""
    print("🚀 Text File Loader")
    print("=" * 30)
    
    filename_str: str = get_filename_from_user()
    if not filename_str:
        return ""
    
    # filename_str from get_filename_from_user should be a validated, existing path string
    content: str = read_file(filename_str) # read_file expects str or Path
    
    if content:
        # PREVIEW_LENGTH is now a constant
        if len(content) > PREVIEW_LENGTH:
            preview: str = content[:PREVIEW_LENGTH] + "..."
        else:
            preview: str = content
        
        print(f"\n📖 File Preview:")
        print("-" * 20)
        print(preview)
        print("-" * 20)
    
    return content

# =============================================================================
# TEXT PROCESSING FUNCTIONS (Module 3C / Enhanced in 4B & 4C)
# =============================================================================

def clean_text_for_sentence_analysis(text: Optional[str]) -> str:
    """Clean and preprocess text lightly, preserving sentence structures for analysis."""
    if not text or not isinstance(text, str): # isinstance check is good
        return ""
    
    cleaned_text: str = text.lower()
    # Normalize whitespace but try to keep sentence-relevant punctuation
    cleaned_text = ' '.join(cleaned_text.split())
    # This regex was designed to keep sentence delimiters.
    cleaned_text = SENTENCE_CLEAN_REGEX.sub('', cleaned_text) # Kept ' for contractions.
    
    return cleaned_text

def clean_text(text: Optional[str], advanced: bool = False) -> str: # New from Module 4C
    """
    Converts text to lowercase and removes ALL punctuation.
    If advanced is True, also removes URLs, emails, and optionally numbers.
    
    Args:
        text (Optional[str]): Input text
        advanced (bool): Flag to enable advanced cleaning
        
    Returns:
        str: Cleaned text
    """
    if text is None: # Explicit check for None
        return ""
    
    processed_text: str = text.lower() # Keep 'text' as original for sequential regex
    
    if advanced:
        # Remove URLs
        processed_text = URL_REGEX.sub('', processed_text)
        # Remove email addresses
        processed_text = EMAIL_REGEX.sub('', processed_text)
        # Remove numbers (optional - commented out as per M4C guide)
        # processed_text = NUMBERS_REGEX.sub('', processed_text) 
        # Remove extra whitespace that might have been introduced by above steps
        processed_text = EXTRA_WHITESPACE_REGEX.sub(' ', processed_text).strip()
    
    # Remove ALL punctuation for word tokenization
    translator = str.maketrans('', '', string.punctuation)
    processed_text = processed_text.translate(translator)
    
    # Final whitespace cleanup
    processed_text = EXTRA_WHITESPACE_REGEX.sub(' ', processed_text).strip()
    
    return processed_text

# clean_text_for_words is being removed. Its functionality will be covered by
# clean_text(text, advanced=False)

def tokenize_text(text: Optional[str]) -> List[str]:
    """Splits text into a list of words (tokens)."""
    if not text: # Handles None or empty string
        return []
    return text.split()

def remove_stop_words(tokens: List[str]) -> List[str]:
    """
    Removes common stop words from a list of tokens. (Enhancement 1 from Module 4B)
    
    Args:
        tokens (List[str]): List of word tokens
        
    Returns:
        List[str]: Filtered list without stop words
    """
    # Uses module-level STOP_WORDS constant
    original_token_count: int = len(tokens)
    filtered_tokens: List[str] = [token for token in tokens if token not in STOP_WORDS]
    removed_count: int = original_token_count - len(filtered_tokens)
    if removed_count > 0 : # Only print if words were actually removed
        print(f"ℹ️ Removed {removed_count} stop words.")
    return filtered_tokens

def count_words(text: Optional[str], use_stop_words: bool = False) -> Counter[str]:
    """Count word frequencies in text."""
    if not text:
        return Counter()
    
    # Use clean_text with advanced=False to replicate clean_text_for_words functionality
    cleaned_text: str = clean_text(text, advanced=False) 
    words: List[str] = cleaned_text.split() # clean_text already handles stripping and whitespace normalization
    words = [word for word in words if len(word) > 0] # Filter out empty strings

    if use_stop_words:
        words = remove_stop_words(words) # remove_stop_words expects List[str]
        
    word_counts: Counter[str] = Counter(words)
    return word_counts

def get_word_count_stats(word_counts: Counter[str]) -> Dict[str, Any]:
    """Calculate statistics from word counts."""
    if not word_counts: # Check if the Counter is empty
        return {
            'total_words': 0,
            'unique_words': 0,
            'most_common': [],
            'average_frequency': 0
        }
    
    total_words: int = sum(word_counts.values())
    unique_words: int = len(word_counts)
    # most_common returns List[Tuple[str, int]]
    most_common: List[Tuple[str, int]] = word_counts.most_common(5) # From Module 3E, used for summary
    average_frequency: float = total_words / unique_words if unique_words > 0 else 0.0
    
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'most_common': most_common,
        'average_frequency': round(average_frequency, 2)
    }

def count_sentences(text: Optional[str]) -> int:
    """Count sentences in text."""
    if not text:
        return 0
    
    # re.split returns List[str]
    sentences: List[str] = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return len(sentences)

def analyze_sentences(text: Optional[str]) -> Dict[str, Any]:
    """Analyze sentence structure in text."""
    if not text:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0.0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    sentences: List[str] = re.split(r'[.!?]+', text) # Uses original text before heavy cleaning
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0.0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    sentence_word_counts: List[int] = []
    for sentence_str in sentences: # Renamed sentence to sentence_str to avoid conflict
        # For sentence word counts, use clean_text(advanced=False) to get a reasonable word split
        words_in_sentence: List[str] = clean_text(sentence_str, advanced=False).split()
        words_in_sentence = [word for word in words_in_sentence if len(word) > 0]
        sentence_word_counts.append(len(words_in_sentence))
    
    average_words: float = sum(sentence_word_counts) / len(sentence_word_counts) if sentence_word_counts else 0.0
    
    longest_idx: int = sentence_word_counts.index(max(sentence_word_counts)) if sentence_word_counts else -1
    shortest_idx: int = sentence_word_counts.index(min(sentence_word_counts)) if sentence_word_counts else -1
    
    return {
        'sentence_count': len(sentences),
        'average_words_per_sentence': round(average_words, 1),
        'longest_sentence': sentences[longest_idx].strip() if longest_idx != -1 else "",
        'shortest_sentence': sentences[shortest_idx].strip() if shortest_idx != -1 else ""
    }

def analyze_text_complete(
    text: Optional[str], 
    use_stop_words: bool = False, 
    num_common_words_to_display: int = DEFAULT_TOP_WORDS_DISPLAY
) -> Dict[str, Any]:
    """Complete text analysis pipeline."""
    if not text: # Handles None or empty string
        return {
            'error': 'No text provided for analysis',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {},
            'processed_tokens': [],
            'readability_stats': {}, # Add new keys to default error return
            'interesting_patterns': {}
        }
    
    try:
        # Sentence analysis (uses lightly cleaned text for sentence splitting)
        text_for_sentence_structure: str = clean_text_for_sentence_analysis(text)
        sentence_stats: Dict[str, Any] = analyze_sentences(text_for_sentence_structure)

        # Word analysis (Primary pipeline)
        text_for_word_tokenization: str = clean_text(text, advanced=True) # Using advanced cleaning
        tokens_after_cleaning: List[str] = tokenize_text(text_for_word_tokenization)
        
        processed_tokens: List[str]
        if use_stop_words:
            processed_tokens = remove_stop_words(tokens_after_cleaning)
        else:
            processed_tokens = tokens_after_cleaning
        
        final_word_counts: Counter[str] = Counter(processed_tokens)
        word_stats: Dict[str, Any] = get_word_count_stats(final_word_counts)
        # Unique words list is derived directly from final_word_counts
        unique_words_list: List[str] = sorted(final_word_counts.keys()) if final_word_counts else []
            
        char_count: int = len(text) # Raw text length
        char_count_no_spaces: int = len(text.replace(' ', '')) # Raw text, no spaces
            
        general_stats: Dict[str, Any] = {
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'word_count': word_stats['total_words'], 
            'sentence_count': sentence_stats['sentence_count'],
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()])
        }
            
        # Ensure num_common_words_to_display is not negative
        num_to_display = max(0, num_common_words_to_display)

        # Calculate readability and patterns here
        readability_stats_result: Dict[str, Any] = {}
        interesting_patterns_result: Dict[str, Any] = {}
        if final_word_counts: # Only calculate if there are words
            readability_stats_result = calculate_readability_stats(
                text, # Original text
                final_word_counts,
                sentence_stats
            )
            interesting_patterns_result = find_interesting_patterns(
                final_word_counts,
                text # Original text
            )

        return {
            'word_analysis': {
                'word_frequencies': dict(final_word_counts.most_common(num_to_display)),
                'statistics': word_stats, 
                'unique_words_sample': unique_words_list[:10], # Keep sample size fixed or make configurable
                'full_word_counts_obj': final_word_counts 
            },
            'processed_tokens': processed_tokens, 
            'sentence_analysis': sentence_stats,
            'general_stats': general_stats,
            'original_text': text,
            'readability_stats': readability_stats_result, # Add to return
            'interesting_patterns': interesting_patterns_result # Add to return
        }
        
    except Exception as e:
        # It's good practice to log the exception here or re-raise a custom one
        # For now, returning a dict with error is consistent with current design
        return {
            'error': f'Analysis failed: {str(e)}',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {},
            'processed_tokens': [],
            'readability_stats': {}, # Add new keys to default error return
            'interesting_patterns': {}
        }

# =============================================================================
# ANALYSIS & DISPLAY FUNCTIONS (Module 3D / Enhanced in 4C)
# =============================================================================

def time_function(func: callable, *args: Any, **kwargs: Any) -> Any: # New from Module 4C
    """Times the execution of a function and prints the duration."""
    start_time: float = time.time()
    result: Any = func(*args, **kwargs)
    end_time: float = time.time()
    # Optional: print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds.")
    return result

def analyze_word_lengths(tokens: List[str]) -> Counter[int]: # New from Module 4C
    """
    Analyzes the distribution of word lengths and prints the analysis.
    
    Args:
        tokens (List[str]): List of word tokens
        
    Returns:
        Counter[int]: Counter object with word lengths as keys and counts as values
    """
    if not tokens:
        print("\nℹ️ No tokens to analyze for word lengths.")
        return Counter()

    length_counts: Counter[int] = Counter(len(word) for word in tokens)
    
    print("\n--- Word Length Analysis ---")
    # Sort by length for display
    for length_val in sorted(length_counts.keys()): # Renamed length to length_val to avoid conflict
        count: int = length_counts[length_val]
        percentage: float = (count / len(tokens)) * 100 if len(tokens) > 0 else 0.0
        print(f"{length_val:2d} letter(s): {count:4d} words ({percentage:5.1f}%)")
    
    if len(tokens) > 0:
        avg_length: float = sum(len(word) for word in tokens) / len(tokens)
        print(f"\nAverage word length: {avg_length:.1f} letters")
    else:
        print("\nAverage word length: N/A (no tokens)")
    print("--------------------------")
    
    return length_counts

def calculate_readability_stats(text: str, word_counts: Counter[str], sentence_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate readability and complexity statistics."""
    if not text or not word_counts: # Check word_counts as it's now primary for word stats
        return {
            'avg_word_length': 0.0,
            'complexity_score': 0.0,
            'readability_level': 'Unknown'
        }
    
    total_chars_in_counted_words: int = sum(len(word) * count for word, count in word_counts.items())
    total_counted_words: int = sum(word_counts.values())
    avg_word_length: float = total_chars_in_counted_words / total_counted_words if total_counted_words > 0 else 0.0
    
    avg_sentence_length: float = sentence_analysis.get('average_words_per_sentence', 0.0)
    complexity_score: float = (avg_word_length * 0.6) + (avg_sentence_length * 0.4)
    
    readability_level: str = 'Unknown'
    if complexity_score < 8:
        readability_level = 'Easy'
    elif complexity_score < 12:
        readability_level = 'Moderate'
    elif complexity_score < 16:
        readability_level = 'Difficult'
    else:
        readability_level = 'Very Difficult'
    
    return {
        'avg_word_length': round(avg_word_length, 1),
        'complexity_score': round(complexity_score, 1),
        'readability_level': readability_level
    }

def find_interesting_patterns(word_counts: Counter[str], text: str) -> Dict[str, Any]: # text parameter might be less used
    """Find interesting patterns in the text."""
    patterns: Dict[str, Any] = {
        'repeated_words': [],
        'long_words': [],
        'short_words': [],
        'word_variety': 0.0
    }
    
    if not word_counts:
        return patterns
    
    patterns['repeated_words'] = [
        (word, count) for word, count in word_counts.most_common(10) 
        if count > 1
    ]
    
    patterns['long_words'] = [
        word for word in word_counts.keys() 
        if len(word) >= 7
    ][:10] # Top 10 long words
    
    patterns['short_words'] = [
        word for word in word_counts.keys() 
        if len(word) <= 2
    ][:10] # Top 10 short words
    
    total_words: int = sum(word_counts.values())
    unique_words_count: int = len(word_counts)
    patterns['word_variety'] = round(unique_words_count / total_words * 100, 1) if total_words > 0 else 0.0
    
    return patterns

def print_header(title: str, width: int = 60) -> None:
    """Print a formatted header."""
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_section(title: str, width: int = 60) -> None:
    """Print a formatted section header."""
    print(f"\n{title}")
    print("-" * len(title) if len(title) <= width else "-" * width)


def display_general_statistics(stats: Dict[str, Any]) -> None:
    """Display general text statistics in a formatted way."""
    print_section("📊 General Statistics")
    
    print(f"📄 Total Characters (raw): {stats.get('character_count', 0):,}")
    print(f"🔤 Characters (raw, no spaces): {stats.get('character_count_no_spaces', 0):,}")
    print(f"📝 Total Words (after cleaning/stop words): {stats.get('word_count', 0):,}")
    print(f"📋 Total Sentences: {stats.get('sentence_count', 0):,}")
    print(f"📄 Paragraphs: {stats.get('paragraph_count', 0):,}")
    
    if stats.get('sentence_count', 0) > 0 and stats.get('word_count', 0) > 0 :
        words_per_sentence: float = stats['word_count'] / stats['sentence_count']
        print(f"📏 Average Words per Sentence: {words_per_sentence:.1f}")
    
    # avg_word_length from readability_stats is more accurate for analyzed words
    # if stats.get('word_count', 0) > 0:
    #     pass 

def display_word_analysis(word_analysis: Dict[str, Any]) -> None:
    """Display word frequency analysis."""
    print_section("🔤 Word Frequency Analysis")
    
    word_frequencies: Dict[str, int] = word_analysis.get('word_frequencies', {})
    statistics: Dict[str, Any] = word_analysis.get('statistics', {})
    
    print(f"🎯 Unique Words: {statistics.get('unique_words', 0):,}")
    print(f"📊 Total Word Count (in analysis): {statistics.get('total_words', 0):,}")
    
    if word_frequencies and statistics.get('total_words', 0) > 0:
        # num_common_words_to_display is used in analyze_text_complete to create word_frequencies
        # So, the length of word_frequencies dict is the number to display.
        print(f"\n🏆 Top {len(word_frequencies)} Most Common Words:")
        for i, (word, count) in enumerate(word_frequencies.items(), 1):
            percentage: float = (count / statistics['total_words']) * 100
            print(f"  {i:2d}. '{word}' - {count} times ({percentage:.1f}%)")
    elif not word_frequencies:
        print("No word frequencies to display (perhaps all words were stop words or file was empty after cleaning).")


def display_sentence_analysis(sentence_analysis: Dict[str, Any]) -> None:
    """Display sentence analysis results."""
    print_section("📋 Sentence Analysis")
    
    print(f"📊 Total Sentences: {sentence_analysis.get('sentence_count',0)}")
    print(f"📏 Average Words per Sentence: {sentence_analysis.get('average_words_per_sentence',0.0)}")
    
    longest: str = sentence_analysis.get('longest_sentence', '')
    if longest:
        print(f"\n📏 Longest Sentence:")
        print(f"   \"{longest[:PREVIEW_LENGTH]}{'...' if len(longest) > PREVIEW_LENGTH else ''}\"") # Use PREVIEW_LENGTH
    
    shortest: str = sentence_analysis.get('shortest_sentence', '')
    if shortest:
        print(f"\n📏 Shortest Sentence:")
        print(f"   \"{shortest}\"")

def display_readability_analysis(readability_stats: Dict[str, Any]) -> None:
    """Display readability analysis."""
    print_section("📖 Readability Analysis")
    
    print(f"📐 Average Word Length (of analyzed words): {readability_stats.get('avg_word_length',0.0)} characters")
    print(f"🎯 Complexity Score: {readability_stats.get('complexity_score',0.0)}") # Removed /20 as it's not a fixed scale
    print(f"📚 Readability Level: {readability_stats.get('readability_level','Unknown')}")
    
    level: Optional[str] = readability_stats.get('readability_level')
    if level == 'Easy':
        print("   💡 This text is easy to read and understand.")
    elif level == 'Moderate':
        print("   💡 This text requires moderate reading skills.")
    elif level == 'Difficult':
        print("   💡 This text is challenging and requires good reading skills.")
    elif level == 'Very Difficult':
        print("   💡 This text is very difficult and requires advanced reading skills.")
    else:
        print("   💡 Readability level could not be determined.")


def display_interesting_patterns(patterns: Dict[str, Any]) -> None:
    """Display interesting patterns found in the text."""
    print_section("🔍 Interesting Patterns")
    
    print(f"🎨 Word Variety (analyzed words): {patterns.get('word_variety',0.0)}% (unique words / total analyzed words)")
    
    repeated: List[Tuple[str, int]] = patterns.get('repeated_words', [])
    if repeated:
        print(f"\n🔄 Most Repeated Words (among analyzed):")
        for word, count in repeated[:5]: # Show top 5
            print(f"   '{word}' appears {count} times")
    
    long_w: List[str] = patterns.get('long_words', [])
    if long_w:
        print(f"\n📏 Long Words (7+ characters, among analyzed):")
        print(f"   {', '.join(long_w[:8])}") # Show up to 8
    
    short_w: List[str] = patterns.get('short_words', [])
    if short_w:
        print(f"\n🔤 Short Words (1-2 characters, among analyzed):")
        print(f"   {', '.join(short_w[:10])}") # Show up to 10

def display_complete_analysis(analysis_results: Dict[str, Any]) -> None:
    """Display complete text analysis in a professional format."""
    if 'error' in analysis_results and analysis_results['error']:
        print(f"❌ Analysis Error: {analysis_results['error']}")
        return
    
    print_header("📊 TEXT ANALYSIS REPORT 📊")
    
    if 'general_stats' in analysis_results:
        display_general_statistics(analysis_results['general_stats'])
    
    if 'word_analysis' in analysis_results:
        display_word_analysis(analysis_results['word_analysis'])
    
    if 'sentence_analysis' in analysis_results:
        display_sentence_analysis(analysis_results['sentence_analysis'])
    
    if 'word_analysis' in analysis_results and 'sentence_analysis' in analysis_results:
        # Use pre-calculated readability and patterns
        readability_stats_data = analysis_results.get('readability_stats', {})
        if readability_stats_data:
            display_readability_analysis(readability_stats_data)
        else:
            print("\nℹ️ Readability stats not available.")

        patterns_data = analysis_results.get('interesting_patterns', {})
        if patterns_data:
            display_interesting_patterns(patterns_data)
        else:
            print("\nℹ️ Interesting patterns not available.")
            
    print_section("✅ Analysis Complete")
    print("📝 Report generated successfully!")

def save_results_to_file(
    frequencies_counter: Counter[str], 
    num_top_words: int, 
    unique_word_count: int, 
    output_filename: str = DEFAULT_RESULTS_FILENAME
) -> None:
    """
    Saves analysis results to a file. (Enhancement 3 from Module 4B)
    
    Args:
        frequencies_counter (Counter[str]): Word frequency Counter object.
        num_top_words (int): Number of top words to save.
        unique_word_count (int): Total number of unique words.
        output_filename (str): Name of the file to save results.
    """
    try:
        # Ensure output_filename is a Path object for open()
        output_path: Path = Path(output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Text Analysis Results\n")
            f.write("=" * 30 + "\n\n")
            
            actual_top_n: int = min(num_top_words, unique_word_count)
            most_common: List[Tuple[str, int]] = frequencies_counter.most_common(actual_top_n)
            
            f.write(f"Top {actual_top_n} most common words:\n")
            f.write("-" * 30 + "\n")
            
            for word, count in most_common:
                f.write(f"{word:15} : {count:3d}\n")
            
            f.write("-" * 30 + "\n")
            f.write(f"Total unique words: {unique_word_count}\n")
            
            total_words_val: int
            # This check is a bit fragile. Assumes Counter won't have 'total_words' as a key.
            # Better to rely on sum(frequencies_counter.values())
            total_words_val = sum(frequencies_counter.values())

            f.write(f"Total words (in analysis): {total_words_val}\n\n")
            f.write("Analysis complete.\n")
        
        print(f"\n✅ Results successfully saved to {output_path}")
    except IOError: # More specific exception
        print(f"\n❌ Error: Could not write results to {output_filename}. Check permissions or path.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred while saving results: {e}")

def display_summary(analysis_results: Dict[str, Any]) -> None:
    """Display a quick summary of the analysis."""
    if 'error' in analysis_results and analysis_results['error']:
        print(f"❌ Error: {analysis_results['error']}")
        return
    
    general: Dict[str, Any] = analysis_results.get('general_stats', {})
    word_analysis: Dict[str, Any] = analysis_results.get('word_analysis', {})
    stats: Dict[str, Any] = word_analysis.get('statistics', {}) 
    
    print("\n" + "="*40)
    print("📊 QUICK SUMMARY")
    print("="*40)
    print(f"📄 Characters (raw): {general.get('character_count', 0):,}")
    print(f"📝 Words (analyzed): {stats.get('total_words', 0):,}") 
    print(f"📋 Sentences: {general.get('sentence_count', 0):,}")
    print(f"🎯 Unique Words (analyzed): {stats.get('unique_words', 0):,}")
    
    most_common_list: List[Tuple[str, int]] = stats.get('most_common', []) 
    if most_common_list:
        top_word, count = most_common_list[0]
        print(f"🏆 Most Common Word: '{top_word}' ({count} times)")
    
    print("="*40)

# =============================================================================
# MAIN INTEGRATION & TESTING (Module 3E / Enhanced in 4B)
# =============================================================================

def run_comprehensive_test() -> bool:
    """Run comprehensive testing of all components."""
    # This function would need updates if parameters of core functions change.
    # For now, keeping it as is from Module 3E.
    print_header("🧪 COMPREHENSIVE TESTING SUITE 🧪")
    
    test_results: Dict[str, bool] = {
        'file_io': False,
        'text_processing': False,
        'analysis': False,
        'display': False
    }
    
    # Test 1: File I/O (Simplified for brevity, assumes functions work)
    print_section("📁 Testing File I/O System")
    if callable(load_text_file):
        print("✅ File I/O system assumed functional for this test.")
        test_results['file_io'] = True
    else:
        print("❌ File I/O functions not found.")
    
    # Test 2: Text Processing
    print_section("🔄 Testing Text Processing Pipeline")
    try:
        test_text: str = "Hello world! This is a test with the word test."
        # Test with stop words off for baseline
        word_counts_test: Counter[str] = count_words(test_text, use_stop_words=False)
        sentence_count_test: int = count_sentences(test_text)
        
        if word_counts_test.get('test', 0) == 2 and sentence_count_test > 0:
            print("✅ Text processing (no stop words) functional.")
            # Test with stop words on
            word_counts_sw_test: Counter[str] = count_words(test_text, use_stop_words=True)
            # Check against STOP_WORDS set directly for robustness
            if not any(sw in word_counts_sw_test for sw in STOP_WORDS if sw in word_counts_test):
                 print("✅ Text processing (with stop words) functional.")
                 test_results['text_processing'] = True
            else:
                print("❌ Stop word removal test failed.")
        else:
            print("❌ Text processing (no stop words) test failed.")
    except Exception as e:
        print(f"❌ Text processing error: {e}")
    
    # Test 3: Analysis
    print_section("📊 Testing Analysis Functions")
    try:
        test_text_analysis: str = "The quick brown fox. Jumps over the lazy dog."
        results_analysis: Dict[str, Any] = analyze_text_complete(test_text_analysis, use_stop_words=False) # Test without stop words
        
        if 'error' not in results_analysis and results_analysis.get('general_stats',{}).get('word_count',0) > 0:
            print("✅ Analysis functions working.")
            test_results['analysis'] = True
        else:
            print(f"❌ Analysis test failed. Error: {results_analysis.get('error','')}")
    except Exception as e:
        print(f"❌ Analysis error: {e}")
    
    # Test 4: Display (Conceptual check, actual display is visual)
    print_section("🖥️ Testing Display Functions")
    if callable(display_complete_analysis) and callable(display_summary):
        print("✅ Display functions are present.")
        test_results['display'] = True
    else:
        print("❌ Display functions not found.")
        
    print_section("🎯 Test Results Summary")
    all_passed: bool = all(test_results.values())
    for component, passed in test_results.items():
        status: str = "✅ PASS" if passed else "❌ FAIL"
        print(f"{component.replace('_', ' ').title()}: {status}")
    
    if all_passed:
        print("\n🎉 All tests passed! Your text analyzer is ready!")
    else:
        print("\n⚠️ Some tests failed. Please review the errors above.")
    return all_passed


def _handle_analyze_file_option() -> None:
    """Handles the logic for menu option 1: Analyze Text File."""
    # Filepath is now fixed for this option.
    filepath_config: str = str(FIXED_TARGET_FILEPATH)
    print(f"ℹ️ Analyzing fixed file: {filepath_config}")

    num_common_words_config: int
    use_stop_words_config: bool
    num_common_words_config, use_stop_words_config = get_user_input_config()
    
    # Validate the fixed filepath
    is_valid_path, path_message = validate_file_path(filepath_config)
    if not is_valid_path:
        print(f"❌ Error with fixed file path '{filepath_config}': {path_message}")
        print("Please ensure 's.txt' exists in the script directory.")
        print("Returning to main menu.")
        return

    content: str = read_file(filepath_config)
    
    if not content:
        print(f"❌ No content loaded from '{filepath_config}' (file might be empty or unreadable). Returning to main menu.")
        return
    
    print("\n🔄 Running complete analysis...")
    pipeline_start_time = time.time() # Start timing for M4C

    if use_stop_words_config:
        print("ℹ️ Stop word removal is ON.")
    else:
        print("ℹ️ Stop word removal is OFF.")
    
    results = analyze_text_complete(content, 
                                    use_stop_words=use_stop_words_config, 
                                    num_common_words_to_display=num_common_words_config)
    
    pipeline_end_time = time.time() # End timing for M4C
    print(f"\n⏱️ Total processing pipeline took: {pipeline_end_time - pipeline_start_time:.4f} seconds")

    if 'error' in results and results['error']:
        print(f"❌ Analysis error: {results['error']}")
        return
    
    # Display options
    print("\n📊 Analysis complete! Choose display format:")
    print("1. Complete Report")
    print("2. Quick Summary")
    print("3. Both")
    
    display_choice_input = input("Enter choice (1-3): ").strip() # Renamed variable
    
    if display_choice_input == "1":
        display_complete_analysis(results)
    elif display_choice_input == "2":
        display_summary(results)
    elif display_choice_input == "3":
        display_summary(results)
        display_complete_analysis(results)
    else: # Default to summary if invalid choice
        print("⚠️ Invalid display choice, showing summary:")
        display_summary(results)

    # Word Length Analysis display (M4C)
    processed_tokens_for_length_analysis = results.get('processed_tokens', [])
    if processed_tokens_for_length_analysis:
        analyze_word_lengths(processed_tokens_for_length_analysis)
    # No specific "else" needed here, analyze_word_lengths handles empty tokens.

    # Ask to save results
    if 'word_analysis' in results and results['word_analysis'].get('full_word_counts_obj'):
        while True:
            save_choice = input("\n💾 Save analysis results to file? (yes/no, default: no): ").strip().lower()
            if not save_choice or save_choice == 'no':
                break
            elif save_choice == 'yes':
                default_output_filename = "analysis_results.txt"
                output_filename_input = input(f"Enter output filename (default: {default_output_filename}): ").strip()
                if not output_filename_input:
                    output_filename_input = default_output_filename
                
                # Prepare data for save_results_to_file
                freq_counter = results['word_analysis']['full_word_counts_obj']
                # num_common_words_config is the number of words user wanted to *display*
                # For saving, we can use the same or decide on a fixed number, e.g., all or top N.
                # Let's use num_common_words_config for consistency with display.
                n_to_save = num_common_words_config 
                unique_count_to_save = len(freq_counter)
                
                save_results_to_file(freq_counter, n_to_save, unique_count_to_save, output_filename_input)
                break
            else:
                print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")


def main() -> None:
    """Main execution function - Complete integrated application."""
    print_header("🚀 TEXT ANALYZER - COMPLETE VERSION 🚀")
    print("Welcome to the comprehensive text analysis tool!")
    print("Built through Modules 3A-3E. Now enhancing with Module 4B features.")
    
    while True:
        try:
            print("\n" + "="*50)
            print("📋 Main Menu")
            print("="*50)
            print("1. 📊 Analyze Fixed Text File (s.txt)") 
            print("2. 📂 Analyze Custom Text File") # New menu option
            print("3. 🧪 Run System Tests")
            print("4. ❓ Help & Information")
            print("5. 🚪 Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                _handle_analyze_file_option()
            
            elif choice == "2": # New handler for custom file
                custom_filepath_content = load_text_file()
                if custom_filepath_content:
                    num_common_words_cfg, use_stop_words_cfg = get_user_input_config()
                    print("\n🔄 Running complete analysis...")
                    pipeline_start_time = time.time()
                    if use_stop_words_cfg:
                        print("ℹ️ Stop word removal is ON.")
                    else:
                        print("ℹ️ Stop word removal is OFF.")
                    
                    results = analyze_text_complete(
                        custom_filepath_content,
                        use_stop_words=use_stop_words_cfg,
                        num_common_words_to_display=num_common_words_cfg
                    )
                    pipeline_end_time = time.time()
                    print(f"\n⏱️ Total processing pipeline took: {pipeline_end_time - pipeline_start_time:.4f} seconds")

                    if 'error' in results and results['error']:
                        print(f"❌ Analysis error: {results['error']}")
                    else:
                        # Display options
                        print("\n📊 Analysis complete! Choose display format:")
                        print("1. Complete Report")
                        print("2. Quick Summary")
                        print("3. Both")
                        display_choice = input("Enter choice (1-3): ").strip()
                        if display_choice == "1":
                            display_complete_analysis(results)
                        elif display_choice == "2":
                            display_summary(results)
                        elif display_choice == "3":
                            display_summary(results)
                            display_complete_analysis(results)
                        else:
                            print("⚠️ Invalid display choice, showing summary:")
                            display_summary(results)

                        processed_tokens_len_analysis = results.get('processed_tokens', [])
                        if processed_tokens_len_analysis:
                            analyze_word_lengths(processed_tokens_len_analysis)

                        if 'word_analysis' in results and results['word_analysis'].get('full_word_counts_obj'):
                            while True:
                                save_choice = input("\n💾 Save analysis results to file? (yes/no, default: no): ").strip().lower()
                                if not save_choice or save_choice == 'no':
                                    break
                                elif save_choice == 'yes':
                                    default_out_fn = "custom_analysis_results.txt"
                                    out_fn_input = input(f"Enter output filename (default: {default_out_fn}): ").strip()
                                    if not out_fn_input:
                                        out_fn_input = default_out_fn
                                    
                                    freq_ctr = results['word_analysis']['full_word_counts_obj']
                                    n_save = num_common_words_cfg
                                    unique_save = len(freq_ctr)
                                    save_results_to_file(freq_ctr, n_save, unique_save, out_fn_input)
                                    break
                                else:
                                    print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")
                else:
                    print("❌ No content loaded from custom file. Returning to main menu.")

            elif choice == "3":
                run_comprehensive_test()
            
            elif choice == "4":
                print_header("❓ HELP & INFORMATION ❓")
                print("This text analyzer can process any UTF-8 text file and provide:")
                print("• Word frequency analysis (optionally with stop word removal)")
                print("• Sentence structure analysis")
                print("• Readability assessment")
                print("• Pattern detection")
                print("• Professional formatting")
                print("\nFor best results:")
                print("• Use plain text files (.txt)")
                print("• Keep files under 10MB")
                print("• Ensure UTF-8 encoding")
                # print("• Place files in the same directory as this script or provide path") 
            
            elif choice == "5":
                print("\n👋 Thank you for using Text Analyzer!")
                print("🎉 Module 3 series complete! Module 4 enhancements started.")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-5.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user. Exiting.")
            break 
        except Exception as e:
            print(f"\n❌ An unexpected error occurred in the main menu: {e}")
            print("💡 Please try again or restart the application.")
            # Consider whether to break or continue after a generic exception
            # For robustness, might be better to log and continue, or offer to exit.
            # For this educational script, continuing is fine.

if __name__ == "__main__":
    main()
