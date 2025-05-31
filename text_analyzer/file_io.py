"""
File I/O operations for the Text Analyzer application.
"""

import os
import csv 
import json 
from pathlib import Path
from typing import Union, Tuple, List, Any, Set, Optional # Added Optional
from collections import Counter

from . import config as cfg
from .text_processing import correct_text_typos # Keep this if used by read_file or other functions
from typing import Dict, Generator # Ensure Dict and Generator are imported if not already

# Added json and csv if they are not already present from previous steps
# import json # Already present
# import csv # Already present

# =============================================================================
# FILE I/O FUNCTIONS (Originally from Module 3B)
# =============================================================================

# Placeholder for the new save functions that will be defined below
def _save_results_to_txt(analysis_results: Dict[str, Any], filepath: Path) -> None:
    """Saves comprehensive analysis results to a text file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("===== TEXT ANALYSIS REPORT =====\n")

            # General Statistics
            gs = analysis_results.get('general_stats', {})
            f.write("\n--- General Statistics ---\n")
            f.write(f"Raw Character Count: {gs.get('character_count', 'N/A')}\n")
            f.write(f"Character Count (no spaces): {gs.get('character_count_no_spaces', 'N/A')}\n")
            f.write(f"Word Count (analyzed): {gs.get('word_count', 'N/A')}\n")
            f.write(f"Sentence Count: {gs.get('sentence_count', 'N/A')}\n")
            f.write(f"Paragraph Count: {gs.get('paragraph_count', 'N/A')}\n")

            wa = analysis_results.get('word_analysis', {})
            removed_sw_count = wa.get('removed_stop_words_count', 0)
            if removed_sw_count > 0 : # Only show if stop words were actually removed
                f.write(f"Stop Words Removed: {removed_sw_count}\n")

            # Word Frequencies & Statistics
            wf_dict = wa.get('word_frequencies', {}) # This is already a dict of top N
            ws = wa.get('statistics', {})
            f.write("\n--- Word Frequencies & Statistics ---\n")
            f.write(f"Unique Words (after processing): {ws.get('unique_words', 'N/A')}\n")
            f.write(f"Total Words (after processing): {ws.get('total_words', 'N/A')}\n")
            f.write(f"Average Word Frequency: {ws.get('average_frequency', 'N/A')}\n")
            if wf_dict and ws.get('total_words', 0) > 0:
                f.write(f"\nTop {len(wf_dict)} Most Common Words:\n")
                for word, count in wf_dict.items(): # Assumes wf_dict is already top N
                    percentage = (count / ws['total_words']) * 100
                    f.write(f"  '{word}': {count} times ({percentage:.1f}%)\n")
            else:
                f.write("No word frequencies to display.\n")

            # Sentence Analysis
            sa = analysis_results.get('sentence_analysis', {})
            f.write("\n--- Sentence Analysis ---\n")
            f.write(f"Average Words per Sentence: {sa.get('average_words_per_sentence', 'N/A')}\n")
            f.write(f"Longest Sentence: \"{sa.get('longest_sentence', 'N/A')}\"\n")
            f.write(f"Shortest Sentence: \"{sa.get('shortest_sentence', 'N/A')}\"\n")

            # Readability
            rs = analysis_results.get('readability_stats', {})
            f.write("\n--- Readability ---\n")
            f.write(f"Average Word Length: {rs.get('avg_word_length', 'N/A')} characters\n")
            f.write(f"Complexity Score: {rs.get('complexity_score', 'N/A')}\n")
            f.write(f"Readability Level: {rs.get('readability_level', 'N/A')}\n")
            standard_indices = {
                "flesch_reading_ease": "Flesch Reading Ease", "flesch_kincaid_grade": "Flesch-Kincaid Grade Level",
                "gunning_fog": "Gunning Fog Index", "smog_index": "SMOG Index",
                "coleman_liau_index": "Coleman-Liau Index", "dale_chall_readability_score": "Dale-Chall Readability Score",
                "automated_readability_index": "Automated Readability Index (ARI)"}
            f.write("  Standardized Readability Indices:\n")
            for key, name in standard_indices.items():
                f.write(f"    - {name}: {rs.get(key, 'N/A')}\n")
            if rs.get('error'): f.write(f"    Note on Standardized Indices: {rs['error']}\n")


            # Word Length Distribution
            wlc = analysis_results.get('word_length_counts_obj', Counter())
            f.write("\n--- Word Length Distribution ---\n")
            if wlc:
                total_words_for_lengths = sum(wlc.values())
                for length, count in sorted(wlc.items()):
                    percentage = (count / total_words_for_lengths * 100) if total_words_for_lengths > 0 else 0
                    f.write(f"Length {length}: {count} words ({percentage:.2f}%)\n")
            else:
                f.write("No word length data to display.\n")

            # Interesting Patterns
            ip = analysis_results.get('interesting_patterns', {})
            f.write("\n--- Pattern Analysis ---\n")
            f.write(f"Word Variety: {ip.get('word_variety', 'N/A')}%\n")
            f.write(f"Most Repeated Words (sample): {ip.get('repeated_words', [])}\n")
            f.write(f"Long Words (sample, >=7 chars): {ip.get('long_words', [])}\n")
            f.write(f"Short Words (sample, <=2 chars): {ip.get('short_words', [])}\n")

            user_patterns = ip.get('user_defined_pattern_results', {})
            if user_patterns:
                f.write("\n  User-Defined Patterns:\n")
                for name, matches_or_err in user_patterns.items():
                    if isinstance(matches_or_err, dict) and 'error' in matches_or_err:
                        f.write(f"    Pattern '{name}': Error - {matches_or_err['error']}\n")
                    else:
                        f.write(f"    Pattern '{name}': Found {len(matches_or_err)} - {matches_or_err}\n")

            common_patterns = ip.get('common_patterns', {})
            if common_patterns:
                f.write("\n  Common Regex Pattern Matches:\n")
                for name, matches_or_err in common_patterns.items():
                    if isinstance(matches_or_err, dict) and 'error' in matches_or_err:
                        f.write(f"    Pattern '{name}': Error - {matches_or_err['error']}\n")
                    else:
                        f.write(f"    Pattern '{name}': Found {len(matches_or_err)} - {matches_or_err}\n")


            # N-gram Frequencies
            ngram_data = analysis_results.get('ngram_frequencies', {})
            f.write("\n--- N-gram Frequencies ---\n")
            if not ngram_data:
                f.write("N-gram data not available.\n")
            else:
                for ngram_type, ngrams_list in ngram_data.items():
                    f.write(f"  {ngram_type.capitalize()}:\n")
                    if ngrams_list:
                        for ngram, count in ngrams_list:
                            f.write(f"    - \"{ngram}\": {count}\n")
                    else:
                        f.write(f"    No {ngram_type.lower()} found.\n")

            # Sentiment Analysis
            sentiment_data = analysis_results.get('sentiment_analysis', {})
            f.write("\n--- Sentiment Analysis (VADER) ---\n")
            if sentiment_data.get('error'):
                f.write(f"Error in sentiment analysis: {sentiment_data['error']}\n")
            elif not sentiment_data or 'compound' not in sentiment_data:
                f.write("Sentiment data not available or incomplete.\n")
            else:
                f.write(f"  Positive Score: {sentiment_data.get('pos', 0.0):.3f}\n")
                f.write(f"  Neutral Score: {sentiment_data.get('neu', 0.0):.3f}\n")
                f.write(f"  Negative Score: {sentiment_data.get('neg', 0.0):.3f}\n")
                f.write(f"  Compound Score: {sentiment_data.get('compound', 0.0):.3f}\n")
                compound_score = sentiment_data.get('compound', 0.0)
                overall_sentiment = "Neutral"
                if compound_score >= 0.05: overall_sentiment = "Positive"
                elif compound_score <= -0.05: overall_sentiment = "Negative"
                f.write(f"  Overall Sentiment: {overall_sentiment}\n")

            # Part-of-Speech (POS) Tagging
            pos_data = analysis_results.get('pos_analysis', {})
            f.write("\n--- Part-of-Speech (POS) Tagging (spaCy) ---\n")
            if pos_data.get('error'):
                f.write(f"Error in POS analysis: {pos_data['error']}\n")
            elif not pos_data or pos_data.get('total_pos_tags', 0) == 0:
                f.write("POS data not available or no tags found.\n")
            else:
                f.write(f"  Total POS Tags (excluding punctuation/spaces): {pos_data.get('total_pos_tags', 0):,}\n")
                if pos_data.get('most_common_pos'):
                    f.write("  Most Common POS Tags:\n")
                    for tag, count in pos_data['most_common_pos']:
                        percentage = (count / pos_data['total_pos_tags'] * 100) if pos_data['total_pos_tags'] > 0 else 0
                        f.write(f"    - {tag}: {count} ({percentage:.1f}%)\n")
                lex_density = pos_data.get('lexical_density')
                if lex_density is not None: f.write(f"  Lexical Density: {lex_density:.2f}%\n")

            # Named Entity Recognition (NER)
            ner_data = analysis_results.get('ner_analysis', {})
            f.write("\n--- Named Entity Recognition (NER) (spaCy) ---\n")
            if ner_data.get('error'):
                f.write(f"Error in NER analysis: {ner_data['error']}\n")
            elif not ner_data or ner_data.get('total_entities', 0) == 0:
                f.write("NER data not available or no entities found.\n")
            else:
                f.write(f"  Total Named Entity Mentions: {ner_data.get('total_entities', 0):,}\n")
                if ner_data.get('most_common_entity_types'):
                    f.write("  Most Common Entity Types:\n")
                    entities_by_type = ner_data.get('entities_by_type', {})
                    for entity_type, count in ner_data['most_common_entity_types']:
                        examples = entities_by_type.get(entity_type, [])
                        example_str = ""
                        if examples:
                            display_examples = [ex[:30] + '...' if len(ex) > 30 else ex for ex in examples[:3]]
                            example_str = f" (e.g., {', '.join(display_examples)})"
                        f.write(f"    - {entity_type}: {count} mentions{example_str}\n")

            # Keyword Analysis
            keyword_data = analysis_results.get('keyword_analysis', [])
            f.write("\n--- Keyword Extraction (RAKE) ---\n")
            if not keyword_data:
                f.write("No keywords extracted.\n")
            else:
                f.write("Top Extracted Keywords/Keyphrases (Score):\n")
                for i, (phrase, score) in enumerate(keyword_data, 1):
                    f.write(f"  {i:2d}. \"{phrase}\" (Score: {score:.2f})\n")

            f.write("\n\n--- Analysis Complete ---\n")
    except Exception as e: # Catch any error during file writing or data access
        # This top-level try-except in the function is good, error will be caught by the dispatcher's try-except
        raise IOError(f"Failed to write TXT report: {e}")


def _save_results_to_json(analysis_results: Dict[str, Any], filepath: Path) -> None:
    """Saves comprehensive analysis results to a JSON file."""

    # Custom serializer for objects that are not directly JSON serializable (like Counter)
    def custom_serializer(obj):
        if isinstance(obj, Counter):
            return dict(obj)
        # Add other type checks if needed, e.g., for Path objects if they creep in
        if isinstance(obj, Path):
            return str(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    try:
        # Create a deep copy to modify for serialization without altering original
        results_to_serialize = json.loads(json.dumps(analysis_results, default=custom_serializer))

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_to_serialize, f, indent=4)

    except TypeError as te: # Should be caught by custom_serializer mostly
        raise IOError(f"TypeError during JSON serialization: {te}. Check for non-standard data types.")
    except Exception as e:
        raise IOError(f"Failed to write JSON report: {e}")


def _save_results_to_csv(analysis_results: Dict[str, Any], filepath: Path) -> None:
    """Saves selected analysis results to a CSV file."""
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)

            # Section 1: General Statistics
            writer.writerow(["Section", "Metric", "Value"])
            gs = analysis_results.get('general_stats', {})
            for key, value in gs.items():
                writer.writerow(["General Statistics", key, value])
            wa_stats = analysis_results.get('word_analysis', {}).get('statistics', {})
            writer.writerow(["General Statistics", "Unique Words (processed)", wa_stats.get('unique_words', 'N/A')])
            writer.writerow(["General Statistics", "Total Words (processed)", wa_stats.get('total_words', 'N/A')])
            writer.writerow(["General Statistics", "Average Word Frequency", wa_stats.get('average_frequency', 'N/A')])
            removed_sw = analysis_results.get('word_analysis', {}).get('removed_stop_words_count', 0)
            if removed_sw > 0:
                 writer.writerow(["General Statistics", "Stop Words Removed", removed_sw])
            writer.writerow([]) # Blank row as separator

            # Section 2: Word Frequencies (Top N, as provided in 'word_frequencies')
            writer.writerow(["Section", "Word", "Count", "Percentage"])
            wf_dict = analysis_results.get('word_analysis', {}).get('word_frequencies', {}) # This is dict of top N
            total_words_for_perc = analysis_results.get('word_analysis', {}).get('statistics', {}).get('total_words', 0)
            if wf_dict and total_words_for_perc > 0:
                for word, count in wf_dict.items():
                    percentage = (count / total_words_for_perc) * 100
                    writer.writerow(["Word Frequencies", word, count, f"{percentage:.2f}%"])
            else:
                writer.writerow(["Word Frequencies", "N/A", "N/A", "N/A"])
            writer.writerow([]) # Blank row

            # Section 3: Sentiment Scores
            writer.writerow(["Section", "Sentiment Metric", "Score"])
            sentiment_data = analysis_results.get('sentiment_analysis', {})
            if sentiment_data.get('error'):
                writer.writerow(["Sentiment Analysis", "Error", sentiment_data['error']])
            elif 'compound' in sentiment_data : # Check if scores are available
                writer.writerow(["Sentiment Analysis", "Positive Score", sentiment_data.get('pos', 0.0)])
                writer.writerow(["Sentiment Analysis", "Neutral Score", sentiment_data.get('neu', 0.0)])
                writer.writerow(["Sentiment Analysis", "Negative Score", sentiment_data.get('neg', 0.0)])
                writer.writerow(["Sentiment Analysis", "Compound Score", sentiment_data.get('compound', 0.0)])
                compound_score = sentiment_data.get('compound', 0.0)
                overall_sentiment = "Neutral"
                if compound_score >= 0.05: overall_sentiment = "Positive"
                elif compound_score <= -0.05: overall_sentiment = "Negative"
                writer.writerow(["Sentiment Analysis", "Overall Sentiment", overall_sentiment])
            else:
                writer.writerow(["Sentiment Analysis", "N/A", "Data not available or incomplete"])
            writer.writerow([]) # Blank row

            # Section 4: Top N-grams (e.g., top 10 of each type, as provided)
            writer.writerow(["Section", "N-gram Type", "N-gram", "Count"])
            ngram_data = analysis_results.get('ngram_frequencies', {}) # This contains lists of top N ngrams
            if ngram_data:
                for ngram_type, ngrams_list in ngram_data.items():
                    if ngrams_list:
                        for ngram, count in ngrams_list: # Assumes ngrams_list is already top N
                            writer.writerow(["N-gram Frequencies", ngram_type.capitalize(), ngram, count])
                    else:
                        writer.writerow(["N-gram Frequencies", ngram_type.capitalize(), f"No {ngram_type.lower()} found", "N/A"])
            else:
                 writer.writerow(["N-gram Frequencies", "N/A", "No N-gram data available", "N/A"])
            writer.writerow([])

            # Add more sections as desired, e.g., Keywords, POS, NER
            # For Keywords (RAKE)
            writer.writerow(["Section", "Keyword/Keyphrase", "Score"])
            keyword_data = analysis_results.get('keyword_analysis', [])
            if keyword_data:
                for phrase, score in keyword_data: # Assumes keyword_data is already top N
                    writer.writerow(["Keyword Extraction (RAKE)", phrase, f"{score:.2f}"])
            else:
                writer.writerow(["Keyword Extraction (RAKE)", "No keywords extracted", "N/A"])
            writer.writerow([])

    except Exception as e:
        raise IOError(f"Failed to write CSV report: {e}")

# The old save_results_to_file function is now obsolete and will be removed.
# Its logic was moved into _save_results_to_txt and is handled by save_analysis_results.

# The old function definition that is now empty and slated for removal started here.
# Removing it entirely.

def save_analysis_results(analysis_results: Dict[str, Any], output_filename_str: str, format_choice: str = 'txt') -> None:
    """
    Saves the complete analysis results to a file in the specified format.

    Args:
        analysis_results (Dict[str, Any]): The comprehensive dictionary from analysis.analyze_text_complete.
        output_filename_str (str): The full path for the output file.
        format_choice (str): The desired output format ('txt', 'json', or 'csv').
    """
    output_path = Path(output_filename_str)
    try:
        if format_choice == 'txt':
            _save_results_to_txt(analysis_results, output_path)
        elif format_choice == 'json':
            _save_results_to_json(analysis_results, output_path)
        elif format_choice == 'csv':
            _save_results_to_csv(analysis_results, output_path)
        else:
            print(f"❌ Error: Unsupported save format '{format_choice}'. Defaulting to .txt")
            # Ensure the filename has .txt extension if we default
            if output_path.suffix.lower() not in ['.txt', '.json', '.csv']:
                 output_path = output_path.with_suffix('.txt') # Default to .txt if suffix is weird
            _save_results_to_txt(analysis_results, output_path) # Fallback to TXT

        print(f"✅ Analysis results successfully saved to: {output_path.resolve()}")

    except NotImplementedError: # If a save function isn't ready
        print(f"❌ Error: Saving to '{format_choice.upper()}' is not yet implemented.")
    except IOError as e:
        print(f"❌ IOError: Could not write results to '{output_path}': {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred while saving results to '{output_path}': {type(e).__name__} - {e}")


def read_file_in_chunks(filepath: Union[str, Path], chunk_size_bytes: int = 1024 * 1024) -> Generator[str, None, None]:
    """
    Reads a file in chunks (binary mode) and yields decoded string chunks.
    Default chunk size is 1MB.

    Args:
        filepath (Union[str, Path]): The path to the file.
        chunk_size_bytes (int): The size of each chunk in bytes.

    Yields:
        str: A chunk of the file content, decoded to a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If there's no permission to read the file.
        Exception: For other potential I/O errors.
    """
    try:
        file_to_read: Path = Path(filepath)
        if not file_to_read.exists():
            raise FileNotFoundError(f"File '{filepath}' not found.")
        if not file_to_read.is_file():
            raise IsADirectoryError(f"Path '{filepath}' is a directory, not a file.")

        with open(file_to_read, 'rb') as file: # Read in binary mode
            while True:
                chunk_bytes = file.read(chunk_size_bytes)
                if not chunk_bytes:
                    break
                try:
                    # Attempt to decode using UTF-8 first, then fallback to ISO-8859-1
                    yield chunk_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        yield chunk_bytes.decode('iso-8859-1')
                    except UnicodeDecodeError as ude:
                        # Log or handle chunks that cannot be decoded by either
                        print(f"⚠️ Warning: Chunk from '{filepath}' could not be decoded using UTF-8 or ISO-8859-1: {ude}")
                        # Optionally, yield a placeholder or skip the chunk
                        # yield "[undecodable chunk]"
                        continue
            print(f"✅ Successfully finished reading file in chunks: {file_to_read}")

    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found.")
        raise # Re-raise to allow calling function to handle
    except PermissionError:
        print(f"❌ Error: No permission to read file '{filepath}'.")
        raise
    except IsADirectoryError:
        print(f"❌ Error: Path '{filepath}' is a directory, not a file.")
        raise
    except Exception as e:
        print(f"❌ Unexpected error reading file '{filepath}' in chunks: {type(e).__name__} - {e}")
        raise

def validate_file_path(filename: Union[str, Path]) -> Tuple[bool, str]:
    """Validate that a file path is safe and accessible."""
    try:
        file_path: Path = Path(filename).resolve()
        
        if not file_path.exists():
            return False, f"File '{file_path}' does not exist"
        
        if not file_path.is_file():
            return False, f"'{file_path}' is not a file"
        
        # For stop word files, size limit might be different or not applicable.
        # However, for general text files, this is good.
        # We can add a parameter to skip size check if needed for specific use cases.
        # For now, applying to all.
        file_size: int = file_path.stat().st_size
        if file_size > cfg.MAX_FILE_SIZE_BYTES: # General max file size
            # Specific check for stop word files if we want a smaller limit for them
            # if filename.suffix.lower() == '.txt' and "stopwords" in filename.name.lower():
            #     if file_size > SOME_SMALLER_LIMIT_FOR_STOPWORDS:
            #         return False, "Stop word file too large"
            # else: (the general check)
            return False, f"File too large ({file_size} bytes). Maximum: {cfg.MAX_FILE_SIZE_BYTES} bytes"
        
        return True, "File validation passed"
        
    except Exception as e:
        return False, f"Error validating file '{filename}': {type(e).__name__} - {e}"

def read_file(filename: Union[str, Path]) -> str:
    """
    Read text from a file with comprehensive error handling.
    Currently reads the entire file content at once.
    Typo correction is applied to the full content.
    """
    # Example of how one might use the chunking generator if downstream processing supported it:
    #
    # from . import text_processing as tp # Assuming text_processing module is available
    # from collections import Counter
    #
    # def process_file_in_chunks_example(filepath: Union[str, Path]):
    #     all_content_parts = []
    #     word_counts_chunked = Counter()
    #     try:
    #         for chunk_num, text_chunk in enumerate(read_file_in_chunks(filepath)):
    #             print(f"Processing chunk {chunk_num + 1}...")
    #             # Apply typo correction per chunk if desired (might be complex for context-sensitive typos)
    #             # corrected_chunk = correct_text_typos(text_chunk)
    #             all_content_parts.append(text_chunk) # Or corrected_chunk
    #
    #             # Example: Basic tokenization and counting for each chunk
    #             # cleaned_chunk = tp.clean_text_for_word_tokenization(text_chunk, advanced=True)
    #             # tokens_in_chunk = tp.tokenize_text(cleaned_chunk)
    #             # word_counts_chunked.update(tokens_in_chunk)
    #
    #         full_content_from_chunks = "".join(all_content_parts)
    #         # Apply typo correction on the full reassembled content if not done per chunk
    #         full_content_from_chunks = correct_text_typos(full_content_from_chunks)
    #         print(f"Total words from chunked processing: {sum(word_counts_chunked.values())}")
    #         return full_content_from_chunks
    #     except Exception as e:
    #         print(f"Error during chunked processing example: {e}")
    #         return ""
    #
    # # To use it (hypothetically):
    # # content = process_file_in_chunks_example(filename)
    # # if content:
    # #     # ... proceed with analysis of 'content'
    # # else:
    # #     # ... handle error

    # Current implementation (reads full file):
    try:
        file_to_read: Path = Path(filename)
        # Note: Consider 'utf-8' as primary encoding, 'iso-8859-1' as fallback
        # The chunk reader tries utf-8 then iso-8859-1. For consistency, this could be aligned.
        with open(file_to_read, 'r', encoding='iso-8859-1') as file:
            content: str = file.read()
            # Typo correction is applied to the full content here.
            # If chunking were fully active for this function's main return,
            # this would need to be chunk-aware or applied per chunk,
            # which can be complex for typos that might span chunk boundaries
            # or require broader context.
            content = correct_text_typos(content)
            print(f"✅ Successfully read file: {file_to_read}")
            print(f"📄 File size: {len(content)} characters")
            return content
            
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        return ""
    except PermissionError:
        print(f"❌ Error: No permission to read file '{filename}'.")
        return ""
    except UnicodeDecodeError:
        print(f"❌ Error: Unable to decode file '{filename}' as text.")
        return ""
    except IsADirectoryError:
        print(f"❌ Error: Path '{filename}' is a directory, not a file.")
        return ""
    except Exception as e:
        print(f"❌ Unexpected error reading file '{filename}': {type(e).__name__} - {e}")
        return ""

def get_filename_from_user(prompt_message: str = "Enter filename") -> str: # Added prompt_message
    """Get filename from user with input validation and retry logic."""
    attempts: int = 0
    
    while attempts < cfg.MAX_INPUT_ATTEMPTS:
        try:
            print(f"\n📂 {prompt_message} (attempt {attempts + 1}/{cfg.MAX_INPUT_ATTEMPTS}):")
            if "custom stop word file" not in prompt_message.lower(): # Only show tip for main file input
                 print(f"💡 Tip: Use '{cfg.DEFAULT_SAMPLE_FILEPATH.name}' for testing (located in script directory)")
            print("💡 Type 'quit' to exit")
            
            filename_str: str = input("Filename: ").strip()
            
            if filename_str.lower() in ['quit', 'exit', 'q']:
                print("👋 User chose to quit input.")
                return ""
            
            if not filename_str:
                print("⚠️  Please enter a filename.")
                attempts += 1
                continue
            
            input_path: Path = Path(filename_str)
            
            if input_path.is_absolute():
                path_to_validate = input_path.resolve()
            else: # Relative path, try CWD then script directory
                path_cwd = (Path.cwd() / input_path).resolve()
                if path_cwd.exists() and path_cwd.is_file():
                    path_to_validate = path_cwd
                else:
                    path_to_validate = (cfg.SCRIPT_DIRECTORY / input_path).resolve()

            is_valid, message = validate_file_path(path_to_validate)
            if is_valid:
                print(f"✅ Validated path: {path_to_validate}")
                return str(path_to_validate)
            else:
                print(f"❌ Invalid path: {message}")
                # Try to give more context if relative path failed in both locations
                if not input_path.is_absolute():
                    path_script_dir_check = (cfg.SCRIPT_DIRECTORY / input_path).resolve()
                    if path_to_validate != path_script_dir_check: # if CWD was tried and failed
                        is_valid_script, message_script = validate_file_path(path_script_dir_check)
                        if not is_valid_script:
                             print(f"❌ Also not found or invalid in script directory: {message_script}")
                attempts += 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            return ""
        except Exception as e:
            print(f"❌ Error getting input: {type(e).__name__} - {e}")
            attempts += 1
    
    print(f"\n❌ Maximum attempts ({cfg.MAX_INPUT_ATTEMPTS}) reached for {prompt_message.lower()}.")
    return ""

# =============================================================================
# CUSTOM STOP WORD FILE LOADER (New for dynamic stop words)
# =============================================================================
def load_custom_stop_words(filepath_str: str) -> Tuple[Optional[Set[str]], str]:
    """
    Loads stop words from a custom file. Each stop word should be on a new line.
    Words are converted to lowercase and stripped of whitespace.

    Args:
        filepath_str (str): The path to the custom stop word file.

    Returns:
        Tuple[Optional[Set[str]], str]: A tuple containing:
                                         - A set of stop words if successful.
                                         - An error message string if an error occurred, otherwise an empty string.
    """
    filepath = Path(filepath_str)
    stop_words_set: Set[str] = set()
    error_message: str = ""

    try:
        # Validate the file path first (existence, is_file, basic size check)
        is_valid, val_message = validate_file_path(filepath)
        if not is_valid:
            return None, val_message # Return validation message as error

        with open(filepath, 'r', encoding='utf-8') as f: # Assume UTF-8 for custom stop word files
            for line in f:
                word = line.strip().lower()
                if word: # Add if not empty after stripping
                    stop_words_set.add(word)
        
        if not stop_words_set:
            error_message = f"⚠️ No stop words found in custom file '{filepath}'. File might be empty or incorrectly formatted."
            return None, error_message # Return None if no words loaded, but not a file error

        print(f"✅ Successfully loaded {len(stop_words_set)} custom stop words from '{filepath}'.")
        return stop_words_set, ""

    except FileNotFoundError:
        error_message = f"❌ Error: Custom stop word file '{filepath}' not found."
    except PermissionError:
        error_message = f"❌ Error: No permission to read custom stop word file '{filepath}'."
    except UnicodeDecodeError:
        error_message = f"❌ Error: Unable to decode custom stop word file '{filepath}' as UTF-8 text."
    except Exception as e:
        error_message = f"❌ Unexpected error loading custom stop words from '{filepath}': {type(e).__name__} - {e}"
    
    return None, error_message


def load_text_file() -> str: # This function's role changes slightly with stop word management
    """Complete file loading workflow for main analysis text. Handles .txt, .csv, and .json files."""
    print("🚀 Main Text File Loader") # Clarified purpose
    print("=" * 30)
    
    filename_str: str = get_filename_from_user("Enter filename for text analysis") # More specific prompt
    if not filename_str:
        return ""
    
    file_path: Path = Path(filename_str)
    content: str = ""
    error_msg_load: str = "" # To capture errors from specific readers
    
    file_suffix_lower = file_path.suffix.lower()

    if file_suffix_lower == '.csv':
        print(f"\n📄 CSV file detected: {file_path.name}")
        column_id_str = input("Enter the column name or index (e.g., 'text_column' or 0) to analyze: ").strip()
        if not column_id_str:
            print("❌ Column identifier cannot be empty. Aborting.")
            return ""
        column_identifier: Union[str, int]
        if column_id_str.isdigit():
            column_identifier = int(column_id_str)
        else:
            column_identifier = column_id_str
        content, error_msg_load = read_csv_file(file_path, column_identifier)
    elif file_suffix_lower == '.json':
        print(f"\n📄 JSON file detected: {file_path.name}")
        key_name_str = input("Enter the key name containing the text to analyze (e.g., 'text_field'): ").strip()
        if not key_name_str:
            print("❌ Key name cannot be empty. Aborting.")
            return ""
        content, error_msg_load = read_json_file(file_path, key_name_str)
    elif file_suffix_lower == '.txt':
        content = read_file(filename_str) # read_file prints its own success/errors
    else:
        print(f"⚠️ Unrecognized file type '{file_path.suffix}'. Attempting to read as plain text.")
        content = read_file(filename_str)

    if error_msg_load: # If read_csv/json_file returned an error
        print(error_msg_load)
        return ""
    
    if content:
        # Preview logic moved here to ensure it runs only if content is successfully loaded
        if len(content) > cfg.PREVIEW_LENGTH:
            preview: str = content[:cfg.PREVIEW_LENGTH] + "..."
        else:
            preview: str = content
        print(f"\n📖 File Preview (first {cfg.PREVIEW_LENGTH} chars):")
        print("-" * 20)
        print(preview)
        print("-" * 20)
    elif not error_msg_load and not content: # If no specific error but content is empty (e.g. read_file returned "")
        print("ℹ️ No content loaded from the file (it might be empty or an issue occurred).")

    return content

# ... (rest of the file: read_csv_file, read_json_file, save_results_to_file)
# The definitions of read_csv_file and read_json_file are already in the provided content.
# I will ensure they are correctly placed relative to the new load_custom_stop_words.
# The save_results_to_file function remains at the end.
# The order will be: validate_file_path, read_file, get_filename_from_user, load_custom_stop_words, read_csv_file, read_json_file, load_text_file, save_results_to_file.
# This seems logical.

# =============================================================================
# CSV FILE READING FUNCTION (New for CSV support)
# =============================================================================
def read_csv_file(filepath: Path, column_identifier: Union[str, int]) -> Tuple[str, str]:
    """
    Reads text from a specified column in a CSV file.

    Args:
        filepath (Path): The path to the CSV file.
        column_identifier (Union[str, int]): The name (string) or index (int) of the column to extract text from.

    Returns:
        Tuple[str, str]: A tuple containing:
                         - The concatenated text content from the specified column.
                         - An error message string if an error occurred, otherwise an empty string.
    """
    texts: List[str] = []
    error_message: str = ""

    try:
        with open(filepath, 'r', encoding='iso-8859-1', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header: Optional[List[str]] = None
            
            try:
                header = next(reader) 
                normalized_header = [col.lower().strip() for col in header] if header else []
            except StopIteration:
                error_message = f"CSV file '{filepath}' is empty."
                return "", error_message

            col_index: Optional[int] = None

            if isinstance(column_identifier, str): 
                try:
                    if not header:
                        error_message = f"CSV file '{filepath}' has no header row to find column name '{column_identifier}'."
                        return "", error_message
                    col_index = normalized_header.index(column_identifier.lower().strip())
                except ValueError:
                    error_message = f"Column name '{column_identifier}' not found in CSV header: {header}."
                    return "", error_message
            elif isinstance(column_identifier, int): 
                col_index = column_identifier
            else:
                error_message = "Invalid column_identifier type. Must be string (name) or int (index)."
                return "", error_message
            
            # Data rows processing (header is already consumed)
            for row_number, row in enumerate(reader, start=1): 
                if col_index is not None and col_index < len(row):
                    texts.append(row[col_index])
                elif col_index is not None:
                    print(f"⚠️ Warning: Row {row_number + 1} in '{filepath}' is too short for column index {col_index}. Skipping cell.")
            
            if not texts and not error_message: 
                if header and isinstance(column_identifier, str): 
                     error_message = f"Column '{column_identifier}' found, but no data rows in '{filepath}' or column was empty in all data rows."
                elif isinstance(column_identifier, int): 
                     error_message = f"No data found for column index {column_identifier} in '{filepath}' or column was empty in all data rows."

        if not texts and not error_message: 
             error_message = f"No text data extracted from column '{column_identifier}' in '{filepath}'."
        
        concatenated_text = "\n".join(texts) 
        
        if concatenated_text:
             corrected_text = correct_text_typos(concatenated_text)
             print(f"✅ Successfully read and processed CSV file: {filepath}, column: {column_identifier}")
             print(f"📄 Extracted text size: {len(corrected_text)} characters")
             return corrected_text, ""
        else:
            if not error_message:
                error_message = f"No text content found in column '{column_identifier}' of '{filepath}'."
            return "", error_message

    except FileNotFoundError: error_message = f"❌ Error: File '{filepath}' not found."; return "", error_message
    except PermissionError: error_message = f"❌ Error: No permission to read file '{filepath}'."; return "", error_message
    except csv.Error as e: error_message = f"❌ Error parsing CSV file '{filepath}': {type(e).__name__} - {e}"; return "", error_message
    except Exception as e: error_message = f"❌ Unexpected error reading CSV file '{filepath}': {type(e).__name__} - {e}"; return "", error_message

# =============================================================================
# JSON FILE READING FUNCTION (New for JSON support)
# =============================================================================
def read_json_file(filepath: Path, key_name: str) -> Tuple[str, str]:
    error_message: str = ""; extracted_text: str = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as jsonfile: 
            data = json.load(jsonfile)
        if not isinstance(data, dict):
            error_message = f"❌ Error: JSON content in '{filepath}' is not a dictionary (object)."
            return "", error_message
        value = data.get(key_name)
        if value is None:
            error_message = f"❌ Error: Key '{key_name}' not found in JSON file '{filepath}'."
            return "", error_message
        if isinstance(value, str): extracted_text = value
        elif isinstance(value, list):
            if all(isinstance(item, str) for item in value):
                extracted_text = "\n".join(value)
            else:
                error_message = f"❌ Error: Key '{key_name}' in '{filepath}' points to a list, but not all items are strings."
                return "", error_message
        else:
            error_message = f"❌ Error: Value for key '{key_name}' in '{filepath}' is not a string or a list of strings (found type: {type(value).__name__})."
            return "", error_message
        if extracted_text:
            corrected_text = correct_text_typos(extracted_text)
            print(f"✅ Successfully read and processed JSON file: {filepath}, key: {key_name}")
            print(f"📄 Extracted text size: {len(corrected_text)} characters")
            return corrected_text, ""
        else:
            if not error_message:
                 error_message = f"No text content extracted for key '{key_name}' in '{filepath}'."
            return "", error_message
    except FileNotFoundError: error_message = f"❌ Error: File '{filepath}' not found."; return "", error_message
    except PermissionError: error_message = f"❌ Error: No permission to read file '{filepath}'."; return "", error_message
    except json.JSONDecodeError as e: error_message = f"❌ Error parsing JSON file '{filepath}': {e.msg} (line {e.lineno} col {e.colno})"; return "", error_message
    except Exception as e: error_message = f"❌ Unexpected error reading JSON file '{filepath}': {type(e).__name__} - {e}"; return "", error_message

# Old save_results_to_file function removed.
