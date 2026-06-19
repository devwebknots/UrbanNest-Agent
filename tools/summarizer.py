import anthropic
from config.settings import ANTHROPIC_API_KEY, MODEL_NAME

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def summarize_transcript(transcript: str) -> str:
    """
    Takes a raw tenant call transcript and returns
    a clean, professional summary.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""You are a property management assistant for UrbanNest.

A tenant left the following voicemail about a maintenance issue.
Write a short, professional 2-3 sentence summary of their complaint.
Be clear and factual. Do not add information that is not in the transcript.

Transcript:
{transcript}

Summary:"""
            }
        ]
    )

    return response.content[0].text.strip()