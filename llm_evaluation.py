import os
import json
import time
import google.generativeai as genai
from pyairtable import Api
from config import AIRTABLE_ACCESS_TOKEN, AIRTABLE_BASE_ID, APPLICANTS_TABLE, GEMINI_API_KEY

# Initialize Airtable API
api = Api(AIRTABLE_ACCESS_TOKEN)
base_id = AIRTABLE_BASE_ID

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def call_gemini_api(compressed_json):
    """Call Gemini API to evaluate applicant"""
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash-lite')
        
        prompt = f"""
        You are a recruiting analyst. Given this JSON applicant profile, do four things:
        1. Provide a concise 75-word summary.
        2. Rate overall candidate quality from 1-10 (higher is better).
        3. List any data gaps or inconsistencies you notice.
        4. Suggest up to three follow-up questions to clarify gaps.
        
        Applicant Data:
        {json.dumps(compressed_json, indent=2)}
        
        Return exactly in this format without any additional text or markdown:
        Summary: <text>
        Score: <integer>
        Issues: <comma-separated list or 'None'>
        Follow-Ups: • <question 1> • <question 2> • <question 3>
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=500,
                temperature=0.3
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini API call failed: {e}")
        return None

def parse_llm_response(response_text):
    """Parse the LLM response into structured data"""
    summary = ""
    score = 0
    issues = "None"
    follow_ups = "None"
    
    if not response_text:
        return summary, score, issues, follow_ups
    
    lines = response_text.split('\n')
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith('Summary:'):
            current_section = 'summary'
            summary = line.replace('Summary:', '').strip()
        elif line.startswith('Score:'):
            current_section = 'score'
            score_str = line.replace('Score:', '').strip()
            try:
                score = int(score_str)
            except ValueError:
                score = 0
        elif line.startswith('Issues:'):
            current_section = 'issues'
            issues = line.replace('Issues:', '').strip()
        elif line.startswith('Follow-Ups:'):
            current_section = 'followups'
            follow_ups = line.replace('Follow-Ups:', '').strip()
        elif current_section == 'summary' and line and not any(line.startswith(prefix) for prefix in ['Score:', 'Issues:', 'Follow-Ups:']):
            summary += " " + line
        elif current_section == 'issues' and line and not any(line.startswith(prefix) for prefix in ['Summary:', 'Score:', 'Follow-Ups:']):
            issues += " " + line
        elif current_section == 'followups' and line and not any(line.startswith(prefix) for prefix in ['Summary:', 'Score:', 'Issues:']):
            follow_ups += " " + line
    
    # Clean up responses
    issues = issues if issues and issues != "None" else "None"
    follow_ups = follow_ups if follow_ups and follow_ups != "None" else "None"
    
    return summary[:500], score, issues[:200], follow_ups[:500]

def evaluate_with_llm(applicant_id, max_retries=3):
    """Evaluate an applicant using LLM with retry logic"""
    applicants = api.table(base_id, APPLICANTS_TABLE)
    records = applicants.all(formula=f"{{Applicant ID}} = '{applicant_id}'")
    
    if not records:
        print(f"Applicant {applicant_id} not found")
        return False
    
    record = records[0]
    compressed_json_str = record['fields'].get('Compressed JSON', '{}')
    
    if not compressed_json_str or compressed_json_str == '{}':
        print(f"No compressed JSON found for applicant {applicant_id}")
        return False
    
    try:
        compressed_data = json.loads(compressed_json_str)
    except json.JSONDecodeError:
        print(f"Invalid JSON for applicant {applicant_id}")
        return False
    
    # Call Gemini API with retry logic
    response = None
    for attempt in range(max_retries):
        response = call_gemini_api(compressed_data)
        if response:
            break
        wait_time = 2 ** attempt  # Exponential backoff
        print(f"Retry {attempt + 1} in {wait_time} seconds...")
        time.sleep(wait_time)
    
    if not response:
        print(f"Failed to get LLM response for applicant {applicant_id} after {max_retries} attempts")
        return False
    
    # Parse response and update record
    summary, score, issues, follow_ups = parse_llm_response(response)
    
    applicants.update(record['id'], {
        "LLM Summary": summary,
        "LLM Score": score,
        "LLM Follow-Ups": follow_ups
    })
    
    print(f"✓ LLM evaluation completed for applicant {applicant_id}")
    return True

def evaluate_all_with_llm():
    """Evaluate all applicants with LLM who haven't been evaluated yet"""
    applicants = api.table(base_id, APPLICANTS_TABLE).all()
    evaluated_count = 0
    
    for applicant in applicants:
        applicant_id = applicant['fields'].get('Applicant ID')
        compressed_json = applicant['fields'].get('Compressed JSON')
        
        # Only evaluate if compressed data exists and hasn't been evaluated
        if compressed_json and compressed_json != '{}' and not applicant['fields'].get('LLM Summary'):
            print(f"Evaluating applicant {applicant_id} with LLM...")
            if evaluate_with_llm(applicant_id):
                evaluated_count += 1
            # Add a small delay to avoid rate limiting
            time.sleep(1)
    
    return evaluated_count

if __name__ == "__main__":
    print("1. Evaluate specific applicant with LLM")
    print("2. Evaluate all applicants with LLM")
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        applicant_id = input("Enter Applicant ID to evaluate with LLM: ")
        evaluate_with_llm(applicant_id)
    elif choice == "2":
        count = evaluate_all_with_llm()
        print(f"LLM evaluation completed! {count} applicants evaluated.")
    else:
        print("Invalid choice")