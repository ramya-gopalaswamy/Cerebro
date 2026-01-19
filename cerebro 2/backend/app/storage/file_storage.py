"""File-based storage system for user state using JSON files."""
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from app.config import settings


class FileStorage:
    """Handles reading and writing user state to JSON files."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize file storage with data directory.
        
        Args:
            data_dir: Directory to store user state files. Defaults to settings.data_dir.
        """
        # Resolve relative path from backend directory
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            # Default: go up from backend/app to cerebro root, then to data/user_states
            backend_dir = Path(__file__).parent.parent.parent
            self.data_dir = backend_dir.parent / "data" / "user_states"
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_user_file_path(self, user_id: str) -> Path:
        """Get file path for a user's state.
        
        Args:
            user_id: User identifier from Auth0.
            
        Returns:
            Path object for the user's JSON file.
        """
        # Sanitize user_id for filename (replace special chars)
        safe_user_id = user_id.replace("|", "_").replace("/", "_")
        return self.data_dir / f"{safe_user_id}.json"
    
    def get_user_state(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user state from JSON file.
        
        Args:
            user_id: User identifier from Auth0.
            
        Returns:
            User state dictionary, or None if not found.
        """
        file_path = self._get_user_file_path(user_id)
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Error reading user state for {user_id}: {e}")
    
    def save_user_state(self, user_id: str, state: Dict[str, Any]) -> None:
        """Save user state to JSON file.
        
        Args:
            user_id: User identifier from Auth0.
            state: User state dictionary to save.
        """
        file_path = self._get_user_file_path(user_id)
        
        try:
            # Write atomically by writing to temp file first
            temp_path = file_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            # Atomic rename
            temp_path.replace(file_path)
        except IOError as e:
            raise ValueError(f"Error saving user state for {user_id}: {e}")
    
    def user_exists(self, user_id: str) -> bool:
        """Check if user state file exists.
        
        Args:
            user_id: User identifier from Auth0.
            
        Returns:
            True if user state exists, False otherwise.
        """
        file_path = self._get_user_file_path(user_id)
        return file_path.exists()
    
    def delete_user_state(self, user_id: str) -> bool:
        """Delete user state file.
        
        Args:
            user_id: User identifier from Auth0.
            
        Returns:
            True if deleted, False if file didn't exist.
        """
        file_path = self._get_user_file_path(user_id)
        
        if file_path.exists():
            file_path.unlink()
            return True
        return False


# Global storage instance
storage = FileStorage()
