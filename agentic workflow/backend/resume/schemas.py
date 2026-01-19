"""
Resume Data Schemas
Defines the structure for parsed resume data
"""
from typing import TypedDict, List, Optional, Literal


class Skill(TypedDict):
    """Individual skill with metadata"""
    name: str
    category: Literal["language", "framework", "tool", "database", "cloud", "soft", "other"]
    proficiency: Optional[Literal["expert", "proficient", "familiar"]]


class Experience(TypedDict):
    """Work experience entry"""
    company: str
    title: str
    start_date: str
    end_date: Optional[str]  # None if current
    duration_months: Optional[int]
    achievements: List[str]
    technologies: List[str]


class Education(TypedDict):
    """Education entry"""
    degree: str
    field: str
    institution: str
    year: str
    gpa: Optional[str]
    coursework: List[str]


class Project(TypedDict):
    """Project entry"""
    name: str
    description: str
    technologies: List[str]
    url: Optional[str]
    impact: Optional[str]


class InferredAnalysis(TypedDict):
    """AI-inferred analysis of the candidate"""
    strengths: List[str]
    weaknesses: List[str]
    ideal_job_types: List[str]
    skills_to_develop: List[str]
    experience_level: Literal["junior", "mid", "senior", "lead"]
    career_trajectory: str
    interview_focus_areas: List[str]


class ParsedResume(TypedDict):
    """Complete parsed resume structure"""
    # Basic Info
    name: str
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    portfolio: Optional[str]
    
    # Professional Summary
    years_experience: int
    current_title: str
    summary: str
    
    # Detailed Sections
    skills: List[Skill]
    experience: List[Experience]
    education: List[Education]
    projects: List[Project]
    certifications: List[str]
    
    # AI-Inferred Analysis
    inferred: InferredAnalysis
    
    # Raw text for reference
    raw_text: str


# JSON Schema for structured output from Claude
RESUME_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "phone": {"type": "string"},
        "location": {"type": "string"},
        "linkedin": {"type": "string"},
        "github": {"type": "string"},
        "portfolio": {"type": "string"},
        "years_experience": {"type": "integer"},
        "current_title": {"type": "string"},
        "summary": {"type": "string"},
        "skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "category": {"type": "string"},
                    "proficiency": {"type": "string"}
                },
                "required": ["name", "category"]
            }
        },
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "company": {"type": "string"},
                    "title": {"type": "string"},
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"},
                    "achievements": {"type": "array", "items": {"type": "string"}},
                    "technologies": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["company", "title"]
            }
        },
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "degree": {"type": "string"},
                    "field": {"type": "string"},
                    "institution": {"type": "string"},
                    "year": {"type": "string"},
                    "coursework": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["degree", "institution"]
            }
        },
        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "technologies": {"type": "array", "items": {"type": "string"}},
                    "impact": {"type": "string"}
                },
                "required": ["name", "description"]
            }
        },
        "certifications": {"type": "array", "items": {"type": "string"}},
        "inferred": {
            "type": "object",
            "properties": {
                "strengths": {"type": "array", "items": {"type": "string"}},
                "weaknesses": {"type": "array", "items": {"type": "string"}},
                "ideal_job_types": {"type": "array", "items": {"type": "string"}},
                "skills_to_develop": {"type": "array", "items": {"type": "string"}},
                "experience_level": {"type": "string"},
                "career_trajectory": {"type": "string"},
                "interview_focus_areas": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["strengths", "weaknesses", "experience_level"]
        }
    },
    "required": ["name", "skills", "experience", "inferred"]
}
