"""
Configuration constants for the Text Analyzer application.
"""

import re
from pathlib import Path
from typing import Set

# =============================================================================
# MODULE-LEVEL CONSTANTS
# =============================================================================
MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB
MAX_INPUT_ATTEMPTS: int = 3
DEFAULT_TOP_WORDS_DISPLAY: int = 10
PREVIEW_LENGTH: int = 100

# Path constants
# __file__ in config.py will point to config.py itself.
# .parent will give the directory containing config.py (text_analyzer)
SCRIPT_DIRECTORY: Path = Path(__file__).resolve().parent
DEFAULT_SAMPLE_FILENAME: str = "sample.txt" # Relative to script directory
DEFAULT_RESULTS_FILENAME: str = "analysis_results.txt" # Relative to CWD or script dir depending on usage
# Construct full default path for sample.txt, assuming it's in the same dir as the script
DEFAULT_SAMPLE_FILEPATH: Path = SCRIPT_DIRECTORY / DEFAULT_SAMPLE_FILENAME

# Fixed target file for automatic analysis
FIXED_TARGET_FILENAME: str = "../dict-sample.txt"
FIXED_TARGET_FILEPATH: Path = SCRIPT_DIRECTORY / FIXED_TARGET_FILENAME

# Stop words set
STOP_WORDS: Set[str] = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
    'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
    'her', 'us', 'them', 'n'
}

# Pre-compiled Regular Expressions for performance
URL_REGEX: re.Pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
EMAIL_REGEX: re.Pattern = re.compile(r'\S+@\S+')
NUMBERS_REGEX: re.Pattern = re.compile(r'\d+') # Optional, if number removal is desired
EXTRA_WHITESPACE_REGEX: re.Pattern = re.compile(r'\s+')
# For clean_text_for_sentence_analysis (will be renamed):
# This regex aims to remove characters NOT typically part of words or basic sentence structure,
# while preserving common punctuation used in sentences.
SENTENCE_STRUCTURE_PRESERVE_CLEAN_REGEX: re.Pattern = re.compile(r'[^\w\s.,!?;:\'-]')

# Constants for analysis and display (related to item #9)
DEFAULT_SUMMARY_MOST_COMMON_WORDS_COUNT: int = 5 # For get_word_count_stats summary
DEFAULT_PATTERNS_REPEATED_WORDS_COUNT: int = 10 # For find_interesting_patterns
DEFAULT_PATTERNS_LONG_WORDS_SAMPLE_SIZE: int = 10
DEFAULT_PATTERNS_SHORT_WORDS_SAMPLE_SIZE: int = 10
DEFAULT_DISPLAY_REPEATED_WORDS_LIMIT: int = 5 # For display_interesting_patterns
DEFAULT_DISPLAY_LONG_WORDS_LIMIT: int = 8
DEFAULT_DISPLAY_SHORT_WORDS_LIMIT: int = 10
DEFAULT_UNIQUE_WORDS_SAMPLE_DISPLAY_LIMIT: int = 10 # For analyze_text_complete unique_words_sample

# Constants for N-gram analysis (New for Module 4C)
DEFAULT_NGRAM_N_VALUES: list[int] = [2, 3]  # Calculate bigrams and trigrams by default
DEFAULT_NGRAM_DISPLAY_COUNT: int = 10      # Number of most common N-grams to display/store

# Constants for POS Tagging and NER (New for Modules 4E, 4F, 4H)
CONTENT_POS_TAGS: Set[str] = {'NOUN', 'VERB', 'ADJ', 'ADV'} # POS tags considered as content words for lexical density
DEFAULT_POS_DISPLAY_COUNT: int = 10        # Number of most common POS tags to display
DEFAULT_NER_DISPLAY_COUNT: int = 5         # Number of most common NER entity types to display with examples
