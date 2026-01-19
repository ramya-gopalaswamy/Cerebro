from fastapi import APIRouter
from app.services.job_service import JobService
from app.services.leetcode_service import LeetCodeService

router = APIRouter()

job_service = JobService()
leetcode_service = LeetCodeService()

@router.get("/dashboard")
async def get_dashboard():
    """Return dynamic dashboard data for frontend."""
    jobs = job_service.search_jobs(keywords="frontend developer", results_per_page=3)
    leetcode_problem = leetcode_service.get_problem()
    return {
        "jars": [
            {"color": "yellow", "count": 5},
            {"color": "blue", "count": 3},
            {"color": "purple", "count": 2},
            {"color": "red", "count": 1}
        ],
        "logicAgent": {
            "challenge": leetcode_problem.get("title", "Unknown"),
            "url": leetcode_problem.get("url", "https://leetcode.com/problemset/all/"),
            "difficulty": leetcode_problem.get("difficulty", "Medium")
        },
        "jobScout": {
            "sources": [job.get("title", "Unknown") for job in jobs],
            "jobs": jobs
        },
        "orbHistory": [
            {"date": "2026-01-10", "orbs": 2},
            {"date": "2026-01-11", "orbs": 3}
        ]
    }
