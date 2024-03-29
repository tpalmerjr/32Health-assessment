from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as payments_router

app = FastAPI()

# CORS
origins = [
    "http://localhost",
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
app.include_router(payments_router, prefix="", tags=["Payments"])
