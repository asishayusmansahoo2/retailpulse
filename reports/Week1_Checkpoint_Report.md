# RetailPulse - Week 1 Checkpoint & EDA Report
**Generated on:** 2026-06-27 16:12:00  
**Project:** AI-Powered Customer Analytics & Demand Forecasting  

---

## 1. Project Overview
RetailPulse is an end-to-end data science platform designed to ingest retail sales, customer, and inventory data to deliver accurate demand forecasts, customer segmentation, and churn predictions. 

## 2. Dataset Summary & EDA
- **Total Customers:** 2,000
- **Total Transactions:** 62,611
- **Date Range:** 2025-01-01 to 2026-06-25 (541 continuous days)

**Key EDA Findings:**
- Transaction amounts are heavily right-skewed (typical retail distribution).
- Clear weekly seasonality observed (weekend spikes).
- Massive holiday seasonality observed in Nov/Dec.
- 2% missing values in `payment_method` were successfully imputed using the mode.

## 3. Data Quality & Validation
- **Great Expectations:** All 5 critical data quality rules passed (no negative amounts, unique IDs, no nulls in critical columns).
- **Stationarity:** Augmented Dickey-Fuller (ADF) test confirmed the presence of a trend (non-stationary), which is expected and handled by Prophet/LSTM.

## 4. Customer Segmentation (RFM)
Using K-Means (k=5) and DBSCAN for outlier detection, we identified the following business segments:
- **Segments:** ['Hibernating', 'Champions', 'New Customers']
- **Distribution:** {'Hibernating': 797, 'Champions': 627, 'New Customers': 576}

## 5. Baseline Forecasting Models (Logged in MLflow)
We established two baseline models for 30-day ahead demand forecasting:
- **Prophet (Statistical):** MAPE = 12.48%
- **LSTM (Deep Learning):** MAPE = 18.81%

*Note: Both models are fully tracked in MLflow with parameters, metrics, and visual artifacts.*

## 6. Next Steps (Week 2)
- Build the **Hybrid Ensemble Model** (Prophet + LSTM) to push MAPE ≤ 12%.
- Implement **Churn Prediction** using XGBoost and SHAP explainability.
- Develop **Inventory Optimization** logic (Safety Stock, Reorder Point).
