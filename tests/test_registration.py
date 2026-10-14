import pytest
from scems.scheduling import EventScheduler
from scems.notification import Notifier
from scems.registration import RegistrationManager, validate_student_id


def setup_system(capacity=2):
    scheduler = EventScheduler()
    notifier = Notifier()
    scheduler.create_event("Hackathon", "2026-10-20", "09:00", "12:00", "Hall A", capacity)
    scheduler.create_event("Quiz", "2026-10-20", "10:00", "11:00", "Hall B", 10)
    return RegistrationManager(scheduler, notifier), notifier


def test_valid_student_id():
    assert validate_student_id("23MIS0074")


def test_invalid_student_id():
    assert not validate_student_id("ABC123")


def test_successful_registration_sends_notification():
    reg, notifier = setup_system()
    assert reg.register("23MIS0074", 1)
    assert len(notifier.messages_for("23MIS0074")) == 1


def test_duplicate_registration_blocked():
    reg, _ = setup_system()
    reg.register("23MIS0074", 1)
    with pytest.raises(ValueError, match="already registered"):
        reg.register("23MIS0074", 1)


def test_registration_blocked_when_no_seats():
    reg, _ = setup_system(capacity=1)
    reg.register("23MIS0074", 1)
    with pytest.raises(ValueError, match="No seats"):
        reg.register("23MIS0075", 1)


def test_time_clash_between_events_blocked():
    reg, _ = setup_system()
    reg.register("23MIS0074", 1)
    with pytest.raises(ValueError, match="Time clash"):
        reg.register("23MIS0074", 2)


def test_invalid_id_rejected():
    reg, _ = setup_system()
    with pytest.raises(ValueError, match="Invalid student ID"):
        reg.register("bad-id", 1)
