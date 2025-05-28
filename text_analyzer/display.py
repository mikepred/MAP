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
    
    # Simplified boolean check using truthiness of numbers for the counts
    if stats.get('sentence_count') and stats.get('word_count'):
        words_per_sentence: float = stats['word_count'] / stats['sentence_count']
        print(f"📏 Average Words per Sentence: {words_per_sentence:.1f}")

def display_word_analysis(word_analysis_data: Dict[str, Any]) -> None: # Renamed param for clarity
    """Display word frequency analysis."""
    print_section("🔤 Word Frequency Analysis")
    
    word_frequencies: Dict[str, int] = word_analysis_data.get('word_frequencies', {})
    statistics: Dict[str, Any] = word_analysis_data.get('statistics', {})
    
    print(f"🎯 Unique Words: {statistics.get('unique_words', 0):,}")
    print(f"📊 Total Word Count (in analysis): {statistics.get('total_words', 0):,}")
    
    # Simplified boolean check for statistics.get('total_words')
    if word_frequencies and statistics.get('total_words'):
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
    elif level and "N/A" in level: print(f"   💡 Custom readability level could not be determined due to: {level.replace('N/A (', '').replace(')', '')}")
    else: print("   💡 Readability level could not be determined.")

    # Display Standardized Readability Indices (New for Module 4G)
    print("\n  Standardized Readability Indices:")
    
    indices_to_display = {
        "flesch_reading_ease": "Flesch Reading Ease",
        "flesch_kincaid_grade": "Flesch-Kincaid Grade Level",
        "gunning_fog": "Gunning Fog Index",
        "smog_index": "SMOG Index",
        "coleman_liau_index": "Coleman-Liau Index",
        "dale_chall_readability_score": "Dale-Chall Readability Score",
        "automated_readability_index": "Automated Readability Index (ARI)"
    }

    error_message = readability_stats_data.get('error')
    if error_message:
        print(f"    Note on Standardized Indices: {error_message}")

    all_na = True
    for key, name in indices_to_display.items():
        score = readability_stats_data.get(key, 'N/A')
        print(f"    - {name}: {score}")
        if score != 'N/A':
            all_na = False
            
    if all_na and not error_message: # If all scores are N/A and no specific error message was already printed
        print("    (All standardized indices are N/A, possibly due to short or unsuitable text.)")


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

    # N-gram Frequencies Display (New for Module 4C)
    ngram_data = analysis_results.get('ngram_frequencies', {})
    if ngram_data: # Check if there's any ngram data to display
        display_ngram_frequencies(ngram_data)
    else:
        # Optionally print a message if no ngram_data at all (e.g. key missing or empty dict)
        # This case should ideally be handled by display_ngram_frequencies if it receives an empty dict.
        # For robustness, we can have a fallback here or ensure display_ngram_frequencies handles empty dict gracefully.
        print_section("📊 N-gram Frequencies")
        print("N-gram data not available or not calculated.")

    # Sentiment Analysis Display (New for Module 4D)
    sentiment_data = analysis_results.get('sentiment_analysis', {})
    display_sentiment_analysis(sentiment_data) # Call the new display function

    # Part-of-Speech (POS) Tagging Display (New for Module 4E)
    pos_data = analysis_results.get('pos_analysis', {})
    display_pos_analysis(pos_data) # Call the new display function for POS tags

    # Named Entity Recognition (NER) Display (New for Module 4F)
    ner_data = analysis_results.get('ner_analysis', {})
    display_ner_analysis(ner_data) # Call the new display function for NER


    print_section("✅ Analysis Complete")
    print("📝 Report generated successfully!")

# =============================================================================
# NAMED ENTITY RECOGNITION (NER) DISPLAY FUNCTIONS (New for Module 4F)
# =============================================================================

def display_ner_analysis(ner_data: Dict[str, Any]) -> None:
    """
    Displays Named Entity Recognition (NER) analysis results.

    Args:
        ner_data (Dict[str, Any]): A dictionary containing NER analysis results,
                                   e.g., {'entity_counts_by_type': Counter, 
                                          'entities_by_type': dict,
                                          'total_entities': int, 
                                          'most_common_entity_types': list,
                                          'error': str/None}.
    """
    print_section("🌍 Named Entity Recognition (NER) Analysis (spaCy)")

    if not ner_data:
        print("NER analysis data not available.")
        return

    if 'error' in ner_data and ner_data['error']:
        print(f"Error in NER analysis: {ner_data['error']}")
        return

    total_entities: int = ner_data.get('total_entities', 0)
    most_common_entity_types: List[Tuple[str, int]] = ner_data.get('most_common_entity_types', [])
    entities_by_type: Dict[str, List[str]] = ner_data.get('entities_by_type', {})

    if total_entities == 0: # This also implies most_common_entity_types would be empty
        print("No named entities found.")
        return
    
    print(f"Total Named Entity Mentions Found: {total_entities:,}")

    if most_common_entity_types:
        print("\nMost Common Entity Types:")
        for i, (entity_type, count) in enumerate(most_common_entity_types, 1):
            examples = entities_by_type.get(entity_type, [])
            example_str = ""
            if examples:
                # Take up to 3 examples, shorten them if they are too long
                display_examples = [ex[:30] + '...' if len(ex) > 30 else ex for ex in examples[:3]]
                example_str = f" (e.g., {', '.join(display_examples)})"
            
            print(f"  {i:2d}. {entity_type}: {count} mentions{example_str}")
    else:
        # This case should be covered by total_entities == 0 check, but as a fallback:
        print("No common entity types to display.")

# =============================================================================
# PART-OF-SPEECH (POS) TAGGING DISPLAY FUNCTIONS (New for Module 4E)
# =============================================================================

def display_pos_analysis(pos_data: Dict[str, Any]) -> None:
    """
    Displays Part-of-Speech (POS) analysis results.

    Args:
        pos_data (Dict[str, Any]): A dictionary containing POS analysis results,
                                   e.g., {'pos_counts': Counter, 'most_common_pos': list, 
                                          'total_pos_tags': int, 'error': str/None}.
    """
    print_section("🏷️ Part-of-Speech (POS) Tag Analysis (spaCy)")

    if not pos_data:
        print("POS analysis data not available.")
        return

    if 'error' in pos_data and pos_data['error']:
        print(f"Error in POS analysis: {pos_data['error']}")
        return

    total_pos_tags: int = pos_data.get('total_pos_tags', 0)
    most_common_pos: List[Tuple[str, int]] = pos_data.get('most_common_pos', [])

    if total_pos_tags == 0 or not most_common_pos:
        print("No POS tags found or text was too short after filtering.")
        return

    print(f"Total POS Tags (excluding punctuation/spaces): {total_pos_tags:,}")

    if most_common_pos:
        print("\nMost Common POS Tags:")
        for i, (tag, count) in enumerate(most_common_pos, 1):
            percentage: float = (count / total_pos_tags) * 100 if total_pos_tags > 0 else 0
            print(f"  {i:2d}. {tag}: {count} times ({percentage:.1f}%)")
    else:
        # This case should be covered by the check above, but as a fallback:
        print("No common POS tags to display.")

    # Display Lexical Density (New for Module 4H)
    lexical_density_score = pos_data.get('lexical_density') # Retrieve the score
    if lexical_density_score is not None: # Check if the key exists and value is not None
        print(f"\nLexical Density: {lexical_density_score:.2f}% (Percentage of content words)")
    # If lexical_density_score is None (e.g. key missing), it won't print, which is fine.
    # The calculation logic in analysis.py should ensure it's 0.0 if not calculable but POS was okay.

# =============================================================================
# SENTIMENT ANALYSIS DISPLAY FUNCTIONS (New for Module 4D)
# =============================================================================

def display_sentiment_analysis(sentiment_scores: Dict[str, float]) -> None:
    """
    Displays sentiment analysis scores and their interpretation.

    Args:
        sentiment_scores (Dict[str, float]): A dictionary with sentiment scores
                                             (e.g., {'neg': 0.1, 'neu': 0.8, 'pos': 0.1, 'compound': 0.0}).
                                             May also contain an 'error' key.
    """
    print_section("💖 Sentiment Analysis (VADER)")

    if not sentiment_scores or 'compound' not in sentiment_scores or 'error' in sentiment_scores:
        # Check for empty dict, missing 'compound' key (essential for interpretation), or an error from analysis step
        error_message = sentiment_scores.get('error', 'Sentiment analysis data not available or not applicable.')
        print(error_message)
        return

    neg_score = sentiment_scores.get('neg', 0.0)
    neu_score = sentiment_scores.get('neu', 0.0)
    pos_score = sentiment_scores.get('pos', 0.0)
    compound_score = sentiment_scores.get('compound', 0.0) # Default to 0.0 if somehow missing after check

    print(f"  Negative Score: {neg_score:.3f}")
    print(f"  Neutral Score:  {neu_score:.3f}")
    print(f"  Positive Score: {pos_score:.3f}")
    print(f"  Compound Score: {compound_score:.3f}")

    overall_sentiment: str
    if compound_score >= 0.05:
        overall_sentiment = "Positive"
    elif compound_score <= -0.05:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"
    
    print(f"\n  Overall Sentiment: {overall_sentiment}")
    print("  (Interpretation based on VADER's compound score thresholds)")

# =============================================================================
# N-GRAM DISPLAY FUNCTIONS (New for Module 4C)
# =============================================================================

def display_ngram_frequencies(ngram_data: Dict[str, List[Tuple[str, int]]]) -> None:
    """
    Displays N-gram frequencies in a formatted way.

    Args:
        ngram_data (Dict[str, List[Tuple[str, int]]]): 
            A dictionary where keys are N-gram types (e.g., "bigrams", "trigrams")
            and values are lists of (N-gram, count) tuples.
    """
    if not ngram_data:
        print_section("📊 N-gram Frequencies")
        print("No N-gram data to display.")
        return

    for ngram_type, ngrams_list in ngram_data.items():
        # Capitalize the first letter of ngram_type for the title, e.g., "Bigrams" -> "Bigram Frequencies"
        title = f"{ngram_type.capitalize()} Frequencies"
        print_section(f"📊 {title}")

        if ngrams_list:
            # Calculate total occurrences for percentage calculation, if desired
            # total_occurrences = sum(count for _, count in ngrams_list) # Uncomment if percentages are needed

            for i, (ngram, count) in enumerate(ngrams_list, 1):
                # Example: "1. 'word one' - 5 times"
                # If percentages are needed:
                # percentage = (count / total_occurrences) * 100 if total_occurrences > 0 else 0
                # print(f"  {i:2d}. '{ngram}' - {count} times ({percentage:.1f}%)")
                print(f"  {i:2d}. '{ngram}' - {count} times")
        else:
            print(f"No {ngram_type.lower()} found.")


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
