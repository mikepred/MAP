import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import os
from collections import Counter # For type hinting and potentially direct use

# Import from the text_analyzer package
from . import text_processing as tp
from . import analysis
from . import config as cfg # To access STOP_WORDS, default values etc.


class TextAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Text Analyzer GUI")
        self.file_content = None # To store the content of the selected file

        # File selection section
        self.file_frame = ttk.LabelFrame(master, text="File Selection")
        self.file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.open_button = ttk.Button(self.file_frame, text="Open File", command=self.open_file)
        self.open_button.grid(row=0, column=0, padx=5, pady=5)

        self.filepath_label = ttk.Label(self.file_frame, text="No file selected.")
        self.filepath_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.file_frame.columnconfigure(1, weight=1) # Allow filepath_label to expand

        # Configuration section
        self.config_frame = ttk.LabelFrame(master, text="Configuration")
        self.config_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

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
        self.analyze_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Results display area
        self.results_frame = ttk.LabelFrame(master, text="Results")
        self.results_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        
        self.results_text = scrolledtext.ScrolledText(self.results_frame, wrap=tk.WORD, width=80, height=20)
        self.results_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.results_frame.rowconfigure(0, weight=1)
        self.results_frame.columnconfigure(0, weight=1)


        # Save Results button
        self.save_button = ttk.Button(master, text="Save Results", command=self.save_results)
        self.save_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        master.columnconfigure(0, weight=1)
        master.rowconfigure(3, weight=1)

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

        if not self.file_content:
            self.results_text.insert(tk.END, "Error: Please load a file first.\n")
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
            raw_text = self.file_content
            
            # Word Analysis Stream
            text_for_words = tp.clean_text_for_word_tokenization(raw_text, advanced=True)
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
            analysis_results = analysis.analyze_text_complete(
                text=raw_text,
                use_stop_words=remove_stopwords_flag,
                num_common_words_to_display=top_n
            )

            if analysis_results.get('error'):
                self.results_text.insert(tk.END, f"Analysis Error: {analysis_results['error']}\n")
                return

            # Format and display results
            formatted_output = self._format_results(analysis_results, top_n, remove_stopwords_flag, removed_stopwords_count)
            self.results_text.delete('1.0', tk.END) # Clear "Starting analysis..."
            self.results_text.insert(tk.END, formatted_output)

        except Exception as e:
            self.results_text.insert(tk.END, f"An unexpected error occurred during analysis: {e}\n")

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
