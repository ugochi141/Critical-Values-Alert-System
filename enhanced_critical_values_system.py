import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Configure page
st.set_page_config(
    page_title="Critical Values Alert System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .critical-alert {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 10px;
        margin: 10px 0;
    }
    .urgent-alert {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 10px;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced lab test data with critical values
@st.cache_data
def generate_enhanced_lab_data(n_patients=1000):
    """Generate realistic lab data with critical values"""
    
    # Patient demographics
    patient_names = [
        "John Smith", "Maria Garcia", "David Johnson", "Jennifer Williams", "Robert Brown",
        "Lisa Davis", "Michael Miller", "Sarah Wilson", "Christopher Moore", "Jessica Taylor",
        "Matthew Anderson", "Ashley Thomas", "Joshua Jackson", "Amanda White", "Daniel Harris",
        "Stephanie Martin", "James Thompson", "Michelle Garcia", "Kevin Martinez", "Nicole Robinson",
        "Brandon Clark", "Melissa Rodriguez", "Jason Lewis", "Kimberly Lee", "Eric Walker",
        "Amy Hall", "Nicholas Allen", "Angela Young", "Justin Hernandez", "Rachel King",
        "Tyler Wright", "Laura Lopez", "Aaron Hill", "Heather Scott", "Jonathan Green",
        "Samantha Adams", "Ryan Baker", "Christina Gonzalez", "Benjamin Nelson", "Megan Carter",
        "Alexander Mitchell", "Kelly Perez", "Jacob Roberts", "Brittany Turner", "William Phillips",
        "Danielle Campbell", "Andrew Parker", "Rebecca Evans", "Steven Edwards", "Lauren Collins"
    ]
    
    # Medical record numbers
    mrns = [f"MRN{str(i).zfill(6)}" for i in range(100001, 100001 + n_patients)]
    
    # Lab tests with critical values and normal ranges
    lab_tests = {
        'Glucose': {
            'unit': 'mg/dL',
            'normal_range': (70, 100),
            'critical_low': 40,
            'critical_high': 400,
            'panic_low': 30,
            'panic_high': 500
        },
        'Potassium': {
            'unit': 'mEq/L',
            'normal_range': (3.5, 5.0),
            'critical_low': 2.5,
            'critical_high': 6.0,
            'panic_low': 2.0,
            'panic_high': 6.5
        },
        'Sodium': {
            'unit': 'mEq/L',
            'normal_range': (136, 145),
            'critical_low': 120,
            'critical_high': 160,
            'panic_low': 115,
            'panic_high': 165
        },
        'Hemoglobin': {
            'unit': 'g/dL',
            'normal_range': (12.0, 16.0),
            'critical_low': 7.0,
            'critical_high': 20.0,
            'panic_low': 5.0,
            'panic_high': 22.0
        },
        'Platelet Count': {
            'unit': 'x10³/μL',
            'normal_range': (150, 450),
            'critical_low': 50,
            'critical_high': 1000,
            'panic_low': 20,
            'panic_high': 1200
        },
        'Creatinine': {
            'unit': 'mg/dL',
            'normal_range': (0.6, 1.2),
            'critical_low': 0.2,
            'critical_high': 5.0,
            'panic_low': 0.1,
            'panic_high': 8.0
        },
        'Troponin I': {
            'unit': 'ng/mL',
            'normal_range': (0.0, 0.04),
            'critical_low': None,
            'critical_high': 0.1,
            'panic_low': None,
            'panic_high': 1.0
        },
        'INR': {
            'unit': '',
            'normal_range': (0.8, 1.2),
            'critical_low': None,
            'critical_high': 5.0,
            'panic_low': None,
            'panic_high': 8.0
        }
    }
    
    # Generate lab results
    results = []
    current_time = datetime.now()
    
    for i in range(n_patients):
        # Patient info
        patient_name = random.choice(patient_names)
        mrn = mrns[i]
        age = random.randint(18, 95)
        gender = random.choice(['M', 'F'])
        
        # Generate multiple lab results per patient
        num_tests = random.randint(1, 5)
        
        for _ in range(num_tests):
            test_name = random.choice(list(lab_tests.keys()))
            test_info = lab_tests[test_name]
            
            # Generate realistic values with some critical/panic values
            prob = random.random()
            
            if prob < 0.02:  # 2% panic values
                if test_info['panic_low'] and test_info['panic_high']:
                    value = random.choice([
                        random.uniform(test_info['panic_low'], test_info['critical_low']),
                        random.uniform(test_info['critical_high'], test_info['panic_high'])
                    ])
                elif test_info['panic_high']:
                    value = random.uniform(test_info['critical_high'], test_info['panic_high'])
                else:
                    value = random.uniform(test_info['normal_range'][0], test_info['normal_range'][1])
                severity = 'PANIC'
            elif prob < 0.08:  # 6% critical values
                if test_info['critical_low'] and test_info['critical_high']:
                    value = random.choice([
                        random.uniform(test_info['critical_low'], test_info['normal_range'][0]),
                        random.uniform(test_info['normal_range'][1], test_info['critical_high'])
                    ])
                elif test_info['critical_high']:
                    value = random.uniform(test_info['normal_range'][1], test_info['critical_high'])
                else:
                    value = random.uniform(test_info['normal_range'][0], test_info['normal_range'][1])
                severity = 'CRITICAL'
            elif prob < 0.20:  # 12% abnormal values
                # Slightly outside normal range
                if random.choice([True, False]):
                    value = random.uniform(test_info['normal_range'][0] * 0.8, test_info['normal_range'][0])
                else:
                    value = random.uniform(test_info['normal_range'][1], test_info['normal_range'][1] * 1.2)
                severity = 'ABNORMAL'
            else:  # Normal values
                value = random.uniform(test_info['normal_range'][0], test_info['normal_range'][1])
                severity = 'NORMAL'
            
            # Round values appropriately
            if test_name in ['Glucose', 'Sodium']:
                value = round(value)
            elif test_name == 'Platelet Count':
                value = round(value)
            else:
                value = round(value, 2)
            
            # Create result entry
            result_time = current_time - timedelta(
                hours=random.randint(0, 72),
                minutes=random.randint(0, 59)
            )
            
            results.append({
                'Patient_Name': patient_name,
                'MRN': mrn,
                'Age': age,
                'Gender': gender,
                'Test_Name': test_name,
                'Result': value,
                'Unit': test_info['unit'],
                'Normal_Range': f"{test_info['normal_range'][0]}-{test_info['normal_range'][1]}",
                'Severity': severity,
                'Result_Time': result_time,
                'Department': random.choice(['Emergency', 'ICU', 'Medicine', 'Surgery', 'Cardiology', 'Oncology']),
                'Physician': random.choice(['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown', 'Dr. Davis']),
                'Acknowledged': random.choice([True, False]) if severity in ['CRITICAL', 'PANIC'] else True,
                'Alert_ID': f"ALT{random.randint(100000, 999999)}"
            })
    
    return pd.DataFrame(results)

@st.cache_data
def get_critical_alerts(df):
    """Get only critical and panic alerts"""
    return df[df['Severity'].isin(['CRITICAL', 'PANIC'])].sort_values('Result_Time', ascending=False)

# Generate data
df = generate_enhanced_lab_data(500)
critical_alerts = get_critical_alerts(df)

# Main title
st.title("🚨 Critical Values Alert System")
st.markdown("### Real-time Laboratory Critical Value Monitoring")

# Sidebar filters
st.sidebar.header("🔧 Filters")
selected_departments = st.sidebar.multiselect(
    "Departments",
    options=df['Department'].unique(),
    default=df['Department'].unique()
)

selected_severity = st.sidebar.multiselect(
    "Severity Levels",
    options=['NORMAL', 'ABNORMAL', 'CRITICAL', 'PANIC'],
    default=['CRITICAL', 'PANIC']
)

selected_tests = st.sidebar.multiselect(
    "Lab Tests",
    options=df['Test_Name'].unique(),
    default=df['Test_Name'].unique()
)

# Filter data
filtered_df = df[
    (df['Department'].isin(selected_departments)) &
    (df['Severity'].isin(selected_severity)) &
    (df['Test_Name'].isin(selected_tests))
]

filtered_critical = filtered_df[filtered_df['Severity'].isin(['CRITICAL', 'PANIC'])]

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        "🚨 Active Critical Alerts",
        len(filtered_critical[~filtered_critical['Acknowledged']]),
        delta=f"{len(filtered_critical)} Total"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    panic_alerts = len(filtered_critical[filtered_critical['Severity'] == 'PANIC'])
    st.metric("⚠️ Panic Values", panic_alerts)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    avg_response_time = random.randint(5, 15)  # Simulated
    st.metric("⏱️ Avg Response Time", f"{avg_response_time} min")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    acknowledgment_rate = len(filtered_critical[filtered_critical['Acknowledged']]) / len(filtered_critical) * 100 if len(filtered_critical) > 0 else 0
    st.metric("✅ Acknowledgment Rate", f"{acknowledgment_rate:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# Alert dashboard
st.header("🚨 Active Critical Alerts")

# Unacknowledged alerts first
unack_alerts = filtered_critical[~filtered_critical['Acknowledged']].head(10)

if len(unack_alerts) > 0:
    for idx, alert in unack_alerts.iterrows():
        severity_class = 'critical-alert' if alert['Severity'] == 'PANIC' else 'urgent-alert'
        
        st.markdown(f"""
        <div class="{severity_class}">
            <strong>🚨 {alert['Severity']} ALERT - {alert['Alert_ID']}</strong><br>
            <strong>Patient:</strong> {alert['Patient_Name']} (MRN: {alert['MRN']})<br>
            <strong>Test:</strong> {alert['Test_Name']} = <strong>{alert['Result']} {alert['Unit']}</strong> 
            (Normal: {alert['Normal_Range']})<br>
            <strong>Department:</strong> {alert['Department']} | <strong>Physician:</strong> {alert['Physician']}<br>
            <strong>Time:</strong> {alert['Result_Time'].strftime('%Y-%m-%d %H:%M')}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button(f"✅ Acknowledge", key=f"ack_{alert['Alert_ID']}"):
                st.success("Alert acknowledged!")
        with col2:
            if st.button(f"📞 Call Physician", key=f"call_{alert['Alert_ID']}"):
                st.info("Physician contacted!")
else:
    st.success("✅ No unacknowledged critical alerts!")

# Analytics section
st.header("📊 Analytics Dashboard")

# Create tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏥 Departments", "🧪 Tests", "📋 Reports"])

with tab1:
    # Trend analysis
    st.subheader("Critical Alerts Over Time")
    
    # Group by hour for trend
    critical_alerts['Hour'] = critical_alerts['Result_Time'].dt.floor('h')
    hourly_trends = critical_alerts.groupby(['Hour', 'Severity']).size().reset_index(name='Count')
    
    if len(hourly_trends) > 0:
        fig_trend = px.line(
            hourly_trends, 
            x='Hour', 
            y='Count', 
            color='Severity',
            title="Critical Alerts by Hour",
            color_discrete_map={'CRITICAL': 'orange', 'PANIC': 'red'}
        )
        st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    # Department analysis
    st.subheader("Critical Alerts by Department")
    
    dept_alerts = filtered_critical.groupby(['Department', 'Severity']).size().reset_index(name='Count')
    
    if len(dept_alerts) > 0:
        fig_dept = px.bar(
            dept_alerts, 
            x='Department', 
            y='Count', 
            color='Severity',
            title="Critical Alerts by Department",
            color_discrete_map={'CRITICAL': 'orange', 'PANIC': 'red'}
        )
        st.plotly_chart(fig_dept, use_container_width=True)

with tab3:
    # Test analysis
    st.subheader("Critical Alerts by Test Type")
    
    test_alerts = filtered_critical.groupby(['Test_Name', 'Severity']).size().reset_index(name='Count')
    
    if len(test_alerts) > 0:
        fig_test = px.bar(
            test_alerts, 
            x='Test_Name', 
            y='Count', 
            color='Severity',
            title="Critical Alerts by Test Type",
            color_discrete_map={'CRITICAL': 'orange', 'PANIC': 'red'}
        )
        fig_test.update_xaxes(tickangle=45)
        st.plotly_chart(fig_test, use_container_width=True)

with tab4:
    # Detailed reports
    st.subheader("Detailed Alert Report")
    
    # Summary statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Alert Summary**")
        summary_stats = filtered_critical['Severity'].value_counts()
        st.write(summary_stats)
    
    with col2:
        st.write("**Response Statistics**")
        response_stats = {
            'Total Alerts': len(filtered_critical),
            'Acknowledged': len(filtered_critical[filtered_critical['Acknowledged']]),
            'Pending': len(filtered_critical[~filtered_critical['Acknowledged']]),
            'Acknowledgment Rate': f"{acknowledgment_rate:.1f}%"
        }
        for key, value in response_stats.items():
            st.write(f"**{key}:** {value}")
    
    # Detailed data table
    st.subheader("Critical Alerts Data")
    display_cols = ['Alert_ID', 'Patient_Name', 'MRN', 'Test_Name', 'Result', 'Unit', 
                   'Severity', 'Department', 'Physician', 'Result_Time', 'Acknowledged']
    st.dataframe(filtered_critical[display_cols], use_container_width=True)
    
    # Export functionality
    if st.button("📥 Export Critical Alerts"):
        csv = filtered_critical.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"critical_alerts_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("**Critical Values Alert System** | Real-time laboratory safety monitoring")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")