import pytest
from fastapi.testclient import TestClient
from main import app
from app.utils import compute_top_10_provider_npis


client = TestClient(app)


# Test creating a claim
def test_process_claim_endpoint():
    # Test data for claim

    claim_data = {
        "submitted_procedure": "D123456",
        "provider_npi": "4561239870",
        "provider_fees": 100.0,
        "member_coinsurance": 20.0,
        "member_copay": 10.0,
        "allowed_fees": 80.0,
        "quadrant": "UR",
        "subscriber_num": "1234567",
        "plan_group": "GRP-1000",
        "service_date": "03/13/2024 0:00",
    }

    # Make POST request to /claims/ endpoint
    response = client.post("/", json=claim_data)

    print("Response", response)

    response_json = response.json()

    # Verify response status code
    assert response.status_code == 200

    # Verify response data contains calculated values
    assert "id" in response_json
    assert "net_fee" in response_json

    # Verify response data calculations are correct
    assert response_json["net_fee"] == (
        claim_data["provider_fees"]
        + claim_data["member_coinsurance"]
        + claim_data["member_copay"]
        - claim_data["allowed_fees"]
    )


@pytest.fixture
def sample_claims_data():
    # Sample claims data for testing top 10 providers
    return [
        ("1234567890", 100.0, 20.0, 10.0, 80.0),  # provider_npi, provider_fees, member_coinsurance, member_copay, allowed_fees
        ("0987654321", 150.0, 30.0, 15.0, 120.0),
        ("1234567891", 80.0, 15.0, 8.0, 60.0),
        ("9876543210", 200.0, 40.0, 20.0, 160.0),
        ("0987654322", 90.0, 18.0, 9.0, 70.0),
        ("1234567892", 100.0, 20.0, 10.0, 80.0),  # provider_npi, provider_fees, member_coinsurance, member_copay, allowed_fees
        ("0987654323", 150.0, 30.0, 15.0, 120.0),
        ("1234567893", 80.0, 15.0, 8.0, 60.0),
        ("9876543211", 200.0, 40.0, 20.0, 160.0),
        ("0987654324", 90.0, 18.0, 9.0, 70.0),
        ("1234567894", 100.0, 20.0, 10.0, 80.0),  # provider_npi, provider_fees, member_coinsurance, member_copay, allowed_fees
        ("0987654325", 150.0, 30.0, 15.0, 120.0),
        ("1234567895", 80.0, 15.0, 8.0, 60.0),
        ("9876543212", 200.0, 40.0, 20.0, 160.0),
        ("0987654326", 90.0, 18.0, 9.0, 70.0),
    ]


def test_compute_top_10_provider_npis(sample_claims_data):
    top_provider_npis = compute_top_10_provider_npis(sample_claims_data)
    assert len(top_provider_npis) == 10
    print(top_provider_npis)
    assert top_provider_npis == [
        '9876543212', '9876543211', '9876543210', '0987654325', '0987654323',
        '0987654321', '1234567894', '1234567892', '1234567890', '0987654326']


# Test the endpoint directly
def test_top_providers_endpoint():
    response = client.get("/top-providers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10
    for provider_npi in data:
        assert isinstance(provider_npi, str)
        assert len(provider_npi) == 10
