"""
Text Analysis Script - Module 3C
A comprehensive text analysis tool for processing and analyzing text files.
"""

import os
import re
import string
from pathlib import Path
from collections import Counter

# =============================================================================
# FILE I/O FUNCTIONS (Module 3B)
# =============================================================================

def validate_file_path(filename):
    """
    Validate that a file path is safe and accessible.
    
    Args:
        filename (str): Path to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Convert to Path object for better handling
        file_path = Path(filename)
        
        # Check if path is absolute and potentially dangerous
        if file_path.is_absolute() and not file_path.is_relative_to(Path.cwd()):
            return False, "For security, please use files in the current directory"
        
        # Check if file exists
        if not file_path.exists():
            return False, f"File '{filename}' does not exist"
        
        # Check if it's actually a file
        if not file_path.is_file():
            return False, f"'{filename}' is not a file"
        
        # Check file size (limit to 10MB for this exercise)
        file_size = file_path.stat().st_size
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            return False, f"File too large ({file_size} bytes). Maximum: {max_size} bytes"
        
        return True, "File validation passed"
        
    except Exception as e:
        return False, f"Error validating file: {e}"

def read_file(filename):
    """
    Read text from a file with comprehensive error handling.
    
    Args:
        filename (str): Path to the text file to read
        
    Returns:
        str: Content of the file, or empty string if error
        
    Raises:
        None: All exceptions are caught and handled gracefully
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"✅ Successfully read file: {filename}")
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

def get_filename_from_user():
    """
    Get filename from user with input validation and retry logic.
    
    Returns:
        str: Valid filename, or empty string if user cancels
    """
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        try:
            print(f"\n📂 Enter filename (attempt {attempts + 1}/{max_attempts}):")
            print("💡 Tip: Use 'sample.txt' for testing")
            print("💡 Type 'quit' to exit")
            
            filename = input("Filename: ").strip()
            
            # Check for quit command
            if filename.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                return ""
            
            # Validate input
            if not filename:
                print("⚠️  Please enter a filename")
                attempts += 1
                continue
            
            # Validate file path
            is_valid, message = validate_file_path(filename)
            if is_valid:
                print(f"✅ {message}")
                return filename
            else:
                print(f"❌ {message}")
                attempts += 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            return ""
        except Exception as e:
            print(f"❌ Error getting input: {e}")
            attempts += 1
    
    print(f"\n❌ Maximum attempts ({max_attempts}) reached")
    return ""

def load_text_file():
    """
    Complete file loading workflow with user interaction.
    
    Returns:
        str: File content, or empty string if failed
    """
    print("🚀 Text File Loader")
    print("=" * 30)
    
    # Get filename from user
    filename = get_filename_from_user()
    if not filename:
        return ""
    
    # Read the file
    content = read_file(filename)
    
    if content:
        # Show preview of content
        preview_length = 100
        if len(content) > preview_length:
            preview = content[:preview_length] + "..."
        else:
            preview = content
        
        print(f"\n📖 File Preview:")
        print("-" * 20)
        print(preview)
        print("-" * 20)
    
    return content

# =============================================================================
# TEXT PROCESSING FUNCTIONS (Module 3C)
# =============================================================================

def clean_text(text):
    """
    Clean and preprocess text for analysis.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text ready for processing
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase for consistent analysis
    cleaned = text.lower()
    
    # Remove extra whitespace and normalize spaces
    cleaned = ' '.join(cleaned.split())
    
    # Optional: Remove or replace specific characters
    # Keep letters, numbers, spaces, and basic punctuation
    cleaned = re.sub(r'[^\w\s.,!?;:-]', '', cleaned)
    
    return cleaned

def clean_text_for_words(text):
    """
    Clean text specifically for word analysis (removes punctuation).
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Text with punctuation removed
    """
    if not text:
        return ""
    
    # Remove punctuation for word counting
    translator = str.maketrans('', '', string.punctuation)
    cleaned = text.translate(translator)
    
    # Normalize whitespace
    cleaned = ' '.join(cleaned.split())
    
    return cleaned.lower()

def count_words(text):
    """
    Count word frequencies in text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        Counter: Word frequencies as Counter object
    """
    if not text:
        return Counter()
    
    # Clean text for word analysis
    cleaned_text = clean_text_for_words(text)
    
    # Split into words
    words = cleaned_text.split()
    
    # Filter out empty strings and very short words if desired
    words = [word for word in words if len(word) > 0]
    
    # Count frequencies
    word_counts = Counter(words)
    
    return word_counts

def get_unique_words(text):
    """
    Get list of unique words in text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        list: Sorted list of unique words
    """
    word_counts = count_words(text)
    return sorted(word_counts.keys())

def get_word_count_stats(word_counts):
    """
    Calculate statistics from word counts.
    
    Args:
        word_counts (Counter): Word frequency counter
        
    Returns:
        dict: Statistics about word usage
    """
    if not word_counts:
        return {
            'total_words': 0,
            'unique_words': 0,
            'most_common': [],
            'average_frequency': 0
        }
    
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)
    most_common = word_counts.most_common(5) # Get top 5 for stats
    average_frequency = total_words / unique_words if unique_words > 0 else 0
    
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'most_common': most_common,
        'average_frequency': round(average_frequency, 2)
    }

def count_sentences(text):
    """
    Count sentences in text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        int: Number of sentences
    """
    if not text:
        return 0
    
    # Split on sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    
    # Filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return len(sentences)

def analyze_sentences(text):
    """
    Analyze sentence structure in text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Sentence analysis results
    """
    if not text:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    # Calculate statistics
    sentence_word_counts = []
    for sentence in sentences:
        words = clean_text_for_words(sentence).split()
        sentence_word_counts.append(len(words))
    
    average_words = sum(sentence_word_counts) / len(sentence_word_counts) if sentence_word_counts else 0
    
    # Find longest and shortest sentences
    longest_sentence_text = ""
    shortest_sentence_text = ""
    if sentences:
        longest_idx = sentence_word_counts.index(max(sentence_word_counts)) if sentence_word_counts else -1
        shortest_idx = sentence_word_counts.index(min(sentence_word_counts)) if sentence_word_counts else -1
        longest_sentence_text = sentences[longest_idx].strip() if longest_idx != -1 else ""
        shortest_sentence_text = sentences[shortest_idx].strip() if shortest_idx != -1 else ""

    return {
        'sentence_count': len(sentences),
        'average_words_per_sentence': round(average_words, 1),
        'longest_sentence': longest_sentence_text,
        'shortest_sentence': shortest_sentence_text
    }

def analyze_text_complete(text):
    """
    Complete text analysis pipeline.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Complete analysis results
    """
    if not text:
        return {
            'error': 'No text provided for analysis',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {}
        }
    
    try:
        # Word analysis
        word_counts = count_words(text)
        word_stats = get_word_count_stats(word_counts)
        unique_words_list = get_unique_words(text) # Renamed to avoid conflict
        
        # Sentence analysis
        sentence_stats = analyze_sentences(text)
        
        # General statistics
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        
        general_stats = {
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'word_count': word_stats['total_words'],
            'sentence_count': sentence_stats['sentence_count'],
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()])
        }
        
        return {
            'word_analysis': {
                'word_frequencies': dict(word_counts.most_common(10)), # Top 10 for preview
                'statistics': word_stats,
                'unique_words_sample': unique_words_list[:10]  # First 10 for preview
            },
            'sentence_analysis': sentence_stats,
            'general_stats': general_stats,
            'original_text': text # Store for potential future use (e.g. Module 3D)
        }
        
    except Exception as e:
        # It's good practice to log the error or be more specific
        # For now, returning a generic error message
        print(f"Error during analysis: {e}") # Added print for debugging
        return {
            'error': f'Analysis failed: {str(e)}',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {}
        }

# =============================================================================
# MAIN FUNCTION (Updated for Module 3C Testing)
# =============================================================================

def main():
    """Main execution function - testing text processing pipeline."""
    print("Text Analyzer - Module 3C: Text Processing Testing")
    print("=" * 60)
    
    # Load text file
    content = load_text_file()
    
    if not content:
        print("❌ No content to analyze. Exiting.")
        return
    
    print("\n🔄 Processing text...")
    
    # Run complete analysis
    results = analyze_text_complete(content)
    
    if 'error' in results and results['error']: # Check if error key exists and has a value
        print(f"❌ Analysis error: {results['error']}")
        return
    
    # Display results preview
    print("\n📊 Analysis Results Preview:")
    print("-" * 30)
    
    # General stats
    general = results.get('general_stats', {}) # Use .get for safety
    print(f"📄 Characters: {general.get('character_count', 0)}")
    print(f"📝 Words: {general.get('word_count', 0)}")
    print(f"📋 Sentences: {general.get('sentence_count', 0)}")
    
    # Word analysis preview
    word_analysis = results.get('word_analysis', {})
    word_frequencies_preview = word_analysis.get('word_frequencies', {})
    print(f"\n🔤 Most common words (sample):")
    for word, count in list(word_frequencies_preview.items())[:3]: # Show top 3 from the preview
        print(f"   '{word}': {count} times")
    
    # Sentence analysis preview
    sentence_analysis = results.get('sentence_analysis', {})
    print(f"\n📏 Average words per sentence: {sentence_analysis.get('average_words_per_sentence', 0.0)}")
    
    print("\n✅ Text processing pipeline (Module 3C) testing complete!")
    print("🎯 Ready for Module 3D: Analysis & Display Functions")

if __name__ == "__main__":
    main()
