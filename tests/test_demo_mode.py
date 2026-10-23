import unittest
from datetime import date, timedelta

from fetch_cost import DEMO_SERVICES, load_demo_costs


class DemoModeTests(unittest.TestCase):
    def test_demo_generates_seven_days_of_service_costs(self):
        end_date = date(2026, 10, 23)
        records = load_demo_costs(end_date)
        self.assertEqual(len(records), 7 * len(DEMO_SERVICES))
        self.assertEqual(len({(day, service) for day, service, _ in records}), len(records))

    def test_demo_uses_only_completed_days(self):
        end_date = date(2026, 10, 23)
        records = load_demo_costs(end_date)
        dates = {day for day, _, _ in records}
        self.assertNotIn(end_date.isoformat(), dates)
        self.assertEqual(min(dates), (end_date - timedelta(days=7)).isoformat())
        self.assertEqual(max(dates), (end_date - timedelta(days=1)).isoformat())

    def test_demo_costs_are_non_negative(self):
        self.assertTrue(all(amount >= 0 for _, _, amount in load_demo_costs()))


if __name__ == "__main__":
    unittest.main()
