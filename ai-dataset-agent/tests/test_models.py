
import copy

import pytest
from pydantic import ValidationError

from src.models import SalesMetrics


@pytest.fixture
def valid_metrics():
    return {
        "total_revenue": 1140.0,
        "revenue_by_category": {
            "Electronics": 590.0,
            "Furniture": 490.0,
            "Office": 60.0,
        },
        "top_category": "Electronics",
    }


def test_valid_metrics(valid_metrics):
    result = SalesMetrics.model_validate(valid_metrics)

    assert result.total_revenue == 1140.0
    assert result.top_category == "Electronics"


def test_reject_incorrect_total(valid_metrics):
    data = copy.deepcopy(valid_metrics)
    data["total_revenue"] = 9999.0

    with pytest.raises(ValidationError, match="Revenue mismatch"):
        SalesMetrics.model_validate(data)


def test_reject_incorrect_top_category(valid_metrics):
    data = copy.deepcopy(valid_metrics)
    data["top_category"] = "Office"

    with pytest.raises(ValidationError, match="Top category mismatch"):
        SalesMetrics.model_validate(data)


def test_reject_negative_total(valid_metrics):
    data = copy.deepcopy(valid_metrics)
    data["total_revenue"] = -500.0

    with pytest.raises(ValidationError):
        SalesMetrics.model_validate(data)


def test_reject_unexpected_fields(valid_metrics):
    data = copy.deepcopy(valid_metrics)
    data["delete_records"] = True

    with pytest.raises(ValidationError):
        SalesMetrics.model_validate(data)
