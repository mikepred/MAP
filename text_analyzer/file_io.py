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
from .text_processing import correct_text_typos

# =============================================================================
# FILE I/O FUNCTIONS (Originally from Module 3B)
# =============================================================================

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
    """Read text from a file with comprehensive error handling."""
    try:
        file_to_read: Path = Path(filename)
        with open(file_to_read, 'r', encoding='iso-8859-1') as file: # Consider utf-8 as primary, iso as fallback
            content: str = file.read()
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

def save_results_to_file(
    frequencies_counter: Counter[str], 
    num_top_words: int, 
    unique_word_count: int, 
    output_filename: str = cfg.DEFAULT_RESULTS_FILENAME
) -> None:
    try:
        output_path: Path = Path(output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Text Analysis Results\n"); f.write("=" * 30 + "\n\n")
            actual_top_n: int = min(num_top_words, unique_word_count)
            most_common: List[Tuple[str, int]] = frequencies_counter.most_common(actual_top_n)
            f.write(f"Top {actual_top_n} most common words:\n"); f.write("-" * 30 + "\n")
            for word, count_value in most_common:
                f.write(f"{word:15} : {count_value:3d}\n")
            f.write("-" * 30 + "\n"); f.write(f"Total unique words: {unique_word_count}\n")
            total_words_val: int = sum(frequencies_counter.values())
            f.write(f"Total words (in analysis): {total_words_val}\n\n"); f.write("Analysis complete.\n")
        print(f"\n✅ Results successfully saved to {output_path.resolve()}")
    except IOError as e: print(f"\n❌ IOError: Could not write results to {output_filename}. {e}")
    except Exception as e: print(f"\n❌ An unexpected error occurred while saving results: {type(e).__name__} - {e}")
