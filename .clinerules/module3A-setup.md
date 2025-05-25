# Module 3A: Project Setup & Architecture

**⏱️ Time Estimate:** 15-20 minutes  
**📍 Module Position:** 1 of 5 in the Module 3 series  
**🎯 Focus:** Foundation and planning

## Learning Objectives

By the end of this module, you will:

- Set up a proper Python project structure
- Create a virtual environment for your project
- Design the overall architecture of your text analyzer
- Create the initial project files and folders
- Plan your development approach

## Prerequisites

- Completion of Module 2 (Python fundamentals)
- Python 3.8+ installed on your system
- Basic understanding of files and folders

## Project Overview

We'll build a **Text Analysis Script** that can:

- Read text files safely with error handling
- Analyze word frequency and text statistics
- Display results in a formatted, professional manner
- Handle various edge cases and user errors

## Step 1: Project Structure Setup

Let's create a well-organized project structure:

```none
text_analyzer/
├── analyzer.py          # Main script file
├── sample.txt          # Sample text for testing
├── README.md           # Project documentation
└── requirements.txt    # Dependencies (if needed)
```

### Create the Project Directory

```bash
# Create the main project directory
mkdir text_analyzer
cd text_analyzer

# Create the main files
touch analyzer.py
touch sample.txt
touch README.md
```

## Step 2: Virtual Environment Setup

**Why Virtual Environments?**

- Isolate project dependencies
- Avoid conflicts between projects
- Professional development practice

### Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

### Verify Setup

```bash
# Check Python location (should show your venv)
which python

# Check pip location
which pip
```

## Step 3: Architecture Planning

### Core Components Design

Our text analyzer will have these main components:

1. **File I/O Module**
   - `read_file()` - Safe file reading with error handling
   - Input validation and path checking

2. **Text Processing Module**
   - `clean_text()` - Text preprocessing and cleaning
   - `count_words()` - Word frequency analysis
   - `analyze_sentences()` - Sentence-level analysis

3. **Analysis Module**
   - `get_statistics()` - Generate text statistics
   - `find_common_words()` - Identify most frequent words

4. **Display Module**
   - `display_results()` - Format and show results
   - `print_summary()` - Create summary output

### Data Flow Architecture

```none
Input File → Read & Validate → Clean Text → Process & Analyze → Display Results
```

## Step 4: Initial File Setup

### Create Sample Text File

Let's create a sample text file for testing:

```python
# sample.txt content
The quick brown fox jumps over the lazy dog. The dog was sleeping under the tree.
This sentence contains many words that will help us test our text analysis program.
Python is a powerful programming language. Programming with Python is fun and efficient.
```

### Create Basic Project Structure

```python
# analyzer.py - Initial structure
"""
Text Analysis Script - Module 3A
A comprehensive text analysis tool for processing and analyzing text files.
"""

def main():
    """Main execution function - will be implemented in later modules."""
    print("Text Analyzer - Module 3A Setup Complete!")
    print("Ready for Module 3B: File I/O & Error Handling")

if __name__ == "__main__":
    main()
```

### Create README.md

```markdown
# Text Analyzer

A Python script for analyzing text files and generating statistics.

## Features

- File reading with error handling
- Word frequency analysis
- Text statistics generation
- Professional output formatting

## Usage

```bash
python analyzer.py
```

## Development Status

- [x] Module 3A: Project Setup ✅
- [ ] Module 3B: File I/O & Error Handling
- [ ] Module 3C: Text Processing Pipeline
- [ ] Module 3D: Analysis & Display Functions
- [ ] Module 3E: Integration & Testing

## Step 5: Test Your Setup

### Verify Project Structure

```bash
# List your project files
ls -la

# Expected output:
# analyzer.py
# sample.txt
# README.md
```

### Test Basic Script

```bash
# Run the initial script
python analyzer.py

# Expected output:
# Text Analyzer - Module 3A Setup Complete!
# Ready for Module 3B: File I/O & Error Handling
```

## ✅ Checkpoint: Module 3A Complete

**You should now have:**

- ✅ A properly structured project directory
- ✅ Virtual environment set up and activated
- ✅ Basic project files created
- ✅ Initial script running successfully
- ✅ Clear architecture plan for development

## 🚧 Troubleshooting

**Virtual Environment Issues:**

```bash
# If activation fails, try:
python3 -m venv venv

# Or use explicit path:
C:\Python39\python.exe -m venv venv
```

**Permission Issues:**

```bash
# On Windows, if scripts disabled:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path Issues:**

- Ensure you're in the correct directory
- Use `pwd` (macOS/Linux) or `cd` (Windows) to check location

## 🎯 Key Concepts Learned

1. **Project Organization:** Proper file structure for maintainable code
2. **Virtual Environments:** Isolation and dependency management
3. **Architecture Planning:** Thinking before coding
4. **Professional Setup:** Industry-standard development practices

## ➡️ Next Steps

Ready to move forward? Head to **[Module 3B: File I/O & Error Handling](module3B-file-io.md)** where we'll implement robust file reading capabilities with comprehensive error handling.

**Coming up in Module 3B:**

- Safe file reading operations
- Error handling best practices
- User input validation
- Path security considerations

---

📚 **Navigation:**

- ⬅️ Previous: [Module 3 Overview](module3-overview.md)
- ➡️ Next: [Module 3B: File I/O & Error Handling](module3B-file-io.md)
- 🏠 Home: [Module 3 Navigation Guide](module3-navigation.md)
