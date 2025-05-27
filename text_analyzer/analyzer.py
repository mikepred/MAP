"""
Text Analysis Script - Complete Version
A comprehensive text analysis tool for processing and analyzing text files.

Modules 3A-3E: Complete Integration. Enhanced with Module 4B features.
"""

import os
import re
import string
from pathlib import Path
from collections import Counter
import time # Added for Module 4C
from typing import Optional, List, Dict, Tuple, Set, Any, Union # For type hints

# Import configuration
from . import config as cfg
# Import file I/O functions
from . import file_io
# Import text processing functions
from . import text_processing as tp
# Import analysis functions
from . import analysis
# Import display functions
from . import display

# =============================================================================
# UTILITY AND MAIN SCRIPT LOGIC
# =============================================================================

def time_function(func: callable, *args: Any, **kwargs: Any) -> Tuple[Any, float]: # Stays in analyzer.py
    """Times the execution of a function and returns the result and duration."""
    start_time: float = time.time()
    result: Any = func(*args, **kwargs)
    end_time: float = time.time()
    duration: float = end_time - start_time
    # The caller will decide whether to print the duration.
    return result, duration

def analyze_word_lengths(tokens: List[str]) -> Counter[int]: # New from Module 4C
    """
    Analyzes the distribution of word lengths and prints the analysis.
    
    Args:
        tokens (List[str]): List of word tokens
        
    Returns:
        Counter[int]: Counter object with word lengths as keys and counts as values
    """
    # analyze_word_lengths is in analysis.py and returns Counter.
    # Display logic for word lengths will be in display.py.
    # This function definition in analyzer.py is now removed.

# =============================================================================
# USER INPUT CONFIGURATION (Remains in analyzer.py as it's UI related for main script)
# =============================================================================
def get_user_input_config() -> Tuple[int, bool]:
    """
    Gets configuration from user input for number of top words and stop word removal.
    (Enhancement 2 from Module 4B)
    Filepath is NOT asked here as it's handled differently by the caller.
    
    Returns:
        Tuple[int, bool]: (num_words_to_display, enable_stop_word_removal)
    """
    print("\n--- ⚙️ Text Analysis Configuration ---")
    
    num_words: int = cfg.DEFAULT_TOP_WORDS_DISPLAY
    while True:
        try:
            num_words_str_input: str = input(f"Number of top words to display (default: {num_words}): ").strip()
            if not num_words_str_input:
                break
            else:
                num_words_val: int = int(num_words_str_input)
                if num_words_val <= 0:
                    print("⚠️ Please enter a positive number for top words.")
                    continue
                num_words = num_words_val
            break
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")
            
    enable_stop_words: bool = True # Default
    while True:
        default_sw_choice_str: str = 'yes' if enable_stop_words else 'no'
        stop_words_prompt: str = f"Remove stop words? (yes/no, default: {default_sw_choice_str}): "
        stop_words_choice: str = input(stop_words_prompt).strip().lower()
        if not stop_words_choice:
            break
        elif stop_words_choice == 'yes':
            enable_stop_words = True
            break
        elif stop_words_choice == 'no':
            enable_stop_words = False
            break
        else:
            print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")
            
    return num_words, enable_stop_words

# =============================================================================
# MAIN SCRIPT LOGIC
# =============================================================================

def run_comprehensive_test() -> bool:
    """Run comprehensive testing of all components."""
    display.print_header("🧪 COMPREHENSIVE TESTING SUITE 🧪") # Updated
    
    test_results: Dict[str, bool] = {
        'file_io': False,
        'text_processing': False,
        'analysis': False,
        'display': False
    }
    
    # Test 1: File I/O
    display.print_section("📁 Testing File I/O System")
    # This is harder to test without actual file operations or mocking.
    # For now, we'll keep it as a conceptual check.
    # A more robust test would involve creating a temp file, reading it, and verifying content.
    try:
        # Create a dummy sample file for testing read operations
        dummy_file_path = cfg.SCRIPT_DIRECTORY / "test_dummy_file.txt"
        with open(dummy_file_path, "w", encoding="utf-8") as f:
            f.write("Hello test world.")
        
        if callable(file_io.read_file) and file_io.read_file(dummy_file_path) == "Hello test world.":
            print("✅ File I/O (read_file) basic test passed.")
            test_results['file_io'] = True
        else:
            print("❌ File I/O (read_file) basic test failed.")
        os.remove(dummy_file_path) # Clean up dummy file
    except Exception as e:
        print(f"❌ File I/O test error: {e}")
        if 'dummy_file_path' in locals() and dummy_file_path.exists():
            os.remove(dummy_file_path)


    # Test 2: Text Processing
    display.print_section("🔄 Testing Text Processing Pipeline")
    try:
        test_text_proc: str = "  Hello, World! This is a test... with THE test words.  "
        expected_tokens_no_sw = ['hello', 'world', 'this', 'is', 'a', 'test', 'with', 'the', 'test', 'words']
        expected_tokens_with_sw = ['hello', 'world', 'test', 'test', 'words'] # Assuming 'this', 'is', 'a', 'with', 'the' are stop words

        # Test cleaning (for word tokenization, basic)
        cleaned_for_words = tp.clean_text_for_word_tokenization(test_text_proc, advanced=False)
        assert cleaned_for_words == "hello world this is a test with the test words", f"Basic cleaning failed: {cleaned_for_words}"
        
        # Test tokenization
        tokens = tp.tokenize_text(cleaned_for_words)
        assert tokens == expected_tokens_no_sw, f"Tokenization failed: {tokens}"
        
        # Test stop word removal
        tokens_no_stopwords = tp.remove_stop_words(tokens)
        assert tokens_no_stopwords == expected_tokens_with_sw, f"Stop word removal failed: {tokens_no_stopwords}"
        
        # Test count_words (which includes cleaning and tokenizing)
        counts_no_sw = tp.count_words(test_text_proc, use_stop_words=False)
        assert counts_no_sw['test'] == 2 and counts_no_sw['hello'] == 1, "count_words (no stop words) failed"
        
        counts_with_sw = tp.count_words(test_text_proc, use_stop_words=True)
        assert counts_with_sw['test'] == 2 and 'is' not in counts_with_sw, "count_words (with stop words) failed"
        
        print("✅ Text processing functions passed assertions.")
        test_results['text_processing'] = True
    except AssertionError as e:
        print(f"❌ Text processing assertion failed: {e}")
    except Exception as e:
        print(f"❌ Text processing error: {e}")

    # Test 3: Analysis
    display.print_section("📊 Testing Analysis Functions")
    try:
        test_text_analysis: str = "First sentence. Second sentence is a bit longer, yes it is!"
        # Expected: 2 sentences.
        # Sentence 1: "First sentence" -> 2 words
        # Sentence 2: "Second sentence is a bit longer yes it is" -> 9 words
        # Total words (for sentence analysis) = 11. Avg = 5.5
        
        # Test count_sentences
        num_sentences = analysis.count_sentences(test_text_analysis)
        assert num_sentences == 2, f"count_sentences failed: expected 2, got {num_sentences}"

        # Test analyze_sentences
        sentence_analysis_res = analysis.analyze_sentences(test_text_analysis)
        assert sentence_analysis_res['sentence_count'] == 2, "analyze_sentences: sentence_count failed"
        assert sentence_analysis_res['average_words_per_sentence'] == 5.5, "analyze_sentences: average_words failed"
        
        # Test analyze_text_complete (a more integrated test)
        complete_results = analysis.analyze_text_complete(test_text_analysis, use_stop_words=False, num_common_words_to_display=2)
        assert 'error' not in complete_results or not complete_results['error'], f"analyze_text_complete returned error: {complete_results.get('error')}"
        assert complete_results.get('general_stats', {}).get('sentence_count') == 2, "analyze_text_complete: general_stats.sentence_count failed"
        # Word count from analyze_text_complete uses advanced cleaning, so it might differ from simple sentence word counts
        # For "First sentence. Second sentence is a bit longer, yes it is!"
        # Cleaned (adv): "first sentence second sentence is a bit longer yes it is"
        # Tokens: ['first', 'sentence', 'second', 'sentence', 'is', 'a', 'bit', 'longer', 'yes', 'it', 'is'] (11 tokens)
        assert complete_results.get('general_stats', {}).get('word_count') == 11, \
            f"analyze_text_complete: general_stats.word_count failed. Expected 11, got {complete_results.get('general_stats', {}).get('word_count')}"
        
        print("✅ Analysis functions passed assertions.")
        test_results['analysis'] = True
    except AssertionError as e:
        print(f"❌ Analysis assertion failed: {e}")
    except Exception as e:
        print(f"❌ Analysis error: {e}")
    
    # Test 4: Display (Conceptual check - ensure functions are callable)
    display.print_section("🖥️ Testing Display Functions")
    try:
        # Check if main display functions are callable
        assert callable(display.display_complete_analysis)
        assert callable(display.display_summary)
        assert callable(display.display_word_length_analysis)
        print("✅ Display functions are present and callable.")
        test_results['display'] = True
    except AssertionError:
        print("❌ Core display functions not found or not callable.")
    except Exception as e:
        print(f"❌ Display functions check error: {e}")
        
    display.print_section("🎯 Test Results Summary")
    all_passed: bool = all(test_results.values())
    for component, passed in test_results.items():
        status: str = "✅ PASS" if passed else "❌ FAIL"
        print(f"{component.replace('_', ' ').title()}: {status}")
    
    if all_passed:
        print("\n🎉 All tests passed! Your text analyzer is ready!")
    else:
        print("\n⚠️ Some tests failed. Please review the errors above.")
    return all_passed


def _handle_custom_file_option() -> None:
    """Handles the logic for menu option 2: Analyze Custom Text File."""
    custom_filepath_content = file_io.load_text_file()
    if custom_filepath_content:
        num_common_words_cfg, use_stop_words_cfg = get_user_input_config()
        display.print_section("🔄 Running complete analysis...")
        # pipeline_start_time = time.time() # Replaced by time_function call
        if use_stop_words_cfg:
            print("ℹ️ Stop word removal is ON.")
        else:
            print("ℹ️ Stop word removal is OFF.")
        
        results, analysis_duration = time_function(
            analysis.analyze_text_complete,
            custom_filepath_content,
            use_stop_words=use_stop_words_cfg,
            num_common_words_to_display=num_common_words_cfg
        )
        # pipeline_end_time = time.time() # Replaced by time_function call
        print(f"\n⏱️ Text analysis pipeline took: {analysis_duration:.4f} seconds")

        if 'error' in results and results['error']:
            print(f"❌ Analysis error: {results['error']}")
        else:
            # Display options
            print("\n📊 Analysis complete! Choose display format:")
            print("1. Complete Report")
            print("2. Quick Summary")
            print("3. Both")
            display_choice = input("Enter choice (1-3): ").strip()
            if display_choice == "1":
                display.display_complete_analysis(results)
            elif display_choice == "2":
                display.display_summary(results)
            elif display_choice == "3":
                display.display_summary(results)
                display.display_complete_analysis(results)
            else:
                print("⚠️ Invalid display choice, showing summary:")
                display.display_summary(results)

            processed_tokens_len_analysis = results.get('processed_tokens', [])
            # Ensure word_length_counts_obj is correctly populated in analysis_results by analyze_text_complete
            # For now, let's assume analyze_word_lengths from analysis module returns the counter
            custom_word_length_counts = analysis.analyze_word_lengths(processed_tokens_len_analysis)
            if custom_word_length_counts: # Check if the counter is not empty
                display.display_word_length_analysis(custom_word_length_counts, len(processed_tokens_len_analysis))

            if 'word_analysis' in results and results['word_analysis'].get('full_word_counts_obj'):
                while True:
                    save_choice = input("\n💾 Save analysis results to file? (yes/no, default: no): ").strip().lower()
                    if not save_choice or save_choice == 'no':
                        break
                    elif save_choice == 'yes':
                        default_out_fn = f"custom_{cfg.DEFAULT_RESULTS_FILENAME}"
                        out_fn_input = input(f"Enter output filename (default: {default_out_fn}): ").strip()
                        if not out_fn_input:
                            out_fn_input = default_out_fn
                        
                        freq_ctr = results['word_analysis']['full_word_counts_obj']
                        n_save = num_common_words_cfg
                        unique_save = len(freq_ctr)
                        file_io.save_results_to_file(freq_ctr, n_save, unique_save, out_fn_input)
                        break
                    else:
                        print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")
    else:
        print("❌ No content loaded from custom file. Returning to main menu.")


def _handle_analyze_file_option() -> None:
    """Handles the logic for menu option 1: Analyze Text File."""
    # Filepath is now fixed for this option.
    filepath_config: str = str(cfg.FIXED_TARGET_FILEPATH)
    print(f"ℹ️ Analyzing fixed file: {filepath_config}")

    num_common_words_config: int
    use_stop_words_config: bool
    # get_user_input_config is in this file (analyzer.py)
    num_common_words_config, use_stop_words_config = get_user_input_config()
    
    # Validate the fixed filepath
    is_valid_path, path_message = file_io.validate_file_path(filepath_config)
    if not is_valid_path:
        print(f"❌ Error with fixed file path '{filepath_config}': {path_message}")
        print("Please ensure 's.txt' exists in the script directory.")
        print("Returning to main menu.")
        return

    content: str = file_io.read_file(filepath_config)
    
    if not content:
        print(f"❌ No content loaded from '{filepath_config}' (file might be empty or unreadable). Returning to main menu.")
        return
    
    print("\n🔄 Running complete analysis...")
    # pipeline_start_time = time.time() # Replaced by time_function call

    if use_stop_words_config:
        print("ℹ️ Stop word removal is ON.")
    else:
        print("ℹ️ Stop word removal is OFF.")
    
    results, analysis_duration = time_function(
        analysis.analyze_text_complete,
        content, 
        use_stop_words=use_stop_words_config, 
        num_common_words_to_display=num_common_words_config
    )
    # pipeline_end_time = time.time() # Replaced by time_function call
    print(f"\n⏱️ Text analysis pipeline took: {analysis_duration:.4f} seconds")

    if 'error' in results and results['error']:
        print(f"❌ Analysis error: {results['error']}")
        return
    
    # Display options
    print("\n📊 Analysis complete! Choose display format:")
    print("1. Complete Report")
    print("2. Quick Summary")
    print("3. Both")
    
    display_choice_input = input("Enter choice (1-3): ").strip() # Renamed variable
    
    if display_choice_input == "1":
        display.display_complete_analysis(results) # Updated
    elif display_choice_input == "2":
        display.display_summary(results) # Updated
    elif display_choice_input == "3":
        display.display_summary(results) # Updated
        display.display_complete_analysis(results) # Updated
    else: # Default to summary if invalid choice
        print("⚠️ Invalid display choice, showing summary:")
        display.display_summary(results) # Updated

    # Word Length Analysis display (M4C)
    processed_tokens_for_length_analysis = results.get('processed_tokens', [])
    # Call analysis.analyze_word_lengths to get the Counter object
    word_length_counts_data = analysis.analyze_word_lengths(processed_tokens_for_length_analysis)
    if word_length_counts_data: # Check if Counter is not empty
        display.display_word_length_analysis(word_length_counts_data, len(processed_tokens_for_length_analysis)) # Updated

    # Ask to save results
    if 'word_analysis' in results and results['word_analysis'].get('full_word_counts_obj'):
        while True:
            save_choice = input("\n💾 Save analysis results to file? (yes/no, default: no): ").strip().lower()
            if not save_choice or save_choice == 'no':
                break
            elif save_choice == 'yes':
                default_output_filename = cfg.DEFAULT_RESULTS_FILENAME
                output_filename_input = input(f"Enter output filename (default: {default_output_filename}): ").strip()
                if not output_filename_input:
                    output_filename_input = default_output_filename
                
                # Prepare data for save_results_to_file
                freq_counter = results['word_analysis']['full_word_counts_obj']
                # num_common_words_config is the number of words user wanted to *display*
                # For saving, we can use the same or decide on a fixed number, e.g., all or top N.
                # Let's use num_common_words_config for consistency with display.
                n_to_save = num_common_words_config 
                unique_count_to_save = len(freq_counter)
                
                file_io.save_results_to_file(freq_counter, n_to_save, unique_count_to_save, output_filename_input) # Updated
                break
            else:
                print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")


def main() -> None:
    """Main execution function - Complete integrated application."""
    display.print_header("🚀 TEXT ANALYZER - COMPLETE VERSION 🚀") # Updated
    print("Welcome to the comprehensive text analysis tool!")
    print("Built through Modules 3A-3E. Now enhancing with Module 4B features.")
    
    while True:
        try:
            print("\n" + "="*50)
            print("📋 Main Menu")
            print("="*50)
            print("1. 📊 Analyze Fixed Text File (s.txt)") 
            print("2. 📂 Analyze Custom Text File") # New menu option
            print("3. 🧪 Run System Tests")
            print("4. ❓ Help & Information")
            print("5. 🚪 Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                _handle_analyze_file_option()
            
            elif choice == "2": 
                _handle_custom_file_option() # Call the new helper function

            elif choice == "3":
                run_comprehensive_test()
            
            elif choice == "4":
                display.print_header("❓ HELP & INFORMATION ❓") # Updated
                print("This text analyzer can process any UTF-8 text file and provide:")
                print("• Word frequency analysis (optionally with stop word removal)")
                print("• Sentence structure analysis")
                print("• Readability assessment")
                print("• Pattern detection")
                print("• Professional formatting")
                print("\nFor best results:")
                print("• Use plain text files (.txt)")
                print("• Keep files under 10MB")
                print("• Ensure UTF-8 encoding")
                # print("• Place files in the same directory as this script or provide path") 
            
            elif choice == "5":
                print("\n👋 Thank you for using Text Analyzer!")
                print("🎉 Module 3 series complete! Module 4 enhancements started.")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-5.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Interrupted by user. Exiting.")
            break 
        except Exception as e:
            print(f"\n❌ An unexpected error occurred in the main menu: {e}")
            print("💡 Please try again or restart the application.")
            # Consider whether to break or continue after a generic exception
            # For robustness, might be better to log and continue, or offer to exit.
            # For this educational script, continuing is fine.

if __name__ == "__main__":
    main()
