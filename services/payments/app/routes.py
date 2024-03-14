from fastapi import APIRouter, HTTPException
from typing import List


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello from payments"}
