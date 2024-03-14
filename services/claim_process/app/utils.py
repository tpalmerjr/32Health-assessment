import heapq
from app.models import ClaimInput, ClaimOutput
from db.models import Claim


def convert_claim_input_model_to_db_claim_model(claim: ClaimInput) -> Claim:
    """
    Converts the ClaimInput model to a DB Claim model.
    :param claim: ClaimInput
    :return: Claim
    """
    return Claim(**dict(claim.__dict__), net_fee=calculate_net_fee(claim))


def convert_db_claim_model_to_claim_output_model(claim: Claim) -> ClaimOutput:
    """
    Converts the DB Claim model to a ClaimOutput model.
    :param claim: Claim
    :return: ClaimOutput
    """
    return ClaimOutput(**dict(claim.__dict__))


def calculate_net_fee(claim_model: ClaimInput):
    """
    Calculates the net_fee for a claim.
    :param claim_model: ClaimInput
    :return: float
    """
    return (
            claim_model.provider_fees
            + claim_model.member_coinsurance
            + claim_model.member_copay
            - claim_model.allowed_fees
    )


def compute_top_10_provider_npis(claims_data):
    provider_net_fees = {}  # HashMap to store provider_npi as keys and net fees as values

    # Calculate net fee for each claim and update the hashmap
    for claim in claims_data:
        provider_npi = claim[0]
        net_fee = claim[1] + claim[2] + claim[3] - claim[4]
        provider_net_fees[provider_npi] = provider_net_fees.get(provider_npi, 0) + net_fee

    # Create a priority queue to maintain the top 10 provider_npis based on net fees
    top_provider_npis_heap = []

    # Iterate through the hashmap and push each provider_npi with its net fee into the priority queue
    for provider_npi, net_fee in provider_net_fees.items():
        heapq.heappush(top_provider_npis_heap, (net_fee, provider_npi))
        if len(top_provider_npis_heap) > 10:
            heapq.heappop(top_provider_npis_heap)  # Maintain only the top 10 elements in the queue

    # Extract the top 10 provider_npis from the priority queue
    top_10_provider_npis = [provider_npi for net_fee, provider_npi in sorted(top_provider_npis_heap, reverse=True)]

    return top_10_provider_npis
