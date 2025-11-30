import streamlit as st
import pandas as pd
from utils.detect_delays import detect_delays
import os

# Load custom CSS
def load_custom_css():
    with open('style/custom.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()

st.title("Upload Shipments to Detect Delays")

uploaded_file = st.file_uploader("Upload Shipment CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    # Save full dataset
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/full_shipments.csv', index=False)

    # Detect delays
    delayed_df = detect_delays(df)

    if delayed_df is not None and not delayed_df.empty:
        # Save delayed shipments as CSV
        delayed_df.to_csv('data/delayed_shipments.csv', index=False)

        st.success(f"{len(delayed_df)} delayed shipments detected!")

        st.info("Files saved as 'full_shipments.csv' and 'delayed_shipments.csv'. Please proceed to Dashboard or Chatbot.")
    else:
        st.info("No delayed shipments found.")
