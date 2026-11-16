# dashboard/app.py
import streamlit as st

import pandas as pd

def _kpis():
    t = pd.read_csv('data/transactions_cleaned.csv', parse_dates=['date'])
    end = t['date'].max()
    cur = t[t['date'] > end - pd.Timedelta(days=30)]
    prev = t[(t['date'] > end - pd.Timedelta(days=60)) & (t['date'] <= end - pd.Timedelta(days=30))]
    d = pd.read_csv('data/daily_sales_prepared.csv', parse_dates=['date'])
    fc = pd.read_csv('data/forecast_eval.csv', parse_dates=['ds'])
    last = d['date'].max()
    a = d[d['date'] > last - pd.Timedelta(days=29)][['date', 'total_amount']]
    a = a.rename(columns={'date': 'ds', 'total_amount': 'y'})
    m = a.merge(fc[['ds', 'yhat']], on='ds')
    mape = (abs(m['y'] - m['yhat']) / m['y']).mean() * 100
    return (cur['total_amount'].sum(), prev['total_amount'].sum(),
            cur['customer_id'].nunique(), prev['customer_id'].nunique(),
            len(cur), len(prev), mape)

k_rev, k_rev_p, k_cust, k_cust_p, k_n, k_n_p, k_mape = _kpis()

import pandas as pd

# ==========================================
# Page Configuration (Must be the first Streamlit command)
# ==========================================
st.set_page_config(
    page_title="RetailPulse - AI Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Custom CSS for a polished, modern look
# ==========================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# Hero Section
# ==========================================
st.markdown('<p class="main-header">📊 RetailPulse</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Customer Analytics & Demand Forecasting Platform</p>', unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# High-Level KPI Cards (Mocked for the skeleton)
# ==========================================
st.subheader("🚀 Platform Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Revenue (30D)", value=f"${k_rev:,.0f}", delta=f"{(k_rev/k_rev_p-1)*100:+.1f}%")
with col2:
    st.metric(label="Active Customers (30D)", value=f"{k_cust:,}", delta=f"{k_cust-k_cust_p:+d}")
with col3:
    st.metric(label="Forecast MAPE (Prophet, 30D)", value=f"{k_mape:.1f}%", delta="Target: <=12%", delta_color="off")
with col4:
    st.metric(label="Transactions (30D)", value=f"{k_n:,}", delta=f"{(k_n/k_n_p-1)*100:+.1f}%")

st.markdown("---")

# ==========================================
# Welcome Message & Navigation Guide
# ==========================================
st.subheader("Welcome to the Command Center")
st.write("""
RetailPulse is an end-to-end data science platform designed to ingest retail sales, customer, and inventory data 
to deliver accurate demand forecasts, customer segmentation, and churn predictions.

**👈 Use the sidebar on the left to navigate through the different modules:**
- **📈 Demand Forecasting:** View our Hybrid Ensemble (Prophet + LSTM) predictions.
- **👥 Customer Segmentation:** Explore RFM clusters and churn risk alerts.
- **📦 Inventory Optimization:** Check automated reorder recommendations.
- **⚙️ MLOps Monitoring:** View data drift reports and model performance metrics.
""")

# ==========================================
# Footer
# ==========================================
st.markdown("---")
st.caption("Built for Zidio Development | Data Science & Analytics Domain | March 2026")