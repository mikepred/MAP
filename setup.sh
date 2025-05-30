#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Download NLTK data
python -m nltk.downloader punkt
python -m nltk.downloader stopwords

# Set execute permissions for the script
chmod +x setup.sh
