# RetailPulse: AI-Powered Customer Analytics & Demand Forecasting

Retail analytics platform with a Streamlit dashboard.

## Modules
- Customer segmentation (RFM, K-Means/DBSCAN)
- Demand forecasting (Prophet + LSTM), target MAPE <= 12%
- Churn prediction (XGBoost + SHAP), target AUC-ROC >= 0.88
- Inventory optimization (reorder recommendations)
- MLOps: MLflow tracking, Evidently drift monitoring, Airflow retraining

## Setup
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    streamlit run dashboard/app.py

## Live demo
https://retailpulse-6pszmt2n6gp9zgjc8ynqsb.streamlit.app

## Author
Asish Ayusman Sahoo

## Results

| Module | Result | Target | Status |
|---|---|---|---|
| Demand forecasting (Prophet baseline) | MAPE 12.48% | MAPE <= 12% | Slightly above target |
| Demand forecasting (LSTM) | MAPE 18.81% | n/a | Weaker than Prophet |
| Churn prediction | AUC about 0.5 (leakage-free) | AUC-ROC >= 0.88 | Not met, see below |
| Customer segmentation | RFM + K-Means, 4 dashboard pages | n/a | Done |
| MLOps | MLflow, Evidently drift report, Airflow DAG, Docker, CI | n/a | Done |

## Churn model: leakage finding

The original churn label was `recency > 90`, and `recency` was also a model feature, so the earlier AUC of 1.0 was caused by label leakage and is not a valid result.

With a leakage-free setup:
- Original label without `recency` and `segment`: AUC 0.61
- Forward-looking label (features before a cutoff date, churn = no purchase in the next 30/45/60 days): AUC 0.54 / 0.49 / 0.48

The synthetic transactions assign each purchase to a randomly chosen customer, so customers have no individual behavior for a model to learn. The AUC target is not reachable on this data. The same pipeline should be re-evaluated on real customer data.

The dashboard shows a rule-based "risk score", not a trained model prediction.
See `scripts/churn_leakage_check.py` and `reports/Churn_Leakage_Findings.md`.

## Results

| Module | Result | Target | Status |
|---|---|---|---|
| Demand forecasting (Prophet baseline) | MAPE 12.48% | MAPE <= 12% | Slightly above target |
| Demand forecasting (LSTM) | MAPE 18.81% | n/a | Weaker than Prophet |
| Churn prediction | AUC about 0.5 (leakage-free) | AUC-ROC >= 0.88 | Not met, see below |
| Customer segmentation | RFM + K-Means, 4 dashboard pages | n/a | Done |
| MLOps | MLflow, Evidently drift report, Airflow DAG, Docker, CI | n/a | Done |

## Churn model: leakage finding

The original churn label was `recency > 90`, and `recency` was also a model feature, so the earlier AUC of 1.0 was caused by label leakage and is not a valid result.

With a leakage-free setup:
- Original label without `recency` and `segment`: AUC 0.61
- Forward-looking label (features before a cutoff date, churn = no purchase in the next 30/45/60 days): AUC 0.54 / 0.49 / 0.48

The synthetic transactions assign each purchase to a randomly chosen customer, so customers have no individual behavior for a model to learn. The AUC target is not reachable on this data. The same pipeline should be re-evaluated on real customer data.

The dashboard shows a rule-based "risk score", not a trained model prediction.
See `scripts/churn_leakage_check.py` and `reports/Churn_Leakage_Findings.md`.
