import unittest
from event_manager import EventManager, EventManagerError


class TestEventManager(unittest.TestCase):

    def setUp(self):
        self.manager = EventManager()
        self.manager.create_event("Event 1", "2026-05-01", 3)
        self.manager.create_event("Event 2", "2026-06-01", 2)

    def test_register_attendee_success_1(self):
        """TC-01: Register attendee successfully"""
        attendee = self.manager.register_attendee(1, "Alice", "alice@example.com")
        self.assertEqual(attendee.name, "Alice")

    def test_register_attendee_success_2(self):
        """TC-02: Check attendee email"""
        attendee = self.manager.register_attendee(1, "Bob", "bob@example.com")
        self.assertEqual(attendee.email, "bob@example.com")

    def test_register_multiple_attendees(self):
        """TC-03: Register multiple attendees"""
        self.manager.register_attendee(1, "Alice", "alice@example.com")
        self.manager.register_attendee(1, "Bob", "bob@example.com")
        attendee = self.manager.register_attendee(1, "Charlie", "charlie@example.com")
        self.assertEqual(attendee.name, "Charlie")

    def test_register_attendee_other_event(self):
        """TC-04: Register attendee in another event"""
        attendee = self.manager.register_attendee(2, "David", "david@example.com")
        self.assertEqual(attendee.email, "david@example.com")

    def test_name_and_email_normalization(self):
        """TC-05: Name and email normalization"""
        attendee = self.manager.register_attendee(1, "  Alice  ", "ALICE@EXAMPLE.COM")
        self.assertEqual(attendee.name, "Alice")
        self.assertEqual(attendee.email, "alice@example.com")

    def test_minimal_name(self):
        """TC-06: Minimal valid name"""
        attendee = self.manager.register_attendee(1, "Z", "z@example.com")
        self.assertEqual(attendee.name, "Z")

    def test_event_full(self):
        """TC-07: Event full error"""
        self.manager.register_attendee(1, "A", "a@example.com")
        self.manager.register_attendee(1, "B", "b@example.com")
        self.manager.register_attendee(1, "C", "c@example.com")

        with self.assertRaises(EventManagerError):
            self.manager.register_attendee(1, "D", "d@example.com")

    def test_complex_email(self):
        """TC-08: Complex valid email"""
        attendee = self.manager.register_attendee(1, "User", "user.name+test@example.co.uk")
        self.assertIn("@", attendee.email)

    def test_invalid_event_id(self):
        """TC-09: Invalid event ID"""
        with self.assertRaises(EventManagerError):
            self.manager.register_attendee(999, "Alice", "alice@example.com")

    def test_empty_name(self):
        """TC-10: Empty name"""
        with self.assertRaises(EventManagerError):
            self.manager.register_attendee(1, "   ", "test@example.com")

    def test_invalid_email(self):
        """TC-11: Invalid email"""
        with self.assertRaises(EventManagerError):
            self.manager.register_attendee(1, "Alice", "invalid-email")

    def test_duplicate_registration(self):
        """TC-12: Duplicate registration"""
        self.manager.register_attendee(1, "Alice", "alice@example.com")

        with self.assertRaises(EventManagerError):
            self.manager.register_attendee(1, "Alice2", "alice@example.com")

    def test_none_name(self):
        """TC-13: Name is None"""
        with self.assertRaises(EventManagerError):
            self.manager.register_attendee(1, None, "test@example.com")

    def test_none_email(self):
        """TC-14: Email is None"""
        with self.assertRaises(EventManagerError):
            self.manager.register_attendee(1, "Alice", None)


if __name__ == "__main__":
    unittest.main()
