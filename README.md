# AI Workflows Assessment Project

## Project Overview

A complete contractor application system built on Airtable with AI-powered evaluation using Google Gemini API. This system handles multi-table data collection, JSON compression/decompression, automated candidate shortlisting, and LLM-based qualitative assessment.

## Features Implemented

### Core Requirements

* **Multi-Table Form Flow** : Three separate forms for Personal Details, Work Experience, and Salary Preferences
* **JSON Compression** : Python script that gathers data from linked tables into a single JSON object
* **JSON Decompression** : Script to restore data from JSON back to normalized tables
* **Auto-Shortlisting** : Rules-based candidate evaluation (experience, compensation, location)
* **LLM Integration** : Google Gemini API for qualitative candidate assessment

### Additional Features

* Error handling with exponential backoff
* Environment-based configuration
* Mock LLM mode for testing without API keys
* Comprehensive logging and validation
* Automatic field type detection (Link vs Text fields)

## Technology Stack

* **Python 3.8+** : Core automation scripts
* **Airtable** : Database and form management
* **Google Gemini API** : AI-powered candidate evaluation
* **pyAirtable** : Airtable API integration
* **python-dotenv** : Environment configuration

## Project Structure

```
Recruiting/
├── main.py                 # Main orchestrator script
├── config.py              # Configuration and constants
├── utils.py               # Utility functions and helpers
├── compress_json.py       # JSON compression script
├── decompress_json.py     # JSON decompression script
├── shortlist_candidates.py # Auto-shortlisting logic
├── llm_evaluation_gemini.py # Gemini AI integration
├── mock_llm_evaluation.py # Mock LLM (no API needed)
├── create_sample_data.py  # Sample data generator
├── debug_schema.py        # Airtable schema debugger
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
└── README.md            # This documentation
```

## Airtable Setup

### Step 1: Create Airtable Base

1. Go to [Airtable.com](https://airtable.com/) and create account
2. Click "Add a base" → "Start from scratch"
3. Name it "Contractor Applications"

### Step 2: Create Tables with These Fields

**Applicants Table** (Main table)

* Applicant ID (Autonumber, Primary field)
* Compressed JSON (Long text)
* Shortlist Status (Single select: Pending, Shortlisted, Rejected)
* LLM Summary (Long text)
* LLM Score (Number)
* LLM Follow-Ups (Long text)
* Created Time (Created time, auto)

**Personal Details Table**

* Record ID (Autonumber)
* Applicant ID (Link to Applicants OR Text field)
* Full Name (Single line text)
* Email (Email)
* Location (Single line text)
* LinkedIn URL (URL)

**Work Experience Table**

* Record ID (Autonumber)
* Applicant ID (Link to Applicants OR Text field)
* Company (Single line text)
* Title (Single line text)
* Start Date (Date)
* End Date (Date)
* Technologies (Long text)

**Salary Preferences Table**

* Record ID (Autonumber)
* Applicant ID (Link to Applicants OR Text field)
* Preferred Rate (Currency)
* Minimum Rate (Currency)
* Currency (Single select: USD, CAD, GBP, EUR, INR)
* Availability (Number)

**Shortlisted Leads Table**

* Record ID (Autonumber)
* Applicant (Link to Applicants)
* Compressed JSON (Long text)
* Score Reason (Long text)
* Created At (Created time)

### Step 3: Create Forms

Create three separate forms for:

1. **Personal Details Form** : Includes Applicant ID (text field), Full Name, Email, Location, LinkedIn URL
2. **Work Experience Form** : Includes Applicant ID (text field), Company, Title, Start Date, End Date, Technologies
3. **Salary Preferences Form** : Includes Applicant ID (text field), Preferred Rate, Minimum Rate, Currency, Availability

### Step 4: Get Airtable Credentials

1. Go to [Airtable Account](https://airtable.com/account)
2. Under "API" → "Generate personal access token"
3. Copy your token (starts with `pat...`)
4. Get your Base ID from your base URL: `https://airtable.com/appXXXXXXXXXXXXXX/...`

## Local Setup

### Prerequisites

* Python 3.8 or higher
* Airtable account
* Google Gemini API key (optional - mock mode available)

### Step 1: Download Project

```
# Clone the repository
git clone https://github.com/Shreshth-07/Recruiting.git
cd Recruiting

# Or download ZIP and extract
# Then navigate to the project directory
```

### Step 2: Create Virtual Environment

```
# On macOS/Linux:
python -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```
pip install -r requirements.txt
```

### Step 4: Configure Environment

```
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use any text editor
```

**Edit .env file:**

```
# Airtable Configuration
AIRTABLE_ACCESS_TOKEN=your_personal_access_token_here
AIRTABLE_BASE_ID=your_base_id_here

# Gemini API Configuration (Optional)
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 5: Get Gemini API Key (Optional)

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with Google account
3. Click "Get API key" and create new key
4. Add it to your `.env` file

## How to Run

### Option 1: Complete Pipeline

```
python main.py
```

This runs:

1. Compression of all applicant data
2. Shortlisting based on criteria
3. LLM evaluation of candidates

### Option 2: Individual Scripts

**Compress Data:**

```
python compress_json.py
# Choose: 1 for specific applicant, 2 for all applicants
```

**Decompress Data:**

```
python decompress_json.py
# Choose: 1 for specific applicant, 2 for all applicants
```

**Shortlist Candidates:**

```
python shortlist_candidates.py
```

**LLM Evaluation:**

```
# With Gemini API:
python llm_evaluation_gemini.py

# Or with mock LLM (no API key needed):
python mock_llm_evaluation.py
```

### Option 3: Step-by-Step Workflow

1. **Create Applicant Record** : Manually in Airtable or use sample script
2. **Submit Forms** : Use the three forms with the same Applicant ID
3. **Compress Data** : `python compress_json.py` → Choose option 2
4. **Shortlist Candidates** : `python shortlist_candidates.py`
5. **LLM Evaluation** : `python llm_evaluation_gemini.py` → Choose option 2

## Shortlisting Criteria

Candidates are automatically shortlisted based on:

| Criterion              | Rule                                                             |
| ---------------------- | ---------------------------------------------------------------- |
| **Experience**   | ≥4 years total OR worked at Tier-1 company (Google, Meta, etc.) |
| **Compensation** | Preferred Rate ≤ $100 USD/hour AND Availability ≥ 20 hrs/week  |
| **Location**     | In US, Canada, UK, Germany, or India                             |

## LLM Evaluation

The AI evaluation provides:

* **Summary** : 75-word candidate overview
* **Score** : Quality rating from 1-10
* **Issues** : Data gaps or inconsistencies
* **Follow-ups** : 3 clarifying questions

## Customization

### Modify Shortlist Criteria

Edit `evaluate_applicant()` function in `shortlist_candidates.py`:

```
# Current criteria in utils.py:
def evaluate_applicant(applicant_id, compressed_json):
    # Modify these rules as needed
    experience_ok = experience_years >= 4 or has_tier1_experience(experience_data)
    compensation_ok = usd_rate <= 100 and availability >= 20
    location_ok = meets_location_criteria(location)
```

### Change LLM Prompt

Edit the prompt in `llm_evaluation_gemini.py`:

```
prompt = f"""
You are a recruiting analyst. Given this JSON applicant profile, do four things:
1. Provide a concise 75-word summary.
2. Rate overall candidate quality from 1-10 (higher is better).
3. List any data gaps or inconsistencies you notice.
4. Suggest up to three follow-up questions to clarify gaps.
"""
```

## Usage Example

1. **Create applicant** in Airtable (gets auto ID like "19")
2. **Fill forms** with Applicant ID "19":
   * Personal Details form
   * Work Experience form
   * Salary Preferences form
3. **Run compression** : `python compress_json.py` → Enter "19"
4. **Run shortlisting** : `python shortlist_candidates.py`
5. **Run LLM eval** : `python llm_evaluation_gemini.py` → Enter "19"

## API Rate Limits

* **Airtable** : 5 requests per second
* **Gemini** : 60 requests per minute (free tier)
* Built-in retry logic with exponential backoff

## Security Notes

* API keys stored in `.env` file (never in code)
* `.env` included in `.gitignore`
* Personal access tokens instead of deprecated API keys
* No sensitive data in repository

## Sample Output

Successful run will show:

```
===Application System ===
Starting complete processing pipeline...

1. Compressing applicant data...
Compressing data for applicant 19...
Updated compressed JSON for applicant 19

2. Shortlisting candidates...
✓ Shortlisted applicant 19

3. Running LLM evaluation...
Evaluating applicant 19 with LLM...
✓ LLM evaluation completed for applicant 19

=== Processing Complete ===
Shortlisted: 1 applicants
LLM Evaluated: 1 applicants
Check your Airtable base for results!
```
