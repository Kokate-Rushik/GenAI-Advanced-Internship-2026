from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from prompts.system_prompts import EXTRACTION_PROMPT, SCORING_PROMPT
import os

def get_screening_chain():
    # Initialize Groq LLM with the versatile Llama model
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.1, # Lower temperature for extraction accuracy
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    
    extract_prompt = ChatPromptTemplate.from_messages([
        ("system", EXTRACTION_PROMPT),
        ("user", "Resume Text: {resume_text}")
    ])
    
    
    scoring_prompt = ChatPromptTemplate.from_messages([
        ("system", SCORING_PROMPT),
        ("user", "Extracted Data: {extracted_data}\nJob Description: {job_description}")
    ])

    
    # We return the components so main.py can invoke them sequentially
    extraction_chain = extract_prompt | llm | JsonOutputParser()
    scoring_chain = scoring_prompt | llm | JsonOutputParser()
    
    return extraction_chain, scoring_chain