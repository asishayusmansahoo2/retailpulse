# dashboard/app.py
import streamlit as st
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
    st.metric(label="Total Revenue (30D)", value="$1.24M", delta="+12.5%")
with col2:
    st.metric(label="Active Customers", value="1,842", delta="+45")
with col3:
    st.metric(label="Forecast Accuracy", value="91.4%", delta="+2.1%")
with col4:
    st.metric(label="Inventory Health", value="94%", delta="-1.2%")

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