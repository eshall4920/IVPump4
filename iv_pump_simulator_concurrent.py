
import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="IV Pump Simulator", layout="wide")

# Initialize session state for both pumps
for pump in ["A", "B"]:
    if f"infusing_{pump}" not in st.session_state:
        st.session_state[f"infusing_{pump}"] = False
    if f"progress_{pump}" not in st.session_state:
        st.session_state[f"progress_{pump}"] = 0
    if f"start_time_{pump}" not in st.session_state:
        st.session_state[f"start_time_{pump}"] = None

# Medication options
medications = ["IV Fluids", "Blood", "Heparin"]

# Infusion log
if "infusion_log" not in st.session_state:
    st.session_state.infusion_log = []

st.title("💉 IV Pump Simulator with Concurrent Infusion")

# Layout for Pump A and Pump B
col1, col2 = st.columns(2)

def pump_interface(pump_label, col):
    with col:
        st.header(f"Pump {pump_label}")
        medication = st.selectbox(f"Select Medication for Pump {pump_label}", medications, key=f"med_{pump_label}")
        volume = st.number_input(f"Volume to Infuse (mL) - Pump {pump_label}", min_value=1, max_value=1000, key=f"vol_{pump_label}")
        rate = st.number_input(f"Infusion Rate (mL/hr) - Pump {pump_label}", min_value=1, max_value=1000, key=f"rate_{pump_label}")

        if medication == "Heparin":
            st.warning("⚠️ Heparin is a high-alert medication. Double-check dosage and patient information.")

        start = st.button(f"Start Infusion - Pump {pump_label}", key=f"start_{pump_label}")
        stop = st.button(f"Stop Infusion - Pump {pump_label}", key=f"stop_{pump_label}")

        if start and not st.session_state[f"infusing_{pump_label}"]:
            st.session_state[f"infusing_{pump_label}"] = True
            st.session_state[f"start_time_{pump_label}"] = time.time()
            st.session_state[f"progress_{pump_label}"] = 0
            st.success(f"Infusion started on Pump {pump_label}")
            st.session_state.infusion_log.append({
                "pump": pump_label,
                "medication": medication,
                "volume": volume,
                "rate": rate,
                "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        if stop and st.session_state[f"infusing_{pump_label}"]:
            st.session_state[f"infusing_{pump_label}"] = False
            st.success(f"Infusion stopped on Pump {pump_label}")

        # Simulate infusion progress
        if st.session_state[f"infusing_{pump_label}"]:
            elapsed = (time.time() - st.session_state[f"start_time_{pump_label}"]) / 3600  # in hours
            infused = elapsed * rate
            progress = min(infused / volume, 1.0)
            st.session_state[f"progress_{pump_label}"] = progress
            st.progress(progress, text=f"Pump {pump_label} Infusing... {int(progress * 100)}%")

            if progress >= 1.0:
                st.session_state[f"infusing_{pump_label}"] = False
                st.error(f"🚨 Infusion complete on Pump {pump_label}!")

# Render both pump interfaces
pump_interface("A", col1)
pump_interface("B", col2)

# Display infusion log
st.subheader("📋 Infusion Log")
if st.session_state.infusion_log:
    st.table(st.session_state.infusion_log)
else:
    st.info("No infusions logged yet.")
