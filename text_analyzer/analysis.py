"""
Analysis functions for the Text Analyzer application.
These functions take processed text data and derive higher-level insights.
"""

import re
from collections import Counter, defaultdict
from typing import Optional, List, Dict, Tuple, Any, Set, Iterable # Added Set and Iterable

from . import config as cfg
from . import text_processing as tp 

import spacy
import textstat
from rake_nltk import Rake
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# =============================================================================
# GLOBAL MODEL INITIALIZATIONS
# =============================================================================
_nlp_model = None
SPACY_MODEL_NAME = 'en_core_web_sm'

def _get_nlp_model():
    """Loads and caches the spaCy model."""
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load(SPACY_MODEL_NAME)
        except OSError:
            print(f"spaCy '{SPACY_MODEL_NAME}' model not found. Please download it by running:")
            print(f"    python -m spacy download {SPACY_MODEL_NAME}")
            print("Part-of-Speech (POS) tagging and Named Entity Recognition (NER) will be unavailable.")
            # Return None to indicate failure, error handled in analysis functions
            return None
        except Exception as e:
            print(f"An unexpected error occurred while loading the spaCy model: {e}")
            # Return None to indicate failure, error handled in analysis functions
            return None
    return _nlp_model

try:
    _vader_analyzer = SentimentIntensityAnalyzer()
except LookupError:
    print("VADER lexicon not found. Please download it using: python -m nltk.downloader vader_lexicon")
    _vader_analyzer = None

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

# Illustrative example for processing text chunks for word counts
def _process_chunks_for_word_counts_example(text_chunk_iterator: Iterable[str],
                                            active_stop_words: Optional[Set[str]] = None) -> Counter[str]:
    """
    Example function to demonstrate processing an iterator of text chunks
    to incrementally build a word count.

    Args:
        text_chunk_iterator: An iterator yielding strings (text chunks).
        active_stop_words: An optional set of stop words to remove.

    Returns:
        A Counter object with word frequencies.
    """
    final_word_counts = Counter()

    for i, chunk in enumerate(text_chunk_iterator):
        print(f"Processing chunk {i+1} for word counts...")

        # 1. Clean the chunk for word tokenization
        # (Mimicking part of analyze_text_complete's preprocessing)
        text_for_tokenization_chunk = tp.clean_text_for_word_tokenization(chunk, advanced=True)

        # 2. Tokenize the cleaned chunk
        tokens_in_chunk = tp.tokenize_text(text_for_tokenization_chunk)

        # 3. Remove stop words from chunk tokens (if applicable)
        processed_tokens_chunk: List[str]
        if active_stop_words:
            processed_tokens_chunk, _ = tp.remove_stop_words(tokens_in_chunk, active_stop_words)
        else:
            processed_tokens_chunk = tokens_in_chunk

        # 4. Update the main counter
        final_word_counts.update(processed_tokens_chunk)

    print(f"Finished processing all chunks. Total unique words: {len(final_word_counts)}")
    return final_word_counts

# Example usage (conceptual):
#
# from .file_io import read_file_in_chunks # Assuming this import
#
# filepath_to_process = "path/to/large_file.txt"
# try:
#   chunk_iterator = read_file_in_chunks(filepath_to_process)
#   # Assuming `current_stop_words` is defined elsewhere (e.g., from config or user input)
#   word_counts_from_chunks = _process_chunks_for_word_counts_example(chunk_iterator, active_stop_words=current_stop_words)
#   # Now `word_counts_from_chunks` can be used, e.g., passed to get_word_count_stats
#   stats = get_word_count_stats(word_counts_from_chunks)
#   print(stats)
# except FileNotFoundError:
#   print(f"Example error: File {filepath_to_process} not found.")
# except Exception as e:
#   print(f"Example error: {e}")


def get_word_count_stats(word_counts: Counter[str]) -> Dict[str, Any]:
    if not word_counts:
        return {'total_words': 0, 'unique_words': 0, 'most_common': [], 'average_frequency': 0.0}
    total_words: int = sum(word_counts.values())
    unique_words: int = len(word_counts)
    most_common: List[Tuple[str, int]] = word_counts.most_common(cfg.DEFAULT_SUMMARY_MOST_COMMON_WORDS_COUNT)
    average_frequency: float = total_words / unique_words if unique_words else 0.0
    return {'total_words': total_words, 'unique_words': unique_words, 'most_common': most_common, 'average_frequency': round(average_frequency, 2)}

def count_sentences(text: Optional[str]) -> int:
    if not text: return 0
    sentences: List[str] = re.split(r'[.!?]+', text)
    return len([s.strip() for s in sentences if s.strip()])

def analyze_sentences(text: Optional[str]) -> Dict[str, Any]:
    default_return = {'sentence_count': 0, 'average_words_per_sentence': 0.0, 'longest_sentence': '', 'shortest_sentence': ''}
    if not text: return default_return
    raw_sentences: List[str] = re.split(r'[.!?]+', text)
    sentences: List[str] = [s.strip() for s in raw_sentences if s.strip()]
    if not sentences: return default_return
    sentence_word_counts: List[int] = []
    for sentence_str in sentences:
        words_in_sentence: List[str] = tp.clean_text_for_word_tokenization(sentence_str, advanced=False).split()
        sentence_word_counts.append(len([word for word in words_in_sentence if word]))
    average_words: float = sum(sentence_word_counts) / len(sentence_word_counts) if sentence_word_counts else 0.0
    longest_idx: int = sentence_word_counts.index(max(sentence_word_counts)) if sentence_word_counts else -1
    shortest_idx: int = sentence_word_counts.index(min(sentence_word_counts)) if sentence_word_counts else -1
    return {
        'sentence_count': len(sentences), 
        'average_words_per_sentence': round(average_words, 1),
        'longest_sentence': sentences[longest_idx].strip() if longest_idx != -1 else "",
        'shortest_sentence': sentences[shortest_idx].strip() if shortest_idx != -1 else ""
    }

def extract_keywords_rake(text: str, num_keywords: int = cfg.DEFAULT_NUM_KEYWORDS) -> List[Tuple[str, float]]:
    if not text or not text.strip(): return []
    try:
        r = Rake()
        r.extract_keywords_from_text(text)
        ranked_phrases_with_scores = r.get_ranked_phrases_with_scores()
        return [(phrase, score) for score, phrase in ranked_phrases_with_scores[:num_keywords]]
    except Exception as e:
        print(f"❌ Error during RAKE keyword extraction: {type(e).__name__} - {e}")
        return []

def analyze_text_complete(
    text: Optional[str], 
    active_stop_words: Optional[Set[str]] = None,
    num_common_words_to_display: int = cfg.DEFAULT_TOP_WORDS_DISPLAY,
    user_patterns: Optional[List[Dict[str, str]]] = None # Added user_patterns parameter
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
    - Keyword extraction (RAKE).
    Stop words are removed if an active_stop_words set is provided and is not empty.

    Note: Term Frequency (TF) for the current document is available via 'word_analysis.full_word_counts_obj'.
    For TF-IDF (Term Frequency-Inverse Document Frequency), which measures word importance across a
    collection of documents (corpus), see the placeholder function `calculate_tfidf_scores_corpus`
    for a conceptual overview. TF-IDF is not calculated for single-document analysis.
    """
    default_pos_analysis_structure = {'pos_counts': Counter(), 'most_common_pos': [], 'total_pos_tags': 0, 'lexical_density': 0.0, 'error': None}
    default_ner_analysis_structure = {'entity_counts_by_type': Counter(), 'entities_by_type': defaultdict(list), 'total_entities': 0, 'most_common_entity_types': [], 'error': None}
    default_readability_stats_structure = {'avg_word_length': 0.0, 'complexity_score': 0.0, 'readability_level': 'Unknown', 'flesch_reading_ease': 'N/A', 'flesch_kincaid_grade': 'N/A', 'gunning_fog': 'N/A', 'smog_index': 'N/A', 'coleman_liau_index': 'N/A', 'dale_chall_readability_score': 'N/A', 'automated_readability_index': 'N/A', 'error': None}
    
    error_response_base: Dict[str, Any] = {
        'word_analysis': {}, 'sentence_analysis': {}, 'general_stats': {}, 
        'processed_tokens': [], 'readability_stats': default_readability_stats_structure.copy(), 
        'interesting_patterns': {}, 'ngram_frequencies': {}, 'sentiment_analysis': {},
        'pos_analysis': default_pos_analysis_structure.copy(),
        'ner_analysis': default_ner_analysis_structure.copy(),
        'keyword_analysis': [], 
    }

    if not text:
        return {**error_response_base, 'error': 'No text provided for analysis'}
    
    removed_stop_words_count: int = 0
    try:
        text_for_sentence_structure: str = tp.preprocess_text_for_sentence_analysis(text)
        sentence_stats: Dict[str, Any] = analyze_sentences(text_for_sentence_structure)
        sentiment_scores: Dict[str, float] = analyze_sentiment_vader(text_for_sentence_structure)
        pos_analysis_results: Dict[str, Any] = analyze_pos_tags_spacy(text_for_sentence_structure, top_n_tags=cfg.DEFAULT_POS_DISPLAY_COUNT)
        if not pos_analysis_results.get('error'):
            pos_analysis_results['lexical_density'] = calculate_lexical_density(pos_analysis_results.get('pos_counts', Counter()), pos_analysis_results.get('total_pos_tags', 0))
        else:
            pos_analysis_results['lexical_density'] = 0.0
        ner_analysis_results: Dict[str, Any] = analyze_ner_spacy(text_for_sentence_structure, top_n_entity_types=cfg.DEFAULT_NER_DISPLAY_COUNT)
        keyword_analysis_results: List[Tuple[str, float]] = extract_keywords_rake(text_for_sentence_structure, num_keywords=cfg.DEFAULT_NUM_KEYWORDS)

        text_for_word_tokenization: str = tp.clean_text_for_word_tokenization(text, advanced=True)
        tokens_after_cleaning: List[str] = tp.tokenize_text(text_for_word_tokenization)
        
        processed_tokens: List[str]
        if active_stop_words: # MODIFIED: Check active_stop_words set
            processed_tokens, removed_stop_words_count = tp.remove_stop_words(tokens_after_cleaning, active_stop_words)
        else:
            processed_tokens = tokens_after_cleaning
        
        final_word_counts: Counter[str] = Counter(processed_tokens)
        word_stats: Dict[str, Any] = get_word_count_stats(final_word_counts)
        unique_words_list: List[str] = sorted(final_word_counts.keys()) if final_word_counts else []
            
        char_count: int = len(text)
        char_count_no_spaces: int = len(text.replace(' ', ''))
            
        general_stats: Dict[str, Any] = {'character_count': char_count, 'character_count_no_spaces': char_count_no_spaces, 'word_count': word_stats['total_words'], 'sentence_count': sentence_stats['sentence_count'], 'paragraph_count': len([p for p in text.split('\n\n') if p.strip()])}
            
        num_to_display = max(0, num_common_words_to_display)
        readability_stats_result: Dict[str, Any] = default_readability_stats_structure.copy()
        interesting_patterns_result: Dict[str, Any] = {}
        
        if final_word_counts:
             readability_stats_result = calculate_readability_stats(text_for_sentence_structure, final_word_counts, sentence_stats)
             interesting_patterns_result = find_interesting_patterns(final_word_counts, text, user_patterns=user_patterns)
        elif text_for_sentence_structure:
            readability_stats_result = calculate_readability_stats(text_for_sentence_structure, final_word_counts, sentence_stats)
        
        word_length_counts_obj: Counter[int] = analyze_word_lengths(processed_tokens)
        ngram_results: Dict[str, List[Tuple[str, int]]] = {}
        if processed_tokens:
            raw_ngrams: Dict[int, List[Tuple[str, ...]]] = tp.generate_ngrams(processed_tokens, cfg.DEFAULT_NGRAM_N_VALUES)
            ngram_freq_counters: Dict[str, Counter[str]] = calculate_ngram_frequencies(raw_ngrams)
            for name, counter_obj in ngram_freq_counters.items():
                ngram_results[name] = counter_obj.most_common(cfg.DEFAULT_NGRAM_DISPLAY_COUNT)
        else:
            for n_val in cfg.DEFAULT_NGRAM_N_VALUES:
                name = calculate_ngram_frequencies({n_val: []}).get(n_val, f"{n_val}-grams")
                if n_val == 2: 
                    name = "bigrams"
                elif n_val == 3: 
                    name = "trigrams"
                ngram_results[name] = []

        return {
            'word_analysis': {'word_frequencies': dict(final_word_counts.most_common(num_to_display)), 'statistics': word_stats, 'unique_words_sample': unique_words_list[:cfg.DEFAULT_UNIQUE_WORDS_SAMPLE_DISPLAY_LIMIT], 'full_word_counts_obj': final_word_counts, 'removed_stop_words_count': removed_stop_words_count},
            'processed_tokens': processed_tokens, 'word_length_counts_obj': word_length_counts_obj,
            'sentence_analysis': sentence_stats, 'general_stats': general_stats,
            'original_text': text, 'readability_stats': readability_stats_result,
            'interesting_patterns': interesting_patterns_result, 'ngram_frequencies': ngram_results, 
            'sentiment_analysis': sentiment_scores, 'pos_analysis': pos_analysis_results,
            'ner_analysis': ner_analysis_results, 'keyword_analysis': keyword_analysis_results
        }
    except Exception as e:
        return {**error_response_base, 'error': f'Analysis failed: {type(e).__name__} - {str(e)}'}

def analyze_ner_spacy(text: str, top_n_entity_types: int = 5) -> Dict[str, Any]:
    default_return = {'entity_counts_by_type': Counter(), 'entities_by_type': defaultdict(list), 'total_entities': 0, 'most_common_entity_types': [], 'error': None}
    nlp = _get_nlp_model()
    if nlp is None:
        default_return['error'] = f"spaCy model '{SPACY_MODEL_NAME}' not available. NER unavailable."
        return default_return
    if not text or not text.strip(): default_return['error'] = "Input text is empty. NER cannot be performed."; return default_return
    try:
        doc = nlp(text)
        if not doc.ents: return default_return 
        entities_by_type_dd = defaultdict(list)
        for ent in doc.ents: entities_by_type_dd[ent.label_].append(ent.text)
        final_entities_by_type: Dict[str, List[str]] = {label: sorted(list(set(texts))) for label, texts in entities_by_type_dd.items()}
        entity_type_counts: Counter[str] = Counter(ent.label_ for ent in doc.ents)
        return {'entity_counts_by_type': entity_type_counts, 'entities_by_type': final_entities_by_type, 'total_entities': len(doc.ents), 'most_common_entity_types': entity_type_counts.most_common(top_n_entity_types), 'error': None}
    except Exception as e: default_return['error'] = f"spaCy NER processing failed: {type(e).__name__} - {str(e)}"; return default_return

def calculate_lexical_density(pos_counts: Counter[str], total_pos_tags: int) -> float:
    if total_pos_tags == 0: return 0.0
    content_word_count: int = sum(pos_counts[tag] for tag in cfg.CONTENT_POS_TAGS if tag in pos_counts)
    return round((content_word_count / total_pos_tags) * 100, 2)

def analyze_pos_tags_spacy(text: str, top_n_tags: int = 10) -> Dict[str, Any]:
    default_return = {'pos_counts': Counter(), 'most_common_pos': [], 'total_pos_tags': 0, 'lexical_density': 0.0, 'error': None}
    nlp = _get_nlp_model()
    if nlp is None:
        default_return['error'] = f"spaCy model '{SPACY_MODEL_NAME}' not available. POS tagging unavailable."
        return default_return
    if not text or not text.strip(): default_return['error'] = "Input text is empty. POS tagging cannot be performed."; return default_return
    try:
        doc = nlp(text)
        pos_tags: List[str] = [token.pos_ for token in doc if not token.is_punct and not token.is_space]
        if not pos_tags: default_return['error'] = "No valid tokens for POS tagging after filtering punctuation/spaces."; return default_return
        pos_counts: Counter[str] = Counter(pos_tags)
        return {'pos_counts': pos_counts, 'most_common_pos': pos_counts.most_common(top_n_tags), 'total_pos_tags': len(pos_tags), 'error': None}
    except Exception as e: default_return['error'] = f"spaCy POS tagging failed: {type(e).__name__} - {str(e)}"; return default_return

def analyze_sentiment_vader(text: str) -> Dict[str, float]:
    if not text or _vader_analyzer is None: return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0, 'error': 'VADER analyzer not available or empty text'}
    try: return _vader_analyzer.polarity_scores(text)
    except Exception as e: return {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0, 'error': f'VADER analysis failed: {str(e)}'}

def analyze_word_lengths(tokens: List[str]) -> Counter[int]:
    if not tokens: return Counter()
    return Counter(len(word) for word in tokens)

def calculate_readability_stats(text_for_textstat: str, word_counts: Counter[str], sentence_analysis: Dict[str, Any]) -> Dict[str, Any]:
    stats: Dict[str, Any] = {'avg_word_length': 0.0, 'complexity_score': 0.0, 'readability_level': 'Unknown', 'flesch_reading_ease': 'N/A', 'flesch_kincaid_grade': 'N/A', 'gunning_fog': 'N/A', 'smog_index': 'N/A', 'coleman_liau_index': 'N/A', 'dale_chall_readability_score': 'N/A', 'automated_readability_index': 'N/A', 'error': None}
    if word_counts and sum(word_counts.values()) > 0 :
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
    else: stats['avg_word_length'] = 0.0; stats['complexity_score'] = 0.0; stats['readability_level'] = 'N/A (Not enough data)'
    if not text_for_textstat or not text_for_textstat.strip(): stats['error'] = "Input text for textstat is empty or too short."; return stats
    textstat_functions = {'flesch_reading_ease': textstat.flesch_reading_ease, 'flesch_kincaid_grade': textstat.flesch_kincaid_grade, 'gunning_fog': textstat.gunning_fog, 'smog_index': textstat.smog_index, 'coleman_liau_index': textstat.coleman_liau_index, 'dale_chall_readability_score': textstat.dale_chall_readability_score, 'automated_readability_index': textstat.automated_readability_index}
    for key, func in textstat_functions.items():
        try: stats[key] = round(func(text_for_textstat), 2)
        except (ZeroDivisionError, Exception) as e: stats[key] = 'N/A'; stats['error'] = stats.get('error') or f"Error calculating {key}: {type(e).__name__}"
    return stats

def find_interesting_patterns(word_counts: Counter[str], text: str, user_patterns: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    patterns: Dict[str, Any] = {
        'repeated_words': [],
        'long_words': [],
        'short_words': [],
        'word_variety': 0.0,
        'common_patterns': {},
        'user_defined_pattern_results': {}
    }

    if word_counts:
        # Repeated words: .most_common() is efficient. Filter for count > 1.
        patterns['repeated_words'] = [
            (word, count) for word, count in word_counts.most_common(cfg.DEFAULT_PATTERNS_REPEATED_WORDS_COUNT) if count > 1
        ]

        # Long and short words: Iterate unique words from word_counts.keys() once.
        # cfg.MIN_LONG_WORD_LENGTH and cfg.MAX_SHORT_WORD_LENGTH should ideally be used if defined in config.
        # Using hardcoded values 7 and 2 as per original visible logic.
        min_long_len = 7  # Placeholder for cfg.MIN_LONG_WORD_LENGTH
        max_short_len = 2 # Placeholder for cfg.MAX_SHORT_WORD_LENGTH

        long_word_candidates = []
        short_word_candidates = []

        for word in word_counts.keys():
            word_len = len(word)
            if word_len >= min_long_len:
                long_word_candidates.append(word)
            if word_len <= max_short_len:
                short_word_candidates.append(word)

        # Sort candidates alphabetically, then take the sample slice.
        # This matches the "seems to sort [...] alphabetically" part of the subtask's observation,
        # assuming the length criteria are primary filters.
        # If sort by length then alphabetically is desired for the sample:
        # sorted_long_words = sorted(long_word_candidates, key=lambda w: (-len(w), w))
        # sorted_short_words = sorted(short_word_candidates, key=lambda w: (len(w), w))
        # For now, simple alphabetical sort of the candidates before slicing:

        patterns['long_words'] = sorted(long_word_candidates)[:cfg.DEFAULT_PATTERNS_LONG_WORDS_SAMPLE_SIZE]
        patterns['short_words'] = sorted(short_word_candidates)[:cfg.DEFAULT_PATTERNS_SHORT_WORDS_SAMPLE_SIZE]

        # Word Variety: calculation is efficient.
        total_words: int = sum(word_counts.values())
        unique_words_count: int = len(word_counts) # Number of unique words
        patterns['word_variety'] = round(unique_words_count / total_words * 100, 1) if total_words else 0.0

    # Regex pattern matching (remains unchanged as it operates on 'text', not 'word_counts')
    if text:
        for pattern_name, regex_str in cfg.COMMON_PATTERNS.items():
            try: patterns['common_patterns'][pattern_name] = re.compile(regex_str).findall(text)[:cfg.DEFAULT_PATTERN_MATCH_LIMIT]
            except re.error as e: patterns['common_patterns'][pattern_name] = {'error': f"Invalid regex: {str(e)}"}
    if text and user_patterns:
        for user_pattern_dict in user_patterns:
            pattern_name = user_pattern_dict.get('name'); regex_str = user_pattern_dict.get('regex')
            if not pattern_name or not regex_str: patterns['user_defined_pattern_results'][f"UnnamedPattern_{len(patterns['user_defined_pattern_results'])}"] = {'error': 'Pattern name or regex string missing.'}; continue
            try: patterns['user_defined_pattern_results'][pattern_name] = re.compile(regex_str).findall(text)[:cfg.DEFAULT_PATTERN_MATCH_LIMIT]
            except re.error as e: patterns['user_defined_pattern_results'][pattern_name] = {'error': f"Invalid regex: {str(e)}"}
            except Exception as e: patterns['user_defined_pattern_results'][pattern_name] = {'error': f"Unexpected error processing pattern: {str(e)}"}
    return patterns

def get_sentences_for_word(text_content: str, word: str) -> List[str]:
    if not text_content or not word: return []
    sentences: List[str] = [s.strip() for s in re.split(r'[.!?]+', text_content) if s.strip()]
    found_sentences: List[str] = []
    try: word_regex = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    except re.error: return [] 
    for sentence in sentences:
        if word_regex.search(sentence): found_sentences.append(sentence + '.')
    return found_sentences

def calculate_ngram_frequencies(ngrams_data: Dict[int, List[Tuple[str, ...]]]) -> Dict[str, Counter[str]]:
    ngram_frequencies: Dict[str, Counter[str]] = {}
    n_value_to_name_map: Dict[int, str] = {1: "unigrams", 2: "bigrams", 3: "trigrams", 4: "quadgrams", 5: "pentagrams"}
    for n_value, ngram_list in ngrams_data.items():
        if not ngram_list: continue
        string_ngrams: List[str] = [" ".join(ngram_tuple) for ngram_tuple in ngram_list]
        descriptive_name: str = n_value_to_name_map.get(n_value, f"{n_value}-grams")
        ngram_frequencies[descriptive_name] = Counter(string_ngrams)
    return ngram_frequencies

def calculate_tfidf_scores_corpus(corpus_texts: List[str]) -> None:
    raise NotImplementedError("This function is a placeholder for corpus-level TF-IDF analysis.")
