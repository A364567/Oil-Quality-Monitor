import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

API_URL = "http://127.0.0.1:5000/latest"

st.set_page_config(page_title="Oil Quality Dashboard", layout="wide")

st.markdown("""
<div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); padding:25px; border-radius:15px; color:white; text-align:center;">
    <h1>🛢️ OIL QUALITY MONITORING SYSTEM</h1>
    <p>Real-time Predictive Maintenance | AI-Powered</p>
</div>
""", unsafe_allow_html=True)

def generate_demo_data():
    dates = [datetime.now() - timedelta(hours=i) for i in range(72, 0, -1)]
    data = {
        'DateTime': dates,
        'Temperature (C)': np.random.normal(65, 3, 72).clip(60, 70),
        'Viscosity (cSt)': np.random.normal(45, 4, 72).clip(40, 50),
        'Turbidity': np.random.normal(15, 2, 72).clip(10, 20),
        'Oil_Humidity_percent': np.random.normal(25, 3, 72).clip(20, 30),
        'Quality_Score': np.random.normal(75, 8, 72).clip(60, 95)
    }
    df = pd.DataFrame(data)
    df['Condition'] = df['Quality_Score'].apply(lambda x: 
        "🟢 EXCELLENT" if x > 85 else 
        "🟡 GOOD" if x > 70 else 
        "🟠 FAIR" if x > 60 else 
        "🔴 POOR"
    )
    return df

if 'demo_data' not in st.session_state:
    st.session_state.demo_data = generate_demo_data()

st.subheader("📈 LIVE SENSOR READINGS")
metric_cols = st.columns(4)

current_temp = st.session_state.demo_data['Temperature (C)'].iloc[-1]
current_vis = st.session_state.demo_data['Viscosity (cSt)'].iloc[-1]
current_turb = st.session_state.demo_data['Turbidity'].iloc[-1]
current_hum = st.session_state.demo_data['Oil_Humidity_percent'].iloc[-1]

with metric_cols[0]:
    st.metric("🌡️ Temperature", f"{current_temp:.1f}°C", f"{np.random.choice([-1, 1])*0.5:.1f}°C")
with metric_cols[1]:
    st.metric("🛢️ Viscosity", f"{current_vis:.1f} cSt", f"{np.random.choice([-1, 1])*0.3:.1f} cSt")
with metric_cols[2]:
    st.metric("🌀 Turbidity", f"{current_turb:.1f} NTU", f"{np.random.choice([-1, 1])*0.2:.1f} NTU")
with metric_cols[3]:
    st.metric("💧 Humidity", f"{current_hum:.1f}%", f"{np.random.choice([-1, 1])*0.4:.1f}%")

current_quality = st.session_state.demo_data['Quality_Score'].iloc[-1]
current_condition = st.session_state.demo_data['Condition'].iloc[-1]

status_col1, status_col2 = st.columns([1, 2])
with status_col1:
    st.subheader("🔍 OIL QUALITY STATUS")
    if "EXCELLENT" in current_condition:
        st.success(f"## {current_condition}")
    elif "GOOD" in current_condition:
        st.info(f"## {current_condition}")
    elif "FAIR" in current_condition:
        st.warning(f"## {current_condition}")
    else:
        st.error(f"## {current_condition}")
    
    st.progress(current_quality/100)
    st.metric("Quality Score", f"{current_quality:.1f}/100")

with status_col2:
    st.subheader("📊 TREND ANALYSIS")
    chart_data = st.session_state.demo_data.set_index('DateTime')[['Temperature (C)', 'Viscosity (cSt)', 'Turbidity', 'Oil_Humidity_percent']].tail(24)
    st.line_chart(chart_data, height=300)

st.subheader("📊 SENSOR DETAILS")
tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Temperature", "🛢️ Viscosity", "🌀 Turbidity", "💧 Humidity"])

with tab1:
    st.line_chart(st.session_state.demo_data.set_index('DateTime')['Temperature (C)'].tail(24), height=250)
with tab2:
    st.line_chart(st.session_state.demo_data.set_index('DateTime')['Viscosity (cSt)'].tail(24), height=250)
with tab3:
    st.line_chart(st.session_state.demo_data.set_index('DateTime')['Turbidity'].tail(24), height=250)
with tab4:
    st.line_chart(st.session_state.demo_data.set_index('DateTime')['Oil_Humidity_percent'].tail(24), height=250)

def update_demo():
    new_dt = datetime.now()
    new_row = {
        'DateTime': new_dt,
        'Temperature (C)': np.random.normal(65, 3),
        'Viscosity (cSt)': np.random.normal(45, 4),
        'Turbidity': np.random.normal(15, 2),
        'Oil_Humidity_percent': np.random.normal(25, 3),
        'Quality_Score': np.random.normal(75, 8)
    }
    new_row['Quality_Score'] = max(60, min(95, new_row['Quality_Score']))
    new_row['Condition'] = "🟢 EXCELLENT" if new_row['Quality_Score'] > 85 else "🟡 GOOD" if new_row['Quality_Score'] > 70 else "🟠 FAIR" if new_row['Quality_Score'] > 60 else "🔴 POOR"
    
    st.session_state.demo_data = pd.concat([
        st.session_state.demo_data.iloc[1:],
        pd.DataFrame([new_row])
    ], ignore_index=True)

if st.button("🔄 Simulate Live Update"):
    update_demo()
    st.rerun()

time.sleep(3)
update_demo()
st.rerun()