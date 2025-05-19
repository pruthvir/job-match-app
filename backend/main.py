from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

API_KEY = os.getenv("API_KEY", "supersecurekey")
API_KEY_NAME = "x-api-key"

def verify_api_key(request: Request):
    client_key = request.headers.get(API_KEY_NAME)
    if client_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")

@app.get("/ping")
def ping():
    return {"status": "alive"}

@app.post("/upload-resume/")
@limiter.limit("5/minute")
async def upload_resume(request: Request, _: None = Depends(verify_api_key)):
    return {"message": "Resume uploaded securely."}

@app.post("/set-preferences/")
@limiter.limit("5/minute")
async def upload_resume(request: Request, _: None = Depends(verify_api_key)):
    return {"message": "Resume uploaded securely."}

@app.get("/jobs/")
@limiter.limit("10/minute")
async def get_jobs(request: Request, _: None = Depends(verify_api_key)):
    return {"matched_jobs": [], "other_sources": []}
