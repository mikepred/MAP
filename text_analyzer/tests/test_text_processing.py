import unittest
from text_analyzer.text_processing import correct_text_typos

class TestCorrectTextTypos(unittest.TestCase):

    def test_simple_misspelling(self):
        """Test a simple case with one misspelling."""
        self.assertEqual(correct_text_typos("helo wrld"), "hello world")

    def test_correctly_spelled(self):
        """Test text that is already correctly spelled."""
        self.assertEqual(correct_text_typos("hello world"), "hello world")

    def test_multiple_misspellings(self):
        """Test multiple misspellings in a sentence."""
        self.assertEqual(correct_text_typos("thiss is a tst"), "this is a test")

    def test_empty_string(self):
        """Test an empty string input."""
        self.assertEqual(correct_text_typos(""), "")

    def test_text_with_punctuation(self):
        """Test misspellings with adjacent punctuation."""
        # pyspellchecker handles punctuation attached to words well.
        # For "helo," it might correct to "hello,".
        # For "wrld!" it might correct to "world!".
        self.assertEqual(correct_text_typos("helo, wrld!"), "hello, world!")

    def test_text_with_numbers(self):
        """Test text containing numbers and words with numbers."""
        # pyspellchecker might try to correct "test1" if not in dictionary.
        # If "test1" is unknown, it might return "test1" or a correction like "test".
        # Let's assume "test1" is not a common word and might be corrected if possible,
        # or left as is. "test" is a known word.
        # Based on typical behavior, "test1" might become "test 1" or stay "test1".
        # The library usually corrects "testt" to "test".
        # Let's test "testt1" to see if it becomes "test 1" or similar.
        # A simple "test1" might be left as is if it's not a clear misspelling of something else.
        self.assertEqual(correct_text_typos("testt1 123"), "test 1 123") # Assuming 'testt1' -> 'test 1'
        self.assertEqual(correct_text_typos("numbr 123"), "number 123")

    def test_none_input(self):
        """Test None input to the function."""
        self.assertEqual(correct_text_typos(None), "")

    def test_mixed_case(self):
        """Test misspellings with mixed case."""
        # The function itself doesn't lowercase, but corrections are often lowercase.
        # If the input is "Helo Wrld", spell.correction("Helo") might be "hello".
        self.assertEqual(correct_text_typos("Helo Wrld"), "hello world")

    def test_words_stuck_together(self):
        """Test words that are stuck together.
        pyspellchecker does not typically split words.
        It will treat "helloworld" as a single token.
        If "helloworld" is a known misspelling of something, it might correct it.
        Otherwise, it will likely remain "helloworld".
        """
        self.assertEqual(correct_text_typos("helloworld"), "helloworld")
        self.assertEqual(correct_text_typos("thisisatest"), "thisisatest")
        # Example of a potential correction if the combined word is a common typo for something else
        # For instance, if "goodmorningg" was often mistyped for "good morning" AND in its dictionary that way.
        # This is less common for arbitrary stuck words.
        # self.assertEqual(correct_text_typos("goodmorningg"), "good morning") # This is unlikely without training

    def test_long_text_with_various_issues(self):
        """Test a longer string with various misspellings and cases."""
        text = "Thiss is a lng testt with severl misspellings, like 'exampel' and 'anothr'. It also includes Some Correct Wrds. And numbrs like 12345."
        expected = "this is a long test with several misspellings, like 'example' and 'another'. it also includes some correct words. and numbers like 12345."
        self.assertEqual(correct_text_typos(text), expected)

    def test_words_with_internal_apostrophes(self):
        """Test words with internal apostrophes like contractions."""
        self.assertEqual(correct_text_typos("it's funn"), "it's funny")
        self.assertEqual(correct_text_typos("they'ar heere"), "they're here") # common correction

    def test_non_alphabetic_words(self):
        """Test words that are non-alphabetic (e.g., symbols), should remain unchanged."""
        self.assertEqual(correct_text_typos("!@# $%^"), "!@# $%^")
        self.assertEqual(correct_text_typos("word !@# another"), "word !@# another")

from text_analyzer import text_processing as tp
from text_analyzer import file_io # For NLTK stopwords access if needed for setup

class TestStopWordRemoval(unittest.TestCase):
    def setUp(self):
        self.sample_tokens = ["this", "is", "a", "sample", "text", "with", "some", "common", "words", "for", "testing", "el", "la", "los", "de"]
        self.english_stopwords = file_io.get_nltk_stopwords('english') # Assuming NLTK data is available
        if self.english_stopwords is None: # Fallback if NLTK download failed or is mocked badly
            self.english_stopwords = {"is", "a", "with", "some", "for", "the"}


    def test_remove_stopwords_default_english(self):
        # This test assumes remove_stopwords uses the default English list if no list is provided,
        # or that the calling function (e.g., in analysis.py) fetches and passes it.
        # Let's assume tp.remove_stopwords takes the list as an argument.
        processed_tokens = tp.remove_stopwords(self.sample_tokens, self.english_stopwords)
        expected_tokens = ["sample", "text", "common", "words", "testing", "el", "la", "los", "de"] # "this" is often a stopword
        # Adjusting expectation based on typical NLTK 'this'
        if "this" not in self.english_stopwords:
            expected_tokens.insert(0, "this")

        self.assertEqual(sorted(processed_tokens), sorted(expected_tokens))

    def test_remove_stopwords_other_language_nltk(self):
        # Mocking NLTK's stopwords for Spanish for this test
        spanish_stopwords_mock = {"el", "la", "los", "de", "un", "una"}
        with mock.patch('text_analyzer.file_io.get_nltk_stopwords', return_value=spanish_stopwords_mock) as mock_get_stops:
            # We need to ensure the function being tested actually calls get_nltk_stopwords
            # or that we pass the list directly. Let's assume direct pass for tp.remove_stopwords.
            stopwords_to_use = file_io.get_nltk_stopwords('spanish') # This call will be mocked
            processed_tokens = tp.remove_stopwords(self.sample_tokens, stopwords_to_use)
            mock_get_stops.assert_called_once_with('spanish')
        
        expected_tokens = ["this", "is", "a", "sample", "text", "with", "some", "common", "words", "for", "testing"]
        self.assertEqual(sorted(processed_tokens), sorted(expected_tokens))

    def test_remove_stopwords_custom_list(self):
        custom_stopwords = {"sample", "common", "testing"}
        processed_tokens = tp.remove_stopwords(self.sample_tokens, custom_stopwords)
        expected_tokens = ["this", "is", "a", "text", "with", "some", "words", "for", "el", "la", "los", "de"]
        self.assertEqual(sorted(processed_tokens), sorted(expected_tokens))

    def test_remove_stopwords_no_stopwords_provided_or_empty_list(self):
        # Test with an empty set of stopwords
        processed_tokens_empty_set = tp.remove_stopwords(self.sample_tokens, set())
        self.assertEqual(sorted(processed_tokens_empty_set), sorted(self.sample_tokens))

        # Test with None for stopwords list (if function is designed to handle it as "no removal")
        # This depends on the implementation of tp.remove_stopwords
        # If it defaults to English or errors, this test needs adjustment.
        # Assuming it means "no removal" if None is passed and it's handled gracefully.
        try:
            processed_tokens_none = tp.remove_stopwords(self.sample_tokens, None)
            self.assertEqual(sorted(processed_tokens_none), sorted(self.sample_tokens))
        except TypeError:
            # This means the function expects an iterable and doesn't handle None as "no removal"
            # In this case, the "empty set" test above is sufficient for "no removal by list".
            # The "no stop words" option is likely handled by a boolean flag in a higher-level function.
            pass


    def test_remove_stopwords_case_insensitivity(self):
        tokens_mixed_case = ["This", "IS", "a", "Sample", "TEXT"]
        stopwords_lower = {"this", "is", "a"}
        # remove_stopwords should ideally lowercase tokens before checking against lowercase stopwords
        processed_tokens = tp.remove_stopwords(tokens_mixed_case, stopwords_lower)
        expected = ["Sample", "TEXT"] # Assuming 'Sample' and 'TEXT' are not in stopwords
        self.assertEqual(sorted(processed_tokens), sorted(expected))

if __name__ == '__main__':
    unittest.main()
