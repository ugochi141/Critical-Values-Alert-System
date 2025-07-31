import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Set page configuration with improved settings
st.set_page_config(
    page_title="Lab Order TAT Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache data generation for better performance
@st.cache_data(ttl=300)  # Cache for 5 minutes
def generate_random_data(n_samples=100):
    np.random.seed(42)  # for reproducibility
    
    data = {
        'Order_ID': range(1, n_samples + 1),
        'Test_Type': np.random.choice(['CBC', 'Metabolic Panel', 'Lipid Panel', 'Thyroid Panel'], n_samples),
        'Priority': np.random.choice(['Routine', 'STAT'], n_samples, p=[0.8, 0.2]),
        'TAT_Hours': np.random.normal(loc=24, scale=8, size=n_samples).round(2),
        'Department': np.random.choice(['Hematology', 'Chemistry', 'Immunology'], n_samples),
        'Order_Date': pd.date_range(end=datetime.now(), periods=n_samples, freq='H'),
    }
    
    df = pd.DataFrame(data)
    df['TAT_Hours'] = np.abs(df['TAT_Hours'])  # Ensure positive TAT
    df.loc[df['Priority'] == 'STAT', 'TAT_Hours'] *= 0.5  # STAT orders are typically faster
    
    # Add critical value flag for some tests
    df['Is_Critical'] = np.random.choice([True, False], n_samples, p=[0.1, 0.9])
    df.loc[df['Is_Critical'], 'TAT_Hours'] *= 0.3  # Critical values are handled faster
    
    return df

# Error handling wrapper
def safe_load_data():
    try:
        return generate_random_data(1000)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Initialize session state for data persistence
if 'data' not in st.session_state:
    st.session_state.data = safe_load_data()

# Load data
df = st.session_state.data

# Dashboard title with last update time
col_title, col_time = st.columns([3, 1])
with col_title:
    st.title("Lab Order Turnaround Time (TAT) Dashboard")
with col_time:
    st.info(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Add a refresh button
if st.button("🔄 Refresh Data"):
    st.session_state.data = safe_load_data()
    st.rerun()

# Sidebar for filters
st.sidebar.header("Filters")

# Department filter
selected_dept = st.sidebar.multiselect(
    "Select Department",
    options=df['Department'].unique() if not df.empty else [],
    default=df['Department'].unique() if not df.empty else []
)

# Priority filter
selected_priority = st.sidebar.multiselect(
    "Select Priority",
    options=df['Priority'].unique() if not df.empty else [],
    default=df['Priority'].unique() if not df.empty else []
)

# Critical values filter
show_critical_only = st.sidebar.checkbox("Show Critical Values Only", value=False)

# Filter the dataframe
if not df.empty:
    filtered_df = df[
        (df['Department'].isin(selected_dept)) & 
        (df['Priority'].isin(selected_priority))
    ]
    
    if show_critical_only:
        filtered_df = filtered_df[filtered_df['Is_Critical']]
else:
    filtered_df = df

# Display key metrics with error handling
if not filtered_df.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_tat = filtered_df['TAT_Hours'].mean()
        st.metric("Average TAT (Hours)", f"{avg_tat:.2f}")
    
    with col2:
        median_tat = filtered_df['TAT_Hours'].median()
        st.metric("Median TAT (Hours)", f"{median_tat:.2f}")
    
    with col3:
        p90_tat = filtered_df['TAT_Hours'].quantile(0.9)
        st.metric("90th Percentile TAT (Hours)", f"{p90_tat:.2f}")
    
    with col4:
        critical_count = filtered_df['Is_Critical'].sum() if 'Is_Critical' in filtered_df.columns else 0
        st.metric("Critical Values", critical_count)
    
    # Create visualizations with error handling
    try:
        # TAT Distribution by Test Type
        st.subheader("TAT Distribution by Test Type")
        fig1 = px.box(
            filtered_df, 
            x="Test_Type", 
            y="TAT_Hours", 
            color="Priority",
            title="TAT Distribution by Test Type and Priority"
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Average TAT by Department
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Average TAT by Department")
            dept_avg = filtered_df.groupby("Department")["TAT_Hours"].mean().reset_index()
            fig2 = px.bar(
                dept_avg, 
                x="Department", 
                y="TAT_Hours", 
                color="Department",
                title="Average TAT by Department"
            )
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.subheader("TAT Trend Over Time")
            if 'Order_Date' in filtered_df.columns:
                hourly_avg = filtered_df.groupby(pd.Grouper(key='Order_Date', freq='6H'))['TAT_Hours'].mean().reset_index()
                fig3 = px.line(
                    hourly_avg, 
                    x='Order_Date', 
                    y='TAT_Hours',
                    title="Average TAT Trend (6-hour intervals)"
                )
                fig3.update_layout(height=350)
                st.plotly_chart(fig3, use_container_width=True)
        
        # Critical Values Alert Section
        if show_critical_only or critical_count > 0:
            st.subheader("⚠️ Critical Values Alert")
            critical_df = filtered_df[filtered_df['Is_Critical']]
            if not critical_df.empty:
                st.dataframe(
                    critical_df[['Order_ID', 'Test_Type', 'TAT_Hours', 'Department', 'Order_Date']].head(10),
                    use_container_width=True
                )
        
    except Exception as e:
        st.error(f"Error creating visualizations: {str(e)}")
    
    # Display raw data with download option
    st.subheader("Raw Data")
    
    # Add download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download data as CSV",
        data=csv,
        file_name=f'lab_tat_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv'
    )
    
    # Display data table
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
else:
    st.warning("No data available. Please check your filters or refresh the data.")

# Footer with connection status
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🟢 Dashboard Status: Active")
with col2:
    st.caption(f"📊 Total Records: {len(df)}")
with col3:
    st.caption("🔄 Auto-refresh: Disabled")