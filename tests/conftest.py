import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import pytest
@pytest.fixture
def sample_vehicles():
    """Create a small list of vehicles for testing."""

    v1 = Vehicle(
        brand="Toyota",
        model="Yaris",
        price=15000,
        body="hatchback",
        energy="petrol"
    )

    v2 = Vehicle(
        brand="Tesla",
        model="Model 3",
        price=45000,
        body="sedan",
        energy="electric"
    )

    v3 = Vehicle(
        brand="Renault",
        model="Clio",
        price=18000,
        body="hatchback",
        energy="diesel"
    )

    return [v1, v2, v3]