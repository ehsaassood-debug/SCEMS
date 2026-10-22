import pytest
from scems.scheduling import EventScheduler
from scems.registration import RegistrationManager
from scems.attendance import AttendanceManager


def setup_system():
    scheduler = EventScheduler()
    scheduler.create_event("Hackathon", "2026-10-20", "09:00", "12:00", "Hall A", 5)
    reg = RegistrationManager(scheduler)
    reg.register("23MIS0074", 1)
    return AttendanceManager(reg)


def test_mark_attendance_for_registered_student():
    att = setup_system()
    assert att.mark_attendance("23MIS0074", 1)
    assert att.has_attended("23MIS0074", 1)


def test_unregistered_student_cannot_attend():
    att = setup_system()
    with pytest.raises(ValueError, match="not registered"):
        att.mark_attendance("23MIS0099", 1)


def test_certificate_requires_attendance():
    att = setup_system()
    with pytest.raises(ValueError, match="attendance not marked"):
        att.generate_certificate("23MIS0074", 1)


def test_certificate_generated_after_attendance(tmp_path):
    att = setup_system()
    att.mark_attendance("23MIS0074", 1)
    text = att.generate_certificate("23MIS0074", 1, out_dir=str(tmp_path))
    assert "23MIS0074" in text and "Hackathon" in text
    assert (tmp_path / "certificate_23MIS0074_event1.txt").exists()
