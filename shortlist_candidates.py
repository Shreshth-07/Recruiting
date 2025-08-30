import os
import json
from pyairtable import Api
from datetime import datetime
from config import AIRTABLE_ACCESS_TOKEN, AIRTABLE_BASE_ID, APPLICANTS_TABLE, SHORTLISTED_TABLE
from utils import calculate_experience_years, has_tier1_experience, meets_location_criteria, convert_to_usd, format_currency

# Initialize Airtable API
api = Api(AIRTABLE_ACCESS_TOKEN)
base_id = AIRTABLE_BASE_ID

def evaluate_applicant(applicant_id, compressed_json):
    """Evaluate if applicant meets shortlist criteria"""
    personal_data = compressed_json.get('personal', {})
    experience_data = compressed_json.get('experience', [])
    salary_data = compressed_json.get('salary', {})
    
    # Experience criteria: ≥4 years OR tier-1 company
    experience_years = calculate_experience_years(experience_data)
    tier1_experience = has_tier1_experience(experience_data)
    experience_ok = experience_years >= 4 or tier1_experience
    
    # Compensation criteria: Preferred Rate ≤ $100 USD/hour AND Availability ≥ 20 hrs/week
    currency = salary_data.get('currency', 'USD')
    preferred_rate = salary_data.get('preferred_rate', 0)
    availability = salary_data.get('availability', 0)
    
    # Convert to USD
    usd_rate = convert_to_usd(preferred_rate, currency)
    compensation_ok = usd_rate <= 100 and availability >= 20
    
    # Location criteria
    location = personal_data.get('location', '')
    location_ok = meets_location_criteria(location)
    
    # Generate score reason
    score_reason_parts = []
    
    if experience_ok:
        if experience_years >= 4:
            score_reason_parts.append(f"{experience_years:.1f} years of experience")
        else:
            score_reason_parts.append("Worked at tier-1 company")
    else:
        score_reason_parts.append("Insufficient experience")
    
    if compensation_ok:
        score_reason_parts.append(f"Rate {format_currency(usd_rate)}/hr, {availability} hrs/wk available")
    else:
        if usd_rate > 100:
            score_reason_parts.append(f"Rate {format_currency(usd_rate)}/hr exceeds $100 limit")
        if availability < 20:
            score_reason_parts.append(f"Only {availability} hrs/wk available (needs 20+)")
    
    if location_ok:
        score_reason_parts.append("Location acceptable")
    else:
        score_reason_parts.append(f"Location '{location}' not in target regions")
    
    return all([experience_ok, compensation_ok, location_ok]), " | ".join(score_reason_parts)

def shortlist_applicants():
    """Evaluate all applicants and shortlist those who meet criteria"""
    applicants = api.table(base_id, APPLICANTS_TABLE).all()
    shortlisted_count = 0
    
    for applicant in applicants:
        applicant_id = applicant['fields'].get('Applicant ID')
        compressed_json_str = applicant['fields'].get('Compressed JSON', '{}')
        
        if not compressed_json_str:
            print(f"Skipping applicant {applicant_id} - no compressed data")
            continue
            
        try:
            compressed_data = json.loads(compressed_json_str)
        except json.JSONDecodeError:
            print(f"Skipping applicant {applicant_id} - invalid JSON")
            continue
            
        should_shortlist, score_reason = evaluate_applicant(applicant_id, compressed_data)
        
        # Update shortlist status
        api.table(base_id, APPLICANTS_TABLE).update(applicant['id'], {
            "Shortlist Status": "Shortlisted" if should_shortlist else "Rejected"
        })
        
        # Create Shortlisted Leads record if applicable
        if should_shortlist:
            # Check if already exists
            existing_records = api.table(base_id, SHORTLISTED_TABLE).all(
                formula=f"{{Applicant}} = '{applicant_id}'"
            )
            
            if not existing_records:
                api.table(base_id, SHORTLISTED_TABLE).create({
                    "Applicant": applicant_id,
                    "Compressed JSON": compressed_json_str,
                    "Score Reason": score_reason,
                    "Created At": datetime.now().isoformat()
                })
                print(f"✓ Shortlisted applicant {applicant_id}")
                shortlisted_count += 1
            else:
                print(f"Applicant {applicant_id} already shortlisted")
        else:
            print(f"✗ Rejected applicant {applicant_id}: {score_reason}")
    
    return shortlisted_count

if __name__ == "__main__":
    print("Starting shortlist evaluation...")
    count = shortlist_applicants()
    print(f"Shortlisting completed! {count} applicants shortlisted.")