from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional

DATE_FORMAT = "%Y-%m-%d"

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
    description: str = ""
    attendees: List[Attendee] = field(default_factory=list)

    def available_slots(self) -> int:
        return self.capacity - len(self.attendees)

    def occupancy_rate(self) -> float:
        return 0.0 if self.capacity == 0 else len(self.attendees) / self.capacity

class EventManager:
    def __init__(self, storage_path: str = "events_data.json"):
        self.storage_path = Path(storage_path)
        self.events: List[Event] = []
        self.reminder_days = 3

    def parse_date(self, value: str):
        try:
            return datetime.strptime(value, DATE_FORMAT).date()
        except ValueError as exc:
            raise EventManagerError("Invalid date format. Use YYYY-MM-DD.") from exc

    def validate_name(self, name: str):
        name = name.strip()
        if not name:
            raise EventManagerError("Event name cannot be empty.")
        return name

    def validate_capacity(self, capacity: int):
        if capacity <= 0:
            raise EventManagerError("Capacity must be greater than 0.")
        return capacity

    def validate_email(self, email: str):
        email = email.strip().lower()
        if "@" not in email or "." not in email:
            raise EventManagerError("Invalid email address.")
        return email

    def next_id(self):
        return max((event.id for event in self.events), default=0) + 1

    def find_event(self, event_id: int):
        for event in self.events:
            if event.id == event_id:
                return event
        raise EventManagerError(f"Event with ID {event_id} not found.")

    def create_event(self, name: str, event_date: str, capacity: int, description: str = ""):
        event = Event(self.next_id(), self.validate_name(name), self.parse_date(event_date).strftime(DATE_FORMAT), self.validate_capacity(capacity), description.strip())
        self.events.append(event)
        return event

    def delete_event(self, event_id: int):
        event = self.find_event(event_id)
        self.events.remove(event)
        return True

    def list_events(self):
        return sorted(self.events, key=lambda e: self.parse_date(e.date))

    def register_attendee(self, event_id: int, name: str, email: str):
        event = self.find_event(event_id)
        email = self.validate_email(email)
        if not name.strip():
            raise EventManagerError("Attendee name cannot be empty.")
        if any(att.email == email for att in event.attendees):
            raise EventManagerError("This attendee is already registered for the event.")
        if len(event.attendees) >= event.capacity:
            raise EventManagerError("Event is full.")
        attendee = Attendee(name=name.strip(), email=email)
        event.attendees.append(attendee)
        return attendee

    def cancel_registration(self, event_id: int, email: str):
        event = self.find_event(event_id)
        email = self.validate_email(email)
        for attendee in event.attendees:
            if attendee.email == email:
                event.attendees.remove(attendee)
                return True
        raise EventManagerError("Attendee registration not found.")

    def show_attendees(self, event_id: int):
        event = self.find_event(event_id)
        return {
            "event_name": event.name,
            "count": len(event.attendees),
            "capacity": event.capacity,
            "available_slots": event.available_slots(),
            "attendees": [att.name for att in sorted(event.attendees, key=lambda a: a.name.lower())],
        }

    def filter_events_by_date(self, start_date: str, end_date: str):
        start = self.parse_date(start_date)
        end = self.parse_date(end_date)
        if start > end:
            raise EventManagerError("Start date cannot be later than end date.")
        return sorted([event for event in self.events if start <= self.parse_date(event.date) <= end], key=lambda e: self.parse_date(e.date))

    def search_event_by_name(self, query: str):
        query = query.strip().lower()
        if not query:
            raise EventManagerError("Search query cannot be empty.")
        return sorted([event for event in self.events if query in event.name.lower()], key=lambda e: (e.name.lower().find(query), e.name.lower()))

    def capacity_bar(self, registered: int, capacity: int, width: int = 20):
        filled = round((registered / capacity) * width) if capacity else 0
        return "#" * filled + "-" * (width - filled)

    def show_event_capacity(self, event_id: int):
        event = self.find_event(event_id)
        percentage = round(event.occupancy_rate() * 100, 2)
        return {
            "event_name": event.name,
            "capacity": event.capacity,
            "registered": len(event.attendees),
            "available_slots": event.available_slots(),
            "percentage_full": percentage,
            "visual": self.capacity_bar(len(event.attendees), event.capacity),
        }

    def save_events(self, path: Optional[str] = None):
        save_path = Path(path) if path else self.storage_path
        payload = {
            "reminder_days": self.reminder_days,
            "events": [{**asdict(event), "attendees": [asdict(att) for att in event.attendees]} for event in self.events],
        }
        save_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return save_path

    def load_events(self, path: Optional[str] = None):
        load_path = Path(path) if path else self.storage_path
        data = json.loads(load_path.read_text(encoding="utf-8"))
        self.reminder_days = data.get("reminder_days", 3)
        self.events = []
        for item in data.get("events", []):
            attendees = [Attendee(**att) for att in item.get("attendees", [])]
            self.events.append(Event(item["id"], item["name"], item["date"], item["capacity"], item.get("description", ""), attendees))
        return self.events

    def attendance_statistics(self):
        total_events = len(self.events)
        total_attendees = sum(len(event.attendees) for event in self.events)
        average = round(total_attendees / total_events, 2) if total_events else 0.0
        popular = sorted(self.events, key=lambda e: len(e.attendees), reverse=True)
        return {
            "total_events": total_events,
            "total_attendees": total_attendees,
            "average_attendance": average,
            "popular_events": [(event.name, len(event.attendees)) for event in popular[:3]],
        }

    def set_reminder_days(self, days: int):
        self.reminder_days = days

    def simple_reminders(self, today: Optional[str] = None):
        current_day = self.parse_date(today) if today else date.today()
        reminders = []
        for event in self.list_events():
            days_left = (self.parse_date(event.date) - current_day).days
            if 0 <= days_left <= self.reminder_days:
                reminders.append(f"Reminder: {event.name} is on {event.date} ({days_left} day(s) left)")
        return reminders

manager = EventManager()
manager.create_event("Tech Conference", "2026-04-10", 100)
manager.create_event("Music Festival", "2026-04-15", 200)
manager.create_event("Art Expo", "2026-05-01", 50)
for event in manager.filter_events_by_date("2026-04-01", "2026-04-30"):
    print(event.name, event.date)
