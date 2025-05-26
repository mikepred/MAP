# File: text_analyzer/explore_nlp_libraries.py
"""
This script demonstrates basic functionalities of NLTK and spaCy
for text processing, as suggested in Module 5C.
"""

import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pathlib # <-- Add this import

# Ensure NLTK data is available (it should be if previous steps were successful)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError as e:
    print(f"NLTK data missing: {e}")
    print("Please ensure 'punkt' and 'stopwords' are downloaded.")
    print("You can try: python -m nltk.downloader punkt stopwords")
    exit()

# Load spaCy model (it should be if previous steps were successful)
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("spaCy 'en_core_web_sm' model not found.")
    print("Please ensure it's downloaded.")
    print("You can try: python -m spacy download en_core_web_sm")
    exit()

def read_sample_file(filename="sample.txt"):
    """Reads content from the sample.txt file, located in the same directory as this script."""
    script_dir = pathlib.Path(__file__).parent.resolve()
    file_path = script_dir / filename
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading '{file_path}': {e}")
        return None

def demonstrate_nltk(text_content):
    """Demonstrates NLTK tokenization and stop word removal."""
    if not text_content:
        print("NLTK: No text content to process.")
        return

    print("\n--- NLTK Demonstration ---")
    
    # Tokenization
    tokens = word_tokenize(text_content.lower()) # NLTK's word_tokenize
    print(f"NLTK - First 20 tokens: {tokens[:20]}")
    
    # Stop word removal
    stop_words_nltk = set(stopwords.words('english'))
    filtered_tokens_nltk = [token for token in tokens if token.isalnum() and token not in stop_words_nltk]
    print(f"NLTK - First 20 tokens after stop word removal (and keeping alpha-numeric): {filtered_tokens_nltk[:20]}")
    print(f"NLTK - Original token count: {len(tokens)}, After stop words: {len(filtered_tokens_nltk)}")

def demonstrate_spacy(text_content):
    """Demonstrates spaCy tokenization and stop word removal."""
    if not text_content:
        print("spaCy: No text content to process.")
        return

    print("\n--- spaCy Demonstration ---")
    
    doc = nlp(text_content) # Process text with spaCy
    
    # Tokenization (spaCy handles punctuation better by default)
    # spaCy tokens are objects with many attributes
    spacy_tokens_text = [token.text.lower() for token in doc]
    print(f"spaCy - First 20 tokens (text): {spacy_tokens_text[:20]}")
    
    # Stop word removal & keeping alpha-numeric
    # token.is_stop checks against spaCy's stop word list
    # token.is_alpha checks if the token consists of alphabetic characters
    filtered_tokens_spacy = [token.text.lower() for token in doc if not token.is_stop and token.is_alpha]
    print(f"spaCy - First 20 tokens after stop word removal (and keeping alpha): {filtered_tokens_spacy[:20]}")
    print(f"spaCy - Original token count (objects): {len(doc)}, After stop words: {len(filtered_tokens_spacy)}")

    # Other spaCy features (example)
    print("\nspaCy - Named Entities (first 5):")
    for ent in doc.ents[:5]:
        print(f"  - Entity: '{ent.text}', Type: {ent.label_}")

    print("\nspaCy - Part-of-speech tags (first 5 tokens):")
    for token in doc[:5]:
        print(f"  - Token: '{token.text}', POS: {token.pos_}, Fine-grained POS: {token.tag_}")


if __name__ == "__main__":
    # The default filename for read_sample_file is "sample.txt"
    # It will now look for it in the same directory as explore_nlp_libraries.py
    sample_text = read_sample_file()

    if sample_text:
        print(f"Successfully read sample.txt. Length: {len(sample_text)} characters.")
        demonstrate_nltk(sample_text)
        demonstrate_spacy(sample_text)
    else:
        # The error message in read_sample_file will be more specific now
        print("Failed to read sample.txt. Check previous error messages.")

    print("\nExploration script finished.")
