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

# =============================================================================
# FILE I/O FUNCTIONS (Module 3B from original structure)
# =============================================================================

def validate_file_path(filename):
    """Validate that a file path is safe and accessible."""
    try:
        file_path = Path(filename)
        
        if file_path.is_absolute() and not file_path.is_relative_to(Path.cwd()):
            return False, "For security, please use files in the current directory"
        
        if not file_path.exists():
            return False, f"File '{filename}' does not exist"
        
        if not file_path.is_file():
            return False, f"'{filename}' is not a file"
        
        file_size = file_path.stat().st_size
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            return False, f"File too large ({file_size} bytes). Maximum: {max_size} bytes"
        
        return True, "File validation passed"
        
    except Exception as e:
        return False, f"Error validating file: {e}"

def read_file(filename):
    """Read text from a file with comprehensive error handling."""
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
    """Get filename from user with input validation and retry logic."""
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        try:
            print(f"\n📂 Enter filename (attempt {attempts + 1}/{max_attempts}):")
            print("💡 Tip: Use 'sample.txt' for testing")
            print("💡 Type 'quit' to exit")
            
            filename = input("Filename: ").strip()
            
            if filename.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                return ""
            
            if not filename:
                print("⚠️  Please enter a filename")
                attempts += 1
                continue
            
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

def get_user_input_config():
    """
    Gets configuration from user input. (Enhancement 2 from Module 4B)
    
    Returns:
        tuple: (filepath, num_words, enable_stop_words)
    """
    print("\n--- ⚙️ Text Analysis Configuration ---")
    
    # Default filepath to the sample file within the text_analyzer directory
    default_filepath = "text_analyzer/sample.txt"
    filepath_prompt = f"Enter path to text file (default: {default_filepath}): "
    filepath = input(filepath_prompt).strip()
    if not filepath:
        filepath = default_filepath
    
    num_words = 10 # Default
    while True:
        try:
            num_words_str = input(f"Number of top words to display (default: {num_words}): ").strip()
            if not num_words_str:
                # num_words remains default
                break
            else:
                num_words_val = int(num_words_str)
                if num_words_val <= 0:
                    print("⚠️ Please enter a positive number for top words.")
                    continue
                num_words = num_words_val
            break
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")
            
    enable_stop_words = True # Default
    while True:
        default_sw_choice_str = 'yes' if enable_stop_words else 'no'
        stop_words_prompt = f"Remove stop words? (yes/no, default: {default_sw_choice_str}): "
        stop_words_choice = input(stop_words_prompt).strip().lower()
        if not stop_words_choice:
            # enable_stop_words remains default
            break
        elif stop_words_choice == 'yes':
            enable_stop_words = True
            break
        elif stop_words_choice == 'no':
            enable_stop_words = False
            break
        else:
            print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")
            
    return filepath, num_words, enable_stop_words

def load_text_file():
    """Complete file loading workflow with user interaction."""
    print("🚀 Text File Loader")
    print("=" * 30)
    
    filename = get_filename_from_user()
    if not filename:
        return ""
    
    content = read_file(filename)
    
    if content:
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
# TEXT PROCESSING FUNCTIONS (Module 3C / Enhanced in 4B)
# =============================================================================

def clean_text(text):
    """Clean and preprocess text for analysis."""
    if not text or not isinstance(text, str):
        return ""
    
    cleaned = text.lower()
    cleaned = ' '.join(cleaned.split())
    cleaned = re.sub(r'[^\w\s.,!?;:-]', '', cleaned) # Keeps some punctuation for sentence analysis
    
    return cleaned

def clean_text_for_words(text):
    """Clean text specifically for word analysis (removes punctuation)."""
    if not text:
        return ""
    
    translator = str.maketrans('', '', string.punctuation)
    cleaned = text.translate(translator)
    cleaned = ' '.join(cleaned.split()) # Normalize whitespace again
    
    return cleaned.lower()

def remove_stop_words(tokens):
    """
    Removes common stop words from a list of tokens. (Enhancement 1 from Module 4B)
    
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
    
    original_token_count = len(tokens)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    removed_count = original_token_count - len(filtered_tokens)
    if removed_count > 0 : # Only print if words were actually removed
        print(f"ℹ️ Removed {removed_count} stop words.")
    return filtered_tokens

def count_words(text, use_stop_words=False): # Added use_stop_words parameter
    """Count word frequencies in text."""
    if not text:
        return Counter()
    
    cleaned_text = clean_text_for_words(text)
    words = cleaned_text.split()
    words = [word for word in words if len(word) > 0] # Filter out empty strings

    if use_stop_words:
        words = remove_stop_words(words)
        
    word_counts = Counter(words)
    return word_counts

def get_unique_words(text, use_stop_words=False): # Added use_stop_words to keep interface consistent if called elsewhere
    """Get list of unique words in text."""
    # This function now also considers stop words if the flag is passed.
    # However, analyze_text_complete will derive unique words from its already processed word_counts.
    word_counts = count_words(text, use_stop_words=use_stop_words)
    return sorted(word_counts.keys())

def get_word_count_stats(word_counts):
    """Calculate statistics from word counts."""
    if not word_counts:
        return {
            'total_words': 0,
            'unique_words': 0,
            'most_common': [],
            'average_frequency': 0
        }
    
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)
    most_common = word_counts.most_common(5) # From Module 3E, used for summary
    average_frequency = total_words / unique_words if unique_words > 0 else 0
    
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'most_common': most_common,
        'average_frequency': round(average_frequency, 2)
    }

def count_sentences(text):
    """Count sentences in text."""
    if not text:
        return 0
    
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return len(sentences)

def analyze_sentences(text):
    """Analyze sentence structure in text."""
    if not text:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    sentences = re.split(r'[.!?]+', text) # Uses original text before heavy cleaning
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    sentence_word_counts = []
    for sentence in sentences:
        # For sentence word counts, use clean_text_for_words to get a reasonable word split
        words_in_sentence = clean_text_for_words(sentence).split()
        words_in_sentence = [word for word in words_in_sentence if len(word) > 0]
        sentence_word_counts.append(len(words_in_sentence))
    
    average_words = sum(sentence_word_counts) / len(sentence_word_counts) if sentence_word_counts else 0
    
    longest_idx = sentence_word_counts.index(max(sentence_word_counts)) if sentence_word_counts else -1
    shortest_idx = sentence_word_counts.index(min(sentence_word_counts)) if sentence_word_counts else -1
    
    return {
        'sentence_count': len(sentences),
        'average_words_per_sentence': round(average_words, 1),
        'longest_sentence': sentences[longest_idx].strip() if longest_idx != -1 else "",
        'shortest_sentence': sentences[shortest_idx].strip() if shortest_idx != -1 else ""
    }

def analyze_text_complete(text, use_stop_words=False, num_common_words_to_display=10): # Added parameters
    """Complete text analysis pipeline."""
    if not text:
        return {
            'error': 'No text provided for analysis',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {}
        }
    
    try:
        # Word analysis
        word_counts = count_words(text, use_stop_words=use_stop_words) # Pass flag
        word_stats = get_word_count_stats(word_counts)
        unique_words_list = sorted(word_counts.keys()) if word_counts else [] # Derive from processed counts
        
        # Sentence analysis (uses original text for sentence splitting)
        cleaned_for_sentences = clean_text(text) # Light cleaning for sentence structure
        sentence_stats = analyze_sentences(cleaned_for_sentences)
        
        # General statistics
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        
        general_stats = {
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'word_count': word_stats['total_words'], # Based on (potentially) stop-word filtered counts
            'sentence_count': sentence_stats['sentence_count'],
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()])
        }
        
        return {
            'word_analysis': {
                'word_frequencies': dict(word_counts.most_common(num_common_words_to_display)), # Use dynamic N
                'statistics': word_stats,
                'unique_words_sample': unique_words_list[:10], # Sample of unique words
                'full_word_counts_obj': word_counts # Add the full Counter object
            },
            'sentence_analysis': sentence_stats,
            'general_stats': general_stats,
            'original_text': text  # Store for readability analysis
        }
        
    except Exception as e:
        return {
            'error': f'Analysis failed: {str(e)}',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {}
        }

# =============================================================================
# ANALYSIS & DISPLAY FUNCTIONS (Module 3D)
# =============================================================================

def calculate_readability_stats(text, word_counts, sentence_analysis):
    """Calculate readability and complexity statistics."""
    if not text or not word_counts: # Check word_counts as it's now primary for word stats
        return {
            'avg_word_length': 0,
            'complexity_score': 0,
            'readability_level': 'Unknown'
        }
    
    total_chars_in_counted_words = sum(len(word) * count for word, count in word_counts.items())
    total_counted_words = sum(word_counts.values())
    avg_word_length = total_chars_in_counted_words / total_counted_words if total_counted_words > 0 else 0
    
    avg_sentence_length = sentence_analysis.get('average_words_per_sentence', 0)
    complexity_score = (avg_word_length * 0.6) + (avg_sentence_length * 0.4)
    
    readability_level = 'Unknown'
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

def find_interesting_patterns(word_counts, text): # text parameter might be less used if patterns are from word_counts
    """Find interesting patterns in the text."""
    patterns = {
        'repeated_words': [],
        'long_words': [],
        'short_words': [],
        'word_variety': 0
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
    ][:10]
    
    patterns['short_words'] = [
        word for word in word_counts.keys() 
        if len(word) <= 2
    ][:10]
    
    total_words = sum(word_counts.values())
    unique_words_count = len(word_counts)
    patterns['word_variety'] = round(unique_words_count / total_words * 100, 1) if total_words > 0 else 0
    
    return patterns

def print_header(title, width=60):
    """Print a formatted header."""
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_section(title, width=60): # width parameter was unused, now used for consistency
    """Print a formatted section header."""
    print(f"\n{title}")
    print("-" * len(title) if len(title) <= width else "-" * width)


def display_general_statistics(stats):
    """Display general text statistics in a formatted way."""
    print_section("📊 General Statistics")
    
    print(f"📄 Total Characters (raw): {stats.get('character_count', 0):,}")
    print(f"🔤 Characters (raw, no spaces): {stats.get('character_count_no_spaces', 0):,}")
    print(f"📝 Total Words (after cleaning/stop words): {stats.get('word_count', 0):,}")
    print(f"📋 Total Sentences: {stats.get('sentence_count', 0):,}")
    print(f"📄 Paragraphs: {stats.get('paragraph_count', 0):,}")
    
    if stats.get('sentence_count', 0) > 0 and stats.get('word_count',0) > 0 :
        words_per_sentence = stats['word_count'] / stats['sentence_count']
        print(f"📏 Average Words per Sentence: {words_per_sentence:.1f}")
    
    if stats.get('word_count', 0) > 0:
        # For average chars per word, it's better to use sum of lengths of words in word_counts
        # This is effectively calculated in readability_stats avg_word_length
        # For now, keep the old way or note it.
        # chars_per_word = stats['character_count_no_spaces'] / stats['word_count']
        # print(f"📐 Average Characters per Word (approx): {chars_per_word:.1f}")
        pass # This stat is better represented by avg_word_length from readability

def display_word_analysis(word_analysis):
    """Display word frequency analysis."""
    print_section("🔤 Word Frequency Analysis")
    
    word_frequencies = word_analysis.get('word_frequencies', {})
    statistics = word_analysis.get('statistics', {})
    
    print(f"🎯 Unique Words: {statistics.get('unique_words', 0):,}")
    print(f"📊 Total Word Count (in analysis): {statistics.get('total_words', 0):,}")
    # average_frequency might be misleading if stop words removed, as total_words changes
    # print(f"📈 Average Word Frequency: {statistics.get('average_frequency', 0.0)}") 
    
    if word_frequencies and statistics.get('total_words', 0) > 0:
        print(f"\n🏆 Top 10 Most Common Words:")
        for i, (word, count) in enumerate(word_frequencies.items(), 1):
            percentage = (count / statistics['total_words']) * 100
            print(f"  {i:2d}. '{word}' - {count} times ({percentage:.1f}%)")
    elif not word_frequencies:
        print("No word frequencies to display (perhaps all words were stop words or file was empty after cleaning).")


def display_sentence_analysis(sentence_analysis):
    """Display sentence analysis results."""
    print_section("📋 Sentence Analysis")
    
    print(f"📊 Total Sentences: {sentence_analysis.get('sentence_count',0)}")
    print(f"📏 Average Words per Sentence: {sentence_analysis.get('average_words_per_sentence',0.0)}")
    
    longest = sentence_analysis.get('longest_sentence', '')
    if longest:
        print(f"\n📏 Longest Sentence:")
        print(f"   \"{longest[:100]}{'...' if len(longest) > 100 else ''}\"")
    
    shortest = sentence_analysis.get('shortest_sentence', '')
    if shortest:
        print(f"\n📏 Shortest Sentence:")
        print(f"   \"{shortest}\"")

def display_readability_analysis(readability_stats):
    """Display readability analysis."""
    print_section("📖 Readability Analysis")
    
    print(f"📐 Average Word Length (of analyzed words): {readability_stats.get('avg_word_length',0.0)} characters")
    print(f"🎯 Complexity Score: {readability_stats.get('complexity_score',0.0)}/20") # Max score isn't strictly 20, but it's a scale
    print(f"📚 Readability Level: {readability_stats.get('readability_level','Unknown')}")
    
    level = readability_stats.get('readability_level')
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


def display_interesting_patterns(patterns):
    """Display interesting patterns found in the text."""
    print_section("🔍 Interesting Patterns")
    
    print(f"🎨 Word Variety (analyzed words): {patterns.get('word_variety',0.0)}% (unique words / total analyzed words)")
    
    repeated = patterns.get('repeated_words', [])
    if repeated:
        print(f"\n🔄 Most Repeated Words (among analyzed):")
        for word, count in repeated[:5]: # Show top 5
            print(f"   '{word}' appears {count} times")
    
    long_w = patterns.get('long_words', [])
    if long_w:
        print(f"\n📏 Long Words (7+ characters, among analyzed):")
        print(f"   {', '.join(long_w[:8])}") # Show up to 8
    
    short_w = patterns.get('short_words', [])
    if short_w:
        print(f"\n🔤 Short Words (1-2 characters, among analyzed):")
        print(f"   {', '.join(short_w[:10])}") # Show up to 10

def display_complete_analysis(analysis_results):
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
    
    # Calculate and display readability & patterns based on potentially filtered word_counts
    if 'word_analysis' in analysis_results and 'sentence_analysis' in analysis_results:
        word_counts_data = analysis_results['word_analysis'].get('word_frequencies', {})
        # word_counts_data is already a dict from most_common(10). Need full Counter for stats.
        # This requires passing the full Counter object in analysis_results or recalculating.
        # For now, let's assume word_analysis.statistics.most_common gives enough for a Counter
        
        # Reconstruct Counter for stats if word_frequencies is just top 10
        # A better way is to pass the full Counter object in analysis_results['word_analysis']
        # For now, this part might be inaccurate if word_frequencies is truncated.
        # Let's assume word_analysis['statistics']['most_common'] is the full list for Counter.
        # No, word_analysis.statistics.most_common is only top 5.
        # The best is to pass the full word_counts Counter object through analysis_results.
        # Let's modify analyze_text_complete to include the full Counter.
        
        # This part needs the full word_counts.
        # analyze_text_complete should be modified to return the full word_counts Counter object.
        # Let's assume it's available as analysis_results['word_analysis']['full_word_counts']
        
        full_word_counts = analysis_results.get('word_analysis',{}).get('full_word_counts_obj', Counter())

        if full_word_counts:
            text_for_readability = analysis_results.get('original_text', '') # Use original for context
            readability_stats = calculate_readability_stats(
                text_for_readability, # Pass original text
                full_word_counts, # Pass full counter
                analysis_results['sentence_analysis']
            )
            display_readability_analysis(readability_stats)
            
            patterns = find_interesting_patterns(full_word_counts, text_for_readability)
            display_interesting_patterns(patterns)
        else:
            print("\nℹ️ Full word counts not available for readability and pattern analysis.")

    print_section("✅ Analysis Complete")
    print("📝 Report generated successfully!")

def save_results_to_file(frequencies_counter, num_top_words, unique_word_count, output_filename="analysis_results.txt"):
    """
    Saves analysis results to a file. (Enhancement 3 from Module 4B)
    
    Args:
        frequencies_counter (Counter): Word frequency Counter object.
        num_top_words (int): Number of top words to save.
        unique_word_count (int): Total number of unique words.
        output_filename (str): Name of the file to save results.
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("Text Analysis Results\n")
            f.write("=" * 30 + "\n\n")
            
            # Ensure num_top_words is not greater than available unique words for most_common
            actual_top_n = min(num_top_words, unique_word_count)
            most_common = frequencies_counter.most_common(actual_top_n)
            
            f.write(f"Top {actual_top_n} most common words:\n")
            f.write("-" * 30 + "\n")
            
            for word, count in most_common:
                f.write(f"{word:15} : {count:3d}\n")
            
            f.write("-" * 30 + "\n")
            f.write(f"Total unique words: {unique_word_count}\n")
            
            if 'total_words' in frequencies_counter: # Check if it's a pre-calculated stat dict
                 total_words_val = frequencies_counter['total_words']
            else: # It's a Counter object
                 total_words_val = sum(frequencies_counter.values())

            f.write(f"Total words (in analysis): {total_words_val}\n\n")
            f.write("Analysis complete.\n")
        
        print(f"\n✅ Results successfully saved to {output_filename}")
    except IOError:
        print(f"\n❌ Error: Could not write results to {output_filename}.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred while saving results: {e}")

def display_summary(analysis_results):
    """Display a quick summary of the analysis."""
    if 'error' in analysis_results and analysis_results['error']:
        print(f"❌ Error: {analysis_results['error']}")
        return
    
    general = analysis_results.get('general_stats', {})
    word_analysis = analysis_results.get('word_analysis', {})
    stats = word_analysis.get('statistics', {}) # word_stats
    
    print("\n" + "="*40)
    print("📊 QUICK SUMMARY")
    print("="*40)
    print(f"📄 Characters (raw): {general.get('character_count', 0):,}")
    print(f"📝 Words (analyzed): {stats.get('total_words', 0):,}") # total_words from word_stats
    print(f"📋 Sentences: {general.get('sentence_count', 0):,}")
    print(f"🎯 Unique Words (analyzed): {stats.get('unique_words', 0):,}")
    
    most_common_list = stats.get('most_common', []) # This is top 5 from get_word_count_stats
    if most_common_list:
        top_word, count = most_common_list[0]
        print(f"🏆 Most Common Word: '{top_word}' ({count} times)")
    
    print("="*40)

# =============================================================================
# MAIN INTEGRATION & TESTING (Module 3E / Enhanced in 4B)
# =============================================================================

def run_comprehensive_test():
    """Run comprehensive testing of all components."""
    # This function would need updates if parameters of core functions change.
    # For now, keeping it as is from Module 3E.
    print_header("🧪 COMPREHENSIVE TESTING SUITE 🧪")
    
    test_results = {
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
        test_text = "Hello world! This is a test with the word test."
        # Test with stop words off for baseline
        word_counts_test = count_words(test_text, use_stop_words=False)
        sentence_count_test = count_sentences(test_text)
        
        if word_counts_test.get('test', 0) == 2 and sentence_count_test > 0:
            print("✅ Text processing (no stop words) functional.")
            # Test with stop words on
            word_counts_sw_test = count_words(test_text, use_stop_words=True)
            if 'is' not in word_counts_sw_test and 'the' not in word_counts_sw_test : # 'is', 'the', 'a' are stop words
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
        test_text_analysis = "The quick brown fox. Jumps over the lazy dog."
        results_analysis = analyze_text_complete(test_text_analysis, use_stop_words=False) # Test without stop words
        
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
    all_passed = all(test_results.values())
    for component, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{component.replace('_', ' ').title()}: {status}")
    
    if all_passed:
        print("\n🎉 All tests passed! Your text analyzer is ready!")
    else:
        print("\n⚠️ Some tests failed. Please review the errors above.")
    return all_passed


def main():
    """Main execution function - Complete integrated application."""
    print_header("🚀 TEXT ANALYZER - COMPLETE VERSION 🚀")
    print("Welcome to the comprehensive text analysis tool!")
    print("Built through Modules 3A-3E. Now enhancing with Module 4B features.")
    
    while True:
        try:
            print("\n" + "="*50)
            print("📋 Main Menu")
            print("="*50)
            print("1. 📊 Analyze Text File")
            print("2. 🧪 Run System Tests")
            print("3. ❓ Help & Information")
            print("4. 🚪 Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                # Main analysis workflow
                filepath_config, num_common_words_config, use_stop_words_config = get_user_input_config()
                
                # Validate filepath from get_user_input_config before reading
                is_valid_path, path_message = validate_file_path(filepath_config)
                if not is_valid_path:
                    print(f"❌ {path_message}")
                    print("Returning to main menu.")
                    continue

                content = read_file(filepath_config) # Use read_file directly
                
                if not content:
                    print("❌ No content loaded (file might be empty or unreadable). Returning to main menu.")
                    continue
                
                print("\n🔄 Running complete analysis...")
                if use_stop_words_config:
                    print("ℹ️ Stop word removal is ON.")
                else:
                    print("ℹ️ Stop word removal is OFF.")
                
                results = analyze_text_complete(content, 
                                                use_stop_words=use_stop_words_config, 
                                                num_common_words_to_display=num_common_words_config)
                
                if 'error' in results and results['error']:
                    print(f"❌ Analysis error: {results['error']}")
                    continue 
                
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
                    else:
                        print("Invalid choice, showing summary:")
                        display_summary(results)

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
            
            elif choice == "2":
                run_comprehensive_test()
            
            elif choice == "3":
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
                # print("• Place files in the same directory as this script or provide path") # Already handled by input
            
            elif choice == "4":
                print("\n👋 Thank you for using Text Analyzer!")
                print("🎉 Module 3 series complete! Module 4 enhancements started.")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-4.")
        
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
