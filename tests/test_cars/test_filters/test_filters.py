import pandas as pd
import pytest
from car.filters.budget_filter import filter_by_budget
from car.filters.energy_filter import filter_by_energy
from car.filters.body_filter import filter_by_body


# ---------------------------------------------------------------------------
# Budget filter
# ---------------------------------------------------------------------------


def test_budget_filter_keeps_vehicles_at_exact_limit(sample_df):
    result = filter_by_budget(sample_df, 18000)
    assert set(result["model"]) == {"Yaris", "Clio"}


def test_budget_filter_empty_result_when_budget_too_low(sample_df):
    result = filter_by_budget(sample_df, 1000)
    assert result.empty


def test_budget_filter_returns_all_when_budget_is_max(sample_df):
    result = filter_by_budget(sample_df, 999_999)
    assert len(result) == len(sample_df)


# ---------------------------------------------------------------------------
# Energy filter
# ---------------------------------------------------------------------------


def test_energy_filter_electric(sample_df):
    result = filter_by_energy(sample_df, "electric")
    assert all(result["energy"].str.contains("elec"))


def test_energy_filter_diesel(sample_df):
    result = filter_by_energy(sample_df, "diesel")
    assert all(result["energy"].str.contains("gazole"))


def test_energy_filter_unknown_returns_empty(sample_df):
    result = filter_by_energy(sample_df, "hydrogen_xyz")
    assert result.empty


# ---------------------------------------------------------------------------
# Body filter
# ---------------------------------------------------------------------------


def test_body_filter_case_insensitive(sample_df):
    result = filter_by_body(sample_df, "Berline")
    assert len(result) == len(sample_df)


def test_body_filter_unknown_returns_empty(sample_df):
    result = filter_by_body(sample_df, "cabriolet_xyz")
    assert result.empty
