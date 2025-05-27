"""
Display functions for the Text Analyzer application.
These functions handle the presentation of analysis results to the user.
"""

from collections import Counter
from typing import Dict, Any, Optional, List, Tuple

from . import config as cfg
# analysis.py will be needed if display functions call analysis functions directly,
# but it seems they mostly take pre-calculated results.
# However, display_complete_analysis might call some analysis functions if not all data is pre-passed.
# For now, let's assume results are passed in. If not, we'll add `from . import analysis`.

# =============================================================================
# DISPLAY FUNCTIONS (Originally Module 3D / Enhanced in 4C)
# =============================================================================

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

def display_word_analysis(word_analysis_data: Dict[str, Any]) -> None: # Renamed param for clarity
    """Display word frequency analysis."""
    print_section("🔤 Word Frequency Analysis")
    
    word_frequencies: Dict[str, int] = word_analysis_data.get('word_frequencies', {})
    statistics: Dict[str, Any] = word_analysis_data.get('statistics', {})
    
    print(f"🎯 Unique Words: {statistics.get('unique_words', 0):,}")
    print(f"📊 Total Word Count (in analysis): {statistics.get('total_words', 0):,}")
    
    if word_frequencies and statistics.get('total_words', 0) > 0:
        print(f"\n🏆 Top {len(word_frequencies)} Most Common Words:")
        for i, (word, count) in enumerate(word_frequencies.items(), 1):
            percentage: float = (count / statistics['total_words']) * 100
            print(f"  {i:2d}. '{word}' - {count} times ({percentage:.1f}%)")
    elif not word_frequencies:
        print("No word frequencies to display (perhaps all words were stop words or file was empty after cleaning).")

def display_sentence_analysis(sentence_analysis_data: Dict[str, Any]) -> None: # Renamed param
    """Display sentence analysis results."""
    print_section("📋 Sentence Analysis")
    
    print(f"📊 Total Sentences: {sentence_analysis_data.get('sentence_count',0)}")
    print(f"📏 Average Words per Sentence: {sentence_analysis_data.get('average_words_per_sentence',0.0)}")
    
    longest: str = sentence_analysis_data.get('longest_sentence', '')
    if longest:
        print(f"\n📏 Longest Sentence:")
        print(f"   \"{longest[:cfg.PREVIEW_LENGTH]}{'...' if len(longest) > cfg.PREVIEW_LENGTH else ''}\"")
    
    shortest: str = sentence_analysis_data.get('shortest_sentence', '')
    if shortest:
        print(f"\n📏 Shortest Sentence:")
        print(f"   \"{shortest}\"")

def display_readability_analysis(readability_stats_data: Dict[str, Any]) -> None: # Renamed param
    """Display readability analysis."""
    print_section("📖 Readability Analysis")
    
    print(f"📐 Average Word Length (of analyzed words): {readability_stats_data.get('avg_word_length',0.0)} characters")
    print(f"🎯 Complexity Score: {readability_stats_data.get('complexity_score',0.0)}")
    print(f"📚 Readability Level: {readability_stats_data.get('readability_level','Unknown')}")
    
    level: Optional[str] = readability_stats_data.get('readability_level')
    # ... (interpretation print statements as before)
    if level == 'Easy': print("   💡 This text is easy to read and understand.")
    elif level == 'Moderate': print("   💡 This text requires moderate reading skills.")
    elif level == 'Difficult': print("   💡 This text is challenging and requires good reading skills.")
    elif level == 'Very Difficult': print("   💡 This text is very difficult and requires advanced reading skills.")
    else: print("   💡 Readability level could not be determined.")

def display_interesting_patterns(patterns_data: Dict[str, Any]) -> None: # Renamed param
    """Display interesting patterns found in the text."""
    print_section("🔍 Interesting Patterns")
    
    print(f"🎨 Word Variety (analyzed words): {patterns_data.get('word_variety',0.0)}% (unique words / total analyzed words)")
    
    repeated: List[Tuple[str, int]] = patterns_data.get('repeated_words', [])
    if repeated:
        print(f"\n🔄 Most Repeated Words (among analyzed):")
        for word, count in repeated[:cfg.DEFAULT_DISPLAY_REPEATED_WORDS_LIMIT]:
            print(f"   '{word}' appears {count} times")
    
    long_w: List[str] = patterns_data.get('long_words', [])
    if long_w:
        print(f"\n📏 Long Words (7+ characters, among analyzed):")
        print(f"   {', '.join(long_w[:cfg.DEFAULT_DISPLAY_LONG_WORDS_LIMIT])}")
    
    short_w: List[str] = patterns_data.get('short_words', [])
    if short_w:
        print(f"\n🔤 Short Words (1-2 characters, among analyzed):")
        print(f"   {', '.join(short_w[:cfg.DEFAULT_DISPLAY_SHORT_WORDS_LIMIT])}")

def display_word_length_analysis(length_counts: Counter[int], total_tokens: int) -> None:
    """Displays the distribution of word lengths."""
    if not length_counts or total_tokens == 0:
        print("\nℹ️ No word length data to display.")
        return

    print("\n--- Word Length Analysis ---")
    for length_val in sorted(length_counts.keys()):
        count: int = length_counts[length_val]
        percentage: float = (count / total_tokens) * 100
        print(f"{length_val:2d} letter(s): {count:4d} words ({percentage:5.1f}%)")
    
    avg_length: float = sum(l * c for l, c in length_counts.items()) / total_tokens
    print(f"\nAverage word length: {avg_length:.1f} letters")
    print("--------------------------")

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
    
    # Display readability and patterns if available
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
    
    # Display word length analysis
    # Requires 'processed_tokens' to be available in analysis_results to get total_tokens
    # and 'word_analysis.full_word_counts_obj' for length_counts (or pass processed_tokens to analyze_word_lengths)
    # Let's assume 'analysis.analyze_word_lengths' returns the Counter, and we pass total tokens.
    # This part will need adjustment based on what analyze_word_lengths in analysis.py returns.
    # For now, assuming word_length_counts_obj and total_processed_tokens are in results.
    word_length_counts = analysis_results.get('word_length_counts_obj') # This key needs to be added to analyze_text_complete results
    total_processed_tokens = len(analysis_results.get('processed_tokens', []))
    if word_length_counts and total_processed_tokens > 0:
         display_word_length_analysis(word_length_counts, total_processed_tokens)
    else:
         print("\nℹ️ Word length analysis data not available.")

    print_section("✅ Analysis Complete")
    print("📝 Report generated successfully!")

def display_summary(analysis_results: Dict[str, Any]) -> None:
    """Display a quick summary of the analysis."""
    if 'error' in analysis_results and analysis_results['error']:
        print(f"❌ Error: {analysis_results['error']}")
        return
    
    general: Dict[str, Any] = analysis_results.get('general_stats', {})
    word_analysis_data: Dict[str, Any] = analysis_results.get('word_analysis', {}) # Renamed
    stats: Dict[str, Any] = word_analysis_data.get('statistics', {}) 
    
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
