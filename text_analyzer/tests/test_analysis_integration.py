import unittest
from collections import Counter
from text_analyzer import analysis
from text_analyzer import text_processing as tp
from text_analyzer import config as cfg
import textstat # For readability tests

# Mock the spaCy NLP object and VADER to avoid heavy model loading in basic unit tests
# We'll test their integration more directly in specific tests or rely on system tests for full NLP lib checks.

class MockSpacyToken:
    def __init__(self, text, pos_, label_="", is_punct=False, is_space=False):
        self.text = text
        self.pos_ = pos_
        self.label_ = label_
        self.is_punct = is_punct
        self.is_space = is_space

class MockSpacyDoc:
    def __init__(self, tokens, ents=None):
        self.tokens = tokens
        self.ents = ents if ents is not None else []

    def __iter__(self):
        return iter(self.tokens)

class MockSpacyNLP:
    def __init__(self):
        self.model_name = "mock_en_core_web_sm"

    def __call__(self, text):
        # This simple mock needs to be smarter if we test POS/NER outputs directly here.
        # For now, it's a placeholder.
        # Based on text, create MockSpacyTokens and a MockSpacyDoc.
        # This is a simplified version. Real tests for POS/NER outputs might need more sophisticated mocks
        # or to run against the actual libraries with carefully chosen small inputs.
        
        # Example tokenization (very basic)
        raw_tokens = text.split()
        mock_tokens = []
        if "A test sentence for POS." in text:
             mock_tokens = [
                MockSpacyToken("A", "DET"), MockSpacyToken("test", "NOUN"), 
                MockSpacyToken("sentence", "NOUN"), MockSpacyToken("for", "ADP"), 
                MockSpacyToken("POS", "PROPN"), MockSpacyToken(".", "PUNCT", is_punct=True)
            ]
        elif "Recognize London and Google." in text:
            mock_tokens = [
                MockSpacyToken("Recognize", "VERB"), MockSpacyToken("London", "PROPN"), 
                MockSpacyToken("and", "CCONJ"), MockSpacyToken("Google", "PROPN"),
                MockSpacyToken(".", "PUNCT", is_punct=True)
            ]
            mock_ents = [
                MockSpacyToken("London", "PROPN", label_="GPE"), 
                MockSpacyToken("Google", "PROPN", label_="ORG")
            ]
            return MockSpacyDoc(mock_tokens, mock_ents)

        return MockSpacyDoc(mock_tokens)

# Monkeypatch the global NLP_SPACY object in analysis.py before tests run
# This is a common way to handle global resources in testing.
# However, analysis.NLP_SPACY is loaded at module import.
# A better approach might be to allow NLP_SPACY to be passed into functions,
# or to have a setter for it for testing.
# For now, we'll assume that if we can't easily mock it, tests requiring it might be slower
# or need to be grouped as "integration tests" that expect the model to be present.
# Let's try to test functions that *use* the results of NLP, or test NLP functions directly with small inputs.

class TestAnalysisIntegration(unittest.TestCase):
    def setUp(self):
        # Potentially override analysis.NLP_SPACY here if a clean way exists.
        # e.g., self.original_nlp_spacy = analysis.NLP_SPACY
        # analysis.NLP_SPACY = MockSpacyNLP()
        # And restore in tearDown. This is tricky with module-level globals.
        # For now, we'll write tests assuming actual NLTK/spaCy models might be used for some parts,
        # and focus on testing the logic that consumes their output.
        pass

    def tearDown(self):
        # analysis.NLP_SPACY = self.original_nlp_spacy
        pass

    def test_generate_ngrams(self):
        tokens = ["this", "is", "a", "sample", "text"]
        expected_bigrams = {2: [("this", "is"), ("is", "a"), ("a", "sample"), ("sample", "text")]}
        bigrams = tp.generate_ngrams(tokens, [2])
        self.assertEqual(bigrams, expected_bigrams)

        expected_tri = {3: [("this", "is", "a"), ("is", "a", "sample"), ("a", "sample", "text")]}
        trigrams = tp.generate_ngrams(tokens, [3])
        self.assertEqual(trigrams, expected_tri)
        
        expected_bi_tri = {
            2: [("this", "is"), ("is", "a"), ("a", "sample"), ("sample", "text")],
            3: [("this", "is", "a"), ("is", "a", "sample"), ("a", "sample", "text")]
        }
        bi_tri_grams = tp.generate_ngrams(tokens, [2, 3])
        self.assertEqual(bi_tri_grams, expected_bi_tri)

        self.assertEqual(tp.generate_ngrams([], [2, 3]), {2: [], 3: []})
        self.assertEqual(tp.generate_ngrams(["one"], [2]), {2: []})

    def test_calculate_ngram_frequencies(self):
        ngrams_data = {
            2: [("this", "is"), ("is", "a"), ("this", "is")],
            3: [("this", "is", "a")]
        }
        expected_freqs = {
            "bigrams": Counter({"this is": 2, "is a": 1}),
            "trigrams": Counter({"this is a": 1})
        }
        freqs = analysis.calculate_ngram_frequencies(ngrams_data)
        self.assertEqual(freqs, expected_freqs)
        
        empty_freqs = analysis.calculate_ngram_frequencies({2: [], 3: []})
        self.assertEqual(empty_freqs, {"bigrams": Counter(), "trigrams": Counter()})

    def test_analyze_sentiment_vader(self):
        # VADER is dictionary-based, so direct testing is usually fine without heavy mocking.
        # Test positive sentiment
        positive_text = "This is a wonderful and fantastic experience!"
        sentiment_positive = analysis.analyze_sentiment_vader(positive_text)
        self.assertTrue(sentiment_positive['compound'] >= 0.05)

        # Test negative sentiment
        negative_text = "This is a horrible and terrible situation."
        sentiment_negative = analysis.analyze_sentiment_vader(negative_text)
        self.assertTrue(sentiment_negative['compound'] <= -0.05)

        # Test neutral sentiment
        neutral_text = "The book is on the table."
        sentiment_neutral = analysis.analyze_sentiment_vader(neutral_text)
        self.assertTrue(-0.05 < sentiment_neutral['compound'] < 0.05)
        
        # Test empty text
        empty_sentiment = analysis.analyze_sentiment_vader("")
        # The expected error message for VADER with empty string is specific
        # In analysis.py, it's "VADER analyzer not available or empty text" if _vader_analyzer is not None
        # or if it's None. Let's check what the actual function returns for an empty string.
        # If _vader_analyzer is loaded, it should be:
        # self.assertEqual(empty_sentiment, {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0})
        # If the error message is included, it would be:
        expected_empty_result = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
        # VADER itself returns all zeros for empty string. The 'error' key is added by my wrapper.
        # Let's check the actual behavior of the wrapped function.
        # The current implementation returns an 'error' key.
        self.assertIn('error', empty_sentiment)
        # And the scores should be default.
        self.assertEqual(empty_sentiment['neg'], 0.0)
        self.assertEqual(empty_sentiment['neu'], 0.0)
        self.assertEqual(empty_sentiment['pos'], 0.0)
        self.assertEqual(empty_sentiment['compound'], 0.0)

    def test_analyze_pos_tags_spacy_and_lexical_density(self):
        # This test uses the actual spaCy model if available.
        # Ensure your environment has 'en_core_web_sm' for this to pass.
        if not analysis.NLP_SPACY: # Check if spaCy model loaded
            self.skipTest("spaCy model 'en_core_web_sm' not available. Skipping POS/NER tests.")
            return

        test_text = "The quick brown fox jumps over the lazy dog." # Common test sentence
        # Expected POS tags might vary slightly by model version, so test for structure and key tags.
        # Expected content words: The, quick, brown, fox, jumps, over, the, lazy, dog (all except '.')
        # For 'en_core_web_sm': DET, ADJ, ADJ, NOUN, VERB, ADP, DET, ADJ, NOUN, PUNCT
        # Content POS: ADJ, ADJ, NOUN, VERB, ADJ, NOUN (6 content words based on default set)
        # Total POS tags (excluding punct): 9
        # Lexical density: (6/9)*100 = 66.66...
        
        results = analysis.analyze_pos_tags_spacy(test_text, top_n_tags=3)
        
        self.assertIsNone(results.get('error'))
        self.assertGreater(results.get('total_pos_tags', 0), 5) # Expect a reasonable number of tags
        self.assertTrue(len(results.get('most_common_pos', [])) <= 3)
        self.assertIn('pos_counts', results)
        self.assertIn('ADJ', results['pos_counts']) # Adjectives should be present
        self.assertIn('NOUN', results['pos_counts']) # Nouns should be present

        # Test lexical density calculation (re-using the POS results)
        # Need to call calculate_lexical_density directly as it's now separate
        density = analysis.calculate_lexical_density(results['pos_counts'], results['total_pos_tags'])
        self.assertGreaterEqual(density, 50) # Expect a certain level of lexical density
        self.assertLessEqual(density, 80) # Expect a certain level of lexical density

        empty_results = analysis.analyze_pos_tags_spacy("")
        self.assertIsNotNone(empty_results.get('error'))
        self.assertEqual(empty_results.get('total_pos_tags', 0), 0)
        self.assertEqual(analysis.calculate_lexical_density(empty_results['pos_counts'], empty_results['total_pos_tags']), 0.0)

    def test_analyze_ner_spacy(self):
        if not analysis.NLP_SPACY:
            self.skipTest("spaCy model 'en_core_web_sm' not available. Skipping NER tests.")
            return

        test_text = "Apple Inc. is looking at buying U.K. startup for $1 billion. Dr. Smith visited London."
        # Expected entities: Apple Inc. (ORG), U.K. (GPE), $1 billion (MONEY), Dr. Smith (PERSON), London (GPE)
        
        results = analysis.analyze_ner_spacy(test_text, top_n_entity_types=3)
        
        self.assertIsNone(results.get('error'))
        self.assertGreaterEqual(results.get('total_entities', 0), 3) # Expect multiple entities
        self.assertTrue(len(results.get('most_common_entity_types', [])) <= 3)
        self.assertIn('entities_by_type', results)
        self.assertIn('GPE', results['entities_by_type']) # Should find London or U.K.
        self.assertIn('ORG', results['entities_by_type']) # Should find Apple Inc.
        
        # Check if specific entities are found (texts might vary slightly based on tokenization)
        # This is more prone to breaking if model changes, so test type presence is more robust.
        gpe_entities = results['entities_by_type'].get('GPE', [])
        self.assertTrue(any('London' in e for e in gpe_entities) or any('U.K.' in e for e in gpe_entities))

        empty_results = analysis.analyze_ner_spacy("")
        self.assertIsNotNone(empty_results.get('error'))
        self.assertEqual(empty_results.get('total_entities', 0), 0)

    def test_calculate_readability_stats(self):
        # Textstat is generally deterministic for a given input.
        test_text = "This is a simple sentence. This is another sentence that is also simple to read."
        # For this text, expected values (approximate, can vary slightly based on textstat version/internals):
        # flesch_reading_ease: around 80-90 (higher is easier)
        # flesch_kincaid_grade: around 2-4 (US grade level)
        
        # We need word_counts and sentence_analysis for the custom part of calculate_readability_stats
        # For testing textstat part, only text is strictly needed if we were to call textstat directly.
        # But we test our wrapper.
        
        # Basic setup for dependent parts:
        mock_word_counts = Counter(tp.tokenize_text(tp.clean_text_for_word_tokenization(test_text)))
        mock_sentence_analysis = analysis.analyze_sentences(tp.preprocess_text_for_sentence_analysis(test_text))

        stats = analysis.calculate_readability_stats(test_text, mock_word_counts, mock_sentence_analysis)
        
        self.assertIsNone(stats.get('error'))
        self.assertIn('flesch_reading_ease', stats)
        self.assertIn('flesch_kincaid_grade', stats)
        self.assertIn('gunning_fog', stats)
        # Check a couple of values are numeric (not 'N/A')
        self.assertIsInstance(stats['flesch_reading_ease'], (int, float))
        self.assertIsInstance(stats['flesch_kincaid_grade'], (int, float))

        # Test with very short text that might cause issues for some textstat indices
        short_text = "Hi."
        mock_short_word_counts = Counter(tp.tokenize_text(tp.clean_text_for_word_tokenization(short_text)))
        mock_short_sentence_analysis = analysis.analyze_sentences(tp.preprocess_text_for_sentence_analysis(short_text))
        short_stats = analysis.calculate_readability_stats(short_text, mock_short_word_counts, mock_short_sentence_analysis)
        self.assertTrue(short_stats['smog_index'] == 'N/A' or isinstance(short_stats['smog_index'], (int, float))) # SMOG often needs more text
        self.assertIsNotNone(short_stats.get('error')) # Expect an error message for short text

    def test_analyze_text_complete_structure_and_key_features(self):
        test_text = "Dr. Emily Carter, CEO of Carter Innovations, announced a new project in London, U.K. This project is exciting! N-grams are sequences of words."
        
        results = analysis.analyze_text_complete(test_text, use_stop_words=False, num_common_words_to_display=3)

        self.assertIsNone(results.get('error'))
        
        # Check for presence of all top-level analysis keys
        self.assertIn('word_analysis', results)
        self.assertIn('sentence_analysis', results)
        self.assertIn('general_stats', results)
        self.assertIn('readability_stats', results)
        self.assertIn('interesting_patterns', results)
        self.assertIn('ngram_frequencies', results)
        self.assertIn('sentiment_analysis', results)
        self.assertIn('pos_analysis', results)
        self.assertIn('ner_analysis', results)
        
        # Check N-grams
        self.assertIn('bigrams', results['ngram_frequencies'])
        # The num_common_words_to_display in analyze_text_complete applies to word frequencies,
        # N-grams use DEFAULT_NGRAM_DISPLAY_COUNT from config.
        # Default is 10.
        self.assertTrue(len(results['ngram_frequencies']['bigrams']) <= cfg.DEFAULT_NGRAM_DISPLAY_COUNT) 

        # Check Sentiment (VADER is robust)
        self.assertIn('compound', results['sentiment_analysis'])
        
        # Check POS and Lexical Density (relies on spaCy model)
        if analysis.NLP_SPACY: # Only check if model is loaded
            self.assertGreater(results['pos_analysis'].get('total_pos_tags', 0), 0)
            self.assertGreater(results['pos_analysis'].get('lexical_density', 0.0), 0.0)
        
        # Check NER (relies on spaCy model)
        if analysis.NLP_SPACY:
            self.assertGreater(results['ner_analysis'].get('total_entities', 0), 0)
            self.assertIn('ORG', results['ner_analysis']['entity_counts_by_type']) # Carter Innovations
            self.assertIn('PERSON', results['ner_analysis']['entity_counts_by_type']) # Dr. Emily Carter
            self.assertIn('GPE', results['ner_analysis']['entity_counts_by_type']) # London, U.K.

        # Check Readability (textstat)
        self.assertIsInstance(results['readability_stats'].get('flesch_kincaid_grade'), (int, float))

        # Test with empty text
        empty_results = analysis.analyze_text_complete("", use_stop_words=False, num_common_words_to_display=3)
        self.assertIsNotNone(empty_results.get('error')) # Should indicate no text or error
        # Ensure all keys are still present due to default structures
        self.assertTrue(all(key in empty_results for key in ['ngram_frequencies', 'sentiment_analysis', 'pos_analysis', 'ner_analysis']))


if __name__ == '__main__':
    unittest.main()
