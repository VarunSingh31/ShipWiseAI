import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
print("API key is set:", os.getenv("ANTHROPIC_API_KEY") is not None)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_response_claude(user_query, source_name, destination_name, source_coords, destination_coords, source_weather, destination_weather):
    prompt = f"""
You are an AI-powered shipment assistant for a logistics company.

Current Shipment:
- Source: {source_name} ({source_coords})
- Destination: {destination_name} ({destination_coords})
- Weather at Source: {source_weather}
- Weather at Destination: {destination_weather}

Based on this context, respond to the following query:
"{user_query}"

Also suggest possible rerouting if shipment delay detected, considering weather and general routing conditions.

Respond like a professional logistics agent, human-like tone.
"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text
