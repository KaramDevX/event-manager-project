import pytest
from event_manager import EventManager, EventManagerError
@pytest.fixture
def manager():
    m = EventManager()
    m.create_event("Event 1", "2026-05-01", 3)
    m.create_event("Event 2", "2026-06-01", 2)
    return m


# -----------------------
# TC (Normal cases)
# -----------------------

def test_register_attendee_success_1(manager):
    attendee = manager.register_attendee(1, "Alice", "alice@example.com")
    assert attendee.name == "Alice"


def test_register_attendee_success_2(manager):
    attendee = manager.register_attendee(1, "Bob", "bob@example.com")
    assert attendee.email == "bob@example.com"


def test_register_attendee_success_3(manager):
    manager.register_attendee(1, "Alice", "alice@example.com")
    manager.register_attendee(1, "Bob", "bob@example.com")
    attendee = manager.register_attendee(1, "Charlie", "charlie@example.com")
    assert attendee.name == "Charlie"


def test_register_attendee_other_event(manager):
    attendee = manager.register_attendee(2, "David", "david@example.com")
    assert attendee.email == "david@example.com"


# -----------------------
# Edge Cases
# -----------------------

def test_name_and_email_normalization(manager):
    attendee = manager.register_attendee(1, "  Alice  ", "ALICE@EXAMPLE.COM")
    assert attendee.name == "Alice"
    assert attendee.email == "alice@example.com"


def test_minimal_name(manager):
    attendee = manager.register_attendee(1, "Z", "z@example.com")
    assert attendee.name == "Z"


def test_event_full(manager):
    manager.register_attendee(1, "A", "a@example.com")
    manager.register_attendee(1, "B", "b@example.com")
    manager.register_attendee(1, "C", "c@example.com")

    with pytest.raises(EventManagerError):
        manager.register_attendee(1, "D", "d@example.com")


def test_complex_email(manager):
    attendee = manager.register_attendee(1, "User", "user.name+test@example.co.uk")
    assert "@" in attendee.email


# -----------------------
# Error Handling
# -----------------------

def test_invalid_event_id(manager):
    with pytest.raises(EventManagerError):
        manager.register_attendee(999, "Alice", "alice@example.com")


def test_empty_name(manager):
    with pytest.raises(EventManagerError):
        manager.register_attendee(1, "   ", "test@example.com")


def test_invalid_email(manager):
    with pytest.raises(EventManagerError):
        manager.register_attendee(1, "Alice", "invalid-email")


def test_duplicate_registration(manager):
    manager.register_attendee(1, "Alice", "alice@example.com")

    with pytest.raises(EventManagerError):
        manager.register_attendee(1, "Alice2", "alice@example.com")


def test_none_name(manager):
    with pytest.raises(EventManagerError):
        manager.register_attendee(1, None, "test@example.com")


def test_none_email(manager):
    with pytest.raises(EventManagerError):
        manager.register_attendee(1, "Alice", None)

