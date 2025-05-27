"""
Core text processing functions for the Text Analyzer application.
Includes cleaning, tokenization, stop word removal, and word counting.
"""

import re
import string
from collections import Counter
from typing import Optional, List

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
        # Example for optional number removal based on a hypothetical config flag
        # if cfg.REMOVE_NUMBERS_DURING_ADVANCED_CLEANING: # Assuming such a flag exists in config
        #     processed_text = cfg.NUMBERS_REGEX.sub('', processed_text)
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

def remove_stop_words(tokens: List[str]) -> List[str]:
    """
    Removes common stop words from a list of tokens.
    """
    original_token_count: int = len(tokens)
    filtered_tokens: List[str] = [token for token in tokens if token not in cfg.STOP_WORDS]
    removed_count: int = original_token_count - len(filtered_tokens)
    if removed_count > 0:
        print(f"ℹ️ Removed {removed_count} stop words.")
    return filtered_tokens

def count_words(text: Optional[str], use_stop_words: bool = False) -> Counter[str]:
    """
    Count word frequencies in text.
    Uses clean_text_for_word_tokenization for cleaning.
    """
    if not text:
        return Counter()
    
    # Use clean_text_for_word_tokenization (advanced=False for basic punctuation removal)
    # The 'advanced' flag in clean_text_for_word_tokenization handles URL/email removal.
    # For simple word counting, we usually want basic cleaning (lowercase, punctuation).
    # If advanced cleaning (URL/email removal) is desired before counting, 
    # it should be applied to 'text' before passing to this function, or this function
    # needs to be aware of that option.
    # For now, assuming 'clean_text_for_word_tokenization' with advanced=False is suitable for word counting.
    cleaned_text: str = clean_text_for_word_tokenization(text, advanced=False) 
    
    words: List[str] = tokenize_text(cleaned_text) # tokenize_text handles empty strings from split
    # words = [word for word in words if len(word) > 0] # tokenize_text should already handle this by text.split() behavior

    if use_stop_words:
        words = remove_stop_words(words)
        
    word_counts: Counter[str] = Counter(words)
    return word_counts
