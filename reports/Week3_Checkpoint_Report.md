# RetailPulse - Week 3 Checkpoint & Frontend Report
**Generated on:** 2026-06-28 15:41:40  
**Project:** AI-Powered Customer Analytics & Demand Forecasting  

---

## 1. Week 3 Objectives
Week 3 focused on Frontend Development, UI/UX Design, and Interactive Data Visualization. We transitioned our backend Python scripts and ML models into a cohesive, multi-page web application using Streamlit.

## 2. Dashboard Architecture
- **Framework:** Streamlit (Python)
- **Visualization Library:** Plotly (for interactive, hover-enabled charts)
- **Structure:** Multi-page architecture using the `pages/` directory routing.
- **Theming:** Custom global theme applied via `.streamlit/config.toml` for a unified, professional brand identity.

## 3. Module Breakdown
### 📈 Demand Forecasting
- Displays 30-day ahead predictions from the Hybrid Ensemble.
- Features an interactive **What-If Analysis Simulator** allowing users to adjust marketing spend and seasonality multipliers to see real-time revenue impact.

###  Customer Segmentation & Churn
- Visualizes K-Means/PCA clusters in a 2D interactive scatter plot.
- Includes sidebar filters for Region and Segment.
- Highlights the **Top 10 At-Risk Customers** for immediate marketing intervention.

### 📦 Inventory Optimization
- Translates ML forecasts into supply chain actions.
- Visualizes Current Stock vs. Reorder Point (ROP).
- Provides a downloadable CSV of recommended order quantities.

### ⚙️ MLOps Monitoring
- Embeds the live **Evidently AI HTML Drift Report** directly into the UI.
- Displays a gauge chart for the Data Drift Score.
- Tracks model performance against Zidio acceptance criteria (MAPE ≤ 12%, AUC-ROC ≥ 0.88).

## 4. Next Steps (Week 4)
- **Containerization:** Dockerize the application and MLflow server.
- **Orchestration:** Finalize Airflow DAG deployment.
- **CI/CD:** Set up GitHub Actions for automated testing.
- **Monitoring:** Configure Prometheus and Grafana for infrastructure metrics.
