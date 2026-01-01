
from fastapi import FastAPI, HTTPException
import sqlite3, hashlib, datetime

app = FastAPI()
DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        created_at TEXT
    )""")
    conn.commit()
    conn.close()

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/register")
def register(username: str, password: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                  (username, hash_password(password), datetime.datetime.utcnow().isoformat()))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()
    return {"message": "User registered"}

@app.post("/login")
def login(username: str, password: str):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row or row[0] != hash_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.get("/users")
def list_users():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, username, created_at FROM users")
    users = c.fetchall()
    conn.close()
    return users
