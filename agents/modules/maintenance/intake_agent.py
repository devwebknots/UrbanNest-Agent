from agents.modules.maintenance.state import MaintenanceState
from tools.summarizer import summarize_transcript
from tools.extraction import extract_fields

def run_intake_agent(transcript: str) -> MaintenanceState:
    """
    Main agent that processes a tenant maintenance call.
    Takes a transcript and returns a fully filled state.
    """

    # Start with a blank state
    state: MaintenanceState = {
        "transcript": transcript,
        "summary": None,
        "issue": None,
        "unit": None,
        "priority": None,
        "category": None,
        "should_create_ticket": None,
        "error": None
    }

    try:
        # Step 1 — Summarize the transcript
        print("Step 1: Summarizing transcript...")
        state["summary"] = summarize_transcript(transcript)

        # Step 2 — Extract structured fields
        print("Step 2: Extracting fields...")
        extracted = extract_fields(transcript)
        state["issue"] = extracted.get("issue")
        state["unit"] = extracted.get("unit")
        state["priority"] = extracted.get("priority")
        state["category"] = extracted.get("category")

        # Step 3 — Decide whether to create a ticket
        print("Step 3: Making ticket decision...")
        state["should_create_ticket"] = bool(state["issue"])

    except Exception as e:
        state["error"] = str(e)
        state["should_create_ticket"] = False

    return state