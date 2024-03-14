from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as claim_process_router
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from db.database import engine, SQLModel

from utils.claim_process import limiter, app

# Execute DB Model Schema
SQLModel.metadata.create_all(engine)

# Adding limiter and exception handler to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
]

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Included Routes
app.include_router(claim_process_router, prefix="", tags=["Claims Process"])
