import anthropic
import json
from config.settings import ANTHROPIC_API_KEY, MODEL_NAME

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def extract_fields(transcript: str) -> dict:
    """
    Takes a raw tenant call transcript and extracts
    structured fields needed for a maintenance ticket.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""You are a property management assistant for UrbanNest.

Extract the following fields from this tenant maintenance call transcript.
Respond ONLY with a JSON object. No explanation, no extra text.

Fields to extract:
- issue: what is broken or needs fixing
- unit: the unit number or apartment (if not mentioned, use "unknown")
- priority: one of [low, medium, high]
- category: one of [plumbing, electrical, hvac, general]

Transcript:
{transcript}

JSON:"""
            }
        ]
    )

    raw = response.content[0].text.strip()

    # Clean up in case Claude adds markdown formatting
    raw = raw.replace("```json", "").replace("```", "").strip()

    return json.loads(raw)