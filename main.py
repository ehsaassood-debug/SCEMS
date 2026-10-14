"""SCEMS command-line interface."""
from scems.scheduling import EventScheduler
from scems.notification import Notifier
from scems.registration import RegistrationManager
from scems.attendance import AttendanceManager

MENU = """
===== Smart Campus Event Management System =====
1. Create event
2. List events
3. Register student for event
4. Mark attendance
5. Generate certificate
6. View notifications for a student
0. Exit
"""


def main():
    scheduler = EventScheduler()
    notifier = Notifier()
    registration = RegistrationManager(scheduler, notifier)
    attendance = AttendanceManager(registration)

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                name = input("Event name: ")
                date = input("Date (YYYY-MM-DD): ")
                start = input("Start time (HH:MM): ")
                end = input("End time (HH:MM): ")
                venue = input("Venue: ")
                capacity = int(input("Capacity: "))
                event = scheduler.create_event(name, date, start, end, venue, capacity)
                print(f"Event created with ID {event.event_id}")

            elif choice == "2":
                for e in scheduler.list_events():
                    print(f"[{e.event_id}] {e.name} | {e.date} {e.start}-{e.end} | "
                          f"{e.venue} | seats left: {registration.seats_left(e.event_id)}")
                if not scheduler.list_events():
                    print("No events yet.")

            elif choice == "3":
                sid = input("Student ID (e.g. 23MIS0074): ").strip().upper()
                eid = int(input("Event ID: "))
                registration.register(sid, eid)
                print("Registration successful.")

            elif choice == "4":
                sid = input("Student ID: ").strip().upper()
                eid = int(input("Event ID: "))
                attendance.mark_attendance(sid, eid)
                print("Attendance marked.")

            elif choice == "5":
                sid = input("Student ID: ").strip().upper()
                eid = int(input("Event ID: "))
                print(attendance.generate_certificate(sid, eid, out_dir="certificates"))

            elif choice == "6":
                sid = input("Student ID: ").strip().upper()
                for m in notifier.messages_for(sid) or ["No notifications."]:
                    print("-", m)

            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    main()
