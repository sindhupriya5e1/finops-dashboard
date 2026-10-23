import unittest

from alerts import classify_cost, WARNING_LIMIT, AT_RISK_LIMIT


class CostAlertTests(unittest.TestCase):
    def test_safe_below_warning_threshold(self):
        self.assertEqual(classify_cost(WARNING_LIMIT - 0.001), "SAFE")

    def test_warning_at_lower_threshold(self):
        self.assertEqual(classify_cost(WARNING_LIMIT), "WARNING")

    def test_warning_at_upper_threshold(self):
        self.assertEqual(classify_cost(AT_RISK_LIMIT), "WARNING")

    def test_at_risk_above_upper_threshold(self):
        self.assertEqual(classify_cost(AT_RISK_LIMIT + 0.001), "AT-RISK")


if __name__ == "__main__":
    unittest.main()
