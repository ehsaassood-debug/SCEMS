import pytest
from scems.scheduling import EventScheduler


def make_scheduler():
    s = EventScheduler()
    s.create_event("Hackathon", "2026-10-20", "09:00", "12:00", "Hall A", 50)
    return s


def test_create_event_success():
    s = EventScheduler()
    event = s.create_event("Workshop", "2026-10-21", "10:00", "11:00", "Lab 1", 30)
    assert event.event_id == 1
    assert len(s.list_events()) == 1


def test_venue_clash_is_blocked():
    s = make_scheduler()
    with pytest.raises(ValueError, match="Clash"):
        s.create_event("Quiz", "2026-10-20", "11:00", "13:00", "Hall A", 20)


def test_same_time_different_venue_allowed():
    s = make_scheduler()
    event = s.create_event("Quiz", "2026-10-20", "09:00", "12:00", "Hall B", 20)
    assert event.event_id == 2


def test_back_to_back_events_allowed():
    s = make_scheduler()
    event = s.create_event("Quiz", "2026-10-20", "12:00", "13:00", "Hall A", 20)
    assert event.event_id == 2


def test_invalid_time_order():
    s = EventScheduler()
    with pytest.raises(ValueError):
        s.create_event("Bad", "2026-10-20", "12:00", "10:00", "Hall A", 20)


def test_invalid_capacity():
    s = EventScheduler()
    with pytest.raises(ValueError):
        s.create_event("Bad", "2026-10-20", "10:00", "12:00", "Hall A", 0)
