# RetailPulse: AI-Powered Customer Analytics & Demand Forecasting Platform

Predictive demand, customer segmentation, churn analysis and inventory optimization in one Streamlit app, with MLOps tooling (MLflow, Evidently AI, Airflow, Docker, Kubernetes, Prometheus, Grafana).

**Live demo:** https://retailpulse-6pszmt2n6gp9zgjc8ynqsb.streamlit.app
**Author:** Asish Ayusman Sahoo | Zidio Development, Data Science & Analytics

## Key features

| ID | Feature | Description | Status |
|---|---|---|---|
| F-01 | Data ingestion and cleaning | Synthetic retail data, cleaning and feature engineering, data validation (Great Expectations, notebook 02) | Done |
| F-02 | Customer segmentation | RFM + K-Means with 6 segments (DBSCAN used for outlier detection) | Done |
| F-03 | Demand forecasting | Prophet (tuned) and LSTM, 30-day forecast | MAPE 12.44% (target <= 12%): not met |
| F-04 | Churn analysis | XGBoost + SHAP; dashboard shows a rule-based risk score | AUC target not met, see Limitations |
| F-05 | Inventory optimization | Reorder recommendations from forecasted demand, CSV export | Done |
| F-06 | Dashboard | 4-page Streamlit app, what-if analysis, CSV exports | Done |

## Results

| Metric | Result | Target |
|---|---|---|
| Prophet MAPE (tuned, last 30 days never used for training or tuning) | 12.44% | <= 12% |
| LSTM MAPE | 18.81% | n/a |
| Ensemble (inverse-error weighted), notebook 08 | 12.48% | <= 12% |
| Segmentation silhouette (k=6) | 0.278 | n/a |
| Churn AUC-ROC, leakage-free | about 0.5 | >= 0.88 |

Details: `reports/Forecast_Tuning_Results.md` and `reports/Churn_Leakage_Findings.md`.

### Customer segments (6)

| Segment | Customers | Avg recency (days) | Avg frequency | Avg monetary |
|---|---|---|---|---|
| Champions | 200 | 6.7 | 40.2 | 15,298 |
| Loyal Customers | 408 | 5.3 | 32.7 | 12,035 |
| Slipping Loyalists | 387 | 27.0 | 35.9 | 13,672 |
| Promising | 264 | 4.9 | 26.4 | 9,109 |
| At Risk | 537 | 30.8 | 29.2 | 10,472 |
| Hibernating | 204 | 33.8 | 22.8 | 7,535 |

## Technology stack

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python 3.11 (Docker and CI), tested locally on 3.12 | Data science ecosystem |
| Data | Pandas, NumPy, scikit-learn | Core data and ML |
| Forecasting | Prophet + LSTM (PyTorch Lightning) | Hybrid time series |
| Churn | XGBoost + SHAP | Interpretable classification |
| Dashboard | Streamlit | Fast interactive analytics |
| Experiment tracking | MLflow | Reproducibility |
| Drift detection | Evidently AI | Data drift report |
| Orchestration | Airflow DAG (retraining) | Automated retraining |
| Containers | Docker (multi-stage), Kubernetes manifests | Consistent deployment |
| Monitoring | Prometheus + Grafana | Metrics and dashboards |
| CI | GitHub Actions (pytest) | Automated tests |
| Hosting | Streamlit Community Cloud | Public HTTPS demo |

Not implemented: PostgreSQL and Redis (CSV files are used), JWT authentication and role-based access. Kubernetes manifests are provided but not deployed to a cluster.

## Architecture

    Raw CSVs -> cleaning + features (notebooks 01-04) -> segmented customers / daily sales
        |
        +-> Prophet / LSTM / ensemble (05, 06, 08) -> models/ + data/forecast_eval.csv
        +-> churn model (09) + SHAP
        +-> inventory logic (10)
        |
    MLflow tracking (11) + Evidently drift (12) + Airflow retrain DAG (13)
        |
    Streamlit dashboard (dashboard/) -> Docker -> Kubernetes / Streamlit Cloud
        |
    Prometheus exporter (monitoring/) -> Prometheus -> Grafana

## Project structure

    dashboard/        Streamlit app (app.py + pages/)
    notebooks         01-20 numbered notebooks in the repo root
    scripts/          resegment.py, tune_forecast.py, churn_leakage_check.py
    airflow_dags/     retraining DAG
    monitoring/       Prometheus exporter, Prometheus and Grafana config
    k8s/              Kubernetes manifests
    models/, data/, reports/, tests/

## Run locally

    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    streamlit run dashboard/app.py
    pytest

Docker: `docker build -t retailpulse .` then `docker run -p 8501:8501 retailpulse`
Monitoring: `docker compose -f monitoring/docker-compose.monitoring.yml up -d` (Prometheus :9090, Grafana :3000)
Kubernetes: `kubectl apply -f k8s/`

## Execution timeline

- Week 1: data, cleaning, segmentation, time series prep, Prophet and LSTM baselines
- Week 2: ensemble, churn model, inventory logic, drift detection, retraining pipeline
- Week 3: Streamlit dashboard (forecast, what-if, segmentation, inventory, MLOps pages)
- Week 4: Docker, Kubernetes, CI, monitoring, deployment, final validation

## Challenges and learnings

- **Label leakage in churn.** The first churn label was `recency > 90` and `recency` was also a feature, so AUC was 1.0. After removing it, AUC was about 0.5. The synthetic transactions assign purchases to random customers, so customers have no individual behavior to learn. Honest result: the AUC target is not reachable on this data and should be re-tested on real customer data.
- **Prophet on Streamlit Cloud.** Prophet's Stan backend could not load on the free server. The Demand Forecasting page falls back to a saved forecast (`data/forecast_eval.csv`).
- **Honest evaluation.** Forecast hyperparameters were tuned on earlier windows only. The reported MAPE is on the last 30 days, never used for training or tuning.
- The dashboard "risk score" is rule-based (segment risk plus recency), not a trained model prediction.

## Limitations

Data is synthetic. Customer data contains no personal information. The churn AUC target (>= 0.88) and precision@top 20% (>= 0.75) are not met with this data.
