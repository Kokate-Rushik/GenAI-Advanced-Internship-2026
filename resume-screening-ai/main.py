import os
from dotenv import load_dotenv
from chains.screening_pipeline import get_screening_chain
import json

# Load environment for LangSmith tracing 
load_dotenv()

def run_assignment():
    # Initialize chains
    extract_chain, score_chain = get_screening_chain()
    
    job_description = "Senior Data Scientist: Requires 5+ years experience, Python, PyTorch, and LLM orchestration."
    
    candidates = {
        "Strong": "8 years as Data Scientist. Expert in Python, PyTorch, and LangChain. Developed RAG systems.",
        "Average": "2 years experience in Data Analysis. Proficient in Python and SQL. Basic ML knowledge.",
        "Weak": "Professional Chef with 10 years experience in Italian cuisine. Expert in kitchen management."
    }

    for category, resume in candidates.items():
        print(f"\n--- Processing {category} Candidate ---")
        
        extracted_info = extract_chain.invoke({"resume_text": resume})    
        
        final_report = score_chain.invoke({
            "extracted_data": extracted_info,
            "job_description": job_description
        })
        
        print(json.dumps(final_report, indent=4))

if __name__ == "__main__":
    run_assignment()