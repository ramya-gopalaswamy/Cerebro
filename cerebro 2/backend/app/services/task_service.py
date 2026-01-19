"""Task generation service that combines job listings and LeetCode problems."""
import uuid
from datetime import datetime
from typing import List, Dict
from app.models.user import Task, DailyTarget
from app.services.job_service import job_service
from app.services.leetcode_service import leetcode_service


class TaskService:
    """Handles task generation and management."""
    
    def __init__(self):
        """Initialize task service."""
        self.job_service = job_service
        self.leetcode_service = leetcode_service
    
    def generate_tasks(self, daily_target: DailyTarget, keywords: str = "frontend developer") -> List[Task]:
        """Generate tasks for a day based on daily targets.
        
        Args:
            daily_target: Daily target configuration (apps, leetcode)
            keywords: Job search keywords (default: "frontend developer")
            
        Returns:
            List of Task objects (jobs + LeetCode problems).
        """
        tasks = []
        
        # Generate job application tasks
        if daily_target.apps > 0:
            job_tasks = self._generate_job_tasks(daily_target.apps, keywords)
            tasks.extend(job_tasks)
        
        # Generate LeetCode problem tasks
        if daily_target.leetcode > 0:
            leetcode_tasks = self._generate_leetcode_tasks(daily_target.leetcode)
            tasks.extend(leetcode_tasks)
        
        return tasks
    
    def _generate_job_tasks(self, count: int, keywords: str) -> List[Task]:
        """Generate job application tasks.
        
        Args:
            count: Number of job tasks to generate
            keywords: Job search keywords
            
        Returns:
            List of Task objects for jobs.
        """
        jobs = self.job_service.search_jobs(keywords=keywords, results_per_page=count)
        
        tasks = []
        for job in jobs:
            task = Task(
                id=f"job_{job['id']}_{uuid.uuid4().hex[:8]}",
                type="job",
                title=f"{job['title']} at {job['company']}",
                url=job.get("url", ""),
                description=job.get("description", ""),
                created_at=datetime.utcnow(),
                completed=False,
            )
            tasks.append(task)
        
        return tasks
    
    def _generate_leetcode_tasks(self, count: int) -> List[Task]:
        """Generate LeetCode problem tasks.
        
        Args:
            count: Number of LeetCode tasks to generate
            
        Returns:
            List of Task objects for LeetCode problems.
        """
        tasks = []
        
        # Start with Easy problems, then Medium, then Hard
        difficulties = ["Easy"] * (count // 2 + 1) + ["Medium"] * (count // 2) + ["Hard"]
        difficulties = difficulties[:count]
        
        for difficulty in difficulties:
            problem = self.leetcode_service.get_problem(difficulty=difficulty)
            
            task = Task(
                id=f"leetcode_{problem['id']}_{uuid.uuid4().hex[:8]}",
                type="leetcode",
                title=f"{problem['title']} ({problem['difficulty']})",
                url=problem.get("url", ""),
                description=problem.get("description", ""),
                created_at=datetime.utcnow(),
                completed=False,
            )
            tasks.append(task)
        
        return tasks
    
    def convert_tasks_to_dict(self, tasks: List[Task]) -> List[Dict]:
        """Convert Task objects to dictionaries for JSON storage.
        
        Args:
            tasks: List of Task objects
            
        Returns:
            List of task dictionaries with datetime converted to ISO strings.
        """
        task_dicts = []
        for task in tasks:
            task_dict = task.model_dump()  # Use model_dump() for Pydantic v2
            # Convert datetime to ISO string for JSON serialization
            if "created_at" in task_dict and task_dict["created_at"]:
                if hasattr(task_dict["created_at"], "isoformat"):
                    task_dict["created_at"] = task_dict["created_at"].isoformat()
            if "completed_at" in task_dict and task_dict["completed_at"]:
                if hasattr(task_dict["completed_at"], "isoformat"):
                    task_dict["completed_at"] = task_dict["completed_at"].isoformat()
            task_dicts.append(task_dict)
        return task_dicts
    
    def convert_tasks_from_dict(self, task_dicts: List[Dict]) -> List[Task]:
        """Convert task dictionaries to Task objects.
        
        Args:
            task_dicts: List of task dictionaries
            
        Returns:
            List of Task objects.
        """
        tasks = []
        for task_dict in task_dicts:
            # Convert datetime strings back to datetime objects
            if "created_at" in task_dict and isinstance(task_dict["created_at"], str):
                task_dict["created_at"] = datetime.fromisoformat(task_dict["created_at"].replace("Z", "+00:00"))
            if "completed_at" in task_dict and isinstance(task_dict["completed_at"], str):
                task_dict["completed_at"] = datetime.fromisoformat(task_dict["completed_at"].replace("Z", "+00:00"))
            
            tasks.append(Task(**task_dict))
        
        return tasks


# Global task service instance
task_service = TaskService()
