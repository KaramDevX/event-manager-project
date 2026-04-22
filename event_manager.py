from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional


class EventManagerError(Exception):
    pass


@dataclass
class Attendee:
    name: str
    email: str
    registered_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class Event:
    id: int
    name: str
    date: str
    capacity: int
    attendees: List[Attendee] = field(default_factory=list)

    def available_slots(self):
        return self.capacity - len(self.attendees)


class EventManager:
    def __init__(self):
        self.events: List[Event] = []

    # -----------------------
    # helpers
    # -----------------------
    def validate_email(self, email: str):
        if email is None:
            raise EventManagerError("Email cannot be None")
        email = email.strip().lower()
        if "@" not in email or "." not in email:
            raise EventManagerError("Invalid email")
        return email

    def find_event(self, event_id: int):
        for event in self.events:
            if event.id == event_id:
                return event
        raise EventManagerError("Event not found")

    # -----------------------
    # create event (needed for tests)
    # -----------------------
    def create_event(self, name: str, date: str, capacity: int):
        event_id = len(self.events) + 1
        event = Event(event_id, name, date, capacity)
        self.events.append(event)
        return event

    # -----------------------
    # FEATURE YOU ARE TESTING
    # -----------------------
    def register_attendee(self, event_id: int, name: str, email: str):
        event = self.find_event(event_id)

        if name is None or not name.strip():
            raise EventManagerError("Invalid name")

        email = self.validate_email(email)

        # duplicate check
        for a in event.attendees:
            if a.email == email:
                raise EventManagerError("Duplicate registration")

        # capacity check
        if len(event.attendees) >= event.capacity:
            raise EventManagerError("Event full")

        attendee = Attendee(name=name.strip(), email=email)
        event.attendees.append(attendee)
        return attendee