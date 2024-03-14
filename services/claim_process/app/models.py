from typing import Optional
from pydantic import BaseModel, field_validator


class ClaimBase(BaseModel):
    """
    Base Claim Model.
    """
    submitted_procedure: str
    provider_npi: str
    provider_fees: float
    member_coinsurance: float
    member_copay: float
    allowed_fees: float
    quadrant: str
    subscriber_num: str
    plan_group: str
    service_date: str


class ClaimOutput(ClaimBase):
    """
    ClaimOutput model used for returning a claim representation as a response to the api request.
    Extends: ClaimBase
    """
    id: int
    net_fee: float


class ClaimInput(ClaimBase):
    """
    ClaimInput model used for the api request value.
    Extends: ClaimBase
    """

    @field_validator("submitted_procedure")
    def validate_submitted_procedure(cls, v):
        """
        Class Field Validator for submitted_procedure. Validates that the value starts with a 'D'.
        """
        if not v.startswith("D"):
            raise ValueError("Submitted procedure must start with 'D'")
        return v

    @field_validator("provider_npi")
    def validate_provider_npi(cls, v):
        """
        Class Field Validator for provider_npi. Validates that the value is digits
        and contains at least 10 digits.
        """
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Provider NPI must be a 10-digit number")
        return v
