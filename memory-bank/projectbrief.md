# Project Brief

This document is the foundation for the project and shapes all other Memory Bank files. It defines the core requirements and goals and serves as the source of truth for the project scope.

## Core Requirements (Text Analyzer)

* The `analyzer.py` script must:
  * Read content from a text file (e.g., `sample.txt`).
  * Clean the text (e.g., convert to lowercase, remove punctuation).
  * Tokenize the text into individual words.
  * Count the frequency of each word.
  * Display the most common words and their counts in a user-friendly format.
  * Be structured with modular functions, each performing a single, well-defined task.
  * Handle potential errors gracefully (e.g., file not found).

## Project Goals (Text Analyzer)

* Provide a functional Python script (`analyzer.py`) that performs basic text analysis.
* Serve as an educational tool for learners to understand fundamental NLP and LLM preprocessing steps.
* Demonstrate the connection between simple text processing techniques and the more complex data handling pipelines used in Large Language Models.
* Offer a clear and accessible entry point for beginners interested in Natural Language Processing and AI.

## Project: Python for Text Processing - A Foundation for LLMs (from .clinerules)

This project brief is derived from the `.clinerules` found in the `c:/Users/miken/OneDrive/Documents/GitHub/MAP/.clinerules/` directory, specifically the lesson plan for creating a Python text processing script.

### Project Goal (from `.clinerules/lesson-plan.md`)

Write a Python script that reads a text file, cleans it, tokenizes it, counts word frequencies, displays the most common words, and is structured with functions.

### Target Audience (from `.clinerules/lesson-plan.md`)

Adventurous learners familiar with Python basics (variables, loops, basic data structures, writing simple functions) but looking to apply these skills to a practical project and understand foundational text processing techniques.

### Overall Learning Objective (from `.clinerules/lesson-plan.md`)

To build a functional text processing pipeline in Python and understand how each component (reading, cleaning, tokenizing, counting) contributes to analyzing text data, drawing parallels to the initial stages of data preparation for LLMs.

### Reference to `llms-from-scratch` (from `.clinerules/lesson-plan.md`)

This project introduces core ideas like tokenization and data processing pipelines, which are fundamental to building LLMs. It's positioned as a foundational step ("learning the ABCs") before tackling more complex LLM concepts like those in the `llms-from-scratch` repository (e.g., `ch02/01_main-chapter-code/ch02.ipynb` or `ch02/05_bpe-from-scratch/bpe-from-scratch.ipynb`).

### Module Structure (from `.clinerules/lesson-plan.md`)

The lesson plan is divided into the following modules:

* **Module 1: Introduction & Setting the Stage** (`.clinerules/module1-introduction.md`)
  * Overview of text processing, project's role, connection to LLMs, and environment setup.
  * Includes creating `text_analyzer/` directory with `analyzer.py`, `sample.txt`, and `README.md`.
* **Module 2: Core Python Concepts for Text Processing** (`.clinerules/module2-python-concepts.md`)
  * Covers file handling, text cleaning (lowercase, punctuation removal), tokenization (`.split()`), frequency counting (`collections.Counter`), displaying results, and modular design with functions.
* **Module 3: Building the Script - Step-by-Step** (`.clinerules/module3-building-script.md`)
  * Provides complete implementations for functions: `read_file()`, `clean_text()`, `tokenize_text()`, `count_frequencies()`, `display_most_common()`, and the main execution block.
* **Module 4: Testing and Refinement** (`.clinerules/module4-testing.md`)
  * Guides through running the script, debugging common issues (file not found, empty output, encoding errors), and suggests enhancements (stop word removal, user input, file output, advanced cleaning, word length analysis, performance timing).
* **Module 5: Connecting to the Bigger World of LLMs** (`.clinerules/module5-llm-connections.md`)
  * Explores how the project's text processing skills relate to LLMs, `llms-from-scratch` concepts (advanced tokenization like BPE, data loading, embeddings), modern applications (chatbots, search, sentiment analysis), and further learning paths (NLTK, spaCy, advanced ML/NLP).

## Overarching Project: Self-Directed AI Engineering Education

### Core Goal
To achieve a deep understanding of AI engineering principles, with a focus on Large Language Models (LLMs), through a self-directed learning process. This involves hands-on implementation, conceptual understanding, and exploration of the current AI landscape.

### Guiding Conceptual Framework: "SAI"
The learning process is framed by the conceptual development of "SAI" (Self-directed AI learning interface/assistant/construct). The act of understanding how to build, or actually building components related to, SAI serves as the primary mechanism for mastering the subject matter.

### Key Learning Resources & Their Roles

1.  **Primary Technical Guide for LLM Implementation:**
    *   **Resource:** "Build a Large Language Model (From Scratch)" by Sebastian Raschka (book and GitHub repository `LLMs-from-scratch-main/`).
    *   **Role:** Provides the core, step-by-step practical guidance for building LLM components from the ground up. Progress through this resource is a primary measure of learning.

2.  **Comprehensive Theoretical & Practical Textbook:**
    *   **Resource:** "Generative AI with Python and PyTorch, Second Edition" (referred to as "GenAI PDF").
    *   **Role:** Serves as a detailed textbook complementing Raschka's work. It offers deeper theoretical explanations, covers foundational concepts (e.g., Deep Learning building blocks, early NLP/text representation via its Chapter 3), and explores advanced topics such as Prompt Engineering (Ch 7), LLM Tooling like LangChain (Ch 8), LLM Optimization (Ch 9), Emerging Applications (Ch 10), and other generative models like VAEs (Ch 11).
    *   **Current Focus:** Chapter 3 of this PDF ("The Rise of Methods for Text Generation") is particularly relevant for the current learning phase on "Text representation/early NLP."

3.  **Inspirational & Reference Curriculum:**
    *   **Resource:** "AI Engineering Master Curriculum" (from the file `This comprehensive lesson plan takes a l.md`, located in `c:/root/MAP/`).
    *   **Role:** Acts as a broad, inspirational map of the AI engineering field. It's a comprehensive reference for deeper dives into specific topics as they arise or for exploring related areas, rather than a strict syllabus to be completed in its entirety.

4.  **Foundational Practical Exercise:**
    *   **Resource:** The `text_analyzer` project.
    *   **Role:** An initial, hands-on project to build fundamental Python programming and basic text processing skills, serving as a stepping stone to more complex topics in Raschka's book and the GenAI PDF.

### Learning & Progress Tracking
*   **Cline's Memory Bank:** Used for session-to-session operational context, tracking immediate learning focus, and high-level progress.
*   **MCP Knowledge Graph Memory Server:** Employed for creating a structured, persistent, and platform-agnostic log of conceptual understanding, relationships between concepts, and learning milestones.

## Project: Git Branch Visualizer

### Core Requirements (Git Branch Visualizer)

* The `branch_visualizer.py` script must:
  * Operate on the Git repository located in the current working directory.
  * Fetch local Git branch names.
  * Fetch Git log data including commit SHAs, parent SHAs, and commit references (e.g., branch names, HEAD).
  * Parse commit references to identify which local branches point to specific commits.
  * Generate Mermaid `gitGraph` syntax that visually represents the local branch structure, commits, and merges.
  * Save the generated Mermaid code to a file named `branch_visualization.mermaid.txt`.

### Project Goals (Git Branch Visualizer)

* Provide a utility (`branch_visualizer.py`) to visualize the Git branch structure of the current repository.
* Output a Mermaid diagram that is compatible with standard Mermaid renderers (e.g., mermaid.live, integrated Markdown previews).
* Assist developers in understanding complex Git branch histories and relationships within their local repository.

## Cline's Operational Directives

The core operational directives governing my behavior and collaboration with you have been refined and are documented in `../../Cline/Rules/00-primary-directive.md`. These directives define my role as an expert, proactive coding partner, emphasizing continuous learning, knowledge persistence, and a principled approach to development and quality assurance.
