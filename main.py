import time
from compress_json import compress_all_applicants
from shortlist_candidates import shortlist_applicants
from llm_evaluation import evaluate_all_with_llm

def main():
    """Main orchestrator function to run the complete pipeline"""
    print("=== Mercor Contractor Application System ===")
    print("Starting complete processing pipeline...")
    
    # Step 1: Compress all applicant data
    print("\n1. Compressing applicant data...")
    compress_all_applicants()
    time.sleep(2)
    
    # Step 2: Shortlist candidates
    print("\n2. Shortlisting candidates...")
    shortlisted_count = shortlist_applicants()
    time.sleep(2)
    
    # Step 3: LLM evaluation
    print("\n3. Running LLM evaluation...")
    evaluated_count = evaluate_all_with_llm()
    
    print(f"\n=== Processing Complete ===")
    print(f"Shortlisted: {shortlisted_count} applicants")
    print(f"LLM Evaluated: {evaluated_count} applicants")
    print("Check your Airtable base for results!")

if __name__ == "__main__":
    main()