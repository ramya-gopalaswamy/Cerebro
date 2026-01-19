"""Job search service for fetching job listings."""
import requests
from typing import List, Dict, Optional
from app.config import settings


class JobService:
    """Handles job search API integration."""
    
    def __init__(self):
        """Initialize job service."""
        self.api_key = settings.job_api_key
        self.base_url = "https://api.adzuna.com/v1/api/jobs"  # Adzuna API (free tier available)
        # Alternative APIs: Indeed, LinkedIn Jobs, GitHub Jobs
    
    def search_jobs(
        self,
        keywords: str = "frontend developer",
        location: str = "us",
        results_per_page: int = 3,
        country: str = "us"
    ) -> List[Dict]:
        """Search for jobs using Adzuna API.
        
        Args:
            keywords: Search keywords (e.g., "frontend developer", "software engineer")
            location: Location code (e.g., "us", "gb")
            results_per_page: Number of results to return (default: 3)
            country: Country code (default: "us")
            
        Returns:
            List of job dictionaries with title, url, company, description.
            
        TODO: Implement API call when API key is available.
        For now, returns mock data for development.
        """
        if not self.api_key:
            # Return mock data for development
            return self._get_mock_jobs(keywords, results_per_page)
        
        try:
            # Adzuna API endpoint
            url = f"{self.base_url}/{country}/search/{results_per_page}"
            params = {
                "app_id": self.api_key.split(":")[0] if ":" in self.api_key else self.api_key,
                "app_key": self.api_key.split(":")[1] if ":" in self.api_key else self.api_key,
                "what": keywords,
                "where": location,
                "results_per_page": results_per_page,
                "content-type": "application/json",
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            jobs = []
            for result in data.get("results", [])[:results_per_page]:
                jobs.append({
                    "id": result.get("id", ""),
                    "title": result.get("title", ""),
                    "company": result.get("company", {}).get("display_name", "Unknown Company"),
                    "url": result.get("redirect_url", ""),
                    "description": result.get("description", ""),
                    "location": result.get("location", {}).get("display_name", ""),
                    "created": result.get("created", ""),
                })
            
            return jobs
            
        except Exception as e:
            # Fallback to mock data on error
            print(f"Job API error: {e}")
            return self._get_mock_jobs(keywords, results_per_page)
    
    def _get_mock_jobs(self, keywords: str, count: int) -> List[Dict]:
        """Generate mock job data for development.
        
        Args:
            keywords: Search keywords
            count: Number of jobs to generate
            
        Returns:
            List of mock job dictionaries.
        """
        mock_jobs = [
            {
                "id": "job_1",
                "title": "Frontend Developer",
                "company": "Tech Startup Inc.",
                "url": "https://example.com/jobs/frontend-dev",
                "description": "Seeking a talented Frontend Developer to join our team.",
                "location": "San Francisco, CA",
                "created": "2024-01-10",
            },
            {
                "id": "job_2",
                "title": "React Developer",
                "company": "Innovation Labs",
                "url": "https://example.com/jobs/react-dev",
                "description": "Looking for an experienced React Developer with TypeScript skills.",
                "location": "Remote",
                "created": "2024-01-09",
            },
            {
                "id": "job_3",
                "title": "Senior Frontend Engineer",
                "company": "Cloud Systems",
                "url": "https://example.com/jobs/senior-frontend",
                "description": "Senior Frontend Engineer position with competitive benefits.",
                "location": "New York, NY",
                "created": "2024-01-08",
            },
            {
                "id": "job_4",
                "title": "Full Stack Developer",
                "company": "Digital Solutions",
                "url": "https://example.com/jobs/fullstack",
                "description": "Full Stack Developer role with modern tech stack.",
                "location": "Austin, TX",
                "created": "2024-01-07",
            },
            {
                "id": "job_5",
                "title": "JavaScript Engineer",
                "company": "Web Innovations",
                "url": "https://example.com/jobs/js-engineer",
                "description": "JavaScript Engineer needed for exciting projects.",
                "location": "Seattle, WA",
                "created": "2024-01-06",
            },
        ]
        
        # Return requested number, cycling through mock data
        return mock_jobs[:count]


# Global job service instance
job_service = JobService()
