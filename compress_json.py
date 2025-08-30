import os
import json
from pyairtable import Api
from config import AIRTABLE_ACCESS_TOKEN, AIRTABLE_BASE_ID, APPLICANTS_TABLE, PERSONAL_TABLE, EXPERIENCE_TABLE, SALARY_TABLE
from utils import validate_applicant_data

# Initialize Airtable API
api = Api(AIRTABLE_ACCESS_TOKEN)
base_id = AIRTABLE_BASE_ID

def get_applicant_data(applicant_id):
    """Fetch all data for a specific applicant across tables"""
    
    # Get personal details
    personal_records = api.table(base_id, PERSONAL_TABLE).all(
        formula=f"{{Applicant ID}} = '{applicant_id}'"
    )
    personal_data = personal_records[0]['fields'] if personal_records else {}
    
    # Get work experience
    experience_records = api.table(base_id, EXPERIENCE_TABLE).all(
        formula=f"{{Applicant ID}} = '{applicant_id}'"
    )
    experience_data = [record['fields'] for record in experience_records]
    
    # Get salary preferences
    salary_records = api.table(base_id, SALARY_TABLE).all(
        formula=f"{{Applicant ID}} = '{applicant_id}'"
    )
    salary_data = salary_records[0]['fields'] if salary_records else {}
    
    # Build compressed JSON
    compressed_json = {
        "personal": {
            "name": personal_data.get("Full Name", ""),
            "email": personal_data.get("Email", ""),
            "location": personal_data.get("Location", ""),
            "linkedin": personal_data.get("LinkedIn URL", "")
        },
        "experience": [
            {
                "company": exp.get("Company", ""),
                "title": exp.get("Title", ""),
                "start": exp.get("Start Date", ""),
                "end": exp.get("End Date", ""),
                "technologies": exp.get("Technologies", "").split(", ") if exp.get("Technologies") else []
            } for exp in experience_data
        ],
        "salary": {
            "preferred_rate": salary_data.get("Preferred Rate", 0),
            "minimum_rate": salary_data.get("Minimum Rate", 0),
            "currency": salary_data.get("Currency", "USD"),
            "availability": salary_data.get("Availability", 0)
        }
    }
    
    return compressed_json

def update_applicant_json(applicant_id, compressed_json):
    """Update the applicant record with compressed JSON"""
    applicants = api.table(base_id, APPLICANTS_TABLE)
    
    # Find the applicant record
    records = applicants.all(formula=f"{{Applicant ID}} = '{applicant_id}'")
    
    if records:
        record_id = records[0]['id']
        applicants.update(record_id, {
            "Compressed JSON": json.dumps(compressed_json, indent=2)
        })
        print(f"Updated compressed JSON for applicant {applicant_id}")
        return True
    else:
        print(f"Applicant {applicant_id} not found")
        return False

def compress_all_applicants():
    """Compress data for all applicants who don't have compressed JSON"""
    applicants = api.table(base_id, APPLICANTS_TABLE).all()
    
    for applicant in applicants:
        applicant_id = applicant['fields'].get('Applicant ID')
        compressed_json = applicant['fields'].get('Compressed JSON')
        
        # Only compress if not already compressed
        if not compressed_json:
            print(f"Compressing data for applicant {applicant_id}...")
            compressed_data = get_applicant_data(applicant_id)
            if validate_applicant_data(compressed_data):
                update_applicant_json(applicant_id, compressed_data)
            else:
                print(f"Incomplete data for applicant {applicant_id}")

if __name__ == "__main__":
    print("1. Compress specific applicant")
    print("2. Compress all applicants")
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        applicant_id = input("Enter Applicant ID to compress: ")
        compressed_data = get_applicant_data(applicant_id)
        if validate_applicant_data(compressed_data):
            update_applicant_json(applicant_id, compressed_data)
            print("Compression completed successfully!")
        else:
            print("Error: Applicant data is incomplete")
    elif choice == "2":
        compress_all_applicants()
        print("Batch compression completed!")
    else:
        print("Invalid choice")