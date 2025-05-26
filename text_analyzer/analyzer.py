"""
Text Analysis Script - Complete Version
A comprehensive text analysis tool for processing and analyzing text files.

Modules 3A-3E: Complete Integration
"""

import os
import re
import string
import re
import string
from pathlib import Path
from collections import Counter

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
# TEXT PROCESSING FUNCTIONS (Module 3C)
# =============================================================================

def clean_text(text):
    """Clean and preprocess text for analysis."""
    if not text or not isinstance(text, str):
        return ""
    
    cleaned = text.lower()
    cleaned = ' '.join(cleaned.split())
    cleaned = re.sub(r'[^\w\s.,!?;:-]', '', cleaned)
    
    return cleaned

def clean_text_for_words(text):
    """Clean text specifically for word analysis (removes punctuation)."""
    if not text:
        return ""
    
    translator = str.maketrans('', '', string.punctuation)
    cleaned = text.translate(translator)
    cleaned = ' '.join(cleaned.split())
    
    return cleaned.lower()

def count_words(text):
    """Count word frequencies in text."""
    if not text:
        return Counter()
    
    cleaned_text = clean_text_for_words(text)
    words = cleaned_text.split()
    words = [word for word in words if len(word) > 0]
    word_counts = Counter(words)
    
    return word_counts

def get_unique_words(text):
    """Get list of unique words in text."""
    word_counts = count_words(text)
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
    most_common = word_counts.most_common(5)
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
    
    sentences = re.split(r'[.!?]+', text)
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
        words = clean_text_for_words(sentence).split()
        sentence_word_counts.append(len(words))
    
    average_words = sum(sentence_word_counts) / len(sentence_word_counts)
    
    longest_idx = sentence_word_counts.index(max(sentence_word_counts))
    shortest_idx = sentence_word_counts.index(min(sentence_word_counts))
    
    return {
        'sentence_count': len(sentences),
        'average_words_per_sentence': round(average_words, 1),
        'longest_sentence': sentences[longest_idx].strip(),
        'shortest_sentence': sentences[shortest_idx].strip()
    }

def analyze_text_complete(text):
    """Complete text analysis pipeline."""
    if not text:
        return {
            'error': 'No text provided for analysis',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {}
        }
    
    try:
        word_counts = count_words(text)
        word_stats = get_word_count_stats(word_counts)
        unique_words = get_unique_words(text)
        
        sentence_stats = analyze_sentences(text)
        
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
                'word_frequencies': dict(word_counts.most_common(10)),
                'statistics': word_stats,
                'unique_words_sample': unique_words[:10]
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
    if not text or not word_counts:
        return {
            'avg_word_length': 0,
            'complexity_score': 0,
            'readability_level': 'Unknown'
        }
    
    total_chars = sum(len(word) * count for word, count in word_counts.items())
    total_words = sum(word_counts.values())
    avg_word_length = total_chars / total_words if total_words > 0 else 0
    
    avg_sentence_length = sentence_analysis.get('average_words_per_sentence', 0)
    complexity_score = (avg_word_length * 0.6) + (avg_sentence_length * 0.4)
    
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

def find_interesting_patterns(word_counts, text):
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
    unique_words = len(word_counts)
    patterns['word_variety'] = round(unique_words / total_words * 100, 1) if total_words > 0 else 0
    
    return patterns

def print_header(title, width=60):
    """Print a formatted header."""
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_section(title, width=60):
    """Print a formatted section header."""
    print(f"\n{title}")
    print("-" * len(title))

def display_general_statistics(stats):
    """Display general text statistics in a formatted way."""
    print_section("📊 General Statistics")
    
    print(f"📄 Total Characters: {stats['character_count']:,}")
    print(f"🔤 Characters (no spaces): {stats['character_count_no_spaces']:,}")
    print(f"📝 Total Words: {stats['word_count']:,}")
    print(f"📋 Total Sentences: {stats['sentence_count']:,}")
    print(f"📄 Paragraphs: {stats['paragraph_count']:,}")
    
    if stats['sentence_count'] > 0:
        words_per_sentence = stats['word_count'] / stats['sentence_count']
        print(f"📏 Average Words per Sentence: {words_per_sentence:.1f}")
    
    if stats['word_count'] > 0:
        chars_per_word = stats['character_count_no_spaces'] / stats['word_count']
        print(f"📐 Average Characters per Word: {chars_per_word:.1f}")

def display_word_analysis(word_analysis):
    """Display word frequency analysis."""
    print_section("🔤 Word Frequency Analysis")
    
    word_frequencies = word_analysis['word_frequencies']
    statistics = word_analysis['statistics']
    
    print(f"🎯 Unique Words: {statistics['unique_words']:,}")
    print(f"📊 Total Word Count: {statistics['total_words']:,}")
    print(f"📈 Average Word Frequency: {statistics['average_frequency']}")
    
    if word_frequencies:
        print(f"\n🏆 Top 10 Most Common Words:")
        for i, (word, count) in enumerate(word_frequencies.items(), 1):
            percentage = (count / statistics['total_words']) * 100
            print(f"  {i:2d}. '{word}' - {count} times ({percentage:.1f}%)")

def display_sentence_analysis(sentence_analysis):
    """Display sentence analysis results."""
    print_section("📋 Sentence Analysis")
    
    print(f"📊 Total Sentences: {sentence_analysis['sentence_count']}")
    print(f"📏 Average Words per Sentence: {sentence_analysis['average_words_per_sentence']}")
    
    if sentence_analysis['longest_sentence']:
        print(f"\n📏 Longest Sentence:")
        print(f"   \"{sentence_analysis['longest_sentence'][:100]}{'...' if len(sentence_analysis['longest_sentence']) > 100 else ''}\"")
    
    if sentence_analysis['shortest_sentence']:
        print(f"\n📏 Shortest Sentence:")
        print(f"   \"{sentence_analysis['shortest_sentence']}\"")

def display_readability_analysis(readability_stats):
    """Display readability analysis."""
    print_section("📖 Readability Analysis")
    
    print(f"📐 Average Word Length: {readability_stats['avg_word_length']} characters")
    print(f"🎯 Complexity Score: {readability_stats['complexity_score']}/20")
    print(f"📚 Readability Level: {readability_stats['readability_level']}")
    
    level = readability_stats['readability_level']
    if level == 'Easy':
        print("   💡 This text is easy to read and understand")
    elif level == 'Moderate':
        print("   💡 This text requires moderate reading skills")
    elif level == 'Difficult':
        print("   💡 This text is challenging and requires good reading skills")
    else:
        print("   💡 This text is very difficult and requires advanced reading skills")

def display_interesting_patterns(patterns):
    """Display interesting patterns found in the text."""
    print_section("🔍 Interesting Patterns")
    
    print(f"🎨 Word Variety: {patterns['word_variety']}% (unique words)")
    
    if patterns['repeated_words']:
        print(f"\n🔄 Most Repeated Words:")
        for word, count in patterns['repeated_words'][:5]:
            print(f"   '{word}' appears {count} times")
    
    if patterns['long_words']:
        print(f"\n📏 Long Words (7+ characters):")
        print(f"   {', '.join(patterns['long_words'][:8])}")
    
    if patterns['short_words']:
        print(f"\n🔤 Short Words (1-2 characters):")
        print(f"   {', '.join(patterns['short_words'][:10])}")

def display_complete_analysis(analysis_results):
    """Display complete text analysis in a professional format."""
    if 'error' in analysis_results:
        print(f"❌ Analysis Error: {analysis_results['error']}")
        return
    
    print_header("📊 TEXT ANALYSIS REPORT 📊")
    
    if 'general_stats' in analysis_results:
        display_general_statistics(analysis_results['general_stats'])
    
    if 'word_analysis' in analysis_results:
        display_word_analysis(analysis_results['word_analysis'])
    
    if 'sentence_analysis' in analysis_results:
        display_sentence_analysis(analysis_results['sentence_analysis'])
    
    if all(key in analysis_results for key in ['word_analysis', 'sentence_analysis']):
        word_counts = Counter(analysis_results['word_analysis']['word_frequencies'])
        text = analysis_results.get('original_text', '')
        
        readability_stats = calculate_readability_stats(
            text,
            word_counts,
            analysis_results['sentence_analysis']
        )
        display_readability_analysis(readability_stats)
        
        patterns = find_interesting_patterns(word_counts, text)
        display_interesting_patterns(patterns)
    
    print_section("✅ Analysis Complete")
    print("📝 Report generated successfully!")
    print("🎯 Ready for Module 3E: Integration & Testing")

def display_summary(analysis_results):
    """Display a quick summary of the analysis."""
    if 'error' in analysis_results:
        print(f"❌ Error: {analysis_results['error']}")
        return
    
    general = analysis_results.get('general_stats', {})
    word_analysis = analysis_results.get('word_analysis', {})
    
    print("\n" + "="*40)
    print("📊 QUICK SUMMARY")
    print("="*40)
    print(f"📄 Characters: {general.get('character_count', 0):,}")
    print(f"📝 Words: {general.get('word_count', 0):,}")
    print(f"📋 Sentences: {general.get('sentence_count', 0):,}")
    
    word_stats = word_analysis.get('statistics', {})
    print(f"🎯 Unique Words: {word_stats.get('unique_words', 0):,}")
    
    most_common = word_stats.get('most_common', [])
    if most_common:
        top_word, count = most_common[0]
        print(f"🏆 Most Common Word: '{top_word}' ({count} times)")
    
    print("="*40)

def main():
    """Main execution function - testing display and analysis."""
    print_header("Text Analyzer - Module 3D: Display Testing")
    
    # Load text file
    content = load_text_file()
    
    if not content:
        print("❌ No content to analyze")
        return
    
    print("\n🔄 Running complete analysis...")
    
    # Run complete analysis
    results = analyze_text_complete(content)
    
    if 'error' in results:
        print(f"❌ Analysis error: {results['error']}")
        return
    
    # Display results
    print("\n" + "="*60)
    print("Choose display format:")
    print("1. Complete Report")
    print("2. Quick Summary")
    print("3. Both")
    print("="*60)
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            display_complete_analysis(results)
        elif choice == "2":
            display_summary(results)
        elif choice == "3":
            display_summary(results)
            display_complete_analysis(results)
        else:
            print("Invalid choice, showing summary:")
            display_summary(results)
            
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted")
    except Exception as e:
        print(f"❌ Display error: {e}")
        display_summary(results)  # Fallback to summary

if __name__ == "__main__":
    main()
