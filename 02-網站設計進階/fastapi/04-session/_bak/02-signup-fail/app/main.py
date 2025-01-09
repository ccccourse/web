from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import random
from fastapi import Request
from fastapi import Body

# User Database (for demonstration purposes)
users = {}

# In-memory session storage (for demonstration purposes)
sessions = {}

@app.post("/signup")
def sign_up(username: str = Body(...), password: str = Body(...)):
    user = users.get(username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    new_user_id = len(users) + 1
    new_user = {
        "username": username,
        "password": password,
        "user_id": new_user_id
    }
    users[username] = new_user
    return {"message": "User registered successfully"}

    # Login endpoint - Creates a new session
@router.post("/login")
def login(user: dict = Depends(authenticate_user)):
    session_id = create_session(user["user_id"])
    return {"message": "Logged in successfully", "session_id": session_id}

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

def create_session(user_id: int):
    session_id = len(sessions) + random.randint(0, 1000000)
    sessions[session_id] = user_id
    return session_id

# Get current user endpoint - Returns the user corresponding to the session ID
@router.get("/getusers/me")
def read_current_user(user: dict = Depends(get_user_from_session_id)):
    return user

# Protected endpoint - Requires authentication
@router.get("/protected")
def protected_endpoint(user: dict = Depends(get_authenticated_user_from_session_id)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    return {"message": "This user can connect to a protected endpoint after successfully autheticated", "user": user}

# Custom middleware for session-based authentication
def get_authenticated_user_from_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id is None or int(session_id) not in sessions:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )
    # Get the user from the session
    user = get_user_from_session(int(session_id))
    return user

# Use the valid session id to get the corresponding user from the users dictionary
def get_user_from_session(session_id: int):
    user = None
    for user_data in users.values():
        if user_data['user_id'] == sessions.get(session_id):
            user = user_data
            break

    return user

# Logout endpoint - Removes the session
@router.post("/logout")
def logout(session_id: int = Depends(get_session_id)):
    if session_id not in sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    sessions.pop(session_id)
    return {"message": "Logged out successfully", "session_id": session_id}

# Create a new dependency to get the session ID from cookies
def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id is None or int(session_id) not in sessions:
        raise HTTPException(status_code=401, detail="Invalid session ID")
    return int(session_id)
