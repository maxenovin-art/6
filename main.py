
from fastapi import FastAPI, HTTPException
import hashlib, datetime

app = FastAPI(title="User Management API")

# In-memory database (Vercel compatible)
users = {}

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/")
def root():
    return {"status": "ok", "message": "User Management API running"}

@app.post("/register")
def register(username: str, password: str):
    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[username] = {
        "password": hash_password(password),
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    return {"message": "User registered successfully"}

@app.post("/login")
def login(username: str, password: str):
    if username not in users:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if users[username]["password"] != hash_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}

@app.get("/users")
def list_users():
    return [
        {"username": u, "created_at": data["created_at"]}
        for u, data in users.items()
    ]
