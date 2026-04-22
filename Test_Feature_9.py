import unittest
from task_09 import EventManager, EventManagerError


class TestTask09ShowEventCapacity(unittest.TestCase):

    def setUp(self):
        self.manager = EventManager()
        self.create = self.manager.create_event
        self.register = self.manager.register_attendee

    # Input–Output Test Cases

    def test_tc9_1_zero_registered(self):
        # TC9-1
        event = self.create("Tech Conference", "2026-04-10", 100)

        info = self.manager.show_event_capacity(event.id)
        self.assertEqual(info["event_name"], "Tech Conference")
        self.assertEqual(info["capacity"], 100)
        self.assertEqual(info["registered"], 0)
        self.assertEqual(info["available_slots"], 100)

    def test_tc9_2_some_registered(self):
        # TC9-2
        event = self.create("Tech Conference", "2026-04-10", 100)
        self.register(event.id, "Alice", "alice@example.com")
        self.register(event.id, "Bob", "bob@example.com")
        self.register(event.id, "Charlie", "charlie@example.com")

        info = self.manager.show_event_capacity(event.id)
        self.assertEqual(info["capacity"], 100)
        self.assertEqual(info["registered"], 3)
        self.assertEqual(info["available_slots"], 97)

    def test_tc9_3_full_event(self):
        # TC9-3
        event = self.create("Music Festival", "2026-04-15", 2)
        self.register(event.id, "Alice", "alice@example.com")
        self.register(event.id, "Bob", "bob@example.com")

        info = self.manager.show_event_capacity(event.id)
        self.assertEqual(info["capacity"], 2)
        self.assertEqual(info["registered"], 2)
        self.assertEqual(info["available_slots"], 0)

    def test_tc9_4_full_event_visualization_present(self):
        # TC9-4
        event = self.create("Workshop", "2026-04-20", 1)
        self.register(event.id, "Alice", "alice@example.com")

        info = self.manager.show_event_capacity(event.id)
        # we just check that some visualization field exists
        self.assertIn("visual", info)
        self.assertIsInstance(info["visual"], str)

    # Edge Cases

    def test_ec9_1_minimum_capacity(self):
        # EC9-1
        event = self.create("Small Meetup", "2026-04-10", 1)

        info = self.manager.show_event_capacity(event.id)
        self.assertEqual(info["capacity"], 1)
        self.assertEqual(info["registered"], 0)
        self.assertEqual(info["available_slots"], 1)

    def test_ec9_2_large_capacity_numbers(self):
        # EC9-2
        event = self.create("Huge Expo", "2026-04-10", 1_000_000)
        for i in range(5):
            self.register(event.id, f"User{i}", f"user{i}@example.com")

        info = self.manager.show_event_capacity(event.id)
        self.assertEqual(info["capacity"], 1_000_000)
        self.assertEqual(info["registered"], 5)
        self.assertEqual(info["available_slots"], 999_995)

    def test_ec9_3_zero_registered_visualization(self):
        # EC9-3
        event = self.create("Zero Registered", "2026-04-10", 50)

        info = self.manager.show_event_capacity(event.id)
        self.assertEqual(info["capacity"], 50)
        self.assertEqual(info["registered"], 0)
        self.assertEqual(info["available_slots"], 50)
        self.assertIn("visual", info)

    # Error Handling

    def test_eh9_1_unknown_event_id_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.show_event_capacity(9999)

    def test_eh9_2_none_event_id_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.show_event_capacity(None)

    def test_eh9_3_negative_id_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.show_event_capacity(-1)


if __name__ == "__main__":
    unittest.main()
