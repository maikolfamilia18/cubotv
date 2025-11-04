from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

IPTV_BASE_URL = os.getenv("IPTV_BASE_URL", "http://taiwan95133.cdn-ak.me/xmltv.php")

@app.get("/")
def home():
    return {"message": "CuboTV backend funcionando correctamente 🚀"}

@app.post("/login")
async def login(username: str, password: str):
    """
    Endpoint para autenticar usuarios y obtener contenido IPTV.
    """
    url = f"{IPTV_BASE_URL}?username={username}&password={password}"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al conectar con el servidor IPTV")
        return JSONResponse(content={"status": "ok", "epg_url": url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
