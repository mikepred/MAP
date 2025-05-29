import nltk

try:
    nltk.data.find('tokenizers/punkt')
    print("NLTK 'punkt' resource already downloaded.")
except LookupError:
    print("Downloading NLTK 'punkt' resource...")
    nltk.download('punkt', quiet=True)
    print("NLTK 'punkt' resource downloaded.")

try:
    nltk.data.find('corpora/stopwords')
    print("NLTK 'stopwords' resource already downloaded.")
except LookupError:
    print("Downloading NLTK 'stopwords' resource...")
    nltk.download('stopwords', quiet=True)
    print("NLTK 'stopwords' resource downloaded.")

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
    print("NLTK 'averaged_perceptron_tagger' resource already downloaded.")
except LookupError:
    print("Downloading NLTK 'averaged_perceptron_tagger' resource...")
    nltk.download('averaged_perceptron_tagger', quiet=True)
    print("NLTK 'averaged_perceptron_tagger' resource downloaded.")

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
    print("NLTK 'vader_lexicon' resource already downloaded.")
except LookupError:
    print("Downloading NLTK 'vader_lexicon' resource...")
    nltk.download('vader_lexicon', quiet=True)
    print("NLTK 'vader_lexicon' resource downloaded.")

print("NLTK resource check/download complete.")
