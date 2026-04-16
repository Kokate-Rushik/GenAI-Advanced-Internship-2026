# System prompt for skill extraction
EXTRACTION_PROMPT = """
Extract the following details from the provided Resume text:
1. Primary Skills
2. Years of Experience 
3. Technical Tools
Return the output as a JSON object. Do NOT assume skills not present.
"""

# System prompt for matching and scoring
SCORING_PROMPT = """
Compare the extracted Resume data with the Job Description.
1. Assign a Fit Score (0-100).
2. Provide a clear reasoning/explanation for the score.
Output must be a structured JSON.
"""