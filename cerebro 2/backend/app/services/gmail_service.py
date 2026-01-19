"""Gmail service for verifying sent job applications."""
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.config import settings

# Try to import Gmail API libraries (optional)
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False


class GmailService:
    """Handles Gmail API integration for email verification."""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self):
        """Initialize Gmail service."""
        self.credentials_path = os.getenv("GMAIL_CREDENTIALS_PATH")
        self.token_path = os.getenv("GMAIL_TOKEN_PATH")
        self.service = None
        
        # Keywords to search for in sent emails
        self.application_keywords = [
            "application",
            "apply",
            "resume",
            "cover letter",
            "interested in position",
            "job application",
            "candidate",
        ]
    
    def _get_service(self):
        """Get Gmail API service instance.
        
        Returns:
            Gmail service instance or None if not configured.
        """
        if not GMAIL_AVAILABLE or not self.credentials_path:
            return None
        
        try:
            creds = None
            if self.token_path and os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Need to run OAuth flow
                    return None
            
            self.service = build('gmail', 'v1', credentials=creds)
            return self.service
        except Exception as e:
            print(f"Gmail API error: {e}")
            return None
    
    def count_sent_emails(
        self,
        timeframe_hours: int = 24,
        keywords: Optional[List[str]] = None
    ) -> int:
        """Count emails sent in the specified timeframe.
        
        Args:
            timeframe_hours: Hours to look back (default: 24)
            keywords: Keywords to search for (default: application_keywords)
            
        Returns:
            Count of matching sent emails.
            
        TODO: Implement actual Gmail API call when credentials are available.
        For now, returns mock count for development.
        """
        if keywords is None:
            keywords = self.application_keywords
        
        service = self._get_service()
        
        if not service:
            # Return mock count for development
            return self._get_mock_count(timeframe_hours)
        
        try:
            # Calculate time threshold
            time_threshold = datetime.utcnow() - timedelta(hours=timeframe_hours)
            timestamp = int(time_threshold.timestamp())
            
            # Build query
            keyword_query = " OR ".join([f'"{keyword}"' for keyword in keywords])
            query = f"in:sent after:{timestamp} ({keyword_query})"
            
            # Search for messages
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=100
            ).execute()
            
            messages = results.get('messages', [])
            return len(messages)
            
        except Exception as e:
            print(f"Gmail API error: {e}")
            return self._get_mock_count(timeframe_hours)
    
    def get_sent_emails(
        self,
        timeframe_hours: int = 24,
        keywords: Optional[List[str]] = None
    ) -> List[Dict]:
        """Get list of sent emails in the specified timeframe.
        
        Args:
            timeframe_hours: Hours to look back (default: 24)
            keywords: Keywords to search for
            
        Returns:
            List of email dictionaries with subject, to, date.
        """
        if keywords is None:
            keywords = self.application_keywords
        
        service = self._get_service()
        
        if not service:
            # Return mock emails for development
            return self._get_mock_emails(timeframe_hours)
        
        try:
            time_threshold = datetime.utcnow() - timedelta(hours=timeframe_hours)
            timestamp = int(time_threshold.timestamp())
            
            keyword_query = " OR ".join([f'"{keyword}"' for keyword in keywords])
            query = f"in:sent after:{timestamp} ({keyword_query})"
            
            results = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=100
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for msg in messages[:20]:  # Limit to 20 for performance
                message = service.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()
                
                headers = message['payload'].get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
                to = next((h['value'] for h in headers if h['name'] == 'To'), '')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                
                emails.append({
                    'id': msg['id'],
                    'subject': subject,
                    'to': to,
                    'date': date,
                })
            
            return emails
            
        except Exception as e:
            print(f"Gmail API error: {e}")
            return self._get_mock_emails(timeframe_hours)
    
    def _get_mock_count(self, timeframe_hours: int) -> int:
        """Get mock count for development.
        
        Args:
            timeframe_hours: Hours to look back
            
        Returns:
            Mock count (random between 0-5 for testing).
        """
        # For development: return a mock count
        # In production, this would be replaced with actual Gmail API calls
        import random
        return random.randint(0, 5)
    
    def _get_mock_emails(self, timeframe_hours: int) -> List[Dict]:
        """Get mock emails for development.
        
        Args:
            timeframe_hours: Hours to look back
            
        Returns:
            List of mock email dictionaries.
        """
        mock_emails = [
            {
                'id': 'mock_1',
                'subject': 'Application for Frontend Developer Position',
                'to': 'jobs@example.com',
                'date': datetime.utcnow().isoformat(),
            },
            {
                'id': 'mock_2',
                'subject': 'Resume - Software Engineer',
                'to': 'careers@startup.com',
                'date': (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            },
        ]
        count = self._get_mock_count(timeframe_hours)
        return mock_emails[:count]


# Global Gmail service instance
gmail_service = GmailService()
