import unittest
from task_08 import EventManager, EventManagerError


class TestTask08SearchEventByName(unittest.TestCase):

    def setUp(self):
        self.manager = EventManager()
        self.create = self.manager.create_event

    # Input–Output Test Cases

    def test_tc8_1_single_match(self):
        # TC8-1
        self.create("Tech Conference", "2026-04-10", 100)
        self.create("Music Festival", "2026-04-15", 200)
        self.create("Art Expo", "2026-05-01", 50)

        result = self.manager.search_event_by_name("Tech")
        names = [e.name for e in result]
        self.assertEqual(["Tech Conference"], names)

    def test_tc8_2_two_matches_case_insensitive(self):
        # TC8-2
        self.create("Tech Conference", "2026-04-10", 100)
        self.create("Tech Meetup", "2026-04-15", 100)

        result = self.manager.search_event_by_name("tech")
        names = [e.name for e in result]
        self.assertCountEqual(["Tech Conference", "Tech Meetup"], names)

    def test_tc8_3_suffix_match(self):
        # TC8-3
        self.create("Tech Conference", "2026-04-10", 100)
        self.create("Music Festival", "2026-04-15", 200)

        result = self.manager.search_event_by_name("Festival")
        names = [e.name for e in result]
        self.assertEqual(["Music Festival"], names)

    def test_tc8_4_no_match_returns_empty_list(self):
        # TC8-4
        self.create("Tech Conference", "2026-04-10", 100)
        self.create("Music Festival", "2026-04-15", 200)

        result = self.manager.search_event_by_name("Game")
        self.assertEqual([], result)

    def test_tc8_5_empty_events_list(self):
        # TC8-5
        result = self.manager.search_event_by_name("Tech")
        self.assertEqual([], result)

    # Edge Cases

    def test_ec8_1_single_letter_query(self):
        # EC8-1
        self.create("T", "2026-01-01", 10)
        self.create("Tech", "2026-02-01", 10)
        self.create("Big Tech Fair", "2026-03-01", 10)

        result = self.manager.search_event_by_name("T")
        names = [e.name for e in result]
        self.assertCountEqual(["T", "Tech", "Big Tech Fair"], names)

    def test_ec8_2_full_name_uppercase(self):
        # EC8-2
        self.create("Tech Conference", "2026-04-10", 100)

        result = self.manager.search_event_by_name("TECH CONFERENCE")
        names = [e.name for e in result]
        self.assertEqual(["Tech Conference"], names)

    def test_ec8_3_numeric_substring_match(self):
        # EC8-3
        self.create("Tech Conference 2026", "2026-04-10", 100)
        self.create("Tech Conference 2027", "2027-04-10", 100)

        result = self.manager.search_event_by_name("2026")
        names = [e.name for e in result]
        self.assertEqual(["Tech Conference 2026"], names)

    # Error Handling

    def test_eh8_1_empty_query_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.search_event_by_name("")

    def test_eh8_2_none_query_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.search_event_by_name(None)

    def test_eh8_3_non_string_query_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.search_event_by_name(123)


if __name__ == "__main__":
    unittest.main()
