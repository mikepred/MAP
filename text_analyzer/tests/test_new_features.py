import unittest
from unittest import mock # For mock.patch and call_count
from collections import Counter
from pathlib import Path
import os
import re
import json
import csv
import tempfile # For temporary directory

# Import functions and classes from the text_analyzer package
from text_analyzer import analysis
from text_analyzer import display
from text_analyzer import file_io
from text_analyzer import config as cfg # For default config values if needed

# Mock spacy if it's not actually installed in the test environment,
# or to control its behavior precisely.
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    spacy = mock.MagicMock() # If spacy is not installed, mock it.
    # Mock specific spacy functionalities if needed by analysis._get_nlp_model
    spacy.load = mock.MagicMock(return_value="mocked_spacy_model_instance")
    SPACY_AVAILABLE = False


# Helper function to get the project root if needed for loading test data,
# but for this task, we'll mostly generate data in tests.
def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent # Adjust based on test file location

# Ensure matplotlib uses a non-GUI backend for tests
import matplotlib
matplotlib.use('Agg')


class TestAnalysisOptimizations(unittest.TestCase):
    def setUp(self):
        # Reset global NLP model in analysis module before each test
        analysis._nlp_model = None

    @mock.patch('spacy.load')
    def test_get_nlp_model_loads_and_caches(self, mock_spacy_load):
        if not SPACY_AVAILABLE and not isinstance(spacy.load, mock.MagicMock):
             self.skipTest("spaCy library not available and not easily mockable for this specific test structure if module-level mock failed.")

        mock_model_instance = "mocked_spacy_model_instance"
        mock_spacy_load.return_value = mock_model_instance

        # First call
        model1 = analysis._get_nlp_model()
        self.assertEqual(model1, mock_model_instance)
        self.assertEqual(mock_spacy_load.call_count, 1)
        self.assertEqual(analysis._nlp_model, mock_model_instance)

        # Second call
        model2 = analysis._get_nlp_model()
        self.assertEqual(model2, mock_model_instance)
        self.assertEqual(mock_spacy_load.call_count, 1) # Should still be 1 (cached)

        analysis._nlp_model = None # Cleanup

    @mock.patch('spacy.load')
    def test_get_nlp_model_handles_load_error(self, mock_spacy_load):
        if not SPACY_AVAILABLE and not isinstance(spacy.load, mock.MagicMock):
            self.skipTest("spaCy library not available and not easily mockable for this specific test structure.")

        mock_spacy_load.side_effect = OSError("Simulated spaCy model loading error")

        # Suppress print statements during this test
        with mock.patch('builtins.print'):
            model = analysis._get_nlp_model()

        self.assertIsNone(model)
        self.assertIsNone(analysis._nlp_model) # Should remain None or be reset to None
        mock_spacy_load.assert_called_once()

        analysis._nlp_model = None # Cleanup

    def test_find_interesting_patterns_output(self):
        word_counts_sample = Counter({
            'example': 5, 'test': 3, 'words': 4, 'another': 2, 'longwordexample': 1,
            'short': 1, 'a': 10, 'b': 1, 'is': 1, 'pattern': 1, 'error': 1
        })
        # text_sample is used for regex matching, not for word_counts based patterns directly
        text_sample = "This is an example test with some words. Phone: 123-456-7890. Another pattern here. ID-ABC. Invalid-Pattern-Test"

        user_patterns_sample = [
            {'name': 'Phone Numbers', 'regex': r'\d{3}-\d{3}-\d{4}'},
            {'name': 'IDs', 'regex': r'ID-[A-Z]+'},
            {'name': 'InvalidRegex', 'regex': r'('} # Invalid regex
        ]

        # Mock cfg values if they are not directly accessible or to control test
        original_cfg_defaults = {
            'DEFAULT_PATTERNS_REPEATED_WORDS_COUNT': cfg.DEFAULT_PATTERNS_REPEATED_WORDS_COUNT,
            'DEFAULT_PATTERNS_LONG_WORDS_SAMPLE_SIZE': cfg.DEFAULT_PATTERNS_LONG_WORDS_SAMPLE_SIZE,
            'DEFAULT_PATTERNS_SHORT_WORDS_SAMPLE_SIZE': cfg.DEFAULT_PATTERNS_SHORT_WORDS_SAMPLE_SIZE,
            'DEFAULT_PATTERN_MATCH_LIMIT': cfg.DEFAULT_PATTERN_MATCH_LIMIT,
            'COMMON_PATTERNS': cfg.COMMON_PATTERNS.copy()
        }
        cfg.DEFAULT_PATTERNS_REPEATED_WORDS_COUNT = 3
        cfg.DEFAULT_PATTERNS_LONG_WORDS_SAMPLE_SIZE = 1
        cfg.DEFAULT_PATTERNS_SHORT_WORDS_SAMPLE_SIZE = 2
        cfg.DEFAULT_PATTERN_MATCH_LIMIT = 2
        cfg.COMMON_PATTERNS = {"TestCommonURL": r'http[s]?://example.com'}


        patterns_data = analysis.find_interesting_patterns(word_counts_sample, text_sample, user_patterns_sample)

        expected_keys = ['repeated_words', 'long_words', 'short_words', 'word_variety',
                         'common_patterns', 'user_defined_pattern_results']
        for key in expected_keys:
            self.assertIn(key, patterns_data)

        self.assertIsInstance(patterns_data['repeated_words'], list)
        if patterns_data['repeated_words']: # It might be empty if no word count > 1
            self.assertIsInstance(patterns_data['repeated_words'][0], tuple)

        self.assertIsInstance(patterns_data['long_words'], list)
        self.assertIsInstance(patterns_data['short_words'], list)
        self.assertIsInstance(patterns_data['user_defined_pattern_results'], dict)

        # Specific content checks
        # Note: long_words/short_words are sorted alphabetically then sliced
        self.assertEqual(patterns_data['long_words'], ['longwordexample']) # 'longwordexample' > 'example' > 'another'

        # Based on current logic: short_word_candidates = ['a', 'b'], sorted -> ['a', 'b'], sliced to 2 -> ['a', 'b']
        self.assertEqual(sorted(patterns_data['short_words']), sorted(['a', 'b']))


        user_results = patterns_data['user_defined_pattern_results']
        self.assertIn('Phone Numbers', user_results)
        self.assertEqual(user_results['Phone Numbers'], ['123-456-7890'])
        self.assertIn('IDs', user_results)
        self.assertEqual(user_results['IDs'], ['ID-ABC'])
        self.assertIn('InvalidRegex', user_results)
        self.assertIn('error', user_results['InvalidRegex'])

        # Restore original cfg values
        cfg.DEFAULT_PATTERNS_REPEATED_WORDS_COUNT = original_cfg_defaults['DEFAULT_PATTERNS_REPEATED_WORDS_COUNT']
        cfg.DEFAULT_PATTERNS_LONG_WORDS_SAMPLE_SIZE = original_cfg_defaults['DEFAULT_PATTERNS_LONG_WORDS_SAMPLE_SIZE']
        cfg.DEFAULT_PATTERNS_SHORT_WORDS_SAMPLE_SIZE = original_cfg_defaults['DEFAULT_PATTERNS_SHORT_WORDS_SAMPLE_SIZE']
        cfg.DEFAULT_PATTERN_MATCH_LIMIT = original_cfg_defaults['DEFAULT_PATTERN_MATCH_LIMIT']
        cfg.COMMON_PATTERNS = original_cfg_defaults['COMMON_PATTERNS']

    @mock.patch('text_analyzer.analysis.Rake')
    def test_extract_keywords_rake_success(self, MockRake):
        if not analysis.RAKE_AVAILABLE:
            self.skipTest("RAKE library (rake-nltk) not available.")

        mock_rake_instance = MockRake.return_value
        # Rake().extract_keywords_from_text() doesn't return anything.
        # Rake().get_ranked_phrases_with_scores() returns the keywords.
        mock_rake_instance.get_ranked_phrases_with_scores.return_value = [
            (12.5, "important keyword"),
            (8.0, "another phrase")
        ]
        
        sample_text = "This text has an important keyword and another phrase."
        keywords = analysis.extract_keywords_rake(sample_text, num_keywords=2)

        MockRake.assert_called_once() # Ensure Rake was instantiated
        mock_rake_instance.extract_keywords_from_text.assert_called_once_with(sample_text)
        mock_rake_instance.get_ranked_phrases_with_scores.assert_called_once()
        
        self.assertEqual(len(keywords), 2)
        self.assertEqual(keywords[0], (12.5, "important keyword"))
        self.assertEqual(keywords[1], (8.0, "another phrase"))

    def test_extract_keywords_rake_empty_text(self):
        if not analysis.RAKE_AVAILABLE:
            self.skipTest("RAKE library not available.")
        
        # Suppress print for "No keywords found" message
        with mock.patch('builtins.print'):
            keywords = analysis.extract_keywords_rake("", num_keywords=5)
        self.assertEqual(keywords, [])

    @mock.patch('text_analyzer.analysis.RAKE_AVAILABLE', False)
    def test_extract_keywords_rake_library_unavailable(self):
        with mock.patch('builtins.print') as mock_print: # Suppress print for error message
            keywords = analysis.extract_keywords_rake("Some text.", num_keywords=5)
        self.assertEqual(keywords, [])
        mock_print.assert_any_call("RAKE keyword extraction is not available. Please install rake-nltk.")


class TestDisplayFeatures(unittest.TestCase):
    def setUp(self):
        self.test_output_dir = Path(tempfile.mkdtemp(prefix="ta_test_display_"))

    def tearDown(self):
        # Cleanup: Remove all files in test_output_dir and the directory itself
        for item in self.test_output_dir.iterdir():
            item.unlink()
        self.test_output_dir.rmdir()

    @mock.patch('text_analyzer.display.WordCloud') # Patch within the display module
    def test_generate_word_cloud_success(self, MockWordCloud):
        if not display.WORDCLOUD_AVAILABLE: # Check the flag in display module
            self.skipTest("WordCloud library not available, skipping dependent test.")

        mock_wc_instance = MockWordCloud.return_value
        mock_wc_instance.to_file = mock.MagicMock()

        sample_freq = Counter({'test': 5, 'example': 3})

        result_path = display.generate_word_cloud(sample_freq, self.test_output_dir, "test_cloud")

        self.assertIsNotNone(result_path)
        self.assertTrue(Path(result_path).name.startswith("test_cloud"))
        self.assertTrue(Path(result_path).name.endswith(".png"))
        MockWordCloud.assert_called_once() # Check if WordCloud constructor was called
        mock_wc_instance.generate_from_frequencies.assert_called_once_with(dict(sample_freq))
        mock_wc_instance.to_file.assert_called_once()


    def test_generate_word_cloud_empty_frequencies(self):
        if not display.WORDCLOUD_AVAILABLE:
            self.skipTest("WordCloud library not available.")
        # Suppress print statements during this test
        with mock.patch('builtins.print'):
            result = display.generate_word_cloud(Counter(), self.test_output_dir)
        self.assertIsNone(result)

    @mock.patch('text_analyzer.display.WORDCLOUD_AVAILABLE', False)
    def test_generate_word_cloud_library_unavailable(self):
         # Suppress print statements during this test
        with mock.patch('builtins.print'):
            result = display.generate_word_cloud(Counter({'test': 1}), self.test_output_dir)
        self.assertIsNone(result)

    @mock.patch('matplotlib.pyplot.figure')
    @mock.patch('matplotlib.pyplot.bar')
    @mock.patch('matplotlib.pyplot.title')
    @mock.patch('matplotlib.pyplot.xlabel')
    @mock.patch('matplotlib.pyplot.ylabel')
    @mock.patch('matplotlib.pyplot.xticks')
    @mock.patch('matplotlib.pyplot.tight_layout')
    @mock.patch('matplotlib.pyplot.savefig')
    @mock.patch('matplotlib.pyplot.close')
    def test_plot_word_frequencies_calls_matplotlib(self, mock_close, mock_savefig, mock_tight_layout, mock_xticks, mock_ylabel, mock_xlabel, mock_title, mock_bar, mock_figure):
        sample_freq = Counter({'test': 5, 'example': 3, 'another': 10})
        filename_base = str(self.test_output_dir / "word_freq_plot")
        
        returned_path = display.plot_word_frequencies(sample_freq, 2, filename_base)

        mock_figure.assert_called_once()
        mock_bar.assert_called_once()
        mock_title.assert_called_once()
        mock_xlabel.assert_called_once()
        mock_ylabel.assert_called_once()
        mock_xticks.assert_called_once()
        mock_tight_layout.assert_called_once()
        mock_savefig.assert_called_once_with(filename_base + "_top_2.png")
        mock_close.assert_called_once()
        self.assertEqual(returned_path, filename_base + "_top_2.png")

    @mock.patch('matplotlib.pyplot.figure')
    @mock.patch('matplotlib.pyplot.hist')
    @mock.patch('matplotlib.pyplot.title')
    @mock.patch('matplotlib.pyplot.xlabel')
    @mock.patch('matplotlib.pyplot.ylabel')
    @mock.patch('matplotlib.pyplot.tight_layout')
    @mock.patch('matplotlib.pyplot.savefig')
    @mock.patch('matplotlib.pyplot.close')
    def test_plot_word_length_distribution_calls_matplotlib(self, mock_close, mock_savefig, mock_tight_layout, mock_ylabel, mock_xlabel, mock_title, mock_hist, mock_figure):
        word_lengths = [1, 2, 2, 3, 3, 3, 4, 4, 5]
        filename_base = str(self.test_output_dir / "word_len_plot")

        returned_path = display.plot_word_length_distribution(word_lengths, filename_base)
        
        mock_figure.assert_called_once()
        mock_hist.assert_called_once()
        mock_title.assert_called_once()
        mock_xlabel.assert_called_once()
        mock_ylabel.assert_called_once()
        mock_tight_layout.assert_called_once()
        mock_savefig.assert_called_once_with(filename_base + "_dist.png")
        mock_close.assert_called_once()
        self.assertEqual(returned_path, filename_base + "_dist.png")

    @mock.patch('matplotlib.pyplot.figure')
    @mock.patch('matplotlib.pyplot.bar') # Assuming bar chart for sentiment
    @mock.patch('matplotlib.pyplot.title')
    @mock.patch('matplotlib.pyplot.xlabel')
    @mock.patch('matplotlib.pyplot.ylabel')
    @mock.patch('matplotlib.pyplot.tight_layout')
    @mock.patch('matplotlib.pyplot.savefig')
    @mock.patch('matplotlib.pyplot.close')
    def test_plot_sentiment_distribution_calls_matplotlib(self, mock_close, mock_savefig, mock_tight_layout, mock_ylabel, mock_xlabel, mock_title, mock_bar, mock_figure):
        # This test assumes plot_sentiment_distribution takes a dictionary of sentiment scores
        # The actual implementation might take raw scores or processed data.
        # For this example, let's assume it takes a dictionary like VADER's output.
        sentiment_scores = {'neg': 0.1, 'neu': 0.6, 'pos': 0.3, 'compound': 0.75}
        filename_base = str(self.test_output_dir / "sentiment_plot")

        returned_path = display.plot_sentiment_distribution(sentiment_scores, filename_base)

        mock_figure.assert_called_once()
        mock_bar.assert_called_once() # Or hist, depending on implementation
        mock_title.assert_called_once()
        # xlabel/ylabel might not be called if the plot is simple
        # mock_xlabel.assert_called_once()
        # mock_ylabel.assert_called_once()
        mock_tight_layout.assert_called_once()
        mock_savefig.assert_called_once_with(filename_base + "_dist.png")
        mock_close.assert_called_once()
        self.assertEqual(returned_path, filename_base + "_dist.png")


class TestFileIOFeatures(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_output_dir = Path(self.temp_dir.name)
        # Sample analysis_results structure (simplified)
        self.sample_results = {
            'general_stats': {'word_count': 100, 'sentence_count': 5},
            'word_analysis': {
                'word_frequencies': {'hello': 10, 'world': 8, 'test': 12}, # Already top N
                'statistics': {'unique_words': 50, 'total_words': 100, 'average_frequency': 2.0},
                'full_word_counts_obj': Counter({'hello': 10, 'world': 8, 'test': 12, 'other': 5}) # For JSON
            },
            'sentiment_analysis': {'pos': 0.5, 'neu': 0.4, 'neg': 0.1, 'compound': 0.8},
            'ngram_frequencies': {
                'bigrams': [('hello world', 5), ('world test', 3)],
                'trigrams': [('hello world test', 2)]
            },
            # Add other sections as needed by save functions
            'sentence_analysis': {}, 'readability_stats': {},
            'interesting_patterns': {}, 'pos_analysis': {}, 'ner_analysis': {}, 'keyword_analysis': []
        }


    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_results_to_json(self):
        filepath = self.test_output_dir / "results.json"
        file_io._save_results_to_json(self.sample_results, filepath)

        self.assertTrue(filepath.exists())
        with open(filepath, 'r') as f:
            loaded_data = json.load(f)

        # Counters should be dicts in JSON
        self.assertEqual(loaded_data['word_analysis']['full_word_counts_obj'],
                         dict(self.sample_results['word_analysis']['full_word_counts_obj']))
        self.assertEqual(loaded_data['general_stats'], self.sample_results['general_stats'])

    def test_save_results_to_csv(self):
        filepath = self.test_output_dir / "results.csv"
        file_io._save_results_to_csv(self.sample_results, filepath)

        self.assertTrue(filepath.exists())
        with open(filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.assertIn(["Section", "Metric", "Value"], rows) # Header for General Stats
        self.assertIn(["General Statistics", "word_count", "100"], rows)
        self.assertIn(["Section", "Word", "Count", "Percentage"], rows) # Header for Word Freq
        self.assertIn(["Word Frequencies", "hello", "10", mock.ANY], rows) # Percentage is float
        self.assertIn(["Section", "Sentiment Metric", "Score"], rows)
        self.assertIn(["Sentiment Analysis", "Compound Score", "0.8"], rows)
        self.assertIn(["Section", "N-gram Type", "N-gram", "Count"], rows)
        self.assertIn(["N-gram Frequencies", "Bigrams", "hello world", "5"], rows)

    @mock.patch('text_analyzer.file_io._save_results_to_txt')
    @mock.patch('text_analyzer.file_io._save_results_to_json')
    @mock.patch('text_analyzer.file_io._save_results_to_csv')
    def test_save_analysis_results_dispatcher(self, mock_save_csv, mock_save_json, mock_save_txt):
        output_filename = str(self.test_output_dir / "dispatch_test")

        file_io.save_analysis_results(self.sample_results, output_filename + ".txt", format_choice='txt')
        mock_save_txt.assert_called_once_with(self.sample_results, Path(output_filename + ".txt"))
        mock_save_json.assert_not_called()
        mock_save_csv.assert_not_called()
        mock_save_txt.reset_mock()

        file_io.save_analysis_results(self.sample_results, output_filename + ".json", format_choice='json')
        mock_save_json.assert_called_once_with(self.sample_results, Path(output_filename + ".json"))
        mock_save_txt.assert_not_called()
        mock_save_csv.assert_not_called()
        mock_save_json.reset_mock()

        file_io.save_analysis_results(self.sample_results, output_filename + ".csv", format_choice='csv')
        mock_save_csv.assert_called_once_with(self.sample_results, Path(output_filename + ".csv"))
        mock_save_txt.assert_not_called()
        mock_save_json.assert_not_called()
        mock_save_csv.reset_mock()

        # Test fallback to txt for unsupported format
        with mock.patch('builtins.print'): # Suppress print for error message
            file_io.save_analysis_results(self.sample_results, output_filename + ".dat", format_choice='dat')
        mock_save_txt.assert_called_once_with(self.sample_results, Path(output_filename + ".dat.txt")) # Check suffix adjustment

    @mock.patch('nltk.corpus.stopwords.words')
    def test_get_nltk_stopwords_success(self, mock_nltk_stopwords):
        mock_nltk_stopwords.return_value = ['stop', 'word', 'list']
        stopwords = file_io.get_nltk_stopwords('english')
        self.assertEqual(stopwords, ['stop', 'word', 'list'])
        mock_nltk_stopwords.assert_called_once_with('english')

    @mock.patch('nltk.corpus.stopwords.words', side_effect=LookupError("NLTK resource not found"))
    def test_get_nltk_stopwords_resource_not_found(self, mock_nltk_stopwords):
        with mock.patch('builtins.print') as mock_print:
            stopwords = file_io.get_nltk_stopwords('fantasy_language')
        self.assertIsNone(stopwords)
        mock_print.assert_any_call(mock.ANY) # Check that some error was printed

    def test_load_custom_stopwords_success(self):
        custom_stopwords_content = "custom\nstop\nword\n"
        stopwords_filepath = self.test_output_dir / "custom_stops.txt"
        with open(stopwords_filepath, 'w') as f:
            f.write(custom_stopwords_content)
        
        stopwords = file_io.load_custom_stopwords(str(stopwords_filepath))
        self.assertEqual(stopwords, {"custom", "stop", "word"})

    def test_load_custom_stopwords_file_not_found(self):
        with mock.patch('builtins.print') as mock_print:
            stopwords = file_io.load_custom_stopwords(str(self.test_output_dir / "non_existent_stops.txt"))
        self.assertIsNone(stopwords)
        mock_print.assert_any_call(mock.ANY)

    def test_load_custom_stopwords_empty_file(self):
        stopwords_filepath = self.test_output_dir / "empty_stops.txt"
        with open(stopwords_filepath, 'w') as f:
            f.write("") # Empty file
        
        stopwords = file_io.load_custom_stopwords(str(stopwords_filepath))
        self.assertEqual(stopwords, set())

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

# Example of how to run specific tests or suites if needed:
# suite = unittest.TestSuite()
# suite.addTest(TestAnalysisOptimizations('test_get_nlp_model_loads_and_caches'))
# runner = unittest.TextTestRunner()
# runner.run(suite)

    def test_load_text_from_csv_success_specific_column(self):
        csv_content = "id,text_content,other_data\n1,Hello world,data1\n2,Another line,data2"
        csv_filepath = self.test_output_dir / "sample.csv"
        with open(csv_filepath, 'w', newline='') as f:
            f.write(csv_content)

        loaded_text = file_io.load_text_from_csv(str(csv_filepath), text_column_name="text_content")
        self.assertEqual(loaded_text, "Hello world\nAnother line")

    def test_load_text_from_csv_success_default_column(self):
        csv_content = "First column text\nSome more text"
        csv_filepath = self.test_output_dir / "sample_default.csv"
        with open(csv_filepath, 'w', newline='') as f:
            f.write(csv_content)
        
        loaded_text = file_io.load_text_from_csv(str(csv_filepath)) # Default column (index 0)
        self.assertEqual(loaded_text, "First column text\nSome more text")

    def test_load_text_from_csv_different_delimiter(self):
        csv_content = "id;text_content;other_data\n1;Hello;data1\n2;World;data2"
        csv_filepath = self.test_output_dir / "sample_semi.csv"
        with open(csv_filepath, 'w', newline='') as f:
            f.write(csv_content)

        loaded_text = file_io.load_text_from_csv(str(csv_filepath), text_column_name="text_content", delimiter=';')
        self.assertEqual(loaded_text, "Hello\nWorld")

    def test_load_text_from_csv_column_not_found(self):
        csv_content = "id,data\n1,val1"
        csv_filepath = self.test_output_dir / "sample_bad_col.csv"
        with open(csv_filepath, 'w', newline='') as f:
            f.write(csv_content)
        
        with mock.patch('builtins.print') as mock_print: # Suppress error print
            loaded_text = file_io.load_text_from_csv(str(csv_filepath), text_column_name="non_existent_column")
        self.assertIsNone(loaded_text)
        mock_print.assert_called()

    def test_load_text_from_csv_file_not_found(self):
        with mock.patch('builtins.print') as mock_print: # Suppress error print
            loaded_text = file_io.load_text_from_csv(str(self.test_output_dir / "non_existent.csv"))
        self.assertIsNone(loaded_text)
        mock_print.assert_called()

    def test_load_text_from_json_success_specific_key(self):
        json_content = {"title": "My Doc", "content": "This is the main text."}
        json_filepath = self.test_output_dir / "sample.json"
        with open(json_filepath, 'w') as f:
            json.dump(json_content, f)

        loaded_text = file_io.load_text_from_json(str(json_filepath), text_key="content")
        self.assertEqual(loaded_text, "This is the main text.")

    def test_load_text_from_json_success_nested_key(self):
        json_content = {"document": {"metadata": {"title": "Nested"}, "body": "Text from nested key."}}
        json_filepath = self.test_output_dir / "sample_nested.json"
        with open(json_filepath, 'w') as f:
            json.dump(json_content, f)
        
        loaded_text = file_io.load_text_from_json(str(json_filepath), text_key="document.body")
        self.assertEqual(loaded_text, "Text from nested key.")

    def test_load_text_from_json_list_of_strings(self):
        json_content = {"paragraphs": ["First paragraph.", "Second paragraph."]}
        json_filepath = self.test_output_dir / "sample_list.json"
        with open(json_filepath, 'w') as f:
            json.dump(json_content, f)

        loaded_text = file_io.load_text_from_json(str(json_filepath), text_key="paragraphs")
        self.assertEqual(loaded_text, "First paragraph.\nSecond paragraph.")
        
    def test_load_text_from_json_key_not_found(self):
        json_content = {"title": "My Doc"}
        json_filepath = self.test_output_dir / "sample_bad_key.json"
        with open(json_filepath, 'w') as f:
            json.dump(json_content, f)

        with mock.patch('builtins.print') as mock_print:
            loaded_text = file_io.load_text_from_json(str(json_filepath), text_key="content")
        self.assertIsNone(loaded_text)
        mock_print.assert_called()

    def test_load_text_from_json_malformed(self):
        json_filepath = self.test_output_dir / "sample_malformed.json"
        with open(json_filepath, 'w') as f:
            f.write("{'invalid_json': ") # Malformed

        with mock.patch('builtins.print') as mock_print:
            loaded_text = file_io.load_text_from_json(str(json_filepath), text_key="content")
        self.assertIsNone(loaded_text)
        mock_print.assert_called()

    def test_load_text_from_json_file_not_found(self):
        with mock.patch('builtins.print') as mock_print:
            loaded_text = file_io.load_text_from_json(str(self.test_output_dir / "non_existent.json"))
        self.assertIsNone(loaded_text)
        mock_print.assert_called()

# To run all tests in this file from command line:
# python -m unittest text_analyzer/tests/test_new_features.py
