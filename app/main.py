from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.routes import message_log, summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_log.router)
app.include_router(summary.router)

@app.get("/")
def read_root():
    return "Welcome to Couch Potato's Workspace 😁\n The integration is at this endpoint 👉🏼 baseurl/integration"

@app.get("/icon")
def get_icon():
    return FileResponse("homework.png", media_type="image/png")

@app.get("/integration")
def get_integration_json():
    return FileResponse("integration.json")
