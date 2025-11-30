import streamlit as st

# Load custom CSS
def load_custom_css():
    with open('style/custom.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()

st.set_page_config(page_title="Shipment Dashboard", layout="wide")
st.title("ShipWise AI")

st.write("Navigate using the sidebar to upload shipment data, analyze delays, and chat with AI support.")


