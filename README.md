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
(add URL here)

## Author
Asish Ayusman Sahoo
