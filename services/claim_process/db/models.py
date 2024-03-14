from typing import Optional
from sqlmodel import SQLModel, Field


class Claim(SQLModel, table=True):
    """
    Claim model used for creation of the DB table as well as representation of DB Claim instances.
    """
    __tablename__ = "claims"

    id: int = Field(default=None, primary_key=True)
    submitted_procedure: str
    provider_npi: str
    provider_fees: float
    member_coinsurance: float
    member_copay: float
    allowed_fees: float
    quadrant: Optional[str]
    subscriber_num: str
    plan_group: str
    net_fee: float
    service_date: str
