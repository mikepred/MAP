import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
from collections import Counter # For type hinting and potentially direct use

# Import from the text_analyzer package
from . import text_processing as tp
from . import analysis
from . import display # Added for word cloud
from . import config as cfg # To access STOP_WORDS, default values etc.
from pathlib import Path # For Path objects
import subprocess # For opening files
import sys # For platform check


class TextAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Text Analyzer GUI")
        self.file_content = None # To store the content of the selected file
        self.analysis_results_store = None # To store the latest analysis results

        # File selection section
        self.file_frame = ttk.LabelFrame(master, text="File Selection")
        self.file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.open_button = ttk.Button(self.file_frame, text="Open File", command=self.open_file)
        self.open_button.grid(row=0, column=0, padx=5, pady=5)

        self.filepath_label = ttk.Label(self.file_frame, text="No file selected.")
        self.filepath_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.file_frame.columnconfigure(1, weight=1) # Allow filepath_label to expand

        # Text Input Section
        self.text_input_frame = ttk.LabelFrame(master, text="Paste Text Input")
        self.text_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.paste_box = scrolledtext.ScrolledText(self.text_input_frame, wrap=tk.WORD, width=78, height=10)
        self.paste_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.clear_paste_box_button = ttk.Button(self.text_input_frame, text="Clear Pasted Text", command=self.clear_paste_box)
        self.clear_paste_box_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.text_input_frame.rowconfigure(0, weight=1)
        self.text_input_frame.columnconfigure(0, weight=1)
        
        # Configuration section
        self.config_frame = ttk.LabelFrame(master, text="Configuration")
        self.config_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.top_words_label = ttk.Label(self.config_frame, text="Number of top words:")
        self.top_words_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.top_words_var = tk.StringVar(value=str(cfg.DEFAULT_TOP_WORDS_DISPLAY)) # Use config value
        self.top_words_entry = ttk.Entry(self.config_frame, textvariable=self.top_words_var, width=5)
        self.top_words_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.remove_stopwords_var = tk.BooleanVar(value=True)
        self.remove_stopwords_check = ttk.Checkbutton(
            self.config_frame, text="Remove stop words?", variable=self.remove_stopwords_var
        )
        self.remove_stopwords_check.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Analyze button
        self.analyze_button = ttk.Button(master, text="Analyze Text", command=self.analyze_text)
        self.analyze_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Results display area
        self.results_frame = ttk.LabelFrame(master, text="Results")
        self.results_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        
        self.results_text = scrolledtext.ScrolledText(self.results_frame, wrap=tk.WORD, width=80, height=20)
        self.results_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.results_frame.rowconfigure(0, weight=1)
        self.results_frame.columnconfigure(0, weight=1)


        # Save Results button
        self.save_button = ttk.Button(master, text="Save Results", command=self.save_results)
        self.save_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew") # Reduced pady for closer packing

        # Word Cloud Button
        self.word_cloud_button = ttk.Button(master, text="Generate Word Cloud", command=self._generate_word_cloud_gui)
        self.word_cloud_button.grid(row=6, column=0, padx=10, pady=5, sticky="ew")


        master.columnconfigure(0, weight=1)
        master.rowconfigure(4, weight=1) # Results frame
        master.rowconfigure(1, weight=1) # Text input frame

    def clear_paste_box(self):
        self.paste_box.delete('1.0', tk.END)
        # Optionally, also clear self.file_content if paste box was the source
        # For now, just clearing the box. Analysis logic will decide source.
        self.results_text.insert(tk.END, "Pasted text cleared.\n")


    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Open Text File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath:
            try:
                abs_filepath = os.path.abspath(filepath)
                with open(abs_filepath, 'r', encoding='utf-8') as f:
                    self.file_content = f.read()
                self.filepath_label.config(text=abs_filepath)
                self.results_text.delete('1.0', tk.END) # Clear previous results or errors
                self.results_text.insert(tk.END, f"File loaded: {abs_filepath}\n")
                self.paste_box.delete('1.0', tk.END) # Clear paste box content
            except Exception as e:
                self.file_content = None
                self.filepath_label.config(text="Error reading file.")
                self.results_text.delete('1.0', tk.END)
                self.results_text.insert(tk.END, f"Error reading file: {e}\n")
        else:
            # self.filepath_label.config(text="No file selected.") # Keep previous or set to this
            pass # If no file is selected, do nothing or update status

    def analyze_text(self):
        self.results_text.delete('1.0', tk.END) # Clear previous results
        
        current_text_to_analyze = None
        source_description = ""

        pasted_text = self.paste_box.get("1.0", tk.END).strip()

        if pasted_text:
            current_text_to_analyze = pasted_text
            self.file_content = pasted_text # Update internal state
            self.filepath_label.config(text="Using pasted text.")
            source_description = "pasted text"
        elif self.file_content:
            current_text_to_analyze = self.file_content
            # self.filepath_label is already set by open_file
            source_description = f"file: {self.filepath_label.cget('text')}"
        else:
            self.results_text.insert(tk.END, "Error: No text input. Please paste text or load a file.\n")
            return

        if not current_text_to_analyze: # Should be caught above, but as a safeguard
            self.results_text.insert(tk.END, "Error: No content to analyze.\n")
            return

        try:
            top_n_str = self.top_words_var.get()
            top_n = int(top_n_str)
            if top_n <= 0:
                raise ValueError("Number of top words must be a positive integer.")
        except ValueError as e:
            self.results_text.insert(tk.END, f"Error: Invalid input for 'Number of top words': {e}\n")
            return

        remove_stopwords_flag = self.remove_stopwords_var.get()
        
        try:
            self.results_text.insert(tk.END, "Starting analysis...\n")
            self.master.update_idletasks() # Refresh UI to show message

            # --- Perform Text Processing and Analysis ---
            # raw_text = self.file_content # Now using current_text_to_analyze
            
            # Word Analysis Stream
            text_for_words = tp.clean_text_for_word_tokenization(current_text_to_analyze, advanced=True)
            tokens = tp.tokenize_text(text_for_words)
            
            analyzed_tokens = tokens
            removed_stopwords_count = 0
            if remove_stopwords_flag:
                analyzed_tokens, removed_stopwords_count = tp.remove_stop_words(tokens)

            word_frequencies_counter = Counter(analyzed_tokens) # analysis.get_word_frequency equivalent
            
            # Sentence Analysis Stream
            # Using the functions from analysis.py which internally use text_processing
            # analyze_text_complete is quite comprehensive, let's use its components
            
            # Call the main analysis function from analysis.py
            # This function bundles many individual analysis steps.
            # Determine the actual set of stop words to use
            active_stop_words_set = cfg.STOP_WORDS if remove_stopwords_flag else set()

            self.analysis_results_store = analysis.analyze_text_complete( # Store results
                text=current_text_to_analyze,
                active_stop_words=active_stop_words_set, # Pass actual stop words
                num_common_words_to_display=top_n,
                user_patterns=None # Or implement UI for this
            )

            if self.analysis_results_store.get('error'):
                self.results_text.insert(tk.END, f"Analysis Error: {self.analysis_results_store['error']}\n")
                self.analysis_results_store = None # Clear results on error
                return

            # Format and display results
            # The removed_stopwords_count is now part of analysis_results_store
            actual_removed_count = self.analysis_results_store.get('word_analysis', {}).get('removed_stop_words_count', 0)
            formatted_output = self._format_results(self.analysis_results_store, top_n, remove_stopwords_flag, actual_removed_count)
            self.results_text.delete('1.0', tk.END) # Clear "Starting analysis..."
            self.results_text.insert(tk.END, formatted_output)

        except Exception as e:
            self.results_text.insert(tk.END, f"An unexpected error occurred during analysis: {e}\n")
            self.analysis_results_store = None # Clear results on error

    def _generate_word_cloud_gui(self):
        self.results_text.insert(tk.END, "\n\nAttempting to generate word cloud...\n")
        if not display.WORDCLOUD_AVAILABLE:
            self.results_text.insert(tk.END, "Error: WordCloud library not installed. Please install it (e.g., 'pip install wordcloud') to use this feature.\n")
            tk.messagebox.showerror("Word Cloud Error", "WordCloud library not installed. This feature is unavailable.")
            return

        if not self.analysis_results_store:
            self.results_text.insert(tk.END, "Error: No analysis results available. Please analyze some text first.\n")
            tk.messagebox.showinfo("Word Cloud Info", "No analysis results available. Please analyze some text first.")
            return

        word_frequencies = self.analysis_results_store.get('word_analysis', {}).get('full_word_counts_obj')
        if not word_frequencies: # Check if it's empty Counter or None
            self.results_text.insert(tk.END, "Error: No word frequencies found in the analysis results (perhaps all words were stop words or text was empty).\n")
            tk.messagebox.showinfo("Word Cloud Info", "No word frequencies found in the analysis results. Cannot generate word cloud.")
            return

        # Suggest a filename based on the source of the text
        source_desc = self.filepath_label.cget("text")
        base_filename = "word_cloud_output" # Default
        if source_desc and "Using pasted text" not in source_desc and "No file selected" not in source_desc and "Error reading file" not in source_desc:
            try:
                # Attempt to get a stem from the filepath_label if it's a valid path
                path_obj = Path(source_desc)
                if path_obj.is_file(): # Check if it's an actual file path
                    base_filename = path_obj.stem + "_word_cloud"
            except Exception:
                # If Path operations fail (e.g. source_desc is not a valid path string),
                # or if it's not a file, keep the default base_filename.
                pass


        save_path_str = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Word Cloud As",
            initialfile=f"{base_filename}.png" # Use the potentially updated base_filename
        )

        if not save_path_str:
            self.results_text.insert(tk.END, "Word cloud generation cancelled by user.\n")
            return

        save_path = Path(save_path_str)
        output_dir = save_path.parent
        filename_prefix = save_path.stem

        try:
            generated_image_path = display.generate_word_cloud(
                word_frequencies=word_frequencies,
                output_dir=output_dir,
                filename_prefix=filename_prefix
            )

            if generated_image_path:
                self.results_text.insert(tk.END, f"Word cloud saved to: {generated_image_path}\n")
                tk.messagebox.showinfo("Word Cloud Success", f"Word cloud saved to:\n{generated_image_path}")
                # Try to open the file
                try:
                    if sys.platform == "win32":
                        os.startfile(generated_image_path) # os.startfile is Windows specific
                    elif sys.platform == "darwin": # macOS
                        subprocess.run(["open", generated_image_path], check=True)
                    else: # Linux and other POSIX
                        subprocess.run(["xdg-open", generated_image_path], check=True)
                except FileNotFoundError as e_fnf: # Specific error for open/xdg-open not found
                    self.results_text.insert(tk.END, f"Could not automatically open image: Command not found ({e_fnf.filename}). Please open it manually.\n")
                    tk.messagebox.showwarning("Open Image", f"Could not automatically open the image: '{e_fnf.filename}' not found. Please open it manually from:\n{generated_image_path}")
                except subprocess.CalledProcessError as e_cpe: # Error from open/xdg-open
                    self.results_text.insert(tk.END, f"Error opening image with external program: {e_cpe}.\n")
                    tk.messagebox.showwarning("Open Image", f"Error opening image with external program: {e_cpe}.\nPlease open it manually from:\n{generated_image_path}")
                except Exception as e_open: # Other errors
                    self.results_text.insert(tk.END, f"Could not automatically open image: {e_open}\n")
                    tk.messagebox.showwarning("Open Image", f"Could not automatically open the image:\n{e_open}.\nPlease open it manually from:\n{generated_image_path}")
            else:
                # The display.generate_word_cloud function already prints to console.
                # This message is for the GUI text area.
                self.results_text.insert(tk.END, "Word cloud generation failed. Check console for details (WordCloud library might print errors there).\n")
                tk.messagebox.showerror("Word Cloud Error", "Word cloud generation failed. See console/terminal for specific errors from the WordCloud library.")
        except Exception as e: # Catch any other unexpected errors during the process
            self.results_text.insert(tk.END, f"Error during word cloud GUI operation: {e}\n")
            tk.messagebox.showerror("Word Cloud Error", f"An unexpected error occurred: {e}")

    def _format_results(self, results: dict, top_n: int, removed_stopwords_flag: bool, removed_stopwords_count: int) -> str:
        """Formats the analysis results for display in the GUI."""
        output = []
        output.append("===== TEXT ANALYSIS RESULTS =====")

        # General Statistics
        gs = results.get('general_stats', {})
        output.append("\n--- General Statistics ---")
        output.append(f"Raw Character Count: {gs.get('character_count', 'N/A')}")
        output.append(f"Character Count (no spaces): {gs.get('character_count_no_spaces', 'N/A')}")
        output.append(f"Word Count (analyzed): {gs.get('word_count', 'N/A')}") # This is from processed tokens
        output.append(f"Sentence Count: {gs.get('sentence_count', 'N/A')}")
        output.append(f"Paragraph Count: {gs.get('paragraph_count', 'N/A')}")
        if removed_stopwords_flag:
            output.append(f"Stop Words Removed: {removed_stopwords_count}")


        # Word Frequencies
        wa = results.get('word_analysis', {})
        wf = wa.get('word_frequencies', {}) # This is already limited by num_common_words_to_display in analyze_text_complete
        total_analyzed_words = gs.get('word_count', 0)
        output.append(f"\n--- Word Frequencies (Top {top_n}) ---")
        if wf:
            for word, count in wf.items():
                percentage = (count / total_analyzed_words * 100) if total_analyzed_words > 0 else 0
                output.append(f"{word}: {count} ({percentage:.2f}%)")
        else:
            output.append("No word frequencies to display.")
        
        ws = wa.get('statistics', {})
        output.append(f"\n--- Word Statistics ---")
        output.append(f"Unique Words: {ws.get('unique_words', 'N/A')}")
        output.append(f"Average Word Frequency: {ws.get('average_frequency', 'N/A')}")


        # Sentence Analysis
        sa = results.get('sentence_analysis', {})
        output.append("\n--- Sentence Analysis ---")
        output.append(f"Average Words per Sentence: {sa.get('average_words_per_sentence', 'N/A')}")
        output.append(f"Longest Sentence (words): {len(sa.get('longest_sentence', '').split())} words")
        # output.append(f"Longest Sentence: \"{sa.get('longest_sentence', 'N/A')}\"") # Can be too long for GUI
        output.append(f"Shortest Sentence (words): {len(sa.get('shortest_sentence', '').split())} words")
        # output.append(f"Shortest Sentence: \"{sa.get('shortest_sentence', 'N/A')}\"")


        # Readability
        rs = results.get('readability_stats', {})
        output.append("\n--- Readability ---")
        output.append(f"Average Word Length: {rs.get('avg_word_length', 'N/A')} characters")
        output.append(f"Complexity Score: {rs.get('complexity_score', 'N/A')}")
        output.append(f"Readability Level: {rs.get('readability_level', 'N/A')}")
        
        # Display Standardized Readability Indices (New for Module 4G)
        output.append("\n  Standardized Readability Indices:")
        standard_indices = {
            "flesch_reading_ease": "Flesch Reading Ease",
            "flesch_kincaid_grade": "Flesch-Kincaid Grade Level",
            "gunning_fog": "Gunning Fog Index",
            "smog_index": "SMOG Index",
            "coleman_liau_index": "Coleman-Liau Index",
            "dale_chall_readability_score": "Dale-Chall Readability Score",
            "automated_readability_index": "Automated Readability Index (ARI)"
        }
        readability_error = rs.get('error')
        if readability_error:
            output.append(f"    Note: {readability_error}")
        
        all_std_indices_na_gui = True
        for key, name in standard_indices.items():
            score = rs.get(key, 'N/A')
            output.append(f"    - {name}: {score}")
            if score != 'N/A':
                all_std_indices_na_gui = False
        if all_std_indices_na_gui and not readability_error:
            output.append("    (Standardized indices N/A, possibly due to short or unsuitable text.)")

        # Word Length Distribution
        # The 'word_length_counts_obj' is directly available in results
        wlc = results.get('word_length_counts_obj', Counter())
        output.append("\n--- Word Length Distribution ---")
        if wlc:
            total_words_for_lengths = sum(wlc.values())
            for length, count in sorted(wlc.items()):
                percentage = (count / total_words_for_lengths * 100) if total_words_for_lengths > 0 else 0
                output.append(f"Length {length}: {count} words ({percentage:.2f}%)")
        else:
            output.append("No word length data to display.")
            
        # Interesting Patterns
        ip = results.get('interesting_patterns', {})
        output.append("\n--- Pattern Analysis ---")
        output.append(f"Word Variety: {ip.get('word_variety', 'N/A')}%")
        
        repeated = ip.get('repeated_words', [])
        output.append(f"Most Repeated Words (sample):")
        if repeated:
            for word, count in repeated[:5]: # Show top 5
                 output.append(f"  '{word}': {count} times")
        else:
            output.append("  No significantly repeated words found.")

        long_words = ip.get('long_words', [])
        output.append(f"Long Words (sample, >=7 chars):")
        if long_words:
            output.append(f"  {', '.join(long_words[:5])}") # Show sample
        else:
            output.append("  No long words found.")

        # N-gram Frequencies (Module 4C)
        output.append("\n--- N-gram Frequencies ---")
        ngram_data = results.get('ngram_frequencies', {})
        if not ngram_data:
            output.append("N-gram data not available.")
        else:
            for ngram_type, ngrams_list in ngram_data.items():
                output.append(f"  {ngram_type.capitalize()}:")
                if ngrams_list:
                    for ngram, count in ngrams_list:
                        output.append(f"    - \"{ngram}\": {count}")
                else:
                    output.append(f"    No {ngram_type.lower()} found.")
        
        # Sentiment Analysis (Module 4D)
        output.append("\n--- Sentiment Analysis (VADER) ---")
        sentiment_data = results.get('sentiment_analysis', {})
        if sentiment_data.get('error'):
            output.append(f"Error in sentiment analysis: {sentiment_data['error']}")
        elif not sentiment_data or 'compound' not in sentiment_data:
            output.append("Sentiment data not available or incomplete.")
        else:
            output.append(f"  Positive Score: {sentiment_data.get('pos', 0.0):.3f}")
            output.append(f"  Neutral Score: {sentiment_data.get('neu', 0.0):.3f}")
            output.append(f"  Negative Score: {sentiment_data.get('neg', 0.0):.3f}")
            output.append(f"  Compound Score: {sentiment_data.get('compound', 0.0):.3f}")
            compound_score = sentiment_data.get('compound', 0.0)
            overall_sentiment = "Neutral"
            if compound_score >= 0.05:
                overall_sentiment = "Positive"
            elif compound_score <= -0.05:
                overall_sentiment = "Negative"
            output.append(f"  Overall Sentiment: {overall_sentiment}")

        # Part-of-Speech (POS) Tagging (Module 4E & 4H)
        output.append("\n--- Part-of-Speech (POS) Tagging (spaCy) ---")
        pos_data = results.get('pos_analysis', {})
        if pos_data.get('error'):
            output.append(f"Error in POS analysis: {pos_data['error']}")
        elif not pos_data or pos_data.get('total_pos_tags', 0) == 0:
            output.append("POS data not available or no tags found.")
        else:
            output.append(f"  Total POS Tags (excluding punctuation/spaces): {pos_data.get('total_pos_tags', 0):,}")
            if pos_data.get('most_common_pos'):
                output.append("  Most Common POS Tags:")
                for tag, count in pos_data['most_common_pos']:
                    percentage = (count / pos_data['total_pos_tags'] * 100) if pos_data['total_pos_tags'] > 0 else 0
                    output.append(f"    - {tag}: {count} ({percentage:.1f}%)")
            
            lex_density = pos_data.get('lexical_density')
            if lex_density is not None:
                 output.append(f"  Lexical Density: {lex_density:.2f}% (Percentage of content words)")
            else: # Should have default 0.0 from analysis if POS was ok
                output.append("  Lexical Density: N/A")


        # Named Entity Recognition (NER) (Module 4F)
        output.append("\n--- Named Entity Recognition (NER) (spaCy) ---")
        ner_data = results.get('ner_analysis', {})
        if ner_data.get('error'):
            output.append(f"Error in NER analysis: {ner_data['error']}")
        elif not ner_data or ner_data.get('total_entities', 0) == 0:
            output.append("NER data not available or no entities found.")
        else:
            output.append(f"  Total Named Entity Mentions: {ner_data.get('total_entities', 0):,}")
            if ner_data.get('most_common_entity_types'):
                output.append("  Most Common Entity Types:")
                entities_by_type = ner_data.get('entities_by_type', {})
                for entity_type, count in ner_data['most_common_entity_types']:
                    examples = entities_by_type.get(entity_type, [])
                    example_str = ""
                    if examples:
                        display_examples = [ex[:30] + '...' if len(ex) > 30 else ex for ex in examples[:3]]
                        example_str = f" (e.g., {', '.join(display_examples)})"
                    output.append(f"    - {entity_type}: {count} mentions{example_str}")
        
        return "\n".join(output)

    def save_results(self):
        results_content = self.results_text.get("1.0", tk.END).strip()
        if not results_content or results_content == "Save Results button clicked. Functionality to be implemented.":
            self.results_text.insert(tk.END, "\n\nNo results to save.\n")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Analysis Results",
            initialfile="analysis_results.txt"
        )

        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(results_content)
                self.results_text.insert(tk.END, f"\n\nResults saved successfully to {filepath}\n")
            except Exception as e:
                self.results_text.insert(tk.END, f"\n\nError saving file: {e}\n")
        else:
            self.results_text.insert(tk.END, "\n\nSave operation cancelled.\n")


if __name__ == '__main__':
    root = tk.Tk()
    app = TextAnalyzerGUI(root)
    root.mainloop()
