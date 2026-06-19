import json
from agents.modules.maintenance.intake_agent import run_intake_agent
from tools.transcription import transcribe_audio

print("=" * 50)
print("UrbanNest Maintenance Intake Agent")
print("=" * 50)
print()

# Option 2 — Fake transcript (text)
fake_transcript = """
Hi, this is Sarah from unit 204. I wanted to report a maintenance issue. 
My bathroom pipe has been leaking since this morning and water is dripping 
through the ceiling. The leak is getting worse and there is now a puddle 
forming on the floor. I am worried about water damage. 
Please send someone as soon as possible. Thank you.
"""

# Option 3 — Real audio file
print("Transcribing audio file...")
real_transcript = transcribe_audio("tests/audio/test_call.mp3")
print(f"Transcript: {real_transcript}")
print()

# Run the agent with real transcript
result = run_intake_agent(real_transcript)

print()
print("=" * 50)
print("RESULT")
print("=" * 50)
print(json.dumps(result, indent=2))