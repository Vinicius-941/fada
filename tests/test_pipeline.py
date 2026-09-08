from src.pipeline import run_pipeline


def test_pipeline_runs_with_sample_data():
    database, summary = run_pipeline(export=False)

    assert len(database) == summary["total_transactions"]
    assert summary["total_transactions"] > 0
    assert "risk_score" in database.columns
    assert "risk_level" in database.columns
    assert database["risk_score"].between(0, 100).all()
