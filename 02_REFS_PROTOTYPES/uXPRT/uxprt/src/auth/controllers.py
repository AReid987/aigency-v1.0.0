import os
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client # Corrected import
from gotrue.errors import AuthApiError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") # This should be the service_role key for admin actions if needed, or anon key for client-side actions.
                                          # For auth, anon key is usually sufficient for client-driven flows.
                                          # However, if we need to, for example, directly create users without email confirmation (not recommended for standard signup)
                                          # or perform other admin actions, service_role key might be used carefully.
                                          # For sign_up and sign_in_with_password, anon key is appropriate.

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables.")

# Removed async get_supabase_client as v2 client is sync and dependency injection needs review
# async def get_supabase_client() -> Client:
#     """
#     Dependency to get a Supabase client.
#     In a real application, you might want to manage the client lifecycle differently,
#     e.g., as a global instance or using a proper dependency injection system.
#     For simplicity, we create a new client per request that needs it.
#     """
#     # supabase-py client creation is synchronous
#     supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
#     return supabase
# Note: A synchronous dependency or global client instance should be used instead.
# For now, functions will expect the client to be passed or created internally.

# Function to create a client synchronously (can be used directly or in a sync dependency)
def create_sync_supabase_client() -> Client:
     """Creates a synchronous Supabase client."""
     return create_client(SUPABASE_URL, SUPABASE_KEY)

# Scheme for bearer token authentication
oauth2_scheme = HTTPBearer()

# Note: get_current_user dependency needs adjustment for sync client creation/injection
# async def get_current_user(
#     token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
#     supabase: Client = Depends(get_supabase_client) # This dependency needs to be sync
# ):
# Made sync. Assumes client is created within or passed via a sync dependency.
def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
):
    """
    FastAPI dependency to get the current user from a JWT token.
    Validates the token using Supabase. Creates its own client.
    """
    supabase = create_sync_supabase_client() # Create client internally

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        # Use synchronous client methods
        user_response = supabase.auth.get_user(token.credentials) # Sync call
        if user_response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_response.user
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {e.message}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception: # Catch any other unexpected errors during token validation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# register_user remains synchronous
def register_user(email: str, password: str, username: str = None): # Removed supabase arg, will create client internally
    """Registers a new user with Supabase."""
    supabase = create_sync_supabase_client() # Create client internally
    try:
        # username can be stored in user_metadata if needed
        options = {}
        if username:
            # Ensure 'data' key exists in options for user_metadata
            options["data"] = {"username": username}

        # Correct sign_up call for supabase-py v2+
        # Pass credentials and options directly as a dictionary
        credentials = {"email": email, "password": password}
        if options:
             credentials["options"] = options

        response = supabase.auth.sign_up(credentials)

        # Check response structure based on supabase-py v2+
        if response.user:
            # You might want to create a corresponding entry in a public 'profiles' table here
            # using response.user.id if your schema requires it.
            # For now, just confirming Supabase auth user creation.
            return {"message": "User registered successfully. Please check your email to confirm.", "user_id": response.user.id, "email": response.user.email}
        else:
             # This case might indicate an issue if sign_up returns without user or error
             # For v2+, errors are raised, so this might not be reachable unless API changes
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User registration failed for an unknown reason (No user data returned).")
    except AuthApiError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        # Log the full error for debugging
        print(f"Unexpected error during registration: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")

# login_user remains synchronous
def login_user(email: str, password: str): # Removed supabase arg
    """Logs in a user with Supabase."""
    supabase = create_sync_supabase_client() # Create client internally
    try:
        # Use synchronous client methods
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.session and response.session.access_token:
            return {"access_token": response.session.access_token, "token_type": "bearer", "user_id": response.user.id}
        else:
             # This might occur if the response structure is unexpected without an error being raised
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password or unexpected login response")
    except AuthApiError as e:
        # Check for specific invalid login credentials error message if available
        if "Invalid login credentials" in e.message:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        else:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
    except Exception as e:
        print(f"Unexpected error during login: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")

# logout_user remains synchronous
def logout_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme) # Keep Depends for token extraction
):
    """Logs out a user by invalidating the session token with Supabase."""
    supabase = create_sync_supabase_client() # Create client internally
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        # Set the JWT for the client instance before calling sign_out
        # This is crucial because sign_out operates on the current session of the client instance.
        supabase.auth.set_session(access_token=token.credentials, refresh_token="dummy") # Dummy refresh token needed for set_session

        # Use synchronous client methods
        supabase.auth.sign_out() # sign_out in v2 returns None on success or raises error

        # If sign_out didn't raise an exception, it succeeded.
        return {"message": "User logged out successfully"}

    except AuthApiError as e: # Catch specific Supabase auth errors
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Logout failed: {e.message}")
    except HTTPException as e: # Re-raise HTTPExceptions if they were raised by token dependency
        raise e
    except Exception as e: # Catch any other unexpected errors during logout
        print(f"Unexpected error during logout: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred during logout: {str(e)}")