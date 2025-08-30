import os
import json
from pyairtable import Api
from config import AIRTABLE_ACCESS_TOKEN, AIRTABLE_BASE_ID, APPLICANTS_TABLE, PERSONAL_TABLE, EXPERIENCE_TABLE, SALARY_TABLE

# Initialize Airtable API
api = Api(AIRTABLE_ACCESS_TOKEN)
base_id = AIRTABLE_BASE_ID

def decompress_json(applicant_id):
    """Decompress JSON and update child tables"""
    
    # Get the compressed JSON from Applicants table
    applicants = api.table(base_id, APPLICANTS_TABLE)
    records = applicants.all(formula=f"{{Applicant ID}} = '{applicant_id}'")
    
    if not records:
        print(f"Applicant {applicant_id} not found")
        return False
    
    compressed_json_str = records[0]['fields'].get('Compressed JSON', '{}')
    compressed_data = json.loads(compressed_json_str)
    
    # Update Personal Details
    personal_data = compressed_data.get('personal', {})
    personal_records = api.table(base_id, PERSONAL_TABLE).all(
        formula=f"{{Applicant ID}} = '{applicant_id}'"
    )
    
    personal_fields = {
        "Full Name": personal_data.get('name', ''),
        "Email": personal_data.get('email', ''),
        "Location": personal_data.get('location', ''),
        "LinkedIn URL": personal_data.get('linkedin', '')
    }
    
    if personal_records:
        api.table(base_id, PERSONAL_TABLE).update(personal_records[0]['id'], personal_fields)
    else:
        personal_fields["Applicant ID"] = applicant_id
        api.table(base_id, PERSONAL_TABLE).create(personal_fields)
    
    # Update Work Experience (delete existing and create new)
    experience_data = compressed_data.get('experience', [])
    existing_exp_records = api.table(base_id, EXPERIENCE_TABLE).all(
        formula=f"{{Applicant ID}} = '{applicant_id}'"
    )
    
    # Delete existing experience records
    for record in existing_exp_records:
        api.table(base_id, EXPERIENCE_TABLE).delete(record['id'])
    
    # Create new experience records
    for exp in experience_data:
        experience_fields = {
            "Applicant ID": applicant_id,
            "Company": exp.get('company', ''),
            "Title": exp.get('title', ''),
            "Start Date": exp.get('start', ''),
            "End Date": exp.get('end', ''),
            "Technologies": ", ".join(exp.get('technologies', []))
        }
        api.table(base_id, EXPERIENCE_TABLE).create(experience_fields)
    
    # Update Salary Preferences
    salary_data = compressed_data.get('salary', {})
    salary_records = api.table(base_id, SALARY_TABLE).all(
        formula=f"{{Applicant ID}} = '{applicant_id}'"
    )
    
    salary_fields = {
        "Preferred Rate": salary_data.get('preferred_rate', 0),
        "Minimum Rate": salary_data.get('minimum_rate', 0),
        "Currency": salary_data.get('currency', 'USD'),
        "Availability": salary_data.get('availability', 0)
    }
    
    if salary_records:
        api.table(base_id, SALARY_TABLE).update(salary_records[0]['id'], salary_fields)
    else:
        salary_fields["Applicant ID"] = applicant_id
        api.table(base_id, SALARY_TABLE).create(salary_fields)
    
    print(f"Decompression completed for applicant {applicant_id}")
    return True

def decompress_all_applicants():
    """Decompress all applicants who have compressed JSON"""
    applicants = api.table(base_id, APPLICANTS_TABLE).all()
    
    for applicant in applicants:
        applicant_id = applicant['fields'].get('Applicant ID')
        compressed_json = applicant['fields'].get('Compressed JSON')
        
        # Only decompress if compressed data exists
        if compressed_json:
            print(f"Decompressing data for applicant {applicant_id}...")
            decompress_json(applicant_id)

if __name__ == "__main__":
    print("1. Decompress specific applicant")
    print("2. Decompress all applicants")
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        applicant_id = input("Enter Applicant ID to decompress: ")
        decompress_json(applicant_id)
    elif choice == "2":
        decompress_all_applicants()
        print("Batch decompression completed!")
    else:
        print("Invalid choice")