from scems.scheduling import EventScheduler
from scems.notification import Notifier


def test_registration_message_contains_event_details():
    scheduler = EventScheduler()
    event = scheduler.create_event("Hackathon", "2026-10-20", "09:00", "12:00", "Hall A", 5)
    notifier = Notifier()
    msg = notifier.notify_registration("23MIS0074", event)
    assert "Hackathon" in msg and "Hall A" in msg


def test_reminder_is_stored_in_outbox():
    scheduler = EventScheduler()
    event = scheduler.create_event("Quiz", "2026-10-21", "10:00", "11:00", "Lab 1", 5)
    notifier = Notifier()
    notifier.notify_reminder("23MIS0074", event)
    assert len(notifier.messages_for("23MIS0074")) == 1
    assert notifier.messages_for("23MIS9999") == []
