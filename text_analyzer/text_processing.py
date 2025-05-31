"""
Core text processing functions for the Text Analyzer application.
Includes cleaning, tokenization, stop word removal, and word counting.
"""

import re
import string
from collections import Counter
from typing import Optional, List, Tuple, Set # MODIFIED: Added Set

from . import config as cfg

# =============================================================================
# TEXT PROCESSING FUNCTIONS (Originally Module 3C / Enhanced in 4B & 4C)
# =============================================================================

def preprocess_text_for_sentence_analysis(text: Optional[str]) -> str:
    """
    Lightly clean and preprocess text, preserving sentence structures for analysis.
    (Formerly clean_text_for_sentence_analysis)
    """
    if not text or not isinstance(text, str):
        return ""
    
    cleaned_text: str = text.lower()
    cleaned_text = ' '.join(cleaned_text.split()) # Normalize whitespace
    # Uses SENTENCE_STRUCTURE_PRESERVE_CLEAN_REGEX from config
    cleaned_text = cfg.SENTENCE_STRUCTURE_PRESERVE_CLEAN_REGEX.sub('', cleaned_text)
    
    return cleaned_text

def clean_text_for_word_tokenization(text: Optional[str], advanced: bool = False) -> str:
    """
    Converts text to lowercase and removes ALL punctuation for word tokenization.
    If advanced is True, also removes URLs, emails. Number removal is optional via config.
    (Formerly clean_text)
    
    Args:
        text (Optional[str]): Input text
        advanced (bool): Flag to enable advanced cleaning (URLs, emails)
        
    Returns:
        str: Cleaned text suitable for word tokenization
    """
    if text is None:
        return ""
    
    processed_text: str = text.lower()
    
    if advanced:
        processed_text = cfg.URL_REGEX.sub('', processed_text)
        processed_text = cfg.EMAIL_REGEX.sub('', processed_text)
        processed_text = cfg.EXTRA_WHITESPACE_REGEX.sub(' ', processed_text).strip()
    
    translator = str.maketrans('', '', string.punctuation)
    processed_text = processed_text.translate(translator)
    
    processed_text = cfg.EXTRA_WHITESPACE_REGEX.sub(' ', processed_text).strip()
    
    return processed_text

def tokenize_text(text: Optional[str]) -> List[str]:
    """Splits text into a list of words (tokens)."""
    if not text:
        return []
    return text.split()

def remove_stop_words(tokens: List[str], active_stop_words: Set[str]) -> Tuple[List[str], int]:
    """
    Removes stop words from a list of tokens using the provided set of active stop words.
    If active_stop_words is empty, no words are removed.

    Args:
        tokens (List[str]): The list of tokens to filter.
        active_stop_words (Set[str]): The set of stop words to remove. 
                                     An empty set means no stop words will be removed.

    Returns:
        Tuple[List[str], int]: A tuple containing the filtered list of tokens
                               and the count of removed stop words.
    """
    original_token_count: int = len(tokens)
    if not active_stop_words: # Handles empty set; None should be handled by caller if that's a state.
        return tokens, 0
    
    filtered_tokens: List[str] = [token for token in tokens if token not in active_stop_words]
    removed_count: int = original_token_count - len(filtered_tokens)
    return filtered_tokens, removed_count

def count_words(text: Optional[str], active_stop_words: Optional[Set[str]] = None) -> Counter[str]:
    """
    Count word frequencies in text.
    Uses clean_text_for_word_tokenization for cleaning.
    Stop words are removed if an active_stop_words set is provided and is not empty.

    Args:
        text (Optional[str]): Input text.
        active_stop_words (Optional[Set[str]]): A set of stop words to remove.
                                                 If None or empty, no stop words are removed.
    Returns:
        Counter[str]: A Counter object with word frequencies.
    """
    if not text:
        return Counter()
    
    cleaned_text: str = clean_text_for_word_tokenization(text, advanced=False) 
    words: List[str] = tokenize_text(cleaned_text)

    if active_stop_words: # If the set is provided and not empty
        words, _ = remove_stop_words(words, active_stop_words)
        
    word_counts: Counter[str] = Counter(words)
    return word_counts

# =============================================================================
# N-GRAM PROCESSING FUNCTIONS (New for Module 4C)
# =============================================================================

from nltk.util import ngrams as nltk_ngrams # Use a more specific import alias

def generate_ngrams(tokens: List[str], n_values: List[int]) -> dict[int, List[Tuple[str, ...]]]:
    """
    Generates n-grams for a list of tokens for specified n-values.

    Args:
        tokens (List[str]): A list of text tokens.
        n_values (List[int]): A list of integers specifying the desired n-gram sizes (e.g., [2, 3] for bigrams and trigrams).

    Returns:
        dict[int, List[Tuple[str, ...]]]: A dictionary where keys are the n-values
        and values are lists of the corresponding n-gram tuples.
        Returns an empty list for an n-value if the number of tokens is less than n.
    """
    if not tokens or not n_values:
        return {}

    output_ngrams: dict[int, List[Tuple[str, ...]]] = {}
    for n in n_values:
        if n <= 0:
            output_ngrams[n] = []
            continue
        if len(tokens) < n:
            output_ngrams[n] = []
        else:
            output_ngrams[n] = list(nltk_ngrams(tokens, n))
            
    return output_ngrams

# =============================================================================
# TYPO CORRECTION FUNCTIONS (New for Module 4D - or whichever module it is)
# =============================================================================

from spellchecker import SpellChecker

def correct_text_typos(text: Optional[str]) -> str:
    """
    Corrects typographical errors in a given text using the `spellchecker` library.

    The function splits the input text into words and attempts to find a correction
    for each word. If a word is misspelled and a correction is found, the
    corrected word is used. If the word is correctly spelled, or if no correction
    can be determined (e.g., it's a very unusual word or not in the dictionary),
    the original word is retained. This ensures that the function does not erroneously
    change correctly spelled unique words or proper nouns not in its dictionary.

    Punctuation attached to words (e.g., "word," or "sentence!") is generally
    handled correctly by the spellchecker, meaning the punctuation will be preserved
    with the corrected word.

    Args:
        text (Optional[str]): The input text to correct.
                              Returns an empty string if text is None or empty.

    Returns:
        str: The text with identified typos corrected. If no typos are found or
             no corrections can be made, the original text (or its equivalent
             after splitting and joining) is returned.
    """
    if not text:
        return ""

    spell = SpellChecker()
    words = text.split()

    corrected_word_list = []
    for word in words:
        if not word:
            corrected_word_list.append("")
            continue
        
        potential_correction = spell.correction(word)

        if potential_correction is None:
            corrected_word_list.append(word)
        else:
            corrected_word_list.append(potential_correction)

    return " ".join(corrected_word_list)
