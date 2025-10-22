from fastapi import FastAPI

from backend.routers.auth import auth

app = FastAPI()
app.include_router(auth)
