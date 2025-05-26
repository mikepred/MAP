"""
Text Analysis Script - Module 3B
A comprehensive text analysis tool for processing and analyzing text files.
"""

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

