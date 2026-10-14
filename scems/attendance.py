"""Attendance & Certificate Module (CI-06).

Marks attendance for registered students and generates certificates
only for students who actually attended.
"""
import os


class AttendanceManager:
    def __init__(self, registration_manager):
        self.reg = registration_manager
        self.attended = {}   # event_id -> set of student IDs

    def mark_attendance(self, student_id, event_id):
        registered = self.reg.registrations.get(event_id, [])
        if student_id not in registered:
            raise ValueError("Student is not registered for this event")
        self.attended.setdefault(event_id, set()).add(student_id)
        return True

    def has_attended(self, student_id, event_id):
        return student_id in self.attended.get(event_id, set())

    def generate_certificate(self, student_id, event_id, out_dir=None):
        if not self.has_attended(student_id, event_id):
            raise ValueError("Certificate not available: attendance not marked")

        event = self.reg.scheduler.get_event(event_id)
        text = (
            "CERTIFICATE OF PARTICIPATION\n"
            "----------------------------\n"
            f"This is to certify that {student_id}\n"
            f"participated in '{event.name}'\n"
            f"held on {event.date} at {event.venue}.\n"
        )
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, f"certificate_{student_id}_event{event_id}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
        return text
