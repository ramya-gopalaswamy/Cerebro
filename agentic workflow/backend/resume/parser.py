"""
Resume Parser
Uses Claude to extract structured data from resume text
"""
import json
import re
import sys
sys.path.append('..')

from llm_factory import get_agent_llm
from resume.schemas import ParsedResume, RESUME_JSON_SCHEMA


RESUME_EXTRACTION_PROMPT = """You are an expert resume parser. Extract information from this resume into JSON.

Resume:
{resume_text}

Return a JSON object with this exact structure (fill in values from resume):
{{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "phone number or null",
  "location": "City, State or null",
  "linkedin": "LinkedIn URL or null",
  "github": "GitHub URL or null",
  "years_experience": 2,
  "current_title": "Job Title",
  "summary": "Brief professional summary",
  "skills": [
    {{"name": "Python", "category": "language", "proficiency": "expert"}},
    {{"name": "React", "category": "framework", "proficiency": "proficient"}}
  ],
  "experience": [
    {{
      "company": "Company Name",
      "title": "Job Title",
      "start_date": "Jan 2022",
      "end_date": "Present",
      "achievements": ["Achievement 1", "Achievement 2"],
      "technologies": ["Tech1", "Tech2"]
    }}
  ],
  "education": [
    {{
      "degree": "Bachelor's",
      "field": "Computer Science",
      "institution": "University Name",
      "year": "2020",
      "coursework": []
    }}
  ],
  "projects": [],
  "certifications": [],
  "inferred": {{
    "strengths": ["Strength 1", "Strength 2", "Strength 3"],
    "weaknesses": ["Area to improve 1"],
    "ideal_job_types": ["Software Engineer", "Backend Developer"],
    "skills_to_develop": ["Skill to learn 1"],
    "experience_level": "mid",
    "career_trajectory": "Brief career path description",
    "interview_focus_areas": ["Topic 1", "Topic 2"]
  }}
}}

IMPORTANT: Return ONLY the JSON object, no other text. Start with {{ and end with }}."""


def extract_json_from_text(text: str) -> dict:
    """
    Extract JSON from text, handling various formats.
    """
    # Remove markdown code blocks if present
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        parts = text.split("```")
        if len(parts) >= 2:
            text = parts[1]
    
    # Find JSON object in text
    text = text.strip()
    
    # Try to find JSON object boundaries
    start_idx = text.find('{')
    if start_idx == -1:
        raise ValueError("No JSON object found in response")
    
    # Find matching closing brace
    brace_count = 0
    end_idx = start_idx
    for i, char in enumerate(text[start_idx:], start_idx):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    json_str = text[start_idx:end_idx]
    
    # Try to parse
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Try to fix common issues
        # Remove trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        return json.loads(json_str)


def create_default_resume(resume_text: str, error_msg: str = "") -> dict:
    """
    Create a default resume structure when parsing fails.
    """
    # Try to extract name from first line
    lines = resume_text.strip().split('\n')
    name = lines[0].strip() if lines else "Unknown"
    
    # Try to find email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
    email = email_match.group(0) if email_match else None
    
    return {
        "name": name,
        "email": email,
        "phone": None,
        "location": None,
        "linkedin": None,
        "github": None,
        "years_experience": 2,
        "current_title": "Software Engineer",
        "summary": f"Resume parsed with limited extraction. {error_msg}",
        "skills": [
            {"name": "Programming", "category": "language", "proficiency": "proficient"}
        ],
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": [],
        "inferred": {
            "strengths": ["Technical skills", "Problem solving"],
            "weaknesses": ["Resume needs more detail"],
            "ideal_job_types": ["Software Engineer"],
            "skills_to_develop": ["Interview preparation"],
            "experience_level": "mid",
            "career_trajectory": "Software development career",
            "interview_focus_areas": ["Technical skills", "Problem solving"]
        },
        "raw_text": resume_text
    }


async def parse_resume_with_llm(resume_text: str) -> ParsedResume:
    """
    Parse resume text using Claude to extract structured data.
    
    Args:
        resume_text: Raw text extracted from PDF
        
    Returns:
        ParsedResume with all extracted and inferred data
    """
    llm = get_agent_llm("resume_parser")
    
    # Truncate if too long (avoid token limits)
    max_chars = 8000
    if len(resume_text) > max_chars:
        resume_text = resume_text[:max_chars] + "\n[Resume truncated...]"
    
    prompt = RESUME_EXTRACTION_PROMPT.format(resume_text=resume_text)
    
    try:
        response = await llm.ainvoke(prompt)
        content = response.content
        
        # Try to extract and parse JSON
        try:
            parsed_data = extract_json_from_text(content)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON extraction failed: {e}")
            print(f"Response was: {content[:500]}...")
            # Return default structure
            parsed_data = create_default_resume(resume_text, str(e))
        
    except Exception as e:
        print(f"LLM call failed: {e}")
        parsed_data = create_default_resume(resume_text, str(e))
    
    # Ensure required fields exist
    parsed_data.setdefault("name", "Unknown")
    parsed_data.setdefault("skills", [])
    parsed_data.setdefault("experience", [])
    parsed_data.setdefault("inferred", {
        "strengths": ["Technical skills"],
        "weaknesses": [],
        "ideal_job_types": ["Software Engineer"],
        "skills_to_develop": [],
        "experience_level": "mid",
        "career_trajectory": "",
        "interview_focus_areas": []
    })
    
    # Add raw text
    parsed_data["raw_text"] = resume_text
    
    return parsed_data


def parse_resume_sync(resume_text: str) -> ParsedResume:
    """
    Synchronous version of resume parsing.
    
    Args:
        resume_text: Raw text extracted from PDF
        
    Returns:
        ParsedResume with all extracted and inferred data
    """
    import asyncio
    return asyncio.run(parse_resume_with_llm(resume_text))


# Convenience function for full pipeline
async def process_resume_pdf(pdf_bytes: bytes) -> ParsedResume:
    """
    Full pipeline: PDF bytes -> extracted text -> parsed resume.
    
    Args:
        pdf_bytes: Raw PDF file bytes
        
    Returns:
        Fully parsed and analyzed resume
    """
    from resume.extractor import extract_pdf_from_bytes, clean_extracted_text
    
    # Extract text
    raw_text = extract_pdf_from_bytes(pdf_bytes)
    cleaned_text = clean_extracted_text(raw_text)
    
    # Parse with LLM
    parsed = await parse_resume_with_llm(cleaned_text)
    
    return parsed
