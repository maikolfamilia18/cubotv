from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CuboTV API", version="1.0")

# ===============================
# MODELOS
# ===============================
class LoginRequest(BaseModel):
    username: str
    password: str

class Channel(BaseModel):
    id: int
    name: str
    category: str
    url: str

# ===============================
# BASE DE DATOS SIMULADA
# ===============================
channels_db = [
    {"id": 1, "name": "CuboTV Deportes", "category": "Sports", "url": "https://example.com/deportes.m3u8"},
    {"id": 2, "name": "CuboTV Noticias", "category": "News", "url": "https://example.com/noticias.m3u8"},
    {"id": 3, "name": "CuboTV Cine", "category": "Movies", "url": "https://example.com/cine.m3u8"},
]

# ===============================
# ENDPOINTS
# ===============================
@app.get("/")
def root():
    return {"message": "🚀 CuboTV API online", "version": "1.0"}

@app.get("/status")
def status():
    return {"status": "ok", "channels": len(channels_db)}

@app.get("/channels")
def get_channels():
    return channels_db

@app.get("/channel/{channel_id}")
def get_channel(channel_id: int):
    for ch in channels_db:
        if ch["id"] == channel_id:
            return ch
    raise HTTPException(status_code=404, detail="Channel not found")

@app.get("/playlist")
def get_playlist():
    m3u = "#EXTM3U\n"
    for ch in channels_db:
        m3u += f"#EXTINF:-1,{ch['name']}\n{ch['url']}\n"
    return {"playlist": m3u}

@app.post("/auth/login")
def login(data: LoginRequest):
    if data.username == "admin" and data.password == "1234":
        return {"success": True, "token": "fake-jwt-token-123"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
