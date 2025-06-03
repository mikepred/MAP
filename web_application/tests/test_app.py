import unittest
import io
import sys
import os

# Add this at the beginning of test_app.py to ensure project root is in path
# This allows finding 'web_application.app' and 'text_analyzer'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from web_application.app import app # Import the Flask app instance
from text_analyzer import config as ta_config # For default values

class WebAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for simpler forms in tests
        self.client = app.test_client()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Text Analyzer</title>", response.data)
        self.assertIn(b"<h1>Text Analyzer</h1>", response.data)
        self.assertIn(b"Paste Text:", response.data)
        self.assertIn(b"Or Upload File:", response.data)
        self.assertIn(b"Analyze</button>", response.data)

    def test_analyze_route_text_input(self):
        payload = {
            'text_input': 'This is a simple test sentence. It has several words.',
            'top_words': '3',
            'remove_stopwords': 'true'
        }
        response = self.client.post('/analyze', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"===== TEXT ANALYSIS RESULTS =====", response.data)
        self.assertNotIn(b'class="error_message"', response.data)
        # Check for a specific word that should appear if stop words are removed
        self.assertIn(b'simple: 1', response.data) 

    def test_analyze_route_file_input(self):
        file_content = b"This is sample content from a test file. Testing file uploads."
        payload = {
            'file_input': (io.BytesIO(file_content), 'test_file.txt'),
            'top_words': '4',
            'remove_stopwords': 'false' # Test with stop words not removed
        }
        response = self.client.post('/analyze', data=payload, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"===== TEXT ANALYSIS RESULTS =====", response.data)
        self.assertNotIn(b'class="error_message"', response.data)
        # Check for a word that should be present
        self.assertIn(b'file: 2', response.data) # 'file' appears twice

    def test_analyze_route_no_input(self):
        response = self.client.post('/analyze', data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'class="error_message"', response.data)
        self.assertIn(b"No text provided. Please paste text or upload a file.", response.data)

    def test_analyze_route_invalid_top_words(self):
        # Test with negative value
        payload_negative = {
            'text_input': 'Testing with invalid top words value (-1).',
            'top_words': '-1' 
        }
        response_negative = self.client.post('/analyze', data=payload_negative)
        self.assertEqual(response_negative.status_code, 200)
        self.assertIn(b'class="error_message"', response_negative.data)
        self.assertIn(b"Invalid input for &#39;Number of top words&#39;: Must be a positive integer.", response_negative.data)
        self.assertNotIn(b"===== TEXT ANALYSIS RESULTS =====", response_negative.data)

        # Test with non-numeric value
        payload_non_numeric = {
            'text_input': 'Testing with non-numeric top words (abc).',
            'top_words': 'abc' 
        }
        response_non_numeric = self.client.post('/analyze', data=payload_non_numeric)
        self.assertEqual(response_non_numeric.status_code, 200)
        self.assertIn(b'class="error_message"', response_non_numeric.data)
        self.assertIn(b"Invalid input for &#39;Number of top words&#39;: Must be an integer.", response_non_numeric.data)
        self.assertNotIn(b"===== TEXT ANALYSIS RESULTS =====", response_non_numeric.data)
        
        # Test with zero
        payload_zero = {
            'text_input': 'Testing with invalid top words value (0).',
            'top_words': '0'
        }
        response_zero = self.client.post('/analyze', data=payload_zero)
        self.assertEqual(response_zero.status_code, 200)
        self.assertIn(b'class="error_message"', response_zero.data)
        self.assertIn(b"Invalid input for &#39;Number of top words&#39;: Must be a positive integer.", response_zero.data)
        self.assertNotIn(b"===== TEXT ANALYSIS RESULTS =====", response_zero.data)

    def test_analyze_route_empty_text_input_and_no_file(self):
        # Testing with text_input containing only whitespace
        payload = {
            'text_input': '   ', # Whitespace only
            'top_words': '5'
        }
        response = self.client.post('/analyze', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'class="error_message"', response.data)
        self.assertIn(b"No text provided. Please paste text or upload a file.", response.data)

    def test_analyze_route_text_input_with_default_top_words(self):
        # Test when top_words is not provided, should use default
        payload = {
            'text_input': 'Sample text for default top words.',
            # 'top_words': not specified
        }
        response = self.client.post('/analyze', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"===== TEXT ANALYSIS RESULTS =====", response.data)
        self.assertNotIn(b'class="error_message"', response.data)
        # Further check could be to see if 'Top X' in results matches default_top_words_display
        # e.g. self.assertIn(f"--- Word Frequencies (Top {ta_config.DEFAULT_TOP_WORDS_DISPLAY}) ---".encode(), response.data)


if __name__ == '__main__':
    unittest.main()
