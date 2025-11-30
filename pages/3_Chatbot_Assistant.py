import streamlit as st
import pandas as pd
from Chatbot_utils.response_generator import generate_response_claude
from utils.geocode_utils import get_coordinates
from utils.weather_utils import get_weather
from utils.email_utils import send_plaintext_email


def load_custom_css():
    with open('style/custom.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()


st.title("Shipment AI Chatbot Assistant")


try:
    delayed_df = pd.read_csv("data/delayed_shipments.csv")

    delayed_df.columns = [col.strip().lower().replace(" ", "_") for col in delayed_df.columns]

    shipment_id_col = next((col for col in delayed_df.columns if "shipment_id" in col or "order_id" in col), None)

    if not shipment_id_col:
        st.error("Could not find Shipment ID column in delayed shipments file.")
        st.stop()

    shipment_ids = delayed_df[shipment_id_col].astype(str).tolist()
    selected_shipment_id = st.selectbox("Select Delayed Shipment ID:", shipment_ids)

except FileNotFoundError:
    st.warning("Please detect delayed shipments first.")
    st.stop()
except Exception as e:
    st.error(f"Error loading delayed shipments: {e}")
    st.stop()

# Initialize chat history per shipment
if 'chat_histories' not in st.session_state:
    st.session_state.chat_histories = {}

if selected_shipment_id not in st.session_state.chat_histories:
    st.session_state.chat_histories[selected_shipment_id] = []

chat_history = st.session_state.chat_histories[selected_shipment_id]

# Display conversation so far
st.subheader(f"Conversation for Shipment {selected_shipment_id}")
for message in chat_history:
    st.write(message)

# Source and Destination Inputs
source_city = st.text_input("Enter Source City")
destination_city = st.text_input("Enter Destination City")

# Fetch Weather
if st.button("Fetch Weather & Route Info"):
    if source_city and destination_city:
        source_lat, source_lon = get_coordinates(source_city)
        dest_lat, dest_lon = get_coordinates(destination_city)

        if None in [source_lat, source_lon]:
            st.error(f"Unable to fetch coordinates for **Source City: {source_city}**.")
            st.stop()

        if None in [dest_lat, dest_lon]:
            st.error(f"Unable to fetch coordinates for **Destination City: {destination_city}**.")
            st.stop()

        source_weather_data = get_weather(source_lat, source_lon)
        dest_weather_data = get_weather(dest_lat, dest_lon)

        source_weather = source_weather_data['weather'][0]['description'].capitalize() if source_weather_data else "Unavailable"
        destination_weather = dest_weather_data['weather'][0]['description'].capitalize() if dest_weather_data else "Unavailable"

        st.subheader("Current Weather")
        st.write(f"**{source_city}:** {source_weather}")
        st.write(f"**{destination_city}:** {destination_weather}")

        st.session_state.source_coords = (source_lat, source_lon)
        st.session_state.dest_coords = (dest_lat, dest_lon)
        st.session_state.source_weather = source_weather
        st.session_state.dest_weather = destination_weather

    else:
        st.warning("Please enter both source and destination cities.")


user_query = st.text_input("Ask your shipment-related query:")
if st.button("Ask Bot"):
    if user_query and 'source_coords' in st.session_state:
        source_coords = f"{st.session_state.source_coords[0]}, {st.session_state.source_coords[1]}"
        dest_coords = f"{st.session_state.dest_coords[0]}, {st.session_state.dest_coords[1]}"

        # Prepare full prompt as combined chat history + user query
        history_text = "\n".join(chat_history)
        full_prompt = history_text + f"\nUser: {user_query}"

        # Call Claude using combined history + user query
        response = generate_response_claude(
            full_prompt,
            source_name=source_city,
            destination_name=destination_city,
            source_coords=source_coords,
            destination_coords=dest_coords,
            source_weather=st.session_state.source_weather,
            destination_weather=st.session_state.dest_weather
        )

        chat_history.append(f"User: {user_query}")
        chat_history.append(f"Bot: {response}")

        # Display updated conversation
        st.subheader(f"Conversation for Shipment {selected_shipment_id}")
        for message in chat_history:
            st.write(message)

    else:
        st.warning("Please fetch route & weather information first.")

# Email Summary & Escalation
st.subheader("Email or Escalate Conversation")

user_email = st.text_input("Enter your email to receive chat summary:")

if st.button("Email Me This Chat Summary"):
    chat_summary = "\n".join(chat_history)
    if user_email:
        send_plaintext_email(
            subject=f"Your Shipment {selected_shipment_id} Assistance Chat Summary",
            body=chat_summary,
            recipient_email=user_email
        )
        st.success("Chat summary emailed successfully as plain text.")
    else:
        st.warning("Please enter your email.")

if st.button(" Escalate Issue to Operations Team"):
    chat_summary = "\n".join(chat_history)
    subject = f" Escalation Alert: Shipment {selected_shipment_id} Issue"
    body = (
        f"User Email: {user_email or 'Not Provided'}\n\n"
        f"--- Chat Summary ---\n\n"
        f"{chat_summary}"
    )
    send_plaintext_email(subject, body, "varunsingh3125@gmail.com")
    st.success("Issue escalated to the operations team as plain text email.")
