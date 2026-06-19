from typing import TypedDict, Optional

class MaintenanceState(TypedDict):
    # Input
    transcript: str          # the raw text of the tenant call

    # Processed outputs
    summary: Optional[str]           # clean professional summary
    issue: Optional[str]             # what is broken
    unit: Optional[str]              # which unit/apartment
    priority: Optional[str]          # low / medium / high
    category: Optional[str]          # plumbing / electrical / hvac / general

    # Decision
    should_create_ticket: Optional[bool]  # yes or no

    # Error handling
    error: Optional[str]             # if something goes wrong