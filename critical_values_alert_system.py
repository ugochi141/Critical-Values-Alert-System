import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Critical Values Alert System", layout="wide")

# Function to generate random critical values
def generate_critical_values(n_samples=10):
    now = datetime.now()
    data = {
        'Test_ID': range(1, n_samples + 1),
        'Patient_ID': [f'P{i:03d}' for i in np.random.randint(1, 100, n_samples)],
        'Test_Type': np.random.choice(['CBC', 'Metabolic Panel', 'Cardiac Enzymes', 'Coagulation'], n_samples),
        'Critical_Value': np.random.choice(['Low', 'High'], n_samples),
        'Timestamp': [now - timedelta(minutes=np.random.randint(0, 60)) for _ in range(n_samples)],
        'Acknowledged': np.random.choice([True, False], n_samples, p=[0.7, 0.3]),
        'Escalated': np.random.choice([True, False], n_samples, p=[0.2, 0.8]),
    }
    return pd.DataFrame(data)

# Initialize session state
if 'critical_values' not in st.session_state:
    st.session_state.critical_values = generate_critical_values()

# Dashboard title
st.title("Real-time Critical Values Alert System")

# Sidebar for controls
st.sidebar.header("Controls")
if st.sidebar.button("Generate New Alerts"):
    st.session_state.critical_values = generate_critical_values()

# Main dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("Critical Values Dashboard")
    
    # Summary metrics
    total_alerts = len(st.session_state.critical_values)
    acknowledged = st.session_state.critical_values['Acknowledged'].sum()
    escalated = st.session_state.critical_values['Escalated'].sum()
    
    st.metric("Total Alerts", total_alerts)
    st.metric("Acknowledged", acknowledged)
    st.metric("Escalated", escalated)
    
    # Pie chart for acknowledgment status
    fig_ack = px.pie(names=['Acknowledged', 'Unacknowledged'], 
                     values=[acknowledged, total_alerts - acknowledged],
                     title="Acknowledgment Status")
    st.plotly_chart(fig_ack)

with col2:
    st.subheader("Alert Details")
    
    # Bar chart of alerts by test type
    test_type_counts = st.session_state.critical_values['Test_Type'].value_counts()
    fig_test_type = px.bar(x=test_type_counts.index, y=test_type_counts.values,
                           labels={'x': 'Test Type', 'y': 'Number of Alerts'},
                           title="Alerts by Test Type")
    st.plotly_chart(fig_test_type)
    
    # Timeline of alerts
    fig_timeline = px.scatter(st.session_state.critical_values, x='Timestamp', y='Test_Type',
                              color='Critical_Value', symbol='Acknowledged',
                              labels={'Timestamp': 'Time', 'Test_Type': 'Test Type'},
                              title="Alert Timeline")
    st.plotly_chart(fig_timeline)

# Alert list
st.subheader("Critical Value Alerts")
st.dataframe(st.session_state.critical_values)

# Acknowledgment and Escalation Management
st.subheader("Acknowledgment and Escalation Management")
selected_alert = st.selectbox("Select Alert to Manage", st.session_state.critical_values['Test_ID'])

if selected_alert:
    alert = st.session_state.critical_values[st.session_state.critical_values['Test_ID'] == selected_alert].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Patient ID: {alert['Patient_ID']}")
        st.write(f"Test Type: {alert['Test_Type']}")
        st.write(f"Critical Value: {alert['Critical_Value']}")
        st.write(f"Timestamp: {alert['Timestamp']}")
    
    with col2:
        if st.button("Acknowledge Alert"):
            st.session_state.critical_values.loc[st.session_state.critical_values['Test_ID'] == selected_alert, 'Acknowledged'] = True
            st.success("Alert acknowledged!")
        
        if st.button("Escalate Alert"):
            st.session_state.critical_values.loc[st.session_state.critical_values['Test_ID'] == selected_alert, 'Escalated'] = True
            st.warning("Alert escalated!")

# Note about real-time functionality
st.info("Note: In a real system, this dashboard would update in real-time as new critical values are detected. "
        "For this demo, use the 'Generate New Alerts' button in the sidebar to simulate new data.")
