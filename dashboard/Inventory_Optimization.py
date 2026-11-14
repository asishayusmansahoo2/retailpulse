# dashboard/pages/3_📦_Inventory_Optimization.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Inventory Optimization", page_icon="📦", layout="wide")

st.markdown("# 📦 Inventory Optimization")
st.markdown("### Automated Reorder Recommendations (Safety Stock & ROP)")

st.write("""
This module translates our 30-day demand forecasts into actionable supply chain decisions. 
It calculates Safety Stock and Reorder Points (ROP) based on a 7-day supplier lead time and a 95% service level.
""")

st.markdown("---")

# Placeholder for Inventory Health Chart
st.subheader("📊 Current Stock vs. Reorder Point (ROP)")
st.info("👉 Bar chart comparing current stock to ROP will be loaded here on Day 18.")

st.markdown("---")

# Placeholder for Reorder Table
st.subheader("📝 Recommended Order List")
st.write("Categories highlighted in red require immediate restocking to prevent stockouts.")
st.info("👉 Interactive dataframe of inventory_recommendations.csv will be loaded here on Day 18.")
# dashboard/pages/3_📦_Inventory_Optimization.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Inventory Optimization", page_icon="📦", layout="wide")

st.markdown("# 📦 Inventory Optimization")
st.markdown("### Automated Reorder Recommendations (Safety Stock & ROP)")

st.write("""
This module translates our 30-day demand forecasts into actionable supply chain decisions. 
It calculates Safety Stock and Reorder Points (ROP) based on a 7-day supplier lead time and a 95% service level.
""")

st.markdown("---")

# ==========================================
# 1. Load Inventory Data
# ==========================================
@st.cache_data
def load_inventory_data():
    inv_path = 'data/inventory_recommendations.csv'
    if os.path.exists(inv_path):
        return pd.read_csv(inv_path)
    else:
        # Fallback: Create mock data if file doesn't exist
        st.warning("⚠️ Inventory recommendations file not found. Using sample data.")
        return pd.DataFrame({
            'category': ['Electronics', 'Clothing', 'Groceries', 'Home'],
            'avg_daily_demand': [1500, 800, 2200, 600],
            'std_daily_demand': [300, 150, 400, 100],
            'expected_30d_demand': [45000, 24000, 66000, 18000],
            'safety_stock': [1200, 600, 1600, 400],
            'reorder_point': [11700, 6200, 17000, 4600],
            'current_stock': [10000, 7000, 15000, 5000],
            'needs_reorder': [True, False, True, False],
            'recommended_order_qty': [36200, 0, 52600, 0]
        })

inv_df = load_inventory_data()

# ==========================================
# 2. KPI Cards
# ==========================================
st.subheader("📊 Inventory Health Overview")

total_categories = len(inv_df)
categories_needing_reorder = inv_df['needs_reorder'].sum()
total_recommended_order_value = inv_df['recommended_order_qty'].sum()
avg_stock_health = (inv_df['current_stock'] / inv_df['reorder_point']).mean() * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Categories", total_categories)
with col2:
    st.metric("⚠️ Need Restocking", categories_needing_reorder, delta=f"{categories_needing_reorder/total_categories*100:.0f}% of total")
with col3:
    st.metric("Total Order Value", f"${total_recommended_order_value:,.0f}")
with col4:
    st.metric("Avg Stock Health", f"{avg_stock_health:.1f}%", delta="Target: >100%")

st.markdown("---")

# ==========================================
# 3. Current Stock vs Reorder Point Chart
# ==========================================
st.subheader("📊 Current Stock vs. Reorder Point (ROP)")
st.write("Categories where Current Stock < ROP (red bars) require immediate attention.")

# Create a sorted dataframe for better visualization
plot_df = inv_df.sort_values(by='reorder_point', ascending=True)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=plot_df['category'],
    y=plot_df['current_stock'],
    name='Current Stock',
    marker_color='skyblue',
    text=plot_df['current_stock'].apply(lambda x: f"${x:,.0f}"),
    textposition='auto'
))

fig.add_trace(go.Bar(
    x=plot_df['category'],
    y=plot_df['reorder_point'],
    name='Reorder Point (ROP)',
    marker_color='lightcoral',
    text=plot_df['reorder_point'].apply(lambda x: f"${x:,.0f}"),
    textposition='auto'
))

# Add a line to highlight the threshold
fig.add_hline(y=0, line_width=2, line_color="gray")

fig.update_layout(
    title="Inventory Status: Current Stock vs Reorder Point",
    xaxis_title="Product Category",
    yaxis_title="Inventory Value ($)",
    barmode='group',
    height=500,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 4. Safety Stock Analysis
# ==========================================
st.markdown("---")
st.subheader("🛡️ Safety Stock Analysis")

col1, col2 = st.columns(2)

with col1:
    fig_safety = px.bar(
        inv_df, 
        x='category', 
        y='safety_stock',
        title="Safety Stock by Category",
        color='safety_stock',
        color_continuous_scale='Blues',
        labels={'safety_stock': 'Safety Stock ($)', 'category': 'Category'}
    )
    fig_safety.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_safety, use_container_width=True)

with col2:
    fig_demand = px.bar(
        inv_df, 
        x='category', 
        y='expected_30d_demand',
        title="Expected 30-Day Demand",
        color='expected_30d_demand',
        color_continuous_scale='Greens',
        labels={'expected_30d_demand': '30-Day Demand ($)', 'category': 'Category'}
    )
    fig_demand.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_demand, use_container_width=True)

# ==========================================
# 5. Reorder Recommendations Table
# ==========================================
st.markdown("---")
st.subheader("📝 Recommended Order List")
st.write("Categories highlighted in red require immediate restocking to prevent stockouts.")

# Prepare the table for display
display_df = inv_df.copy()

# Format columns
display_df['current_stock'] = display_df['current_stock'].apply(lambda x: f"${x:,.0f}")
display_df['reorder_point'] = display_df['reorder_point'].apply(lambda x: f"${x:,.0f}")
display_df['safety_stock'] = display_df['safety_stock'].apply(lambda x: f"${x:,.0f}")
display_df['expected_30d_demand'] = display_df['expected_30d_demand'].apply(lambda x: f"${x:,.0f}")
display_df['recommended_order_qty'] = display_df['recommended_order_qty'].apply(lambda x: f"${x:,.0f}" if x > 0 else "-")

# Rename columns for display
display_df = display_df.rename(columns={
    'category': 'Category',
    'current_stock': 'Current Stock',
    'reorder_point': 'Reorder Point',
    'safety_stock': 'Safety Stock',
    'expected_30d_demand': '30-Day Forecast',
    'recommended_order_qty': 'Recommended Order Qty',
    'needs_reorder': 'Needs Reorder'
})

# Show only relevant columns
columns_to_show = ['Category', 'Current Stock', 'Reorder Point', 'Safety Stock', '30-Day Forecast', 'Recommended Order Qty', 'Needs Reorder']

# Use dataframe with conditional styling
st.dataframe(
    display_df[columns_to_show],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Needs Reorder": st.column_config.CheckboxColumn(
            "⚠️ Urgent",
            help="Check if this category needs immediate restocking",
            default=False,
        )
    }
)

# ==========================================
# 6. Export Option
# ==========================================
st.markdown("---")
st.subheader("💾 Export Recommendations")

# Convert to CSV for download
csv = inv_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Reorder Recommendations as CSV",
    data=csv,
    file_name='inventory_reorder_recommendations.csv',
    mime='text/csv',
)

st.info("""
**💡 Supply Chain Best Practices:**
- **Lead Time:** 7 days (configured)
- **Service Level:** 95% (Z-score: 1.65)
- **Safety Stock Formula:** Z × σ_demand × √(Lead Time)
- **Reorder Point:** (Avg Daily Demand × Lead Time) + Safety Stock
""")