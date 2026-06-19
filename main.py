import json
from agents.modules.maintenance.intake_agent import run_intake_agent

# Low priority test - garden not cleaned
transcript = """
Hi, this is Jennifer from unit 512. I just wanted to mention that 
the garden area outside my unit hasn't been cleaned up in a while. 
There are some dry leaves and it looks a bit untidy. No rush at all, 
just whenever someone gets a chance. Thank you.
"""

print("=" * 50)
print("UrbanNest Maintenance Intake Agent")
print("=" * 50)
print()

result = run_intake_agent(transcript)

print()
print("=" * 50)
print("RESULT")
print("=" * 50)
print(json.dumps(result, indent=2))