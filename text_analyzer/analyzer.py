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
import time 
from typing import Optional, List, Dict, Tuple, Set, Any, Union

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
from nltk.corpus import stopwords # For NLTK language stop words

# =============================================================================
# UTILITY AND MAIN SCRIPT LOGIC
# =============================================================================

def time_function(func: callable, *args: Any, **kwargs: Any) -> Tuple[Any, float]:
    start_time: float = time.time()
    result: Any = func(*args, **kwargs)
    end_time: float = time.time()
    duration: float = end_time - start_time
    return result, duration

# =============================================================================
# INTERNAL HELPER FOR ANALYSIS AND DISPLAY
# =============================================================================
def _perform_analysis_and_display(file_content: str, source_filename_hint: str) -> None:
    num_common_words_cfg, stop_word_config, user_defined_patterns = get_user_input_config()

    active_stop_words_set: Optional[Set[str]] = set() # Default to empty set (no removal)
    stop_word_message: str = "ℹ️ Stop word removal is OFF (no option selected or error)."


    if stop_word_config["type"] == "default":
        active_stop_words_set = cfg.STOP_WORDS
        stop_word_message = f"ℹ️ Using default English stop words ({len(active_stop_words_set or [])} words)."
    elif stop_word_config["type"] == "nltk_lang":
        lang = stop_word_config["language"]
        try:
            active_stop_words_set = set(stopwords.words(lang))
            stop_word_message = f"ℹ️ Using NLTK '{lang}' stop words ({len(active_stop_words_set or [])} words)."
        except OSError: 
            print(f"❌ Error: NLTK stopwords for '{lang}' not found. Ensure it's downloaded (e.g., via download_nltk_data.py) and supported.")
            print("Proceeding without stop word removal for this analysis.")
            active_stop_words_set = set() 
            stop_word_message = "ℹ️ Stop word removal is OFF (selected language's stopwords not found)."
        except Exception as e_nltk: # Catch other potential NLTK errors
            print(f"❌ Error loading NLTK stopwords for '{lang}': {e_nltk}")
            active_stop_words_set = set()
            stop_word_message = "ℹ️ Stop word removal is OFF (error loading NLTK language)."
    elif stop_word_config["type"] == "custom":
        custom_path = stop_word_config["path"]
        loaded_set, err_msg = file_io.load_custom_stop_words(custom_path)
        if loaded_set:
            active_stop_words_set = loaded_set
            stop_word_message = f"ℹ️ Using custom stop words from '{Path(custom_path).name}' ({len(active_stop_words_set or [])} words)."
        else:
            print(f"❌ Error loading custom stop words: {err_msg}")
            print("Proceeding without stop word removal for this analysis.")
            active_stop_words_set = set()
            stop_word_message = "ℹ️ Stop word removal is OFF (custom list failed to load)."
    elif stop_word_config["type"] == "none":
        active_stop_words_set = set() 
        stop_word_message = "ℹ️ Stop word removal is OFF (user selected 'none')."

    display.print_section("🔄 Running complete analysis...")
    
    results, analysis_duration = time_function(
        analysis.analyze_text_complete,
        file_content,
        active_stop_words=active_stop_words_set, 
        num_common_words_to_display=num_common_words_cfg,
        user_patterns=user_defined_patterns
    )
    
    print(stop_word_message) 
    removed_count = results.get('word_analysis', {}).get('removed_stop_words_count', 0)
    if active_stop_words_set and removed_count > 0 : 
        print(f"ℹ️ Removed {removed_count} stop words.")
    elif active_stop_words_set and removed_count == 0 and stop_word_config["type"] != "none" and len(active_stop_words_set) > 0:
        print("ℹ️ No stop words (from the active list) were found in the text.")

    print(f"\n⏱️ Text analysis pipeline took: {analysis_duration:.4f} seconds")

    if results.get('error'):
        print(f"❌ Analysis error: {results['error']}")
        return

    print("\n📊 Analysis complete! Choose display format:")
    print("1. Complete Report"); print("2. Quick Summary"); print("3. Both")
    display_choice = input("Enter choice (1-3): ").strip()
    if display_choice == "1": display.display_complete_analysis(results)
    elif display_choice == "2": display.display_summary(results)
    elif display_choice == "3": display.display_summary(results); display.display_complete_analysis(results)
    else: print("⚠️ Invalid display choice, showing summary:"); display.display_summary(results)

    processed_tokens_len_analysis = results.get('processed_tokens', [])
    custom_word_length_counts = analysis.analyze_word_lengths(processed_tokens_len_analysis)
    if custom_word_length_counts:
        display.display_word_length_analysis(custom_word_length_counts, len(processed_tokens_len_analysis))

    if results.get('word_analysis', {}).get('full_word_counts_obj'): # Check if there are results to save
        while True:
            save_choice = input("\n💾 Save analysis results to file? (yes/no, default: no): ").strip().lower()
            if not save_choice or save_choice == 'no':
                break
            elif save_choice == 'yes':
                format_choice_input = input("Choose format: 1. Text, 2. JSON, 3. CSV (default: 1. Text): ").strip()
                format_map = {'1': 'txt', '2': 'json', '3': 'csv'}
                chosen_format = format_map.get(format_choice_input, 'txt') # Default to 'txt'

                # Construct default filename with correct extension
                source_stem = Path(source_filename_hint).stem # Get filename without original extension
                default_out_fn = f"{source_stem}_analysis_results.{chosen_format}"

                out_fn_input = input(f"Enter output filename (default: {default_out_fn}): ").strip()
                if not out_fn_input:
                    out_fn_input = default_out_fn

                # Ensure the filename has the chosen extension if user provides a name without one
                # or if they provide one with a different extension.
                output_path_obj = Path(out_fn_input)
                if output_path_obj.suffix.lower() != f".{chosen_format.lower()}":
                    out_fn_input = str(output_path_obj.with_suffix(f".{chosen_format}"))
                    print(f"ℹ️ Output filename adjusted to: {out_fn_input}")

                # Call the new save function with the full results dictionary
                file_io.save_analysis_results(
                    analysis_results=results,
                    output_filename_str=out_fn_input,
                    format_choice=chosen_format
                )
                break # Exit save loop
            else:
                print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")

    # Plot generation logic (remains unchanged, but consider if word_counts check is still needed or use 'results')
    if results.get('word_analysis', {}).get('full_word_counts_obj'):
        while True:
            plot_choice = input("\n📊 Generate graphical plots for analysis? (yes/no, default: no): ").strip().lower()
            if not plot_choice or plot_choice == 'no': break
            elif plot_choice == 'yes':
                print("Generating plots...")
                plot_output_dir = cfg.SCRIPT_DIRECTORY / cfg.DEFAULT_PLOTS_DIR
                plot_filename_prefix = source_filename_hint.replace('.txt', '').replace('.csv', '').replace('.json', '')
                
                def open_plot(plot_path: Optional[str]):
                    if not plot_path: return
                    try:
                        if os.name == 'nt': # Windows
                            os.startfile(plot_path)
                        elif os.name == 'posix': # macOS, Linux
                            if 'DISPLAY' in os.environ:
                                opener = 'xdg-open' if Path('/usr/bin/xdg-open').exists() else 'open'
                                os.system(f"{opener} \"{plot_path}\"")
                            else:
                                print(f"ℹ️ Plot saved at {plot_path}. No display environment detected to open it automatically.")
                        else:
                            print(f"ℹ️ Plot saved at {plot_path}. Auto-open not supported on this OS.")
                    except Exception as e_open:
                        print(f"⚠️ Could not automatically open plot '{plot_path}': {e_open}")

                if results.get('word_analysis', {}).get('full_word_counts_obj'):
                    saved_plot_path = display.plot_word_frequencies(results['word_analysis']['full_word_counts_obj'], top_n=num_common_words_cfg, output_dir=plot_output_dir, filename_prefix=f"{plot_filename_prefix}_word_freq")
                    open_plot(saved_plot_path)
                
                if results.get('sentiment_analysis'):
                    saved_plot_path = display.plot_sentiment_distribution(results['sentiment_analysis'], output_dir=plot_output_dir, filename_prefix=f"{plot_filename_prefix}_sentiment_dist")
                    open_plot(saved_plot_path)

                if results.get('word_length_counts_obj'):
                    saved_plot_path = display.plot_word_length_distribution(results['word_length_counts_obj'], output_dir=plot_output_dir, filename_prefix=f"{plot_filename_prefix}_word_len_dist")
                    open_plot(saved_plot_path)

                # Word Cloud Generation Prompt
                if display.WORDCLOUD_AVAILABLE and results.get('word_analysis', {}).get('full_word_counts_obj'):
                    wc_choice = input("\n☁️ Generate word cloud image? (yes/no, default: no): ").strip().lower()
                    if wc_choice == 'yes':
                        print("☁️ Generating word cloud...")
                        wc_path = display.generate_word_cloud(
                            word_frequencies=results['word_analysis']['full_word_counts_obj'],
                            output_dir=plot_output_dir, # Reuse same plot directory
                            filename_prefix=f"{plot_filename_prefix}_word_cloud"
                        )
                        if wc_path:
                            print(f"☁️ Word cloud generated: {wc_path}")
                            open_plot(wc_path)
                        else:
                            print("⚠️ Word cloud generation failed or was skipped by the display module.")
                elif not display.WORDCLOUD_AVAILABLE:
                    input("\n☁️ Word cloud generation is unavailable (WordCloud library not installed). Press Enter to continue.")


                break # Exit plot generation loop
            else: print("⚠️ Invalid choice. Please enter 'yes' or 'no'.")

# =============================================================================
# USER INPUT CONFIGURATION
# =============================================================================
def get_user_input_config() -> Tuple[int, Dict[str, Any], List[Dict[str, str]]]: # Updated return type
    print("\n--- ⚙️ Text Analysis Configuration ---")
    num_words: int = cfg.DEFAULT_TOP_WORDS_DISPLAY
    while True:
        try:
            num_words_str_input: str = input(f"Number of top words to display (default: {num_words}): ").strip()
            if not num_words_str_input: break
            num_words_val: int = int(num_words_str_input)
            if num_words_val <= 0: print("⚠️ Please enter a positive number."); continue
            num_words = num_words_val; break
        except ValueError: print("⚠️ Invalid input. Please enter a number.")
            
    stop_word_config: Dict[str, Any] = {"type": "default"} 
    
    print("\n--- Stopwords Configuration ---")
    print("1. Use default English stop words")
    print("2. Use NLTK stop words for another language")
    print("3. Use custom stop words from a file")
    print("4. Do not remove stop words")
    
    while True:
        sw_choice = input("Choose stop word option (1-4, default 1): ").strip()
        if not sw_choice: sw_choice = "1"

        if sw_choice == "1":
            stop_word_config = {"type": "default"}
            break
        elif sw_choice == "2":
            lang_prompt = f"Enter NLTK language for stopwords (e.g., {', '.join(cfg.SUPPORTED_NLTK_STOPWORD_LANGUAGES[:3])}, or 'list' to see all): "
            lang_input = input(lang_prompt).strip().lower()
            if lang_input == 'list':
                try:
                    print("Available NLTK stopwords languages:", ", ".join(stopwords.fileids()))
                except Exception as e_nltk_list:
                    print(f"Could not list NLTK languages: {e_nltk_list}. Ensure NLTK data is downloaded.")
                continue # Re-prompt for choice
            
            # Check against a predefined list in config OR all available NLTK languages
            # For simplicity, let's assume cfg.SUPPORTED_NLTK_STOPWORD_LANGUAGES exists and is used for validation.
            # If not, we might need to check `lang_input in stopwords.fileids()` but that requires NLTK data to be present.
            if lang_input in cfg.SUPPORTED_NLTK_STOPWORD_LANGUAGES:
                stop_word_config = {"type": "nltk_lang", "language": lang_input}
                break
            else:
                print(f"⚠️ Language '{lang_input}' not in configured supported list: {', '.join(cfg.SUPPORTED_NLTK_STOPWORD_LANGUAGES)}")
                print(f"   Or it might be an unsupported/mistyped NLTK language. Please try again.")
        elif sw_choice == "3":
            custom_path = file_io.get_filename_from_user("Enter path to custom stop word file")
            if custom_path:
                stop_word_config = {"type": "custom", "path": custom_path}
                break
            else:
                print("⚠️ No custom file path provided. Returning to stop word option selection.")
        elif sw_choice == "4":
            stop_word_config = {"type": "none"}
            break
        else:
            print("⚠️ Invalid choice. Please enter 1-4.")

    user_patterns: List[Dict[str, str]] = []
    print("\n--- Custom Regex Patterns (Optional) ---")
    if input("Do you want to add custom regex patterns for analysis? (yes/no, default: no): ").strip().lower() == 'yes':
        max_patterns = 5 # Limit number of custom patterns to avoid excessive input
        while len(user_patterns) < max_patterns:
            pattern_name = input(f"Enter a name for your custom pattern (e.g., 'Phone Numbers') (pattern {len(user_patterns) + 1}/{max_patterns}, or leave blank to finish): ").strip()
            if not pattern_name:
                break
            
            regex_string = input(f"Enter the regex string for '{pattern_name}': ").strip()
            if not regex_string:
                print("⚠️ Regex string cannot be empty. Please try again or leave pattern name blank to finish.")
                continue

            try:
                re.compile(regex_string) # Validate regex
                user_patterns.append({'name': pattern_name, 'regex': regex_string})
                print(f"✅ Pattern '{pattern_name}' added.")
            except re.error as e:
                print(f"❌ Invalid regex string: {e}. Please try again.")

            if len(user_patterns) >= max_patterns:
                print(f"ℹ️ Maximum number of {max_patterns} custom patterns reached.")
                break
            if input("Add another custom pattern? (yes/no, default: no): ").strip().lower() != 'yes':
                break
        if user_patterns:
             print(f"ℹ️ Added {len(user_patterns)} custom pattern(s).")

    return num_words, stop_word_config, user_patterns

# =============================================================================
# MAIN SCRIPT LOGIC
# =============================================================================
def run_comprehensive_test() -> bool:
    display.print_header("🧪 COMPREHENSIVE TESTING SUITE 🧪")
    test_results: Dict[str, bool] = {'file_io': False, 'text_processing': False, 'analysis': False, 'display': False}
    try:
        dummy_file_path = cfg.SCRIPT_DIRECTORY / "test_dummy_file.txt"
        with open(dummy_file_path, "w", encoding="utf-8") as f: f.write("Hello test world.")
        if callable(file_io.read_file) and file_io.read_file(dummy_file_path) == "Hello test world.":
            print("✅ File I/O (read_file) basic test passed."); test_results['file_io'] = True
        else: print("❌ File I/O (read_file) basic test failed.")
        os.remove(dummy_file_path)
    except Exception as e: print(f"❌ File I/O test error: {e}"); _ = locals().get('dummy_file_path'); os.remove(_) if _ and _.exists() else None
    
    try:
        test_text_proc: str = "  Hello, World! This is a test... with THE test words.  "
        cleaned_for_words = tp.clean_text_for_word_tokenization(test_text_proc, advanced=False)
        assert cleaned_for_words == "hello world this is a test with the test words"
        tokens = tp.tokenize_text(cleaned_for_words)
        assert tokens == ['hello', 'world', 'this', 'is', 'a', 'test', 'with', 'the', 'test', 'words']
        
        # Test remove_stop_words with default English list from config
        filtered_tokens, removed_count_test = tp.remove_stop_words(tokens, cfg.STOP_WORDS) 
        assert filtered_tokens == ['hello', 'world', 'test', 'test', 'words']
        assert removed_count_test == 5
        
        # Test count_words: no stop words (empty set)
        counts_no_sw = tp.count_words(test_text_proc, active_stop_words=set()) 
        assert counts_no_sw['test'] == 2 and counts_no_sw['hello'] == 1
        
        # Test count_words: with default stop words
        counts_with_sw = tp.count_words(test_text_proc, active_stop_words=cfg.STOP_WORDS) 
        assert counts_with_sw['test'] == 2 and 'is' not in counts_with_sw
        print("✅ Text processing functions passed assertions."); test_results['text_processing'] = True
    except AssertionError as e: print(f"❌ Text processing assertion failed: {e}")
    except Exception as e: print(f"❌ Text processing error: {e}")

    try:
        test_text_analysis: str = "First sentence. Second sentence is a bit longer, yes it is!"
        assert analysis.count_sentences(test_text_analysis) == 2
        sentence_analysis_res = analysis.analyze_sentences(test_text_analysis)
        assert sentence_analysis_res['sentence_count'] == 2 and sentence_analysis_res['average_words_per_sentence'] == 5.5
        
        # Test analyze_text_complete with no stop words (empty set)
        complete_results = analysis.analyze_text_complete(test_text_analysis, active_stop_words=set(), num_common_words_to_display=2)
        assert not complete_results.get('error')
        assert complete_results.get('general_stats', {}).get('sentence_count') == 2
        assert complete_results.get('general_stats', {}).get('word_count') == 11
        print("✅ Analysis functions passed assertions."); test_results['analysis'] = True
    except AssertionError as e: print(f"❌ Analysis assertion failed: {e}")
    except Exception as e: print(f"❌ Analysis error: {e}")

    try:
        assert callable(display.display_complete_analysis) and callable(display.display_summary) and callable(display.display_word_length_analysis)
        print("✅ Display functions are present and callable."); test_results['display'] = True
    except AssertionError: print("❌ Core display functions not found or not callable.")
    except Exception as e: print(f"❌ Display functions check error: {e}")
        
    display.print_section("🎯 Test Results Summary")
    all_passed: bool = all(test_results.values())
    for component, passed in test_results.items(): print(f"{component.replace('_', ' ').title()}: {'✅ PASS' if passed else '❌ FAIL'}")
    print("\n🎉 All tests passed!" if all_passed else "\n⚠️ Some tests failed. Please review errors.")
    return all_passed

def _handle_custom_file_option() -> None:
    custom_filepath_content = file_io.load_text_file()
    if custom_filepath_content:
        _perform_analysis_and_display(custom_filepath_content, "custom_analysis")
    else:
        print("❌ No content loaded from custom file. Returning to main menu.")

def _handle_analyze_file_option() -> None:
    filepath_config: str = str(cfg.FIXED_TARGET_FILEPATH)
    print(f"ℹ️ Analyzing fixed file: {filepath_config}")
    is_valid_path, path_message = file_io.validate_file_path(filepath_config)
    if not is_valid_path:
        print(f"❌ Error with fixed file path '{filepath_config}': {path_message}"); return
    content: Optional[str] = file_io.read_file(filepath_config) 
    if content is not None: _perform_analysis_and_display(content, Path(cfg.FIXED_TARGET_FILENAME).name) # Use filename for hint
    else: print(f"❌ No content loaded from '{filepath_config}'. Returning to main menu.")

def main() -> None:
    display.print_header("🚀 TEXT ANALYZER - COMPLETE VERSION 🚀")
    print("Welcome to the comprehensive text analysis tool!")
    
    while True:
        try:
            print("\n" + "="*50 + "\n📋 Main Menu\n" + "="*50)
            print("1. 📊 Analyze Fixed Text File") 
            print("2. 📂 Analyze Custom Text File")
            print("3. 🧪 Run System Tests")
            print("4. ❓ Help & Information")
            print("5. 🚪 Exit")
            print("="*50)
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1": _handle_analyze_file_option()
            elif choice == "2": _handle_custom_file_option()
            elif choice == "3": run_comprehensive_test()
            elif choice == "4":
                display.print_header("❓ HELP & INFORMATION ❓")
                print("This text analyzer can process text files and provide:")
                print("• Word frequency analysis")
                print("• Sentence structure analysis")
                print("• Readability assessment")
                print("• Pattern detection")
                print("• Keyword Extraction (RAKE)")
                print("• Professional formatting")
                print("• Graphical plots for key metrics")
                print("\nSupported file types:")
                print("• Plain text files (.txt)")
                print("• CSV files (.csv) - you'll be prompted for the column containing text.")
                print("• JSON files (.json) - you'll be prompted for the key containing the text.")
                print("\nStop Word Options:")
                print("• Use default English list, NLTK list for other languages, custom file, or no stop words.")
                print("\nFor best results:")
                print("• Keep files under 10MB")
                print("• Ensure UTF-8 or compatible (iso-8859-1) encoding")
            elif choice == "5": print("\n👋 Thank you for using Text Analyzer!"); break
            else: print("❌ Invalid choice. Please enter 1-5.")
        except KeyboardInterrupt: print("\n\n⚠️ Interrupted by user. Exiting."); break 
        except Exception as e: print(f"\n❌ An unexpected error occurred: {e}"); print("💡 Please try again.")

if __name__ == "__main__":
    main()
