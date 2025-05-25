# Module 3B: File I/O & Error Handling

**⏱️ Time Estimate:** 20-25 minutes  
**📍 Module Position:** 2 of 5 in the Module 3 series  
**🎯 Focus:** Data input and validation

## Learning Objectives

By the end of this module, you will:

- Implement robust file reading with comprehensive error handling
- Validate file paths and handle security considerations
- Process user input safely and effectively
- Handle various file-related exceptions gracefully
- Create professional error messages for users

## Prerequisites

- Completion of Module 3A (Project Setup)
- Basic understanding of Python exceptions
- Text editor with your `analyzer.py` file ready

## File I/O Fundamentals

### Why Error Handling Matters

When dealing with files, many things can go wrong:
- File doesn't exist
- No permission to read
- File is too large
- File is locked by another program
- Invalid file path
- Disk space issues

Professional applications must handle these gracefully.

## Step 1: Basic File Reading Function

Let's start with a simple file reading function and then make it robust:

```python
def read_file(filename):
    """
    Read text from a file with comprehensive error handling.
    
    Args:
        filename (str): Path to the text file to read
        
    Returns:
        str: Content of the file, or empty string if error
        
    Raises:
        None: All exceptions are caught and handled gracefully
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"✅ Successfully read file: {filename}")
            print(f"📄 File size: {len(content)} characters")
            return content
            
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found.")
        print("💡 Please check the filename and path.")
        return ""
        
    except PermissionError:
        print(f"❌ Error: No permission to read '{filename}'.")
        print("💡 Check file permissions or try running as administrator.")
        return ""
        
    except UnicodeDecodeError:
        print(f"❌ Error: Unable to decode '{filename}' as text.")
        print("💡 File might be binary or use different encoding.")
        return ""
        
    except IsADirectoryError:
        print(f"❌ Error: '{filename}' is a directory, not a file.")
        print("💡 Please specify a file, not a folder.")
        return ""
        
    except Exception as e:
        print(f"❌ Unexpected error reading '{filename}': {e}")
        print("💡 Please try again or contact support.")
        return ""
```

## Step 2: Enhanced File Validation

Let's add path validation and security checks:

```python
import os
from pathlib import Path

def validate_file_path(filename):
    """
    Validate that a file path is safe and accessible.
    
    Args:
        filename (str): Path to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Convert to Path object for better handling
        file_path = Path(filename)
        
        # Check if path is absolute and potentially dangerous
        if file_path.is_absolute() and not file_path.is_relative_to(Path.cwd()):
            return False, "For security, please use files in the current directory"
        
        # Check if file exists
        if not file_path.exists():
            return False, f"File '{filename}' does not exist"
        
        # Check if it's actually a file
        if not file_path.is_file():
            return False, f"'{filename}' is not a file"
        
        # Check file size (limit to 10MB for this exercise)
        file_size = file_path.stat().st_size
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            return False, f"File too large ({file_size} bytes). Maximum: {max_size} bytes"
        
        return True, "File validation passed"
        
    except Exception as e:
        return False, f"Error validating file: {e}"
```

## Step 3: User Input Handling

Create a function to get filename from user with validation:

```python
def get_filename_from_user():
    """
    Get filename from user with input validation and retry logic.
    
    Returns:
        str: Valid filename, or empty string if user cancels
    """
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        try:
            print(f"\n📂 Enter filename (attempt {attempts + 1}/{max_attempts}):")
            print("💡 Tip: Use 'sample.txt' for testing")
            print("💡 Type 'quit' to exit")
            
            filename = input("Filename: ").strip()
            
            # Check for quit command
            if filename.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                return ""
            
            # Validate input
            if not filename:
                print("⚠️  Please enter a filename")
                attempts += 1
                continue
            
            # Validate file path
            is_valid, message = validate_file_path(filename)
            if is_valid:
                print(f"✅ {message}")
                return filename
            else:
                print(f"❌ {message}")
                attempts += 1
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            return ""
        except Exception as e:
            print(f"❌ Error getting input: {e}")
            attempts += 1
    
    print(f"\n❌ Maximum attempts ({max_attempts}) reached")
    return ""
```

## Step 4: Integration Function

Now let's create a function that combines everything:

```python
def load_text_file():
    """
    Complete file loading workflow with user interaction.
    
    Returns:
        str: File content, or empty string if failed
    """
    print("🚀 Text File Loader")
    print("=" * 30)
    
    # Get filename from user
    filename = get_filename_from_user()
    if not filename:
        return ""
    
    # Read the file
    content = read_file(filename)
    
    if content:
        # Show preview of content
        preview_length = 100
        if len(content) > preview_length:
            preview = content[:preview_length] + "..."
        else:
            preview = content
        
        print(f"\n📖 File Preview:")
        print("-" * 20)
        print(preview)
        print("-" * 20)
    
    return content
```

## Step 5: Testing Your Implementation

### Update your main() function:

```python
def main():
    """Main execution function - testing file I/O."""
    print("Text Analyzer - Module 3B: File I/O Testing")
    print("=" * 50)
    
    # Test file loading
    content = load_text_file()
    
    if content:
        print(f"\n✅ Successfully loaded {len(content)} characters")
        print("🎯 Ready for Module 3C: Text Processing Pipeline")
    else:
        print("\n❌ No file loaded")
        print("💡 Try again with a valid text file")

if __name__ == "__main__":
    main()
```

## ✅ Testing Checklist

Test your implementation with these scenarios:

### Positive Tests
```bash
# Test 1: Valid file
python analyzer.py
# Enter: sample.txt

# Test 2: Create a test file and load it
echo "This is a test file for our analyzer." > test.txt
python analyzer.py
# Enter: test.txt
```

### Error Handling Tests
```bash
# Test 3: Non-existent file
python analyzer.py
# Enter: nonexistent.txt

# Test 4: Directory instead of file
mkdir testdir
python analyzer.py
# Enter: testdir

# Test 5: Empty input
python analyzer.py
# Enter: (just press Enter)

# Test 6: Quit command
python analyzer.py
# Enter: quit
```

## 🚧 Troubleshooting

**Import Errors:**
```python
# If you get import errors, check you have these at the top:
import os
from pathlib import Path
from collections import Counter
import string
```

**Permission Issues:**
- Make sure your text files are in the same directory as `analyzer.py`
- Check file permissions (right-click → Properties → Security on Windows)

**Unicode Errors:**
- Save your text files with UTF-8 encoding
- Avoid special characters for testing

## 🎯 Key Concepts Learned

1. **Exception Handling:** Specific exceptions for different error types
2. **File Security:** Path validation and safety checks
3. **User Experience:** Clear error messages and retry logic
4. **Defensive Programming:** Assuming things will go wrong and preparing for it
5. **Input Validation:** Never trust user input without validation

## ✅ Checkpoint: Module 3B Complete

**You should now have:**

- ✅ Robust file reading with error handling
- ✅ Path validation and security checks
- ✅ User-friendly input handling with retry logic
- ✅ Professional error messages
- ✅ A complete file loading workflow

## ➡️ Next Steps

Excellent! Your file I/O system is now bulletproof. Head to **[Module 3C: Text Processing Pipeline](module3C-text-processing.md)** where we'll build the core text analysis functions.

**Coming up in Module 3C:**

- Text cleaning and preprocessing
- Word tokenization and counting
- Sentence analysis functions
- Pipeline architecture implementation

---

📚 **Navigation:**
- ⬅️ Previous: [Module 3A: Project Setup](module3A-setup.md)
- ➡️ Next: [Module 3C: Text Processing Pipeline](module3C-text-processing.md)
- 🏠 Home: [Module 3 Navigation Guide](module3-navigation.md)
