"""Notification Module (CI-05).

Builds notification messages and stores them in an outbox.
(In a real deployment the outbox would be sent by email/SMS.)
"""


class Notifier:
    def __init__(self):
        self.outbox = []   # list of (student_id, message)

    def send(self, student_id, message):
        self.outbox.append((student_id, message))
        return message

    def notify_registration(self, student_id, event):
        msg = (f"Registration confirmed for '{event.name}' on {event.date} "
               f"at {event.start} in {event.venue}.")
        return self.send(student_id, msg)

    def notify_reminder(self, student_id, event):
        msg = (f"Reminder: '{event.name}' starts at {event.start} "
               f"on {event.date} in {event.venue}.")
        return self.send(student_id, msg)

    def messages_for(self, student_id):
        return [m for sid, m in self.outbox if sid == student_id]
