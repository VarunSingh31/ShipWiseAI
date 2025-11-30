import streamlit as st
import pandas as pd
import os

# Load custom CSS
def load_custom_css():
    with open('style/custom.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()


st.title("Email History Dashboard")

history_file = "email_history_log.csv"

if os.path.exists(history_file):
    df = pd.read_csv(history_file, names=["Date & Time", "Recipient Email", "Subject"])
    st.dataframe(df.sort_values("Date & Time", ascending=False), use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Email History CSV", data=csv, file_name="email_history.csv")

else:
    st.info("No email history found yet.")

