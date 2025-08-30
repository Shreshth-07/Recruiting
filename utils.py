import json
from datetime import datetime
from config import CURRENCY_RATES, ELIGIBLE_COUNTRIES, TIER_1_COMPANIES

def calculate_experience_years(experience_data):
    """Calculate total years of experience from experience data"""
    total_years = 0
    
    for job in experience_data:
        start_str = job.get('start', '')
        end_str = job.get('end', '')
        
        if start_str and end_str:
            try:
                start_date = datetime.strptime(start_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_str, '%Y-%m-%d')
                years = (end_date - start_date).days / 365.25
                total_years += years
            except ValueError:
                # Handle different date formats if needed
                continue
    
    return total_years

def has_tier1_experience(experience_data):
    """Check if applicant worked at a tier-1 company"""
    for job in experience_data:
        company = job.get('company', '').lower()
        for tier1_company in TIER_1_COMPANIES:
            if tier1_company.lower() in company:
                return True
    return False

def meets_location_criteria(location):
    """Check if location is in allowed countries"""
    if not location:
        return False
    
    location_lower = location.lower()
    return any(country in location_lower for country in ELIGIBLE_COUNTRIES)

def convert_to_usd(amount, currency):
    """Convert amount to USD using conversion rates"""
    return amount * CURRENCY_RATES.get(currency, 1)

def validate_applicant_data(compressed_data):
    """Validate the compressed JSON data structure"""
    required_sections = ['personal', 'experience', 'salary']
    for section in required_sections:
        if section not in compressed_data:
            return False
    
    personal = compressed_data['personal']
    if not all(key in personal for key in ['name', 'email', 'location']):
        return False
    
    return True

def format_currency(amount, currency='USD'):
    """Format currency amount with symbol"""
    symbols = {
        'USD': '$',
        'CAD': 'C$',
        'GBP': '£',
        'EUR': '€',
        'INR': '₹'
    }
    symbol = symbols.get(currency, '$')
    return f"{symbol}{amount:,.2f}"