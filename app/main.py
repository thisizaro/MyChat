from fastapi import FastAPI
from .database import engine, Base
from . import models
from .api import auth, messages
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(messages.router)

@app.get("/")
def root():
    return {"message": "Backend running"}
