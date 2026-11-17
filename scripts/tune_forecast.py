import itertools
import logging
import warnings

import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json

warnings.filterwarnings("ignore")
logging.getLogger("prophet").setLevel(logging.ERROR)
logging.getLogger("cmdstanpy").setLevel(logging.ERROR)

df = pd.read_csv("data/daily_sales_prepared.csv", parse_dates=["date"])
df = df[["date", "total_amount"]].rename(columns={"date": "ds", "total_amount": "y"})
df = df.sort_values("ds").reset_index(drop=True)
n = len(df)


def mape(actual, pred):
    return float(np.mean(np.abs((actual - pred) / actual)) * 100)


def build(cp, mode, monthly):
    m = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=cp,
        seasonality_mode=mode,
    )
    if monthly:
        m.add_seasonality(name="monthly", period=30.5, fourier_order=5)
    return m


results = []
for cp, mode, monthly in itertools.product(
    [0.01, 0.05, 0.1, 0.3], ["additive", "multiplicative"], [False, True]
):
    scores = []
    for k in (90, 60):  # two earlier validation windows
        train = df.iloc[: n - k]
        val = df.iloc[n - k : n - k + 30]
        m = build(cp, mode, monthly)
        m.fit(train)
        scores.append(mape(val["y"].values, m.predict(val[["ds"]])["yhat"].values))
    results.append((float(np.mean(scores)), cp, mode, monthly))
    print(f"cp={cp} mode={mode} monthly={monthly} -> validation MAPE {np.mean(scores):.2f}")

results.sort(key=lambda r: r[0])
best = results[0]
print("Best config:", best)

# Final honest test: train on everything except the last 30 days
train, test = df.iloc[:-30], df.iloc[-30:]
m = build(best[1], best[2], best[3])
m.fit(train)
fc = m.predict(m.make_future_dataframe(periods=30))
merged = fc.merge(test, on="ds")
final = mape(merged["y"].values, merged["yhat"].values)
print(f"HOLDOUT MAPE (last 30 days, never trained on): {final:.2f}%  (target <= 12%)")

with open("models/prophet_model.json", "w") as f:
    f.write(model_to_json(m))
fc[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv("data/forecast_eval.csv", index=False)
with open("reports/forecast_mape.txt", "w") as f:
    f.write(f"{final:.2f}")
with open("reports/Forecast_Tuning_Results.md", "w") as f:
    f.write("# Prophet tuning results\n\n")
    f.write("Hyperparameters were chosen on two earlier 30-day validation windows.\n")
    f.write("The final MAPE is measured on the last 30 days, which were never used for training or tuning.\n\n")
    f.write(f"- Best config: changepoint_prior_scale={best[1]}, seasonality_mode={best[2]}, monthly_seasonality={best[3]}\n")
    f.write(f"- Final holdout MAPE: {final:.2f}% (target <= 12%)\n\n")
    f.write("## Top 5 configs by validation MAPE\n\n")
    for r in results[:5]:
        f.write(f"- {r[0]:.2f}% (changepoint_prior_scale={r[1]}, mode={r[2]}, monthly={r[3]})\n")
