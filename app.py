import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page title
st.set_page_config(page_title="Lab Order TAT Dashboard", layout="wide")

# Function to generate random data
def generate_random_data(n_samples=100):
    np.random.seed(42)  # for reproducibility
    
    data = {
        'Order_ID': range(1, n_samples + 1),
        'Test_Type': np.random.choice(['CBC', 'Metabolic Panel', 'Lipid Panel', 'Thyroid Panel'], n_samples),
        'Priority': np.random.choice(['Routine', 'STAT'], n_samples, p=[0.8, 0.2]),
        'TAT_Hours': np.random.normal(loc=24, scale=8, size=n_samples).round(2),
        'Department': np.random.choice(['Hematology', 'Chemistry', 'Immunology'], n_samples),
    }
    
    df = pd.DataFrame(data)
    df['TAT_Hours'] = np.abs(df['TAT_Hours'])  # Ensure positive TAT
    df.loc[df['Priority'] == 'STAT', 'TAT_Hours'] *= 0.5  # STAT orders are typically faster
    
    return df

# Generate random data
df = generate_random_data(1000)

# Dashboard title
st.title("Lab Order Turnaround Time (TAT) Dashboard")

# Sidebar for filters
st.sidebar.header("Filters")
selected_dept = st.sidebar.multiselect("Select Department", options=df['Department'].unique(), default=df['Department'].unique())
selected_priority = st.sidebar.multiselect("Select Priority", options=df['Priority'].unique(), default=df['Priority'].unique())

# Filter the dataframe
filtered_df = df[(df['Department'].isin(selected_dept)) & (df['Priority'].isin(selected_priority))]

# Display key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Average TAT (Hours)", f"{filtered_df['TAT_Hours'].mean():.2f}")
col2.metric("Median TAT (Hours)", f"{filtered_df['TAT_Hours'].median():.2f}")
col3.metric("90th Percentile TAT (Hours)", f"{filtered_df['TAT_Hours'].quantile(0.9):.2f}")

# Create visualizations
st.subheader("TAT Distribution by Test Type")
fig1 = px.box(filtered_df, x="Test_Type", y="TAT_Hours", color="Priority")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Average TAT by Department")
dept_avg = filtered_df.groupby("Department")["TAT_Hours"].mean().reset_index()
fig2 = px.bar(dept_avg, x="Department", y="TAT_Hours", color="Department")
st.plotly_chart(fig2, use_container_width=True)

# Display raw data
st.subheader("Raw Data")
st.dataframe(filtered_df)
