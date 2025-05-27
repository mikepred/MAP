"""
Analysis functions for the Text Analyzer application.
These functions take processed text data and derive higher-level insights.
"""

import re
from collections import Counter
from typing import Optional, List, Dict, Tuple, Any

from . import config as cfg
from . import text_processing as tp # For functions like preprocess_text_for_sentence_analysis

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def get_word_count_stats(word_counts: Counter[str]) -> Dict[str, Any]:
    """Calculate statistics from word counts."""
    if not word_counts:
        return {
            'total_words': 0,
            'unique_words': 0,
            'most_common': [],
            'average_frequency': 0.0
        }
    
    total_words: int = sum(word_counts.values())
    unique_words: int = len(word_counts)
    most_common: List[Tuple[str, int]] = word_counts.most_common(cfg.DEFAULT_SUMMARY_MOST_COMMON_WORDS_COUNT)
    average_frequency: float = total_words / unique_words if unique_words > 0 else 0.0
    
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'most_common': most_common,
        'average_frequency': round(average_frequency, 2)
    }

def count_sentences(text: Optional[str]) -> int:
    """Count sentences in text. Assumes text is relatively clean for sentence splitting."""
    if not text:
        return 0
    
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
    
    # Use original text for sentence splitting, then clean individual sentences for word counting
    raw_sentences: List[str] = re.split(r'[.!?]+', text)
    sentences: List[str] = [s.strip() for s in raw_sentences if s.strip()]
    
    if not sentences:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0.0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    sentence_word_counts: List[int] = []
    for sentence_str in sentences:
        # Use clean_text_for_word_tokenization for word counting within sentences
        words_in_sentence: List[str] = tp.clean_text_for_word_tokenization(sentence_str, advanced=False).split()
        words_in_sentence = [word for word in words_in_sentence if len(word) > 0]
        sentence_word_counts.append(len(words_in_sentence))
    
    average_words: float = sum(sentence_word_counts) / len(sentence_word_counts) if sentence_word_counts else 0.0
    
    # Find longest and shortest sentences based on word count
    # Ensure sentence_word_counts is not empty before calling max/min
    longest_idx: int = -1
    shortest_idx: int = -1
    if sentence_word_counts:
        longest_idx = sentence_word_counts.index(max(sentence_word_counts))
        shortest_idx = sentence_word_counts.index(min(sentence_word_counts))
    
    return {
        'sentence_count': len(sentences),
        'average_words_per_sentence': round(average_words, 1),
        'longest_sentence': sentences[longest_idx].strip() if longest_idx != -1 else "",
        'shortest_sentence': sentences[shortest_idx].strip() if shortest_idx != -1 else ""
    }

def analyze_text_complete(
    text: Optional[str], 
    use_stop_words: bool = False, 
    num_common_words_to_display: int = cfg.DEFAULT_TOP_WORDS_DISPLAY
) -> Dict[str, Any]:
    """Complete text analysis pipeline."""
    if not text:
        return {
            'error': 'No text provided for analysis', 'word_analysis': {}, 
            'sentence_analysis': {}, 'general_stats': {}, 'processed_tokens': [],
            'readability_stats': {}, 'interesting_patterns': {}
        }
    
    try:
        text_for_sentence_structure: str = tp.preprocess_text_for_sentence_analysis(text)
        sentence_stats: Dict[str, Any] = analyze_sentences(text_for_sentence_structure)

        text_for_word_tokenization: str = tp.clean_text_for_word_tokenization(text, advanced=True)
        tokens_after_cleaning: List[str] = tp.tokenize_text(text_for_word_tokenization)
        
        processed_tokens: List[str]
        if use_stop_words:
            processed_tokens = tp.remove_stop_words(tokens_after_cleaning)
        else:
            processed_tokens = tokens_after_cleaning
        
        final_word_counts: Counter[str] = Counter(processed_tokens)
        word_stats: Dict[str, Any] = get_word_count_stats(final_word_counts)
        unique_words_list: List[str] = sorted(final_word_counts.keys()) if final_word_counts else []
            
        char_count: int = len(text)
        char_count_no_spaces: int = len(text.replace(' ', ''))
            
        general_stats: Dict[str, Any] = {
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'word_count': word_stats['total_words'], 
            'sentence_count': sentence_stats['sentence_count'],
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()])
        }
            
        num_to_display = max(0, num_common_words_to_display)

        readability_stats_result: Dict[str, Any] = {}
        interesting_patterns_result: Dict[str, Any] = {}
        if final_word_counts:
            readability_stats_result = calculate_readability_stats(text, final_word_counts, sentence_stats)
            interesting_patterns_result = find_interesting_patterns(final_word_counts, text)

        return {
        'word_analysis': {
            'word_frequencies': dict(final_word_counts.most_common(num_to_display)),
            'statistics': word_stats, 
            'unique_words_sample': unique_words_list[:cfg.DEFAULT_UNIQUE_WORDS_SAMPLE_DISPLAY_LIMIT],
            'full_word_counts_obj': final_word_counts 
        },
        'processed_tokens': processed_tokens, 
            'sentence_analysis': sentence_stats,
            'general_stats': general_stats,
            'original_text': text, # Useful for some analyses or display
            'readability_stats': readability_stats_result,
            'interesting_patterns': interesting_patterns_result
        }
        
    except Exception as e:
        return {
            'error': f'Analysis failed: {type(e).__name__} - {str(e)}', # Added type of exception
            'word_analysis': {}, 
            'sentence_analysis': {}, 'general_stats': {}, 'processed_tokens': [],
            'readability_stats': {}, 'interesting_patterns': {}
        }

def analyze_word_lengths(tokens: List[str]) -> Counter[int]:
    """Analyzes the distribution of word lengths.""" # Print statements removed, display is separate
    if not tokens:
        return Counter()
    return Counter(len(word) for word in tokens)

def calculate_readability_stats(text: str, word_counts: Counter[str], sentence_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate readability and complexity statistics."""
    if not text or not word_counts:
        return {'avg_word_length': 0.0, 'complexity_score': 0.0, 'readability_level': 'Unknown'}
    
    total_chars_in_counted_words: int = sum(len(word) * count for word, count in word_counts.items())
    total_counted_words: int = sum(word_counts.values())
    avg_word_length: float = total_chars_in_counted_words / total_counted_words if total_counted_words > 0 else 0.0
    
    avg_sentence_length: float = sentence_analysis.get('average_words_per_sentence', 0.0)
    complexity_score: float = (avg_word_length * 0.6) + (avg_sentence_length * 0.4)
    
    readability_level: str
    if complexity_score < 8: readability_level = 'Easy'
    elif complexity_score < 12: readability_level = 'Moderate'
    elif complexity_score < 16: readability_level = 'Difficult'
    else: readability_level = 'Very Difficult'
    
    return {
        'avg_word_length': round(avg_word_length, 1),
        'complexity_score': round(complexity_score, 1),
        'readability_level': readability_level
    }

def find_interesting_patterns(word_counts: Counter[str], text: str) -> Dict[str, Any]:
    """Find interesting patterns in the text. 'text' param kept for potential future use."""
    patterns: Dict[str, Any] = {
        'repeated_words': [], 'long_words': [], 'short_words': [], 'word_variety': 0.0
    }
    if not word_counts: return patterns
    
    patterns['repeated_words'] = [(word, count) for word, count in word_counts.most_common(cfg.DEFAULT_PATTERNS_REPEATED_WORDS_COUNT) if count > 1]
    patterns['long_words'] = [word for word in word_counts.keys() if len(word) >= 7][:cfg.DEFAULT_PATTERNS_LONG_WORDS_SAMPLE_SIZE]
    patterns['short_words'] = [word for word in word_counts.keys() if len(word) <= 2][:cfg.DEFAULT_PATTERNS_SHORT_WORDS_SAMPLE_SIZE]
    
    total_words: int = sum(word_counts.values())
    unique_words_count: int = len(word_counts)
    patterns['word_variety'] = round(unique_words_count / total_words * 100, 1) if total_words > 0 else 0.0
    
    return patterns

# time_function is a utility, might fit better in a utils.py or remain in main if only used there.
# For now, let's assume it's more of a general utility or debugging tool.
# If it's primarily for debugging/dev, it might not need its own module.
# Let's keep it in analyzer.py for now, or move to a new utils.py later.
