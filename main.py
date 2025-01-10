import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client

from models import User, Login

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Retrieve Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and Key must be set in the .env file")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Register user route
@app.post("/register/")
async def register_user(user: User):
    """
    Registers a new user to Supabase using the authentication system.
    """
    try:
        # Create user in Supabase Authentication
        auth_response = supabase.auth.sign_up(
            {
                "email": user.email,
                "password": user.password
            }
        )

        if 'error' in auth_response:
            raise HTTPException(status_code=400, detail=auth_response['error']['message'])

        # Add additional user details to the database
        user_data = {"email": user.email, "name": user.name}
        data_response = supabase.table("users").insert(user_data).execute()

        if data_response.get('status_code') != 201:
            raise HTTPException(status_code=400, detail="Error saving user details")

        return {"message": "User registered successfully", "user_id": auth_response['user']['id']}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Login route
@app.post("/login/")
async def login_user(login: Login):
    """
    Logs in a user using Supabase authentication.

    Parameters:
    - login (Login): A Login object containing the user's email and password.

    Returns:
    - dict: A dictionary containing the user's information, including their ID, email, and access token.

    Raises:
    - HTTPException: If the login credentials are invalid or if there is an error during the login process.
    """


try:
    # Authenticate user with Supabase
    auth_response = supabase.auth.sign_in_with_password(
        {
            "email": login.email,
            "password": login.password
        }
    )

    if auth_response.user is None:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    user = auth_response.user
    session = auth_response.session

    return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email,
        "access_token": session.access_token
    }

except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


# Protected route
@app.get("/protected/")
async def protected_route(user: dict = Depends(verify_token)):


    """


    This is a
    protected
    route
    that
    only
    logged - in users
    can
    access.
    It
    returns
    the
    user
    's information.
    """
return {"message": "Access granted", "user": user}
