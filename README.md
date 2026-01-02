# 📚 Pre-Encoding Automation: PDF → Obsidian Notes Generator

A locally deployable Python application that converts academic PDFs into structured Obsidian-compatible Markdown notes, schemas, and assessments using the Groq LLM API.

## 🎯 Core Functionality

The application provides three main output types from a single PDF:

1. **Rephrased & Clarified Notes** (`_notes.md`)
   - Simplifies complex academic content into student-friendly language
   - Organizes content with hierarchical headings (##, ###) separated by horizontal rules
   - Appends 5-7 Bloom's Taxonomy L1-L2 comprehension questions for self-assessment
   - Maintains semantic structure while improving readability

2. **Schema/Overview Document** (`_schema.md`)
   - 200-300 word executive summary of the material
   - Obsidian-compatible callouts:
     - `abstract`: Key definitions and terminology
     - `settings`: Important assumptions or preconditions
     - `globe`: Real-world applications and examples
     - `chart`: Data, statistics, or numerical insights
     - `zip`: Summary of takeaways
   - Concept map using Mermaid graph diagrams
   - 3-5 quick revision questions for self-testing

3. **Assessment Questions** (`_assessment_{level}.md`)
   - 8-10 questions at a specific Bloom's Taxonomy level
   - Three difficulty levels: **Remember (L1)**, **Understand (L2)**, **Apply (L3)**
   - Questions only—no answers, hints, or solutions
   - Numbered list format, Markdown-compatible

## 📋 Project Structure

```
.
├── main.py                            # Entry point and Groq API initialization
├── requirements.txt                   # Python dependencies
├── .env.example                       # Template for configuration
├── README.md                          # This file
│
├── ui/                                # Web interface layer
│   └── gradio_ui.py                   # Gradio web UI and event handlers
│
├── core/                              # Core processing modules
│   ├── pdf_loader.py                  # PDF text extraction (pypdf)
│   ├── groq_client.py                 # Groq API client with rate limiting (5500 tokens/min)
│   ├── chunked_processor.py           # Text chunking (5000 tokens/chunk)
│   ├── markdown_writer.py             # Markdown file I/O and generation
│   └── json_utils.py                  # JSON serialization utilities
│
├── prompts/                           # LLM prompt templates
│   └── assessment.py                  # Three prompt functions for each output type
│
└── outputs/                           # Generated Markdown files (created at runtime)
    └── (generated .md files appear here)
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Groq API key (free tier available: https://console.groq.com)

### 2. Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Groq API key
cp .env.example .env
# Edit .env and replace 'your_groq_api_key_here' with your actual key
```

### 3. Run the Application

```bash
python main.py
```

The application will start on `http://127.0.0.1:7860` (open in your browser).


## 🎓 Bloom's Taxonomy Reference

| Level | Name | Action | Example Verbs | Question Type |
|-------|------|--------|---------------|---------------|
| **L1** | **Remember** | Recall facts & definitions | Define, List, Identify, Recall, State | "What is X?" |
| **L2** | **Understand** | Explain concepts | Explain, Describe, Summarize, Classify, Interpret | "Why does X occur?" / "Describe X" |
| **L3** | **Apply** | Use in new situations | Apply, Solve, Demonstrate, Construct, Use | "How would you apply X to Y?" |

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `gradio` | 4.26.0 | Web interface framework |
| `groq` | 0.4.2 | Groq LLM API client |
| `pypdf` | 4.0.1 | PDF text extraction |
| `python-dotenv` | 1.0.0 | Environment variable management |

[[preEncodingPhase.png|thumb|center|600px]]

**Pre-Encoding-Automation** The app that I have wanted to build for a long time!
© 2026 Yossef Moftah. Licensed under MIT License.
January 2026.
