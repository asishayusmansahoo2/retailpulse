import pandas as pd


def test_six_segments():
    df = pd.read_csv("data/customers_segmented.csv")
    assert df["segment"].nunique() == 6


def test_no_missing_rfm():
    df = pd.read_csv("data/customers_segmented.csv")
    cols = ["customer_id", "recency", "frequency", "monetary", "segment"]
    assert df[cols].notna().all().all()


def test_unique_customers():
    df = pd.read_csv("data/customers_segmented.csv")
    assert df["customer_id"].is_unique


def test_transactions_clean():
    t = pd.read_csv("data/transactions_cleaned.csv", parse_dates=["date"])
    assert (t["total_amount"] > 0).all()
    assert t["transaction_id"].is_unique


def test_forecast_file():
    fc = pd.read_csv("data/forecast_eval.csv")
    assert {"ds", "yhat", "yhat_lower", "yhat_upper"} <= set(fc.columns)
    assert len(fc) >= 30
    assert (fc["yhat_lower"] <= fc["yhat_upper"]).all()
