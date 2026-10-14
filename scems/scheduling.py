"""Event Scheduling Module (CI-04).

Creates events and prevents two events from clashing at the same venue.
"""
import re
from dataclasses import dataclass


TIME_PATTERN = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


@dataclass
class Event:
    event_id: int
    name: str
    date: str      # YYYY-MM-DD
    start: str     # HH:MM (24-hour)
    end: str       # HH:MM (24-hour)
    venue: str
    capacity: int


def times_overlap(start1, end1, start2, end2):
    """True if two time ranges (HH:MM strings) overlap."""
    return start1 < end2 and start2 < end1


class EventScheduler:
    def __init__(self):
        self.events = {}
        self._next_id = 1

    def create_event(self, name, date, start, end, venue, capacity):
        if not name.strip():
            raise ValueError("Event name cannot be empty")
        if not (TIME_PATTERN.match(start) and TIME_PATTERN.match(end)):
            raise ValueError("Time must be in HH:MM format")
        if start >= end:
            raise ValueError("Start time must be before end time")
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero")

        for existing in self.events.values():
            if (existing.venue == venue and existing.date == date
                    and times_overlap(start, end, existing.start, existing.end)):
                raise ValueError(
                    f"Clash: '{existing.name}' already uses {venue} at that time"
                )

        event = Event(self._next_id, name, date, start, end, venue, capacity)
        self.events[event.event_id] = event
        self._next_id += 1
        return event

    def get_event(self, event_id):
        if event_id not in self.events:
            raise ValueError(f"Event {event_id} not found")
        return self.events[event_id]

    def list_events(self):
        return list(self.events.values())
