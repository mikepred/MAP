# Module 3C: Text Processing Pipeline

**⏱️ Time Estimate:** 25-30 minutes  
**📍 Module Position:** 3 of 5 in the Module 3 series  
**🎯 Focus:** Core text processing logic

## Learning Objectives

By the end of this module, you will:

- Implement text cleaning and preprocessing functions
- Build word tokenization and counting capabilities
- Create sentence analysis functions
- Design a complete text processing pipeline
- Handle edge cases in text processing

## Prerequisites

- Completion of Module 3B (File I/O & Error Handling)
- Understanding of string methods and list operations
- Knowledge of Python's `collections.Counter`

## Text Processing Overview

Our text processing pipeline will consist of:

1. **Text Cleaning** - Remove unwanted characters, normalize case
2. **Tokenization** - Split text into words and sentences
3. **Analysis** - Count frequencies, calculate statistics
4. **Processing** - Apply transformations and filters

## Step 1: Text Cleaning Function

```python
def clean_text(text):
    """
    Clean and preprocess text for analysis.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text ready for processing
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase for consistent analysis
    cleaned = text.lower()
    
    # Remove extra whitespace and normalize spaces
    cleaned = ' '.join(cleaned.split())
    
    # Optional: Remove or replace specific characters
    # Keep letters, numbers, spaces, and basic punctuation
    import re
    cleaned = re.sub(r'[^\w\s.,!?;:-]', '', cleaned)
    
    return cleaned

def clean_text_for_words(text):
    """
    Clean text specifically for word analysis (removes punctuation).
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Text with punctuation removed
    """
    if not text:
        return ""
    
    # Remove punctuation for word counting
    translator = str.maketrans('', '', string.punctuation)
    cleaned = text.translate(translator)
    
    # Normalize whitespace
    cleaned = ' '.join(cleaned.split())
    
    return cleaned.lower()
```

## Step 2: Word Processing Functions

```python
def count_words(text):
    """
    Count word frequencies in text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        Counter: Word frequencies as Counter object
    """
    if not text:
        return Counter()
    
    # Clean text for word analysis
    cleaned_text = clean_text_for_words(text)
    
    # Split into words
    words = cleaned_text.split()
    
    # Filter out empty strings and very short words if desired
    words = [word for word in words if len(word) > 0]
    
    # Count frequencies
    word_counts = Counter(words)
    
    return word_counts

def get_unique_words(text):
    """
    Get list of unique words in text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        list: Sorted list of unique words
    """
    word_counts = count_words(text)
    return sorted(word_counts.keys())

def get_word_count_stats(word_counts):
    """
    Calculate statistics from word counts.
    
    Args:
        word_counts (Counter): Word frequency counter
        
    Returns:
        dict: Statistics about word usage
    """
    if not word_counts:
        return {
            'total_words': 0,
            'unique_words': 0,
            'most_common': [],
            'average_frequency': 0
        }
    
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)
    most_common = word_counts.most_common(5)
    average_frequency = total_words / unique_words if unique_words > 0 else 0
    
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'most_common': most_common,
        'average_frequency': round(average_frequency, 2)
    }
```

## Step 3: Sentence Processing Functions

```python
def count_sentences(text):
    """
    Count sentences in text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        int: Number of sentences
    """
    if not text:
        return 0
    
    # Split on sentence-ending punctuation
    import re
    sentences = re.split(r'[.!?]+', text)
    
    # Filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return len(sentences)

def analyze_sentences(text):
    """
    Analyze sentence structure in text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Sentence analysis results
    """
    if not text:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    # Split into sentences
    import re
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {
            'sentence_count': 0,
            'average_words_per_sentence': 0,
            'longest_sentence': '',
            'shortest_sentence': ''
        }
    
    # Calculate statistics
    sentence_word_counts = []
    for sentence in sentences:
        words = clean_text_for_words(sentence).split()
        sentence_word_counts.append(len(words))
    
    average_words = sum(sentence_word_counts) / len(sentence_word_counts)
    
    # Find longest and shortest sentences
    longest_idx = sentence_word_counts.index(max(sentence_word_counts))
    shortest_idx = sentence_word_counts.index(min(sentence_word_counts))
    
    return {
        'sentence_count': len(sentences),
        'average_words_per_sentence': round(average_words, 1),
        'longest_sentence': sentences[longest_idx].strip(),
        'shortest_sentence': sentences[shortest_idx].strip()
    }
```

## Step 4: Complete Text Analysis Pipeline

```python
def analyze_text_complete(text):
    """
    Complete text analysis pipeline.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        dict: Complete analysis results
    """
    if not text:
        return {
            'error': 'No text provided for analysis',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {}
        }
    
    try:
        # Word analysis
        word_counts = count_words(text)
        word_stats = get_word_count_stats(word_counts)
        unique_words = get_unique_words(text)
        
        # Sentence analysis
        sentence_stats = analyze_sentences(text)
        
        # General statistics
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        
        general_stats = {
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'word_count': word_stats['total_words'],
            'sentence_count': sentence_stats['sentence_count'],
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()])
        }
        
        return {
            'word_analysis': {
                'word_frequencies': dict(word_counts.most_common(10)),
                'statistics': word_stats,
                'unique_words_sample': unique_words[:10]  # First 10 for preview
            },
            'sentence_analysis': sentence_stats,
            'general_stats': general_stats
        }
        
    except Exception as e:
        return {
            'error': f'Analysis failed: {str(e)}',
            'word_analysis': {},
            'sentence_analysis': {},
            'general_stats': {}
        }
```

## Step 5: Testing the Pipeline

Update your main function to test the text processing:

```python
def main():
    """Main execution function - testing text processing pipeline."""
    print("Text Analyzer - Module 3C: Text Processing Testing")
    print("=" * 60)
    
    # Load text file
    content = load_text_file()
    
    if not content:
        print("❌ No content to analyze")
        return
    
    print("\n🔄 Processing text...")
    
    # Run complete analysis
    results = analyze_text_complete(content)
    
    if 'error' in results:
        print(f"❌ Analysis error: {results['error']}")
        return
    
    # Display results preview
    print("\n📊 Analysis Results Preview:")
    print("-" * 30)
    
    # General stats
    general = results['general_stats']
    print(f"📄 Characters: {general['character_count']}")
    print(f"📝 Words: {general['word_count']}")
    print(f"📋 Sentences: {general['sentence_count']}")
    
    # Word analysis preview
    word_analysis = results['word_analysis']
    print(f"\n🔤 Most common words:")
    for word, count in list(word_analysis['word_frequencies'].items())[:3]:
        print(f"   '{word}': {count} times")
    
    # Sentence analysis preview
    sentence_analysis = results['sentence_analysis']
    print(f"\n📏 Average words per sentence: {sentence_analysis['average_words_per_sentence']}")
    
    print("\n✅ Text processing pipeline working!")
    print("🎯 Ready for Module 3D: Analysis & Display Functions")

if __name__ == "__main__":
    main()
```

## ✅ Testing Your Implementation

### Test with sample.txt:

```bash
python analyzer.py
# Enter: sample.txt
```

### Expected output format:
```
Text Analyzer - Module 3C: Text Processing Testing
============================================================

🚀 Text File Loader
==============================
📂 Enter filename (attempt 1/3):
💡 Tip: Use 'sample.txt' for testing
💡 Type 'quit' to exit
Filename: sample.txt
✅ File validation passed
✅ Successfully read file: sample.txt
📄 File size: 187 characters

📖 File Preview:
--------------------
The quick brown fox jumps over the lazy dog. The dog was sleeping under the tree.
This sentence contains many words that will help us test our text analysis...
--------------------

🔄 Processing text...

📊 Analysis Results Preview:
------------------------------
📄 Characters: 187
📝 Words: 32
📋 Sentences: 3
🔤 Most common words:
   'the': 4 times
   'text': 2 times
   'analysis': 2 times
📏 Average words per sentence: 10.7

✅ Text processing pipeline working!
🎯 Ready for Module 3D: Analysis & Display Functions
```

## 🚧 Troubleshooting

**Import Errors:**
```python
# Make sure you have these imports at the top:
import re
import string
from collections import Counter
from pathlib import Path
```

**Empty Results:**
- Check that your text file has content
- Verify the cleaning functions aren't removing too much

**Regex Issues:**
- The `re` module is built into Python
- Test regex patterns separately if needed

## 🎯 Key Concepts Learned

1. **Text Preprocessing:** Cleaning and normalizing text for analysis
2. **Regular Expressions:** Pattern matching for text processing
3. **Pipeline Design:** Breaking complex tasks into smaller functions
4. **Data Structures:** Using Counter for frequency analysis
5. **Error Handling:** Graceful handling of edge cases

## ✅ Checkpoint: Module 3C Complete

**You should now have:**

- ✅ Text cleaning and preprocessing functions
- ✅ Word tokenization and counting capabilities
- ✅ Sentence analysis functions
- ✅ Complete text processing pipeline
- ✅ Comprehensive analysis results structure

## ➡️ Next Steps

Fantastic! Your text processing engine is now complete. Head to **[Module 3D: Analysis & Display Functions](module3D-analysis.md)** where we'll create beautiful, professional output formatting.

**Coming up in Module 3D:**

- Advanced statistical analysis
- Professional results formatting
- Data visualization basics
- User-friendly output design

---

📚 **Navigation:**
- ⬅️ Previous: [Module 3B: File I/O & Error Handling](module3B-file-io.md)
- ➡️ Next: [Module 3D: Analysis & Display Functions](module3D-analysis.md)
- 🏠 Home: [Module 3 Navigation Guide](module3-navigation.md)
