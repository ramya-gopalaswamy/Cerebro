"""Auth0 authentication service."""
from typing import Optional, Dict
from app.config import settings


class AuthService:
    """Handles Auth0 authentication and token verification."""
    
    def __init__(self):
        """Initialize Auth0 service."""
        self.domain = settings.auth0_domain
        self.client_id = settings.auth0_client_id
        self.client_secret = settings.auth0_client_secret
        self.audience = settings.auth0_audience
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify Auth0 JWT token.
        
        Args:
            token: JWT token string.
            
        Returns:
            Decoded token payload, or None if invalid.
            
        TODO: Implement actual Auth0 token verification using jose library.
        """
        if not self.domain:
            # In development, return mock user
            return {"sub": "demo_user", "email": "demo@example.com"}
        
        # TODO: Implement JWT verification
        # from jose import jwt, JWTError
        # try:
        #     jwks = self._get_jwks()
        #     payload = jwt.decode(token, jwks, algorithms=["RS256"], audience=self.audience)
        #     return payload
        # except JWTError:
        #     return None
        
        return None
    
    def get_user_id(self, token_payload: Dict) -> Optional[str]:
        """Extract user ID from token payload.
        
        Args:
            token_payload: Decoded JWT payload.
            
        Returns:
            User ID (sub claim) or None.
        """
        return token_payload.get("sub")
    
    def _get_jwks(self):
        """Fetch Auth0 JWKS (JSON Web Key Set).
        
        TODO: Implement JWKS fetching from Auth0.
        """
        # TODO: Fetch from https://{domain}/.well-known/jwks.json
        pass


# Global auth service instance
auth_service = AuthService()
