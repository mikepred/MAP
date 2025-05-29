"""
Analysis functions for the Text Analyzer application.
These functions take processed text data and derive higher-level insights.
"""

import re
from collections import Counter
from typing import Optional, List, Dict, Tuple, Any

from . import config as cfg
from . import text_processing as tp # For functions like preprocess_text_for_sentence_analysis

import spacy # New import for spaCy
import textstat # New import for Readability (Module 4G)

# =============================================================================
# GLOBAL MODEL INITIALIZATIONS
# =============================================================================

# spaCy model loading (New for Module 4E - POS Tagging)
NLP_SPACY = None
SPACY_MODEL_NAME = 'en_core_web_sm'
try:
    NLP_SPACY = spacy.load(SPACY_MODEL_NAME)
except OSError:
    print(f"spaCy '{SPACY_MODEL_NAME}' model not found. Please download it by running:")
    print(f"    python -m spacy download {SPACY_MODEL_NAME}")
    print("Part-of-Speech (POS) tagging will be unavailable.")
# If NLP_SPACY remains None, dependent functions should handle it gracefully.

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
    average_frequency: float = total_words / unique_words if unique_words else 0.0 # Simplified: truthiness of unique_words
    
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
        words_in_sentence = [word for word in words_in_sentence if word] # Simplified: if word (non-empty string)
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
from collections import defaultdict # New import for NER

# =============================================================================
# GLOBAL MODEL INITIALIZATIONS
# =============================================================================

# spaCy model loading (New for Module 4E - POS Tagging)
NLP_SPACY = None
SPACY_MODEL_NAME = 'en_core_web_sm'
try:
    NLP_SPACY = spacy.load(SPACY_MODEL_NAME)
except OSError:
    print(f"spaCy '{SPACY_MODEL_NAME}' model not found. Please download it by running:")
    print(f"    python -m spacy download {SPACY_MODEL_NAME}")
    print("Part-of-Speech (POS) tagging and Named Entity Recognition (NER) will be unavailable.")
# If NLP_SPACY remains None, dependent functions should handle it gracefully.

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
    average_frequency: float = total_words / unique_words if unique_words else 0.0 # Simplified: truthiness of unique_words
    
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
        words_in_sentence = [word for word in words_in_sentence if word] # Simplified: if word (non-empty string)
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
    """
    Complete text analysis pipeline.

    This function orchestrates the entire text analysis process, including:
    - Text preprocessing (cleaning, tokenization).
    - Basic statistics (word counts, sentence counts, character counts).
    - Word frequency analysis.
    - N-gram frequency analysis (bigrams, trigrams).
    - Sentence structure analysis (longest/shortest sentences, average words per sentence).
    - Readability assessment (custom score and standard indices via textstat).
    - Sentiment analysis (VADER).
    - Part-of-Speech (POS) tagging and Lexical Density (spaCy).
    - Named Entity Recognition (NER) (spaCy).
    - Interesting pattern detection.

    Note: Term Frequency (TF) for the current document is available via 'word_analysis.full_word_counts_obj'.
    For TF-IDF (Term Frequency-Inverse Document Frequency), which measures word importance across a
    collection of documents (corpus), see the placeholder function `calculate_tfidf_scores_corpus`
    for a conceptual overview. TF-IDF is not calculated for single-document analysis.
    """
    # Initialize the basic structure of the error response
    default_pos_analysis_structure = {
        'pos_counts': Counter(), 
        'most_common_pos': [], 
        'total_pos_tags': 0, 
        'lexical_density': 0.0, # Added for lexical density
        'error': None
    }
    default_ner_analysis_structure = {
        'entity_counts_by_type': Counter(), 
        'entities_by_type': defaultdict(list), 
        'total_entities': 0, 
        'most_common_entity_types': [], 
        'error': None
    }
    # Default structure for readability_stats including new textstat keys
    default_readability_stats_structure = {
        'avg_word_length': 0.0, 'complexity_score': 0.0, 'readability_level': 'Unknown',
        'flesch_reading_ease': 'N/A', 'flesch_kincaid_grade': 'N/A',
        'gunning_fog': 'N/A', 'smog_index': 'N/A', 'coleman_liau_index': 'N/A',
        'dale_chall_readability_score': 'N/A', 'automated_readability_index': 'N/A',
        'error': None # To capture any general error during readability calculation
    }
    error_response_base: Dict[str, Any] = {
        'word_analysis': {}, 
        'sentence_analysis': {}, 
        'general_stats': {}, 
        'processed_tokens': [],
        'readability_stats': default_readability_stats_structure.copy(), 
        'interesting_patterns': {},
        'ngram_frequencies': {}, 
        'sentiment_analysis': {},
        'pos_analysis': default_pos_analysis_structure.copy(),
        'ner_analysis': default_ner_analysis_structure.copy()
    }

    if not text: # If no text, return error with all keys initialized
        return {**error_response_base, 'error': 'No text provided for analysis'}
    
    removed_stop_words_count: int = 0  # Initialize count
    try:
        # Preprocess text once for sentence-based analyses (VADER, sentence_stats)
        # VADER benefits from punctuation, so use text processed lightly.
        text_for_sentence_structure: str = tp.preprocess_text_for_sentence_analysis(text)
        
        sentence_stats: Dict[str, Any] = analyze_sentences(text_for_sentence_structure)
        
        # Sentiment analysis using VADER (New for Module 4D)
        # Use text_for_sentence_structure as it preserves punctuation.
        sentiment_scores: Dict[str, float] = analyze_sentiment_vader(text_for_sentence_structure)

        # Part-of-Speech Tagging using spaCy (New for Module 4E)
        # Use text_for_sentence_structure for POS tagging as well.
        # Using cfg.DEFAULT_POS_DISPLAY_COUNT for top_n_tags.
        pos_analysis_results: Dict[str, Any] = analyze_pos_tags_spacy(
            text_for_sentence_structure, 
            top_n_tags=cfg.DEFAULT_POS_DISPLAY_COUNT 
        )
        
        # Calculate lexical density using results from POS tagging (New for Module 4H)
        if not pos_analysis_results.get('error'): # Only calculate if POS tagging was successful
            current_pos_counts = pos_analysis_results.get('pos_counts', Counter())
            current_total_tags = pos_analysis_results.get('total_pos_tags', 0)
            lexical_density_score = calculate_lexical_density(current_pos_counts, current_total_tags)
            pos_analysis_results['lexical_density'] = lexical_density_score
        else:
            # Ensure lexical_density is present even if POS tagging failed before this step
            pos_analysis_results['lexical_density'] = 0.0

        # Named Entity Recognition using spaCy (New for Module 4F)
        # Using cfg.DEFAULT_NER_DISPLAY_COUNT for top_n_entity_types.
        ner_analysis_results: Dict[str, Any] = analyze_ner_spacy(
            text_for_sentence_structure,
            top_n_entity_types=cfg.DEFAULT_NER_DISPLAY_COUNT
        )

        text_for_word_tokenization: str = tp.clean_text_for_word_tokenization(text, advanced=True)
        tokens_after_cleaning: List[str] = tp.tokenize_text(text_for_word_tokenization)
        
        processed_tokens: List[str]
        if use_stop_words:
            # remove_stop_words now returns (filtered_tokens, count)
            processed_tokens, removed_stop_words_count = tp.remove_stop_words(tokens_after_cleaning)
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

        readability_stats_result: Dict[str, Any] = default_readability_stats_structure.copy() # Initialize with defaults
        interesting_patterns_result: Dict[str, Any] = {}
        
        # Readability stats are calculated using 'text_for_sentence_structure' for textstat,
        # and 'final_word_counts', 'sentence_stats' for custom/derived metrics.
        # The original `text` variable in `analyze_text_complete` is the raw input.
        # `text_for_sentence_structure` is `tp.preprocess_text_for_sentence_analysis(text)`
        # This is suitable for textstat.
        if final_word_counts: # Ensure there are words to analyze for custom stats
             readability_stats_result = calculate_readability_stats(
                 text_for_sentence_structure, # Use lightly processed text for textstat
                 final_word_counts, 
                 sentence_stats
             )
             interesting_patterns_result = find_interesting_patterns(final_word_counts, text)
        elif text_for_sentence_structure: # Still attempt textstat if text_for_sentence_structure is available
            readability_stats_result = calculate_readability_stats(
                 text_for_sentence_structure, # Use lightly processed text for textstat
                 final_word_counts, # This will be empty, handled by calculate_readability_stats
                 sentence_stats # This might have some values
             )
        
        # Calculate word length counts using the processed tokens
        word_length_counts_obj: Counter[int] = analyze_word_lengths(processed_tokens)

        # N-gram analysis (New for Module 4C integration)
        ngram_results: Dict[str, List[Tuple[str, int]]] = {}
        if processed_tokens: # Only proceed if there are tokens
            # Use DEFAULT_NGRAM_N_VALUES from cfg
            raw_ngrams: Dict[int, List[Tuple[str, ...]]] = tp.generate_ngrams(
                processed_tokens, 
                cfg.DEFAULT_NGRAM_N_VALUES
            )
            ngram_freq_counters: Dict[str, Counter[str]] = calculate_ngram_frequencies(raw_ngrams)
            
            for name, counter_obj in ngram_freq_counters.items():
                # Use DEFAULT_NGRAM_DISPLAY_COUNT from cfg
                ngram_results[name] = counter_obj.most_common(cfg.DEFAULT_NGRAM_DISPLAY_COUNT)
        else: # Ensure structure exists even if no tokens
            for n_val in cfg.DEFAULT_NGRAM_N_VALUES:
                name = calculate_ngram_frequencies({n_val: []}).get(n_val, f"{n_val}-grams") # Get descriptive name
                # A bit of a workaround to get the name mapping from calculate_ngram_frequencies
                # For a more robust way, the n_value_to_name_map could be a shared utility or part of config
                if n_val == 2: name = "bigrams" # Manual override for common cases if needed
                if n_val == 3: name = "trigrams"
                ngram_results[name] = []


        return {
            'word_analysis': {
                'word_frequencies': dict(final_word_counts.most_common(num_to_display)),
                'statistics': word_stats, 
                'unique_words_sample': unique_words_list[:cfg.DEFAULT_UNIQUE_WORDS_SAMPLE_DISPLAY_LIMIT],
                'full_word_counts_obj': final_word_counts,
                'removed_stop_words_count': removed_stop_words_count
            },
            'processed_tokens': processed_tokens, 
            'word_length_counts_obj': word_length_counts_obj,
            'sentence_analysis': sentence_stats,
            'general_stats': general_stats,
            'original_text': text, 
            'readability_stats': readability_stats_result,
            'interesting_patterns': interesting_patterns_result,
            'ngram_frequencies': ngram_results, 
            'sentiment_analysis': sentiment_scores,
            'pos_analysis': pos_analysis_results,
            'ner_analysis': ner_analysis_results # Add NER analysis results here
        }
        
    except Exception as e:
        # Ensure all keys are present in the error response
        return {
            **error_response_base, # This includes ngram, sentiment, pos, and ner_analysis
            'error': f'Analysis failed: {type(e).__name__} - {str(e)}',
        }

# =============================================================================
# NAMED ENTITY RECOGNITION (NER) FUNCTIONS (New for Module 4F)
# =============================================================================

def analyze_ner_spacy(text: str, top_n_entity_types: int = 5) -> Dict[str, Any]:
    """
    Analyzes Named Entities of the text using spaCy.

    Args:
        text (str): The input text (preferably lightly cleaned, preserving sentence structure).
        top_n_entity_types (int): The number of most common entity types to return.

    Returns:
        Dict[str, Any]: A dictionary containing:
            'entity_counts_by_type': collections.Counter of entity type frequencies.
            'entities_by_type': Dict mapping entity type to a list of unique entity texts.
            'total_entities': Total number of entity mentions found.
            'most_common_entity_types': List of top N (entity_type, count) tuples.
            'error': An error message string if spaCy model is not available or text is empty, else None.
    """
    # Initialize default structure for return, especially for error cases
    default_return = {
        'entity_counts_by_type': Counter(),
        'entities_by_type': defaultdict(list), # Use defaultdict for easier appending
        'total_entities': 0,
        'most_common_entity_types': [],
        'error': None
    }

    if NLP_SPACY is None:
        default_return['error'] = "spaCy model not loaded. NER unavailable."
        return default_return
    
    if not text or not text.strip():
        default_return['error'] = "Input text is empty. NER cannot be performed."
        return default_return

    try:
        doc = NLP_SPACY(text)
        
        if not doc.ents: # No entities found
            # default_return['error'] = "No named entities found in the text." # Optional: report as error or just empty results
            return default_return # Return empty structure is fine

        entities_by_type_dd = defaultdict(list)
        for ent in doc.ents:
            entities_by_type_dd[ent.label_].append(ent.text)
        
        # Convert lists of entity texts to lists of unique entity texts
        final_entities_by_type: Dict[str, List[str]] = {
            label: sorted(list(set(texts))) for label, texts in entities_by_type_dd.items()
        }

        entity_type_counts: Counter[str] = Counter(ent.label_ for ent in doc.ents)
        
        return {
            'entity_counts_by_type': entity_type_counts,
            'entities_by_type': final_entities_by_type,
            'total_entities': len(doc.ents),
            'most_common_entity_types': entity_type_counts.most_common(top_n_entity_types),
            'error': None
        }
    except Exception as e:
        default_return['error'] = f"spaCy NER processing failed: {type(e).__name__} - {str(e)}"
        return default_return

# =============================================================================
# PART-OF-SPEECH (POS) TAGGING FUNCTIONS (New for Module 4E)
# =============================================================================

# CONTENT_POS_TAGS is now defined in config.py and accessed via cfg.CONTENT_POS_TAGS

def calculate_lexical_density(pos_counts: Counter[str], total_pos_tags: int) -> float:
    """
    Calculates lexical density based on POS tag counts.
    Lexical Density = (Number of Content Words / Total Words) * 100

    Args:
        pos_counts (Counter[str]): A Counter object with POS tags as keys and their counts as values.
        total_pos_tags (int): The total number of POS tags (considered as total words for this calculation).

    Returns:
        float: The lexical density percentage, or 0.0 if total_pos_tags is 0.
    """
    if total_pos_tags == 0:
        return 0.0

    content_word_count: int = sum(pos_counts[tag] for tag in cfg.CONTENT_POS_TAGS if tag in pos_counts)
    
    density: float = (content_word_count / total_pos_tags) * 100
    return round(density, 2)


def analyze_pos_tags_spacy(text: str, top_n_tags: int = 10) -> Dict[str, Any]: # top_n_tags refers to POS tags
    """
    Analyzes Part-of-Speech (POS) tags of the text using spaCy.

    Args:
        text (str): The input text (preferably lightly cleaned, preserving sentence structure).
        top_n_tags (int): The number of most common POS tags to return.

    Returns:
        Dict[str, Any]: A dictionary containing:
            'pos_counts': collections.Counter of all POS tags found.
            'most_common_pos': List of top N (tag, count) tuples.
            'total_pos_tags': Total number of non-punctuation/non-space POS tags.
            'lexical_density': Lexical density score (added in Module 4H).
            'error': An error message string if spaCy model is not available or text is empty, else None.
    """
    # Initialize with lexical_density key
    default_return = {'pos_counts': Counter(), 'most_common_pos': [], 'total_pos_tags': 0, 'lexical_density': 0.0, 'error': None}

    if NLP_SPACY is None:
        default_return['error'] = "spaCy model not loaded. POS tagging unavailable."
        return default_return
    
    if not text or not text.strip():
        default_return['error'] = "Input text is empty. POS tagging cannot be performed."
        return default_return

    try:
        doc = NLP_SPACY(text)
        # Filter out punctuation and space tokens before getting POS tags
        pos_tags: List[str] = [token.pos_ for token in doc if not token.is_punct and not token.is_space]
        
        if not pos_tags: # If after filtering, no valid tokens for POS tagging remain
             default_return['error'] = "No valid tokens for POS tagging after filtering punctuation/spaces."
             return default_return

        pos_counts: Counter[str] = Counter(pos_tags)
        
        return {
            'pos_counts': pos_counts,
            'most_common_pos': pos_counts.most_common(top_n_tags),
            'total_pos_tags': len(pos_tags),
            'error': None
        }
    except Exception as e:
        # Catch any unexpected errors during spaCy processing
        default_return['error'] = f"spaCy POS tagging failed: {type(e).__name__} - {str(e)}"
        return default_return

# =============================================================================
# SENTIMENT ANALYSIS FUNCTIONS (New for Module 4D)
# =============================================================================
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize VADER analyzer once globally for efficiency, if thread-safety is not a concern
# For web apps or multi-threaded environments, instantiate it inside the function or use a thread-local instance.
# Given the current CLI structure, global initialization is acceptable.
try:
    _vader_analyzer = SentimentIntensityAnalyzer()
except LookupError:
    # This handles the case where vader_lexicon might not be downloaded yet.
    # The user should be instructed to download it (as per README).
    # For robustness in the code, we can create a dummy analyzer or raise a specific error.
    print("VADER lexicon not found. Please download it using: python -m nltk.downloader vader_lexicon")
    # Fallback to a dummy analyzer or handle appropriately. For now, let it raise if not found.
    # If we want to prevent crashing:
    # _vader_analyzer = None 
    # And then check in analyze_sentiment_vader if _vader_analyzer is None.
    # However, the task implies it should be available after README instructions.
    pass # Let it proceed and potentially fail later if not handled, or rely on user having run downloads


def analyze_sentiment_vader(text: str) -> Dict[str, float]:
    """
    Analyzes sentiment of the text using NLTK's VADER.

    Args:
        text (str): The input text (preferably with punctuation preserved).

    Returns:
        Dict[str, float]: A dictionary containing 'neg', 'neu', 'pos', 
                          and 'compound' sentiment scores. Returns empty if VADER fails.
    """
    if not text or _vader_analyzer is None: # Check if analyzer initialized
        return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0, 'error': 'VADER analyzer not available or empty text'}

    try:
        scores: Dict[str, float] = _vader_analyzer.polarity_scores(text)
        return scores
    except Exception as e: # Catch any other VADER specific errors
        return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0, 'error': f'VADER analysis failed: {str(e)}'}


def analyze_word_lengths(tokens: List[str]) -> Counter[int]:
    """Analyzes the distribution of word lengths.""" # Print statements removed, display is separate
    if not tokens:
        return Counter()
    return Counter(len(word) for word in tokens)

def calculate_readability_stats(text_for_textstat: str, word_counts: Counter[str], sentence_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate readability and complexity statistics, including textstat indices.
    Args:
        text_for_textstat (str): Raw or lightly processed text suitable for textstat.
        word_counts (Counter[str]): Counter of words for custom stats.
        sentence_analysis (Dict[str, Any]): Sentence analysis data for custom stats.
    Returns:
        Dict[str, Any]: Dictionary of readability scores.
    """
    
    # Initialize with default values for all scores
    stats: Dict[str, Any] = {
        'avg_word_length': 0.0, 'complexity_score': 0.0, 'readability_level': 'Unknown',
        'flesch_reading_ease': 'N/A', 'flesch_kincaid_grade': 'N/A',
        'gunning_fog': 'N/A', 'smog_index': 'N/A', 'coleman_liau_index': 'N/A',
        'dale_chall_readability_score': 'N/A', 'automated_readability_index': 'N/A',
        'error': None
    }

    # Custom calculations (avg_word_length, complexity_score, readability_level)
    # These rely on word_counts and sentence_analysis
    if word_counts and sum(word_counts.values()) > 0 : # Check if word_counts is not empty and has words
        total_chars_in_counted_words: int = sum(len(word) * count for word, count in word_counts.items())
        total_counted_words: int = sum(word_counts.values())
        avg_word_length: float = total_chars_in_counted_words / total_counted_words
        stats['avg_word_length'] = round(avg_word_length, 1)
        
        avg_sentence_length: float = sentence_analysis.get('average_words_per_sentence', 0.0)
        complexity_score: float = (avg_word_length * 0.6) + (avg_sentence_length * 0.4)
        stats['complexity_score'] = round(complexity_score, 1)
        
        if complexity_score < 8: stats['readability_level'] = 'Easy'
        elif complexity_score < 12: stats['readability_level'] = 'Moderate'
        elif complexity_score < 16: stats['readability_level'] = 'Difficult'
        else: stats['readability_level'] = 'Very Difficult'
    else: # If no words, custom scores remain at their defaults or indicate inability to calculate
        stats['avg_word_length'] = 0.0 
        stats['complexity_score'] = 0.0
        stats['readability_level'] = 'N/A (Not enough data)'


    # textstat calculations - these rely on text_for_textstat
    if not text_for_textstat or not text_for_textstat.strip():
        stats['error'] = "Input text for textstat is empty or too short."
        # Most textstat scores will remain 'N/A' as initialized
        return stats

    textstat_functions = {
        'flesch_reading_ease': textstat.flesch_reading_ease,
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade,
        'gunning_fog': textstat.gunning_fog,
        'smog_index': textstat.smog_index,
        'coleman_liau_index': textstat.coleman_liau_index,
        'dale_chall_readability_score': textstat.dale_chall_readability_score,
        'automated_readability_index': textstat.automated_readability_index
    }

    for key, func in textstat_functions.items():
        try:
            stats[key] = round(func(text_for_textstat), 2)
        except (ZeroDivisionError, Exception) as e: # Catch specific and general errors
            # print(f"Could not calculate {key} for the given text: {type(e).__name__} - {e}") # Optional: log this
            stats[key] = 'N/A' # Keep as N/A on error
            if not stats['error']: # Record first error encountered from textstat
                stats['error'] = f"Error calculating {key}: {type(e).__name__}"
                
    return stats

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
    patterns['word_variety'] = round(unique_words_count / total_words * 100, 1) if total_words else 0.0 # Simplified
    
    return patterns

# time_function is a utility, might fit better in a utils.py or remain in main if only used there.
# For now, let's assume it's more of a general utility or debugging tool.
# If it's primarily for debugging/dev, it might not need its own module.
# Let's keep it in analyzer.py for now, or move to a new utils.py later.

def get_sentences_for_word(text_content: str, word: str) -> List[str]:
    """
    Finds all sentences in text_content that contain the specified word.

    Args:
        text_content (str): The text to search within.
        word (str): The word to search for (case-insensitive, whole word).

    Returns:
        List[str]: A list of sentences containing the word. Empty if none found.
    """
    if not text_content or not word:
        return []

    # Sentences are split by '.', '!', '?'
    # Using re.split to handle multiple delimiters and keep them if needed (though here we discard them)
    # Stripping whitespace from each sentence after splitting.
    sentences: List[str] = [s.strip() for s in re.split(r'[.!?]+', text_content) if s.strip()]

    found_sentences: List[str] = []
    # Compile regex for whole word, case-insensitive search
    # \b ensures that we match whole words only (e.g., "cat" not "caterpillar")
    try:
        # Attempt to compile the regex to catch potential errors with re.escape(word) if word is unusual
        word_regex = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    except re.error:
        # Handle cases where the word might form an invalid regex even after escaping
        # This is unlikely with re.escape but good for robustness
        return [] 

    for sentence in sentences:
        if word_regex.search(sentence):
            found_sentences.append(sentence + '.') # Append period for completeness, as split removes it.
                                                 # Consider if original punctuation is preferred.
                                                 # For this example, adding '.' is a simplification.
    return found_sentences

# =============================================================================
# N-GRAM ANALYSIS FUNCTIONS (New for Module 4C)
# =============================================================================

def calculate_ngram_frequencies(ngrams_data: Dict[int, List[Tuple[str, ...]]]) -> Dict[str, Counter[str]]:
    """
    Calculates the frequency of each n-gram.

    Args:
        ngrams_data (Dict[int, List[Tuple[str, ...]]]): A dictionary where keys are n-values
                                                       and values are lists of n-gram tuples.
                                                       (Output from text_processing.generate_ngrams)

    Returns:
        Dict[str, Counter[str]]: A dictionary where keys are descriptive names (e.g., "bigrams", "trigrams")
                                 and values are Counter objects mapping string-joined n-grams to their frequencies.
    """
    ngram_frequencies: Dict[str, Counter[str]] = {}
    
    # Mapping n-values to descriptive names
    n_value_to_name_map: Dict[int, str] = {
        1: "unigrams", # Though typically not generated by generate_ngrams with n_values=[2,3]
        2: "bigrams",
        3: "trigrams",
        4: "quadgrams", # Example, can be extended
        5: "pentagrams" # Example, can be extended
        # Add more mappings as needed
    }

    for n_value, ngram_list in ngrams_data.items():
        if not ngram_list: # Skip if no n-grams for this n_value (e.g., text too short)
            continue

        # Convert list of tuples to list of strings (e.g., ("hello", "world") -> "hello world")
        # This makes them suitable for Counter keys
        string_ngrams: List[str] = [" ".join(ngram_tuple) for ngram_tuple in ngram_list]
        
        # Get the descriptive name for the current n_value, or default to "n-grams"
        descriptive_name: str = n_value_to_name_map.get(n_value, f"{n_value}-grams")
        
        ngram_frequencies[descriptive_name] = Counter(string_ngrams)
            
    return ngram_frequencies

# =============================================================================
# TF-IDF PLACEHOLDER FUNCTION (Conceptual for Module 4I)
# =============================================================================

def calculate_tfidf_scores_corpus(corpus_texts: List[str]) -> None:
    """
    Placeholder function for TF-IDF (Term Frequency-Inverse Document Frequency) calculation.
    TF-IDF is a numerical statistic that reflects how important a word is to a document
    in a collection or corpus. It is often used as a weighting factor in information
    retrieval, text mining, and user modeling.

    The TF-IDF value increases proportionally to the number of times a word appears in
    the document (TF) but is offset by the frequency of the word in the corpus (IDF).
    This helps to adjust for the fact that some words appear more frequently in general.

    - Term Frequency (TF): For the current single document analysis, the raw term
      frequencies are already available via the 'word_analysis.full_word_counts_obj'
      (a collections.Counter object) returned by `analyze_text_complete`.
      TF can be normalized, e.g., (term frequency in document) / (total terms in document).

    - Inverse Document Frequency (IDF): This measures how common or rare a word is
      across the entire corpus.
      IDF = log_e(Total documents in corpus / Number of documents with term in it).
      Calculating IDF requires having access to a corpus of multiple documents.

    - TF-IDF Score: The TF-IDF score for a term in a document is typically TF * IDF.

    If a corpus of texts were available (e.g., `corpus_texts` parameter), the steps
    to calculate TF-IDF scores would generally involve:
    1. Preprocessing each document in the corpus (cleaning, tokenization, possibly stemming).
    2. Calculating Term Frequencies (TF) for each term in each document.
    3. Calculating Inverse Document Frequency (IDF) for each term across the corpus.
       This involves counting how many documents each term appears in.
    4. Computing the TF-IDF score for each term in each document.

    Libraries like `scikit-learn` provide efficient tools like `TfidfVectorizer`
    that handle these steps for a given corpus.

    This function is a placeholder as the current application focuses on single-document
    analysis. A full TF-IDF implementation would typically return a matrix of
    TF-IDF scores (documents vs. terms) or a dictionary structure representing these scores.

    Args:
        corpus_texts (List[str]): A list of strings, where each string is the content
                                  of a document in the corpus.

    Raises:
        NotImplementedError: This function is a placeholder and not implemented.
    """
    raise NotImplementedError("This function is a placeholder for corpus-level TF-IDF analysis.")
