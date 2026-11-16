# dashboard/pages/2_👥_Customer_Segmentation.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Customer Segmentation", page_icon="👥", layout="wide")

st.markdown("# 👥 Customer Segmentation & Churn Risk")
st.markdown("### RFM Clustering (K-Means & DBSCAN) + Churn Risk Analysis")

st.write("""
This module visualizes our customer base grouped by Recency, Frequency, and Monetary (RFM) behaviors. 
It also highlights the top at-risk customers to help the marketing team target retention campaigns effectively.
""")

st.markdown("---")

# ==========================================
# Load Data & Simulate Churn Risk
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('data/customers_segmented.csv')
    
    # Simulate Churn Risk Score based on Segment and Recency 
    # (In production, this would be the exact probability from the XGBoost model)
    risk_map = {
        'Hibernating': 0.85,
        'At Risk': 0.65,
        'New Customers': 0.40,
        'Loyal Customers': 0.15,
        'Champions': 0.05
    }
    df['base_risk'] = df['segment'].map(risk_map)
    
    # Adjust risk slightly based on recency (higher recency = higher risk)
    if df['recency'].max() > 0:
        recency_factor = df['recency'] / df['recency'].max()
    else:
        recency_factor = 0
        
    df['churn_probability'] = (df['base_risk'] * 0.7) + (recency_factor * 0.3)
    df['churn_probability'] = df['churn_probability'].clip(0, 1)
    
    return df

customers = load_data()

# ==========================================
# Sidebar Filters
# ==========================================
st.sidebar.header("🔍 Filter Customers")

selected_segments = st.sidebar.multiselect(
    "Select Customer Segments:",
    options=customers['segment'].unique(),
    default=customers['segment'].unique()
)

selected_regions = st.sidebar.multiselect(
    "Select Regions:",
    options=customers['region'].unique(),
    default=customers['region'].unique()
)

# Filter the data
filtered_df = customers[
    (customers['segment'].isin(selected_segments)) & 
    (customers['region'].isin(selected_regions))
]

# ==========================================
# KPI Cards
# ==========================================
st.subheader("📊 Segment Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", f"{len(filtered_df):,}")
with col2:
    st.metric("Avg Recency (Days)", f"{filtered_df['recency'].mean():.1f}")
with col3:
    st.metric("Avg Frequency", f"{filtered_df['frequency'].mean():.1f}")
with col4:
    avg_risk = filtered_df['churn_probability'].mean() * 100
    st.metric("Avg Churn Risk Score", f"{avg_risk:.1f}%")

st.markdown("---")

# ==========================================
# Interactive PCA Scatter Plot
# ==========================================
st.subheader("🌐 Customer Segments in 2D Space (PCA Reduced)")
st.write("Each dot represents a customer. The axes are Principal Components derived from their RFM behaviors.")

if 'pca1' in filtered_df.columns and 'pca2' in filtered_df.columns:
    fig_scatter = px.scatter(
        filtered_df, 
        x='pca1', 
        y='pca2', 
        color='segment',
        hover_data=['customer_id', 'recency', 'frequency', 'monetary', 'churn_probability'],
        title="Customer Clusters (PCA)",
        color_discrete_sequence=px.colors.qualitative.Set1,
        size_max=10
    )
    
    fig_scatter.update_layout(
        height=600,
        legend_title_text='Customer Segment',
        hovermode='closest'
    )
    
    # Format hover template for a clean look
    fig_scatter.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Recency: %{customdata[1]} days<br>Frequency: %{customdata[2]}<br>Monetary: $%{customdata[3]:,.2f}<br>Churn Risk: %{customdata[4]:.2%}<extra></extra>"
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("PCA coordinates not found in the dataset. Please ensure Day 3 notebook was run correctly.")

st.markdown("---")

# ==========================================
# Segment Distribution
# ==========================================
st.subheader("🥧 Segment Distribution")
col1, col2 = st.columns(2)

with col1:
    seg_counts = filtered_df['segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    
    fig_pie = px.pie(
        seg_counts, 
        values='Count', 
        names='Segment', 
        title="Customer Count by Segment",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    seg_risk = filtered_df.groupby('segment')['churn_probability'].mean().reset_index()
    seg_risk.columns = ['Segment', 'Avg Churn Risk']
    seg_risk = seg_risk.sort_values(by='Avg Churn Risk', ascending=False)
    
    fig_bar = px.bar(
        seg_risk, 
        x='Segment', 
        y='Avg Churn Risk', 
        title="Average Churn Risk by Segment",
        color='Avg Churn Risk',
        color_continuous_scale='Reds'
    )
    fig_bar.update_layout(yaxis_tickformat='.0%')
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ==========================================
# Top 10 At-Risk Customers
# ==========================================
st.subheader("🚨 Top 10 At-Risk Customers (Highest Risk Score)")
st.caption("Risk score is a rule-based indicator (recency and customer history), not a trained model prediction. See reports/Churn_Leakage_Findings.md.")
st.write("Target these customers with retention campaigns to maximize ROI.")

# Get top 10 highest churn probability
top_risk = filtered_df.nlargest(10, 'churn_probability')[
    ['customer_id', 'segment', 'recency', 'frequency', 'monetary', 'churn_probability', 'region']
].copy()

# Format for display
top_risk_display = top_risk.copy()
top_risk_display['churn_probability'] = top_risk_display['churn_probability'].apply(lambda x: f"{x:.1%}")
top_risk_display['monetary'] = top_risk_display['monetary'].apply(lambda x: f"${x:,.2f}")
top_risk_display.rename(columns={
    'customer_id': 'Customer ID',
    'segment': 'Segment',
    'recency': 'Days Since Last Purchase',
    'frequency': 'Total Orders',
    'monetary': 'Total Spent',
    'churn_probability': 'Churn Risk %',
    'region': 'Region'
}, inplace=True)

st.dataframe(
    top_risk_display,
    use_container_width=True,
    hide_index=True
)

st.info("💡 **Pro Tip:** Export this list to CSV and feed it directly to your CRM for targeted email campaigns!")
