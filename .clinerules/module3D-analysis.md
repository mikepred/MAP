# Module 3D: Analysis & Display Functions

**⏱️ Time Estimate:** 20-25 minutes  
**📍 Module Position:** 4 of 5 in the Module 3 series  
**🎯 Focus:** Analysis and presentation

## Learning Objectives

By the end of this module, you will:

- Create advanced statistical analysis functions
- Implement professional results formatting
- Build user-friendly display functions
- Design clear, readable output layouts
- Handle data visualization basics

## Prerequisites

- Completion of Module 3C (Text Processing Pipeline)
- Understanding of string formatting
- Knowledge of data structures (dictionaries, lists)

## Display & Analysis Overview

Our display system will provide:

1. **Statistical Analysis** - Advanced metrics and calculations
2. **Professional Formatting** - Clean, readable output
3. **Data Visualization** - Simple charts and graphics
4. **User-Friendly Design** - Clear structure and navigation

## Step 1: Advanced Statistical Analysis

```python
def calculate_readability_stats(text, word_counts, sentence_analysis):
    """
    Calculate readability and complexity statistics.
    
    Args:
        text (str): Original text
        word_counts (Counter): Word frequency data
        sentence_analysis (dict): Sentence analysis results
        
    Returns:
        dict: Readability statistics
    """
    if not text or not word_counts:
        return {
            'avg_word_length': 0,
            'complexity_score': 0,
            'readability_level': 'Unknown'
        }
    
    # Calculate average word length
    total_chars = sum(len(word) * count for word, count in word_counts.items())
    total_words = sum(word_counts.values())
    avg_word_length = total_chars / total_words if total_words > 0 else 0
    
    # Simple complexity score based on word length and sentence length
    avg_sentence_length = sentence_analysis.get('average_words_per_sentence', 0)
    complexity_score = (avg_word_length * 0.6) + (avg_sentence_length * 0.4)
    
    # Determine readability level
    if complexity_score < 8:
        readability_level = 'Easy'
    elif complexity_score < 12:
        readability_level = 'Moderate'
    elif complexity_score < 16:
        readability_level = 'Difficult'
    else:
        readability_level = 'Very Difficult'
    
    return {
        'avg_word_length': round(avg_word_length, 1),
        'complexity_score': round(complexity_score, 1),
        'readability_level': readability_level
    }

def find_interesting_patterns(word_counts, text):
    """
    Find interesting patterns in the text.
    
    Args:
        word_counts (Counter): Word frequency data
        text (str): Original text
        
    Returns:
        dict: Interesting patterns found
    """
    patterns = {
        'repeated_words': [],
        'long_words': [],
        'short_words': [],
        'word_variety': 0
    }
    
    if not word_counts:
        return patterns
    
    # Find words that appear multiple times
    patterns['repeated_words'] = [
        (word, count) for word, count in word_counts.most_common(10) 
        if count > 1
    ]
    
    # Find long words (7+ characters)
    patterns['long_words'] = [
        word for word in word_counts.keys() 
        if len(word) >= 7
    ][:10]
    
    # Find very short words (1-2 characters)
    patterns['short_words'] = [
        word for word in word_counts.keys() 
        if len(word) <= 2
    ][:10]
    
    # Calculate word variety (unique words / total words)
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)
    patterns['word_variety'] = round(unique_words / total_words * 100, 1) if total_words > 0 else 0
    
    return patterns
```

## Step 2: Professional Display Functions

```python
def print_header(title, width=60):
    """Print a formatted header."""
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_section(title, width=60):
    """Print a formatted section header."""
    print(f"\n{title}")
    print("-" * len(title))

def display_general_statistics(stats):
    """
    Display general text statistics in a formatted way.
    
    Args:
        stats (dict): General statistics dictionary
    """
    print_section("📊 General Statistics")
    
    print(f"📄 Total Characters: {stats['character_count']:,}")
    print(f"🔤 Characters (no spaces): {stats['character_count_no_spaces']:,}")
    print(f"📝 Total Words: {stats['word_count']:,}")
    print(f"📋 Total Sentences: {stats['sentence_count']:,}")
    print(f"📄 Paragraphs: {stats['paragraph_count']:,}")
    
    # Calculate derived statistics
    if stats['sentence_count'] > 0:
        words_per_sentence = stats['word_count'] / stats['sentence_count']
        print(f"📏 Average Words per Sentence: {words_per_sentence:.1f}")
    
    if stats['word_count'] > 0:
        chars_per_word = stats['character_count_no_spaces'] / stats['word_count']
        print(f"📐 Average Characters per Word: {chars_per_word:.1f}")

def display_word_analysis(word_analysis):
    """
    Display word frequency analysis.
    
    Args:
        word_analysis (dict): Word analysis results
    """
    print_section("🔤 Word Frequency Analysis")
    
    word_frequencies = word_analysis['word_frequencies']
    statistics = word_analysis['statistics']
    
    print(f"🎯 Unique Words: {statistics['unique_words']:,}")
    print(f"📊 Total Word Count: {statistics['total_words']:,}")
    print(f"📈 Average Word Frequency: {statistics['average_frequency']}")
    
    if word_frequencies:
        print(f"\n🏆 Top 10 Most Common Words:")
        for i, (word, count) in enumerate(word_frequencies.items(), 1):
            percentage = (count / statistics['total_words']) * 100
            print(f"  {i:2d}. '{word}' - {count} times ({percentage:.1f}%)")

def display_sentence_analysis(sentence_analysis):
    """
    Display sentence analysis results.
    
    Args:
        sentence_analysis (dict): Sentence analysis results
    """
    print_section("📋 Sentence Analysis")
    
    print(f"📊 Total Sentences: {sentence_analysis['sentence_count']}")
    print(f"📏 Average Words per Sentence: {sentence_analysis['average_words_per_sentence']}")
    
    if sentence_analysis['longest_sentence']:
        print(f"\n📏 Longest Sentence:")
        print(f"   \"{sentence_analysis['longest_sentence'][:100]}{'...' if len(sentence_analysis['longest_sentence']) > 100 else ''}\"")
    
    if sentence_analysis['shortest_sentence']:
        print(f"\n📏 Shortest Sentence:")
        print(f"   \"{sentence_analysis['shortest_sentence']}\"")

def display_readability_analysis(readability_stats):
    """
    Display readability analysis.
    
    Args:
        readability_stats (dict): Readability statistics
    """
    print_section("📖 Readability Analysis")
    
    print(f"📐 Average Word Length: {readability_stats['avg_word_length']} characters")
    print(f"🎯 Complexity Score: {readability_stats['complexity_score']}/20")
    print(f"📚 Readability Level: {readability_stats['readability_level']}")
    
    # Add interpretation
    level = readability_stats['readability_level']
    if level == 'Easy':
        print("   💡 This text is easy to read and understand")
    elif level == 'Moderate':
        print("   💡 This text requires moderate reading skills")
    elif level == 'Difficult':
        print("   💡 This text is challenging and requires good reading skills")
    else:
        print("   💡 This text is very difficult and requires advanced reading skills")

def display_interesting_patterns(patterns):
    """
    Display interesting patterns found in the text.
    
    Args:
        patterns (dict): Patterns analysis results
    """
    print_section("🔍 Interesting Patterns")
    
    print(f"🎨 Word Variety: {patterns['word_variety']}% (unique words)")
    
    if patterns['repeated_words']:
        print(f"\n🔄 Most Repeated Words:")
        for word, count in patterns['repeated_words'][:5]:
            print(f"   '{word}' appears {count} times")
    
    if patterns['long_words']:
        print(f"\n📏 Long Words (7+ characters):")
        print(f"   {', '.join(patterns['long_words'][:8])}")
    
    if patterns['short_words']:
        print(f"\n🔤 Short Words (1-2 characters):")
        print(f"   {', '.join(patterns['short_words'][:10])}")
```

## Step 3: Complete Display System

```python
def display_complete_analysis(analysis_results):
    """
    Display complete text analysis in a professional format.
    
    Args:
        analysis_results (dict): Complete analysis results
    """
    if 'error' in analysis_results:
        print(f"❌ Analysis Error: {analysis_results['error']}")
        return
    
    # Header
    print_header("📊 TEXT ANALYSIS REPORT 📊")
    
    # General statistics
    if 'general_stats' in analysis_results:
        display_general_statistics(analysis_results['general_stats'])
    
    # Word analysis
    if 'word_analysis' in analysis_results:
        display_word_analysis(analysis_results['word_analysis'])
    
    # Sentence analysis
    if 'sentence_analysis' in analysis_results:
        display_sentence_analysis(analysis_results['sentence_analysis'])
    
    # Calculate and display readability
    if all(key in analysis_results for key in ['word_analysis', 'sentence_analysis']):
        # Get the original text for readability calculation
        # We'll need to pass this from our main function
        word_counts = Counter(analysis_results['word_analysis']['word_frequencies'])
        readability_stats = calculate_readability_stats(
            "",  # We'll improve this in Module 3E
            word_counts,
            analysis_results['sentence_analysis']
        )
        display_readability_analysis(readability_stats)
        
        # Display patterns
        patterns = find_interesting_patterns(word_counts, "")
        display_interesting_patterns(patterns)
    
    # Footer
    print_section("✅ Analysis Complete")
    print("📝 Report generated successfully!")
    print("🎯 Ready for Module 3E: Integration & Testing")

def display_summary(analysis_results):
    """
    Display a quick summary of the analysis.
    
    Args:
        analysis_results (dict): Analysis results
    """
    if 'error' in analysis_results:
        print(f"❌ Error: {analysis_results['error']}")
        return
    
    general = analysis_results.get('general_stats', {})
    word_analysis = analysis_results.get('word_analysis', {})
    
    print("\n" + "="*40)
    print("📊 QUICK SUMMARY")
    print("="*40)
    print(f"📄 Characters: {general.get('character_count', 0):,}")
    print(f"📝 Words: {general.get('word_count', 0):,}")
    print(f"📋 Sentences: {general.get('sentence_count', 0):,}")
    
    word_stats = word_analysis.get('statistics', {})
    print(f"🎯 Unique Words: {word_stats.get('unique_words', 0):,}")
    
    most_common = word_stats.get('most_common', [])
    if most_common:
        top_word, count = most_common[0]
        print(f"🏆 Most Common Word: '{top_word}' ({count} times)")
    
    print("="*40)
```

## Step 4: Updated Main Function

```python
def main():
    """Main execution function - testing display and analysis."""
    print_header("Text Analyzer - Module 3D: Display Testing")
    
    # Load text file
    content = load_text_file()
    
    if not content:
        print("❌ No content to analyze")
        return
    
    print("\n🔄 Running complete analysis...")
    
    # Run complete analysis
    results = analyze_text_complete(content)
    
    if 'error' in results:
        print(f"❌ Analysis error: {results['error']}")
        return
    
    # Display results
    print("\n" + "="*60)
    print("Choose display format:")
    print("1. Complete Report")
    print("2. Quick Summary")
    print("3. Both")
    print("="*60)
    
    try:
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            display_complete_analysis(results)
        elif choice == "2":
            display_summary(results)
        elif choice == "3":
            display_summary(results)
            display_complete_analysis(results)
        else:
            print("Invalid choice, showing summary:")
            display_summary(results)
            
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted")
    except Exception as e:
        print(f"❌ Display error: {e}")
        display_summary(results)  # Fallback to summary

if __name__ == "__main__":
    main()
```

## ✅ Testing Your Implementation

Run your analyzer and test the display functions:

```bash
python analyzer.py
```

Choose different display options to see:
- Complete detailed report
- Quick summary
- Both formats together

## 🚧 Troubleshooting

**Formatting Issues:**
- Check that your terminal supports emojis
- Adjust width parameters if text wraps oddly

**Missing Data:**
- Verify all analysis functions return proper dictionaries
- Check for None values in results

**Display Errors:**
- Add try-except blocks around formatting code
- Provide fallback displays for missing data

## 🎯 Key Concepts Learned

1. **Professional Output:** Clean, readable formatting
2. **Data Presentation:** Making numbers meaningful
3. **User Experience:** Clear navigation and choices
4. **Error Handling:** Graceful fallbacks
5. **Information Hierarchy:** Organizing data logically

## ✅ Checkpoint: Module 3D Complete

**You should now have:**

- ✅ Advanced statistical analysis functions
- ✅ Professional results formatting
- ✅ User-friendly display system
- ✅ Multiple output format options
- ✅ Comprehensive readability analysis

## ➡️ Next Steps

Outstanding! Your analysis and display system is now complete. Head to **[Module 3E: Integration & Testing](module3E-integration.md)** for the final integration and testing phase.

**Coming up in Module 3E:**

- Complete system integration
- Comprehensive testing scenarios
- Performance optimization
- Final application assembly

---

📚 **Navigation:**
- ⬅️ Previous: [Module 3C: Text Processing Pipeline](module3C-text-processing.md)
- ➡️ Next: [Module 3E: Integration & Testing](module3E-integration.md)
- 🏠 Home: [Module 3 Navigation Guide](module3-navigation.md)
