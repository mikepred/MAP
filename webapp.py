from flask import Flask, render_template, request, jsonify # Added jsonify
import json 
from text_analyzer import analysis
from text_analyzer import config as ta_config
from collections import Counter

app = Flask(__name__)

# Function to format results (adapted from text_analyzer.gui.TextAnalyzerGUI._format_results)
def _format_web_results(results: dict, top_n: int, removed_stopwords_flag: bool, removed_stopwords_count_from_analysis: int) -> str:
    output = []
    output.append("===== TEXT ANALYSIS RESULTS =====")

    if results.get('error'):
        output.append(f"\nError during analysis: {results['error']}")
        return "\n".join(output)

    gs = results.get('general_stats', {})
    output.append("\n--- General Statistics ---")
    output.append(f"Raw Character Count: {gs.get('character_count', 'N/A')}")
    output.append(f"Character Count (no spaces): {gs.get('character_count_no_spaces', 'N/A')}")
    output.append(f"Word Count (analyzed): {gs.get('word_count', 'N/A')}") # This is total words after processing (e.g. stop word removal)
    output.append(f"Sentence Count: {gs.get('sentence_count', 'N/A')}")
    output.append(f"Paragraph Count: {gs.get('paragraph_count', 'N/A')}")
    
    # Use the actual count from analysis results
    actual_removed_count = results.get('word_analysis', {}).get('removed_stop_words_count', 0)
    if removed_stopwords_flag or actual_removed_count > 0 : # Show if flag was true or if words were actually removed
        output.append(f"Stop Words Removed: {actual_removed_count}")


    wa = results.get('word_analysis', {})
    wf = wa.get('word_frequencies', {}) # This should be the top_n words from analysis
    
    # The 'word_count' in 'general_stats' is the count *after* stop word removal (if applied),
    # so it's the correct base for frequency percentages of the analyzed words.
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
    # average_frequency from analysis.py's get_word_count_stats is available if desired:
    # output.append(f"Average Word Frequency (among unique words): {ws.get('average_frequency', 'N/A')}")


    sa = results.get('sentence_analysis', {})
    output.append("\n--- Sentence Analysis ---")
    output.append(f"Average Words per Sentence: {sa.get('average_words_per_sentence', 'N/A')}")
    
    longest_sentence_text = sa.get('longest_sentence', '')
    shortest_sentence_text = sa.get('shortest_sentence', '')
    output.append(f"Longest Sentence (words): {len(longest_sentence_text.split())} words ('{longest_sentence_text[:50]}...')")
    output.append(f"Shortest Sentence (words): {len(shortest_sentence_text.split())} words ('{shortest_sentence_text[:50]}...')")

    rs = results.get('readability_stats', {})
    output.append("\n--- Readability ---")
    output.append(f"Average Word Length: {rs.get('avg_word_length', 'N/A')} characters")
    # The prompt mentioned Flesch-Kincaid, but analysis.py provides 'complexity_score' and 'readability_level'
    # I will use what is available from analysis.py
    output.append(f"Complexity Score: {rs.get('complexity_score', 'N/A')}")
    output.append(f"Readability Level: {rs.get('readability_level', 'N/A')}")

    # Enhanced Readability Indices (Module 4G)
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
    
    all_std_indices_na = True
    for key, name in standard_indices.items():
        score = rs.get(key, 'N/A')
        output.append(f"    - {name}: {score}")
        if score != 'N/A':
            all_std_indices_na = False
    if all_std_indices_na and not readability_error:
        output.append("    (Standardized indices N/A, possibly due to short or unsuitable text.)")


    wlc = results.get('word_length_counts_obj', Counter())
    output.append("\n--- Word Length Distribution ---")
    if wlc:
        total_words_for_lengths = sum(wlc.values()) # This should be same as total_analyzed_words
        for length, count in sorted(wlc.items()):
            percentage = (count / total_words_for_lengths * 100) if total_words_for_lengths > 0 else 0
            output.append(f"Length {length}: {count} words ({percentage:.2f}%)")
    else:
        output.append("No word length data to display.")
    
    ip = results.get('interesting_patterns', {})
    output.append("\n--- Interesting Patterns ---")
    output.append(f"Word Variety (Unique/Total * 100): {ip.get('word_variety', 'N/A')}%")
    if ip.get('repeated_words'):
        output.append(f"Most Repeated Words (sample): {', '.join([f'{w}({c})' for w,c in ip.get('repeated_words', [])])}")
    if ip.get('long_words'):
        output.append(f"Long Words (sample, >=7 chars): {', '.join(ip.get('long_words', []))}")
    if ip.get('short_words'):
        output.append(f"Short Words (sample, <=2 chars): {', '.join(ip.get('short_words', []))}")

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
    elif not sentiment_data or 'compound' not in sentiment_data: # Check if essential data is missing
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
        if lex_density is not None: # Check if key exists, could be 0.0
             output.append(f"  Lexical Density: {lex_density:.2f}% (Percentage of content words)")
        else:
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
                    # Take up to 3 examples, shorten them if they are too long
                    display_examples = [ex[:30] + '...' if len(ex) > 30 else ex for ex in examples[:3]]
                    example_str = f" (e.g., {', '.join(display_examples)})"
                output.append(f"    - {entity_type}: {count} mentions{example_str}")

    return "\n".join(output)

@app.route('/')
def home():
    return render_template('index.html', results=None, error_message=None)

@app.route('/analyze', methods=['POST'])
def analyze_route(): # Renamed from 'analyze' to avoid conflict with the module
    text_content = None
    error_message_str = None # Renamed to avoid conflict with template variable name

    if 'file_input' in request.files and request.files['file_input'].filename != '':
        file = request.files['file_input']
        try:
            text_content = file.read().decode('utf-8')
        except Exception as e:
            error_message_str = f"Error reading file: {e}"
    elif 'text_input' in request.form and request.form['text_input'].strip() != '':
        text_content = request.form['text_input']
    else:
        error_message_str = "No text provided. Please paste text or upload a file."

    if error_message_str:
        return render_template('index.html', results=None, error_message=error_message_str)

    if text_content is None: 
        # This case should ideally be caught by the above, but as a fallback:
        return render_template('index.html', results=None, error_message="Error: Could not obtain text content.")

    top_n = ta_config.DEFAULT_TOP_WORDS_DISPLAY # Default value
    top_n_str = request.form.get('top_words')

    if top_n_str: # If top_words was provided
        try:
            top_n_candidate = int(top_n_str)
            if top_n_candidate <= 0:
                error_message_str = "Invalid input for 'Number of top words': Must be a positive integer."
            else:
                top_n = top_n_candidate
        except ValueError:
            error_message_str = "Invalid input for 'Number of top words': Must be an integer."
    # If top_n_str is empty or not provided, it will just use the default without error, which is fine.

    if error_message_str: # If an error was set due to top_words validation
        return render_template('index.html', results=None, error_message=error_message_str)

    remove_stopwords_flag = request.form.get('remove_stopwords') == 'true'

    analysis_results_dict = analysis.analyze_text_complete(
        text=text_content,
        use_stop_words=remove_stopwords_flag,
        num_common_words_to_display=top_n
    )

    if analysis_results_dict.get('error'):
        # Pass the error from analysis to the template
        return render_template('index.html', results=None, error_message=f"Analysis Error: {analysis_results_dict['error']}")

    # If there was a warning from input processing but analysis succeeded, we might want to show it.
    # For this iteration, successful analysis overrides prior input warnings.
    # To show both, the template logic would need to accommodate multiple messages.

    removed_stopwords_count_actual = analysis_results_dict.get('word_analysis', {}).get('removed_stop_words_count', 0)
    
    formatted_results_str = _format_web_results(
        analysis_results_dict, 
        top_n, 
        remove_stopwords_flag, 
        removed_stopwords_count_actual
    )

    # Extract data for chart
    labels = list(analysis_results_dict.get('word_analysis', {}).get('word_frequencies', {}).keys())
    data = list(analysis_results_dict.get('word_analysis', {}).get('word_frequencies', {}).values())

    # Extract sentiment data for pie chart
    sentiment_scores = analysis_results_dict.get('sentiment_analysis', {})
    sentiment_labels = ['Positive', 'Neutral', 'Negative']
    sentiment_data = [sentiment_scores.get('pos', 0.0), sentiment_scores.get('neu', 0.0), sentiment_scores.get('neg', 0.0)]

    # Extract word length distribution for bar chart
    word_length_counts = analysis_results_dict.get('word_length_counts_obj', Counter())
    if word_length_counts:
        sorted_lengths = sorted(word_length_counts.items())
        word_length_labels = [str(item[0]) for item in sorted_lengths]
        word_length_data = [item[1] for item in sorted_lengths]
    else:
        word_length_labels = []
        word_length_data = []
    
    return render_template(
        'index.html', 
        results=formatted_results_str, 
        error_message=error_message_str, # error_message_str would be None or an input warning
        word_freq_labels=json.dumps(labels),
        word_freq_data=json.dumps(data),
        sentiment_chart_labels=json.dumps(sentiment_labels),
        sentiment_chart_data=json.dumps(sentiment_data),
        word_len_labels=json.dumps(word_length_labels),
        word_len_data=json.dumps(word_length_data),
        original_text_content=text_content # Pass original text
    )

@app.route('/get_sentences', methods=['POST'])
def get_sentences_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    text_content = data.get('text_content')
    word = data.get('word')

    if not text_content or not word:
        return jsonify({'error': 'Missing text_content or word'}), 400

    found_sentences = analysis.get_sentences_for_word(text_content, word)
    return jsonify({'sentences': found_sentences})

if __name__ == '__main__':
    app.run(debug=True)
