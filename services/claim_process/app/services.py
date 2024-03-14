from sqlmodel import select

from app.models import ClaimInput, ClaimOutput
from db.utils import start_session
from db.models import Claim
from app.utils import (
    convert_claim_input_model_to_db_claim_model,
    convert_db_claim_model_to_claim_output_model,
    compute_top_10_provider_npis
)


def add_claim(claim_model: ClaimInput) -> ClaimOutput:
    """
    Adds a Claim to the database and returns a ClaimOutput
    :param claim_model: ClaimInput
    :return: ClaimOutput
    """
    with start_session() as session:
        # Converting provided ClaimInput to Claim DB Model
        claim = convert_claim_input_model_to_db_claim_model(claim_model)
        # Inserting Claim into DB
        session.add(claim)
        # Committing DB Transaction
        session.commit()
        # Refreshing claim to return the newly added claim with the id
        session.refresh(claim)

        # Returning converted Claim DB Model as ClaimOutput
        return convert_db_claim_model_to_claim_output_model(claim)


# def get_top_providers():
def get_top_providers() -> [str]:
    with start_session() as session:
        """
        Adds a Claim to the database and returns a ClaimOutput
        :param
        :return: [str]
        """

        # If the net_fee is not stored when creating the claim and must be calculated the query will obtain all
        # necessary values. If the net_fee is stored in the database then it is possible to only obtain the provider_npi
        # and net_fee. This example shows obtaining all necessary values from the database even thought the net_fee
        # is stored.
        claims_data = (
            session.execute(select(Claim.provider_npi, Claim.provider_fees,
                                   Claim.member_coinsurance, Claim.member_copay, Claim.allowed_fees))
            .all()
        )

        # Get the top 10 provider NPI list
        top_provider_npis = compute_top_10_provider_npis(claims_data)

        return top_provider_npis
