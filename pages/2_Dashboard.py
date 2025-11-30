import streamlit as st
import pandas as pd
import os

st.title("Shipment Dashboard")

try:
    full_df = pd.read_csv("data/full_shipments.csv")
    delayed_df = pd.read_csv("data/delayed_shipments.csv")

    total_shipments = len(full_df)
    delayed_shipments = len(delayed_df)
    delay_percent = round((delayed_shipments / total_shipments) * 100, 2)

    st.metric("Total Shipments", total_shipments)
    st.metric("Delayed Shipments", delayed_shipments)
    st.metric("Delay Percentage", f"{delay_percent}%")

    # Optional: Delay analysis chart
    chart_df = pd.DataFrame({
        "Category": ["On Time", "Delayed"],
        "Count": [total_shipments - delayed_shipments, delayed_shipments]
    })
    st.bar_chart(chart_df.set_index("Category"))

except FileNotFoundError:
    st.warning("Please upload and detect shipments first (full and delayed datasets not found).")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
