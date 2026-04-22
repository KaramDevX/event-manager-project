import unittest
from datetime import datetime
from task_07 import EventManager, EventManagerError


class TestTask07FilterEventsByDate(unittest.TestCase):

    def setUp(self):
        self.manager = EventManager()
        # helper for readability
        self.create = self.manager.create_event

    # Input–Output Test Cases

    def test_tc7_1_events_inside_april_range(self):
        # TC7-1
        e1 = self.create("E1", "2026-04-10", 10)
        e2 = self.create("E2", "2026-04-15", 10)
        e3 = self.create("E3", "2026-05-01", 10)

        result = self.manager.filter_events_by_date("2026-04-01", "2026-04-30")
        self.assertEqual([e1, e2], result)

    def test_tc7_2_exact_single_day_range(self):
        # TC7-2
        e1 = self.create("E1", "2026-04-10", 10)
        self.create("E2", "2026-04-15", 10)
        self.create("E3", "2026-05-01", 10)

        result = self.manager.filter_events_by_date("2026-04-10", "2026-04-10")
        self.assertEqual([e1], result)

    def test_tc7_3_full_cover_range(self):
        # TC7-3
        e1 = self.create("E1", "2026-04-10", 10)
        e2 = self.create("E2", "2026-04-15", 10)

        result = self.manager.filter_events_by_date("2026-03-01", "2026-05-31")
        self.assertEqual([e1, e2], result)

    def test_tc7_4_no_events_in_range(self):
        # TC7-4
        self.create("E1", "2026-04-10", 10)
        self.create("E2", "2026-04-15", 10)

        result = self.manager.filter_events_by_date("2026-06-01", "2026-06-30")
        self.assertEqual([], result)

    def test_tc7_5_middle_event_only(self):
        # TC7-5
        self.create("E1", "2026-04-10", 10)
        e2 = self.create("E2", "2026-04-15", 10)
        self.create("E3", "2026-04-20", 10)

        result = self.manager.filter_events_by_date("2026-04-11", "2026-04-19")
        self.assertEqual([e2], result)

    def test_tc7_6_two_events_same_date(self):
        # TC7-6
        e1 = self.create("E1", "2026-04-10", 10)
        e2 = self.create("E2", "2026-04-10", 10)

        result = self.manager.filter_events_by_date("2026-04-10", "2026-04-10")
        # depending on your sort, either [e1, e2] or [e2, e1] is OK;
        # here we just check both are present
        self.assertCountEqual([e1, e2], result)

    def test_tc7_7_empty_events_list(self):
        # TC7-7
        result = self.manager.filter_events_by_date("2026-04-01", "2026-04-30")
        self.assertEqual([], result)

    # Edge Cases
    def test_ec7_1_very_wide_range(self):
        # EC7-1
        e1 = self.create("E1", "2020-01-01", 10)
        e2 = self.create("E2", "2026-04-10", 10)
        e3 = self.create("E3", "2030-12-31", 10)

        result = self.manager.filter_events_by_date("1900-01-01", "2100-12-31")
        self.assertEqual([e1, e2, e3], result)

    def test_ec7_2_single_day_range_without_match(self):
        # EC7-2
        self.create("E1", "2026-04-11", 10)

        result = self.manager.filter_events_by_date("2026-04-10", "2026-04-10")
        self.assertEqual([], result)

    def test_ec7_3_both_boundaries_included(self):
        # EC7-3
        e1 = self.create("E1", "2026-04-01", 10)
        e2 = self.create("E2", "2026-04-30", 10)

        result = self.manager.filter_events_by_date("2026-04-01", "2026-04-30")
        self.assertEqual([e1, e2], result)

    # Error Handling

    def test_eh7_1_start_after_end_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.filter_events_by_date("2026-05-10", "2026-04-01")

    def test_eh7_2_invalid_start_format_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.filter_events_by_date("10-04-2026", "2026-04-30")

    def test_eh7_3_invalid_end_format_raises(self):
        with self.assertRaises(EventManagerError):
            # start ok, end bad
            self.manager.filter_events_by_date("2026-04-01", "30-04-2026")

    def test_eh7_4_empty_start_date_raises(self):
        with self.assertRaises(EventManagerError):
            self.manager.filter_events_by_date("", "2026-04-30")


if __name__ == "__main__":
    unittest.main()
