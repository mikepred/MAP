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

if __name__ == '__main__':
    unittest.main()
