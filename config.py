import os
from dotenv import load_dotenv

load_dotenv()

# Airtable Configuration
AIRTABLE_ACCESS_TOKEN = os.getenv('AIRTABLE_ACCESS_TOKEN')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Table Names
APPLICANTS_TABLE = "Applicants"
PERSONAL_TABLE = "Personal Details"
EXPERIENCE_TABLE = "Work Experience"
SALARY_TABLE = "Salary Preferences"
SHORTLISTED_TABLE = "Shortlisted Leads"

# Tier-1 Companies for Shortlisting
TIER_1_COMPANIES = [
    "Google", "Meta", "OpenAI", "Microsoft", "Apple", 
    "Amazon", "Netflix", "Twitter", "Facebook", "Tesla",
    "Nvidia", "Adobe", "Salesforce", "Uber", "Airbnb"
]

# Currency Conversion Rates (to USD)
CURRENCY_RATES = {
    'USD': 1,
    'CAD': 0.75,
    'GBP': 1.25,
    'EUR': 1.10,
    'INR': 0.012
}

# Eligible Countries
ELIGIBLE_COUNTRIES = [
    'us', 'usa', 'united states', 'united states of america',
    'canada', 'ca',
    'uk', 'united kingdom', 'great britain', 'england',
    'germany', 'de', 'deutschland',
    'india', 'in', 'ind'
]