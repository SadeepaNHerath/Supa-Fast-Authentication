import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# OAuth2PasswordBearer is used for extracting the access token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")


# Verify access token with Supabase
async def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verify the access token using Sublease's client.

    Parameters:
    - token (str): The access token to verify.

    Returns:
    - user (dict): The user information if the token is valid.

    Raises:
    - HTTPException: If the token is invalid or expired.
    """
    try:
        # Verify the token using Sublease's client
        user = supabase.auth.get_user(token)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying token: {str(e)}"
        )
