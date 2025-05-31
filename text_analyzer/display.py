"""
Display functions for the Text Analyzer application.
These functions handle the presentation of analysis results to the user.
"""

import matplotlib
matplotlib.use('Agg') # Use Agg backend for non-interactive environments to save files
import matplotlib.pyplot as plt
import os # For path operations when saving plots
from pathlib import Path # For path operations when saving plots
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
    
    if stats.get('sentence_count') and stats.get('word_count'):
        words_per_sentence: float = stats['word_count'] / stats['sentence_count']
        print(f"📏 Average Words per Sentence: {words_per_sentence:.1f}")

def display_word_analysis(word_analysis_data: Dict[str, Any]) -> None:
    print_section("🔤 Word Frequency Analysis")
    word_frequencies: Dict[str, int] = word_analysis_data.get('word_frequencies', {})
    statistics: Dict[str, Any] = word_analysis_data.get('statistics', {})
    print(f"🎯 Unique Words: {statistics.get('unique_words', 0):,}")
    print(f"📊 Total Word Count (in analysis): {statistics.get('total_words', 0):,}")
    if word_frequencies and statistics.get('total_words'):
        print(f"\n🏆 Top {len(word_frequencies)} Most Common Words:")
        for i, (word, count) in enumerate(word_frequencies.items(), 1):
            percentage: float = (count / statistics['total_words']) * 100
            print(f"  {i:2d}. '{word}' - {count} times ({percentage:.1f}%)")
    elif not word_frequencies:
        print("No word frequencies to display (perhaps all words were stop words or file was empty after cleaning).")

def display_sentence_analysis(sentence_analysis_data: Dict[str, Any]) -> None:
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

def display_readability_analysis(readability_stats_data: Dict[str, Any]) -> None:
    print_section("📖 Readability Analysis")
    print(f"📐 Average Word Length (of analyzed words): {readability_stats_data.get('avg_word_length',0.0)} characters")
    print(f"🎯 Complexity Score: {readability_stats_data.get('complexity_score',0.0)}")
    print(f"📚 Readability Level: {readability_stats_data.get('readability_level','Unknown')}")
    level: Optional[str] = readability_stats_data.get('readability_level')
    if level == 'Easy': print("   💡 This text is easy to read and understand.")
    elif level == 'Moderate': print("   💡 This text requires moderate reading skills.")
    elif level == 'Difficult': print("   💡 This text is challenging and requires good reading skills.")
    elif level == 'Very Difficult': print("   💡 This text is very difficult and requires advanced reading skills.")
    elif level and "N/A" in level: print(f"   💡 Custom readability level could not be determined due to: {level.replace('N/A (', '').replace(')', '')}")
    else: print("   💡 Readability level could not be determined.")
    print("\n  Standardized Readability Indices:")
    indices_to_display = {
        "flesch_reading_ease": "Flesch Reading Ease", "flesch_kincaid_grade": "Flesch-Kincaid Grade Level",
        "gunning_fog": "Gunning Fog Index", "smog_index": "SMOG Index",
        "coleman_liau_index": "Coleman-Liau Index", "dale_chall_readability_score": "Dale-Chall Readability Score",
        "automated_readability_index": "Automated Readability Index (ARI)"
    }
    error_message = readability_stats_data.get('error')
    if error_message:
        print(f"    Note on Standardized Indices: {error_message}")
    all_na = True
    for key, name in indices_to_display.items():
        score = readability_stats_data.get(key, 'N/A')
        print(f"    - {name}: {score}")
        if score != 'N/A': all_na = False
    if all_na and not error_message:
        print("    (All standardized indices are N/A, possibly due to short or unsuitable text.)")

def display_interesting_patterns(patterns_data: Dict[str, Any]) -> None:
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

    # Display User-Defined Patterns
    user_defined_results = patterns_data.get('user_defined_pattern_results', {})
    if user_defined_results:
        print_section("🎨 User-Defined Patterns", width=len("🎨 User-Defined Patterns")) # Adjusted width for shorter title
        for pattern_name, matches_or_error in user_defined_results.items():
            print(f"\n  🔹 Pattern: '{pattern_name}'")
            if isinstance(matches_or_error, dict) and 'error' in matches_or_error:
                print(f"     Error: {matches_or_error['error']}")
            elif isinstance(matches_or_error, list):
                if matches_or_error:
                    print(f"     Found {len(matches_or_error)} match(es) (up to {cfg.DEFAULT_PATTERN_MATCH_LIMIT} displayed):")
                    for match_item in matches_or_error:
                        print(f"       - \"{match_item}\"")
                else:
                    print("     No matches found.")
            else: # Should not happen if analysis.py formats correctly
                print(f"     Unexpected result format for this pattern: {matches_or_error}")

    # Display Common (Built-in) Regex Patterns
    common_pattern_results = patterns_data.get('common_patterns', {})
    if common_pattern_results:
        print_section("🔗 Common Regex Pattern Matches", width=len("🔗 Common Regex Pattern Matches"))
        has_common_matches = False
        for pattern_name, matches_or_error in common_pattern_results.items():
            print(f"\n  🔸 Pattern: '{pattern_name}'")
            if isinstance(matches_or_error, dict) and 'error' in matches_or_error:
                 print(f"     Error: {matches_or_error['error']}")
                 has_common_matches = True # Count error message as something displayed
            elif isinstance(matches_or_error, list) and matches_or_error:
                has_common_matches = True
                print(f"     Found {len(matches_or_error)} match(es) (up to {cfg.DEFAULT_PATTERN_MATCH_LIMIT} displayed):")
                for match_item in matches_or_error:
                    print(f"       - \"{match_item}\"")
            elif not matches_or_error: # Empty list
                pass # Optionally print "No matches found." or just skip for cleaner output if many are empty
        if not has_common_matches:
            print("    No matches found for any common patterns or patterns had errors.")


def display_word_length_analysis(length_counts: Counter[int], total_tokens: int) -> None:
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
    if 'error' in analysis_results and analysis_results['error']:
        print(f"❌ Analysis Error: {analysis_results['error']}")
        return
    print_header("📊 TEXT ANALYSIS REPORT 📊")
    if 'general_stats' in analysis_results: display_general_statistics(analysis_results['general_stats'])
    if 'word_analysis' in analysis_results: display_word_analysis(analysis_results['word_analysis'])
    if 'sentence_analysis' in analysis_results: display_sentence_analysis(analysis_results['sentence_analysis'])
    readability_stats_data = analysis_results.get('readability_stats', {})
    if readability_stats_data: display_readability_analysis(readability_stats_data)
    else: print("\nℹ️ Readability stats not available.")
    patterns_data = analysis_results.get('interesting_patterns', {})
    if patterns_data: display_interesting_patterns(patterns_data)
    else: print("\nℹ️ Interesting patterns not available.")
    word_length_counts = analysis_results.get('word_length_counts_obj')
    total_processed_tokens = len(analysis_results.get('processed_tokens', []))
    if word_length_counts and total_processed_tokens > 0:
         display_word_length_analysis(word_length_counts, total_processed_tokens)
    else: print("\nℹ️ Word length analysis data not available.")
    ngram_data = analysis_results.get('ngram_frequencies', {})
    if ngram_data: display_ngram_frequencies(ngram_data)
    else:
        print_section("📊 N-gram Frequencies")
        print("N-gram data not available or not calculated.")
    sentiment_data = analysis_results.get('sentiment_analysis', {})
    display_sentiment_analysis(sentiment_data)
    pos_data = analysis_results.get('pos_analysis', {})
    display_pos_analysis(pos_data)
    ner_data = analysis_results.get('ner_analysis', {})
    display_ner_analysis(ner_data)
    keyword_data = analysis_results.get('keyword_analysis', []) # Added for RAKE
    display_keyword_analysis(keyword_data) # Added for RAKE
    print_section("✅ Analysis Complete")
    print("📝 Report generated successfully!")

# =============================================================================
# NAMED ENTITY RECOGNITION (NER) DISPLAY FUNCTIONS (New for Module 4F)
# =============================================================================
def display_ner_analysis(ner_data: Dict[str, Any]) -> None:
    print_section("🌍 Named Entity Recognition (NER) Analysis (spaCy)")
    if not ner_data: print("NER analysis data not available."); return
    if 'error' in ner_data and ner_data['error']: print(f"Error in NER analysis: {ner_data['error']}"); return
    total_entities: int = ner_data.get('total_entities', 0)
    if total_entities == 0: print("No named entities found."); return
    print(f"Total Named Entity Mentions Found: {total_entities:,}")
    most_common_entity_types: List[Tuple[str, int]] = ner_data.get('most_common_entity_types', [])
    if most_common_entity_types:
        print("\nMost Common Entity Types:")
        entities_by_type: Dict[str, List[str]] = ner_data.get('entities_by_type', {})
        for i, (entity_type, count) in enumerate(most_common_entity_types, 1):
            examples = entities_by_type.get(entity_type, [])
            example_str = ""
            if examples:
                display_examples = [ex[:30] + '...' if len(ex) > 30 else ex for ex in examples[:3]]
                example_str = f" (e.g., {', '.join(display_examples)})"
            print(f"  {i:2d}. {entity_type}: {count} mentions{example_str}")
    else: print("No common entity types to display.")

# =============================================================================
# PART-OF-SPEECH (POS) TAGGING DISPLAY FUNCTIONS (New for Module 4E)
# =============================================================================
def display_pos_analysis(pos_data: Dict[str, Any]) -> None:
    print_section("🏷️ Part-of-Speech (POS) Tag Analysis (spaCy)")
    if not pos_data: print("POS analysis data not available."); return
    if 'error' in pos_data and pos_data['error']: print(f"Error in POS analysis: {pos_data['error']}"); return
    total_pos_tags: int = pos_data.get('total_pos_tags', 0)
    if total_pos_tags == 0: print("No POS tags found or text was too short after filtering."); return
    print(f"Total POS Tags (excluding punctuation/spaces): {total_pos_tags:,}")
    most_common_pos: List[Tuple[str, int]] = pos_data.get('most_common_pos', [])
    if most_common_pos:
        print("\nMost Common POS Tags:")
        for i, (tag, count) in enumerate(most_common_pos, 1):
            percentage: float = (count / total_pos_tags) * 100 if total_pos_tags > 0 else 0
            print(f"  {i:2d}. {tag}: {count} times ({percentage:.1f}%)")
    else: print("No common POS tags to display.")
    lexical_density_score = pos_data.get('lexical_density')
    if lexical_density_score is not None:
        print(f"\nLexical Density: {lexical_density_score:.2f}% (Percentage of content words)")

# =============================================================================
# KEYWORD EXTRACTION DISPLAY FUNCTIONS (New for RAKE)
# =============================================================================
def display_keyword_analysis(keyword_data: List[Tuple[str, float]]) -> None:
    """
    Displays extracted keywords and their scores.

    Args:
        keyword_data (List[Tuple[str, float]]): A list of (keyword_phrase, score) tuples.
    """
    print_section("🔑 Keyword Extraction (RAKE)")
    if not keyword_data:
        print("No keywords extracted or an error occurred during extraction.")
        return
    
    print("Top Extracted Keywords/Keyphrases (Score):")
    for i, (phrase, score) in enumerate(keyword_data, 1):
        print(f"  {i:2d}. \"{phrase}\" (Score: {score:.2f})")

# =============================================================================
# SENTIMENT ANALYSIS DISPLAY FUNCTIONS (New for Module 4D)
# =============================================================================
def display_sentiment_analysis(sentiment_scores: Dict[str, float]) -> None:
    print_section("💖 Sentiment Analysis (VADER)")
    if not sentiment_scores or 'compound' not in sentiment_scores or 'error' in sentiment_scores:
        error_message = sentiment_scores.get('error', 'Sentiment analysis data not available or not applicable.')
        print(error_message); return
    neg_score = sentiment_scores.get('neg', 0.0)
    neu_score = sentiment_scores.get('neu', 0.0)
    pos_score = sentiment_scores.get('pos', 0.0)
    compound_score = sentiment_scores.get('compound', 0.0)
    print(f"  Negative Score: {neg_score:.3f}")
    print(f"  Neutral Score:  {neu_score:.3f}")
    print(f"  Positive Score: {pos_score:.3f}")
    print(f"  Compound Score: {compound_score:.3f}")
    overall_sentiment: str
    if compound_score >= 0.05: overall_sentiment = "Positive"
    elif compound_score <= -0.05: overall_sentiment = "Negative"
    else: overall_sentiment = "Neutral"
    print(f"\n  Overall Sentiment: {overall_sentiment}")
    print("  (Interpretation based on VADER's compound score thresholds)")

# =============================================================================
# N-GRAM DISPLAY FUNCTIONS (New for Module 4C)
# =============================================================================
def display_ngram_frequencies(ngram_data: Dict[str, List[Tuple[str, int]]]) -> None:
    if not ngram_data: print_section("📊 N-gram Frequencies"); print("No N-gram data to display."); return
    for ngram_type, ngrams_list in ngram_data.items():
        title = f"{ngram_type.capitalize()} Frequencies"
        print_section(f"📊 {title}")
        if ngrams_list:
            for i, (ngram, count) in enumerate(ngrams_list, 1):
                print(f"  {i:2d}. '{ngram}' - {count} times")
        else: print(f"No {ngram_type.lower()} found.")

def display_summary(analysis_results: Dict[str, Any]) -> None:
    if 'error' in analysis_results and analysis_results['error']: print(f"❌ Error: {analysis_results['error']}"); return
    general: Dict[str, Any] = analysis_results.get('general_stats', {})
    word_analysis_data: Dict[str, Any] = analysis_results.get('word_analysis', {})
    stats: Dict[str, Any] = word_analysis_data.get('statistics', {}) 
    print("\n" + "="*40); print("📊 QUICK SUMMARY"); print("="*40)
# =============================================================================
# PLOTTING FUNCTIONS (New for Graphical Output)
# =============================================================================

def plot_word_frequencies(
    word_counts: Counter, 
    top_n: int = 10, 
    output_dir: Path = cfg.SCRIPT_DIRECTORY, 
    filename_prefix: str = "word_frequencies"
) -> Optional[str]:
    if not word_counts: print("ℹ️ No word frequency data to plot."); return None
    most_common_words = word_counts.most_common(top_n)
    if not most_common_words: print("ℹ️ No words to plot after filtering for top_n."); return None
    words, counts = zip(*most_common_words)
    try:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(words, counts, color=cfg.DEFAULT_PLOT_COLOR)
        plt.xlabel("Words"); plt.ylabel("Frequency"); plt.title(f"Top {top_n} Most Common Words")
        plt.xticks(rotation=45, ha="right"); plt.tight_layout()
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.05 * max(counts), int(yval), va='bottom', ha='center')
        if not output_dir.exists(): output_dir.mkdir(parents=True, exist_ok=True)
        plot_filename = f"{filename_prefix}_top_{top_n}.png"
        save_path = output_dir / plot_filename
        plt.savefig(save_path); plt.close()
        print(f"✅ Word frequency plot saved to: {save_path}")
        return str(save_path)
    except Exception as e: print(f"❌ Error generating word frequency plot: {type(e).__name__} - {e}"); return None

def plot_sentiment_distribution(
    sentiment_scores: Dict[str, float], 
    output_dir: Path = cfg.SCRIPT_DIRECTORY, 
    filename_prefix: str = "sentiment_distribution"
) -> Optional[str]:
    if not sentiment_scores or not all(k in sentiment_scores for k in ['neg', 'neu', 'pos']):
        print("ℹ️ Insufficient sentiment data to plot (missing neg, neu, or pos scores)."); return None
    labels = ['Negative', 'Neutral', 'Positive']
    scores = [sentiment_scores.get('neg', 0.0), sentiment_scores.get('neu', 0.0), sentiment_scores.get('pos', 0.0)]
    colors = [cfg.SENTIMENT_PLOT_COLORS.get('negative', 'red'), 
              cfg.SENTIMENT_PLOT_COLORS.get('neutral', 'lightgray'), 
              cfg.SENTIMENT_PLOT_COLORS.get('positive', 'green')]
    try:
        plt.figure(figsize=(8, 6))
        bars = plt.bar(labels, scores, color=colors)
        plt.xlabel("Sentiment"); plt.ylabel("Score (VADER)"); plt.title("Sentiment Score Distribution")
        plt.ylim(0, 1)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.3f}", va='bottom', ha='center')
        if not output_dir.exists(): output_dir.mkdir(parents=True, exist_ok=True)
        plot_filename = f"{filename_prefix}.png"
        save_path = output_dir / plot_filename
        plt.savefig(save_path); plt.close()
        print(f"✅ Sentiment distribution plot saved to: {save_path}")
        return str(save_path)
    except Exception as e: print(f"❌ Error generating sentiment distribution plot: {type(e).__name__} - {e}"); return None

def plot_word_length_distribution(
    length_counts: Counter, 
    output_dir: Path = cfg.SCRIPT_DIRECTORY, 
    filename_prefix: str = "word_length_dist"
) -> Optional[str]:
    if not length_counts: print("ℹ️ No word length data to plot."); return None
    sorted_lengths = sorted(length_counts.keys())
    counts = [length_counts[length] for length in sorted_lengths]
    labels = [str(length) for length in sorted_lengths]
    try:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, counts, color=cfg.DEFAULT_PLOT_COLOR)
        plt.xlabel("Word Length (Number of Characters)"); plt.ylabel("Number of Words")
        plt.title("Word Length Distribution"); plt.tight_layout()
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.05 * max(counts), int(yval), va='bottom', ha='center')
        if not output_dir.exists(): output_dir.mkdir(parents=True, exist_ok=True)
        plot_filename = f"{filename_prefix}.png"
        save_path = output_dir / plot_filename
        plt.savefig(save_path); plt.close()
        print(f"✅ Word length distribution plot saved to: {save_path}")
        return str(save_path)
    except Exception as e: print(f"❌ Error generating word length distribution plot: {type(e).__name__} - {e}"); return None

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
# WORD CLOUD GENERATION (New for Word Cloud Feature)
# =============================================================================
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    # print("⚠️ WordCloud library not found. Word cloud generation will be unavailable.")
    # print("   To install: pip install wordcloud")

def generate_word_cloud(
    word_frequencies: Counter,
    output_dir: Path,
    filename_prefix: str = "word_cloud"
) -> Optional[str]:
    """
    Generates a word cloud image from word frequencies and saves it.

    Args:
        word_frequencies (Counter): A Counter object with word frequencies.
        output_dir (Path): The directory to save the generated image.
        filename_prefix (str): The prefix for the output image filename.

    Returns:
        Optional[str]: The path to the saved image file if successful, else None.
    """
    if not WORDCLOUD_AVAILABLE:
        print("❌ WordCloud library is not installed. Cannot generate word cloud.")
        return None

    if not word_frequencies:
        print("ℹ️ Word frequencies are empty. Cannot generate word cloud.")
        return None

    try:
        wc = WordCloud(width=800, height=400, background_color='white', max_words=100) # Added max_words
        wc.generate_from_frequencies(dict(word_frequencies)) # WordCloud expects a dict

        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

        image_filename = f"{filename_prefix}.png"
        save_path = output_dir / image_filename

        wc.to_file(str(save_path)) # Use WordCloud's to_file method

        # plt.figure(figsize=(10, 5)) # Not needed if using wc.to_file() directly
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis("off")
        # plt.tight_layout(pad=0)
        # plt.savefig(save_path)
        plt.close('all') # Close any figures plt might have opened or WordCloud might have used.
                        # Using 'all' ensures all figures are closed.

        print(f"☁️ Word cloud image saved to: {save_path}")
        return str(save_path)

    except Exception as e:
        print(f"❌ Error generating word cloud: {type(e).__name__} - {e}")
        plt.close('all') # Ensure cleanup even on error
        return None
