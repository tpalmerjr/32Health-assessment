from fastapi import APIRouter, Request
from app.models import ClaimInput, ClaimOutput
from app.services import add_claim, get_top_providers
from utils.claim_process import limiter

router = APIRouter()


# Create a new claim
@router.post("/", response_model=ClaimOutput)
async def process_claim(claim: ClaimInput):
    # TODO: Add any necessary HTTPExceptions
    return add_claim(claim)


@router.get("/top-providers")
@limiter.limit("10/minute")
async def retrieve_top_providers(request: Request):
    # TODO: Add any necessary HTTPExceptions
    return get_top_providers()
