
# Mercor Tooling & AI Workflows Assessment

## Project Overview

A complete contractor application system built on Airtable with AI-powered evaluation using Google Gemini API. The system handles multi-table data collection, compression, automated shortlisting, and LLM-based candidate assessment.

## Features Implemented

### ✅ Core Requirements

- **Multi-Table Form Flow**: Three separate forms for Personal Details, Work Experience, and Salary Preferences
- **JSON Compression**: Python script that gathers data from linked tables into a single JSON object
- **JSON Decompression**: Script to restore data from JSON back to normalized tables
- **Auto-Shortlisting**: Rules-based candidate evaluation (experience, compensation, location)
- **LLM Integration**: Google Gemini API for qualitative candidate assessment

### ✅ Additional Features

- Error handling with exponential backoff
- Environment-based configuration
- Mock LLM mode for testing without API keys
- Comprehensive logging and validation

## Technical Stack

- **Airtable**: Database and form management
- **Python 3.9+**: Core automation scripts
- **Google Gemini API**: AI-powered candidate evaluation
- **pyAirtable**: Airtable API integration

## Setup Instructions

### Prerequisites

1. Airtable account with personal access token
2. Google Gemini API key (optional - mock mode available)
3. Python 3.9+ environment

### Installation


# Clone or download project files
git clone https://github.com/Shreshth-07/Recruiting.git

# Install dependencies
pip install -r requirements.txt

### Environment Setup

Create a `.env` file with your credentials:

AIRTABLE_ACCESS_TOKEN=patRWoTtFVj4BSQWk.8bb1d4b5626d4ccfba03da5deef9ee8d14aeee52e08ee4518a8f9f19cd45e6fd
AIRTABLE_BASE_ID=app3Ol96NiMglNFme
GEMINI_API_KEY=YOUR_GEMINI_API

### Airtable Setup

1. Create base with these tables:
   * Applicants (parent table)
   * Personal Details (linked)
   * Work Experience (linked)
   * Salary Preferences (linked)
   * Shortlisted Leads (output)
2. Create forms for each child table
3. Set up field types and relationships

### Basic Flow

1. Applicants submit three forms with same Applicant ID
2. Run compression: `python compress_json.py`
3. Run shortlisting: `python shortlist_candidates.py`
4. Run LLM evaluation: `python llm_evaluation_gemini.py`

### Complete Pipeline

python main.py

## File Structure


Recruiting/
├── main.py
├── config.py
├── utils.py
├── compress_json.py
├── decompress_json.py
├── shortlist_candidates.py
├── llm_evaluation_gemini.py
├── mock_llm_evaluation.py
├── create_sample_data.py
├── debug_schema.py
├── requirements.txt
├── .env.example
└── README.md

