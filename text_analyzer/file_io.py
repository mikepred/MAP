"""
File I/O operations for the Text Analyzer application.
"""

import os
from pathlib import Path
from typing import Union, Tuple, List, Any # Added List, Any for save_results_to_file if Counter is used there
from collections import Counter # For type hinting save_results_to_file

from . import config as cfg

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
        
        file_size: int = file_path.stat().st_size
        if file_size > cfg.MAX_FILE_SIZE_BYTES:
            return False, f"File too large ({file_size} bytes). Maximum: {cfg.MAX_FILE_SIZE_BYTES} bytes"
        
        return True, "File validation passed"
        
    except Exception as e:
        return False, f"Error validating file '{filename}': {type(e).__name__} - {e}"

def read_file(filename: Union[str, Path]) -> str:
    """Read text from a file with comprehensive error handling."""
    try:
        file_to_read: Path = Path(filename)
        with open(file_to_read, 'r', encoding='utf-8') as file:
            content: str = file.read()
            print(f"✅ Successfully read file: {file_to_read}")
            print(f"📄 File size: {len(content)} characters")
            return content
            
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        print("💡 Please check the filename and path.")
        return ""
    except PermissionError:
        print(f"❌ Error: No permission to read '{filename}'.")
        print("💡 Check file permissions or try running as administrator.")
        return ""
    except UnicodeDecodeError:
        print(f"❌ Error: Unable to decode '{filename}' as text.")
        print("💡 File might be binary or use different encoding.")
        return ""
    except IsADirectoryError:
        print(f"❌ Error: '{filename}' is a directory, not a file.")
        print("💡 Please specify a file, not a folder.")
        return ""
    except Exception as e:
        print(f"❌ Unexpected error reading '{filename}': {e}")
        print("💡 Please try again or contact support.")
        return ""

def get_filename_from_user() -> str:
    """Get filename from user with input validation and retry logic."""
    attempts: int = 0
    
    while attempts < cfg.MAX_INPUT_ATTEMPTS:
        try:
            print(f"\n📂 Enter filename (attempt {attempts + 1}/{cfg.MAX_INPUT_ATTEMPTS}):")
            print(f"💡 Tip: Use '{cfg.DEFAULT_SAMPLE_FILEPATH.name}' for testing (located in script directory)")
            print("💡 Type 'quit' to exit")
            
            filename_str: str = input("Filename: ").strip()
            
            if filename_str.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                return ""
            
            if not filename_str:
                print("⚠️  Please enter a filename.")
                attempts += 1
                continue
            
            input_path: Path = Path(filename_str)
            
            # 1. If absolute, validate directly
            if input_path.is_absolute():
                path_to_validate = input_path.resolve()
                is_valid, message = validate_file_path(path_to_validate)
                if is_valid:
                    print(f"✅ Validated absolute path: {path_to_validate}")
                    return str(path_to_validate)
                else:
                    print(f"❌ Invalid absolute path: {message}")
                    attempts += 1
                    continue # Try again
            else:
                # 2. If relative, try CWD first
                path_cwd = (Path.cwd() / input_path).resolve()
                is_valid_cwd, message_cwd = validate_file_path(path_cwd)
                if is_valid_cwd:
                    print(f"✅ Validated relative path (in CWD): {path_cwd}")
                    return str(path_cwd)
                
                # 3. If not in CWD, try script directory
                path_script_dir = (cfg.SCRIPT_DIRECTORY / input_path).resolve()
                # Avoid re-validating if path_cwd and path_script_dir are the same
                if path_script_dir != path_cwd:
                    is_valid_script, message_script = validate_file_path(path_script_dir)
                    if is_valid_script:
                        print(f"✅ Validated relative path (in script directory): {path_script_dir}")
                        return str(path_script_dir)
                
                # If neither worked, print CWD error message (usually more relevant for user's intent)
                # and then script dir error if different.
                print(f"❌ File not found or invalid in CWD: {message_cwd}")
                if path_script_dir != path_cwd and not is_valid_script: # is_valid_script might not be defined if paths were same
                     _, message_script_fallback = validate_file_path(path_script_dir) # re-validate to get message
                     print(f"❌ Also not found or invalid in script directory: {message_script_fallback}")

                attempts += 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            return ""
        except Exception as e:
            print(f"❌ Error getting input: {type(e).__name__} - {e}")
            attempts += 1
    
    print(f"\n❌ Maximum attempts ({cfg.MAX_INPUT_ATTEMPTS}) reached")
    return ""

def load_text_file() -> str:
    """Complete file loading workflow with user interaction."""
    print("🚀 Text File Loader")
    print("=" * 30)
    
    filename_str: str = get_filename_from_user()
    if not filename_str:
        return ""
    
    content: str = read_file(filename_str)
    
    if content:
        if len(content) > cfg.PREVIEW_LENGTH:
            preview: str = content[:cfg.PREVIEW_LENGTH] + "..."
        else:
            preview: str = content
        
        print(f"\n📖 File Preview:")
        print("-" * 20)
        print(preview)
        print("-" * 20)
    
    return content

def save_results_to_file(
    frequencies_counter: Counter[str], 
    num_top_words: int, 
    unique_word_count: int, 
    output_filename: str = cfg.DEFAULT_RESULTS_FILENAME
) -> None:
    """
    Saves analysis results to a file.
    
    Args:
        frequencies_counter (Counter[str]): Word frequency Counter object.
        num_top_words (int): Number of top words to save.
        unique_word_count (int): Total number of unique words.
        output_filename (str): Name of the file to save results.
    """
    try:
        output_path: Path = Path(output_filename) # Output path can be relative to CWD or absolute
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Text Analysis Results\n")
            f.write("=" * 30 + "\n\n")
            
            actual_top_n: int = min(num_top_words, unique_word_count)
            most_common: List[Tuple[str, int]] = frequencies_counter.most_common(actual_top_n)
            
            f.write(f"Top {actual_top_n} most common words:\n")
            f.write("-" * 30 + "\n")
            
            for word, count_val in most_common: # Renamed count to count_val
                f.write(f"{word:15} : {count_val:3d}\n")
            
            f.write("-" * 30 + "\n")
            f.write(f"Total unique words: {unique_word_count}\n")
            
            total_words_val: int = sum(frequencies_counter.values())
            f.write(f"Total words (in analysis): {total_words_val}\n\n")
            f.write("Analysis complete.\n")
        
        print(f"\n✅ Results successfully saved to {output_path.resolve()}") # Show absolute path
    except IOError as e: # More specific for file operations
        print(f"\n❌ IOError: Could not write results to {output_filename}. {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred while saving results: {type(e).__name__} - {e}")
