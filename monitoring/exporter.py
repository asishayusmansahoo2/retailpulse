import os
import time

import pandas as pd
from prometheus_client import Gauge, start_http_server

DATA = os.environ.get("DATA_DIR", "data")
mape_g = Gauge(
    "retailpulse_forecast_mape_percent", "Forecast MAPE on the last 30 days (percent)"
)
cust_g = Gauge("retailpulse_customers_total", "Customers in the segmented table")
seg_g = Gauge("retailpulse_segment_customers", "Customers per segment", ["segment"])
tx_g = Gauge("retailpulse_transactions_total", "Rows in transactions_cleaned.csv")


def refresh():
    c = pd.read_csv(f"{DATA}/customers_segmented.csv")
    cust_g.set(len(c))
    for seg, n in c["segment"].value_counts().items():
        seg_g.labels(segment=seg).set(int(n))
    tx_g.set(len(pd.read_csv(f"{DATA}/transactions_cleaned.csv")))
    d = pd.read_csv(f"{DATA}/daily_sales_prepared.csv", parse_dates=["date"])
    fc = pd.read_csv(f"{DATA}/forecast_eval.csv", parse_dates=["ds"])
    a = d.tail(30).rename(columns={"date": "ds", "total_amount": "y"})[["ds", "y"]]
    m = a.merge(fc[["ds", "yhat"]], on="ds")
    if len(m):
        mape_g.set(float(((m["y"] - m["yhat"]).abs() / m["y"]).mean() * 100))


if __name__ == "__main__":
    start_http_server(8000)
    while True:
        try:
            refresh()
        except Exception as e:
            print("refresh failed:", e)
        time.sleep(30)
