FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy model
RUN python -m spacy download en_core_web_sm

# Install NLTK data
RUN python -m nltk.downloader punkt stopwords

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 10000

# Command to run the application
CMD exec gunicorn --worker-tmp-dir /dev/shm --bind "0.0.0.0:${PORT}" webapp:app