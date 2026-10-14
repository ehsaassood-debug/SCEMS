"""Registration Module (CI-03).

Validates students, checks seat availability, and blocks duplicate or
time-clashing registrations.
"""
import re
from scems.scheduling import times_overlap

STUDENT_ID_PATTERN = re.compile(r"^\d{2}[A-Z]{3}\d{4}$")   # e.g. 23MIS0074


def validate_student_id(student_id):
    """Return True if the ID looks like a valid VIT registration number."""
    return bool(STUDENT_ID_PATTERN.match(student_id))


class RegistrationManager:
    def __init__(self, scheduler, notifier=None):
        self.scheduler = scheduler
        self.notifier = notifier
        self.registrations = {}   # event_id -> list of student IDs

    def seats_left(self, event_id):
        event = self.scheduler.get_event(event_id)
        return event.capacity - len(self.registrations.get(event_id, []))

    def events_of(self, student_id):
        return [self.scheduler.get_event(eid)
                for eid, students in self.registrations.items()
                if student_id in students]

    def register(self, student_id, event_id):
        if not validate_student_id(student_id):
            raise ValueError("Invalid student ID format (expected e.g. 23MIS0074)")

        event = self.scheduler.get_event(event_id)
        students = self.registrations.setdefault(event_id, [])

        if student_id in students:
            raise ValueError("Student is already registered for this event")
        if self.seats_left(event_id) <= 0:
            raise ValueError("No seats available for this event")

        for other in self.events_of(student_id):
            if (other.date == event.date
                    and times_overlap(event.start, event.end, other.start, other.end)):
                raise ValueError(f"Time clash with '{other.name}'")

        students.append(student_id)
        if self.notifier:
            self.notifier.notify_registration(student_id, event)
        return True
