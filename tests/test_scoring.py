import pandas as pd

from src.scoring import apply_risk_scoring, classify_risk


def test_classify_risk_boundaries():
    assert classify_risk(0) == "LOW"
    assert classify_risk(20) == "MEDIUM"
    assert classify_risk(40) == "HIGH"
    assert classify_risk(70) == "CRITICAL"


def test_apply_risk_scoring_adds_explanations():
    database = pd.DataFrame(
        [
            {
                "high_amount": True,
                "unusual_customer_amount": True,
                "unusual_hour": False,
                "transaction_burst": False,
                "rapid_city_change": False,
                "unusual_category": False,
            }
        ]
    )

    scored = apply_risk_scoring(database)

    assert scored.loc[0, "risk_score"] == 45
    assert scored.loc[0, "risk_level"] == "HIGH"
    assert "high-value" in scored.loc[0, "risk_reasons"]
