-- SCEMS Database Schema (CI-07)
-- Design script for planned persistence. The current CLI build keeps data
-- in memory; this schema defines the tables a future version would use.

CREATE TABLE events (
    event_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    event_date TEXT    NOT NULL,
    start_time TEXT    NOT NULL,
    end_time   TEXT    NOT NULL,
    venue      TEXT    NOT NULL,
    capacity   INTEGER NOT NULL CHECK (capacity > 0)
);

CREATE TABLE registrations (
    event_id   INTEGER NOT NULL REFERENCES events(event_id),
    student_id TEXT    NOT NULL,
    attended   INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (event_id, student_id)
);

CREATE TABLE notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id      TEXT NOT NULL,
    message         TEXT NOT NULL
);
