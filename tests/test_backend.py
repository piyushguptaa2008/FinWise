import unittest
from backend.engine import run_finwise


class TestFinWise(unittest.TestCase):

    def test_backend(self):
        result = run_finwise(
            "data/transactions.csv", 15000
        )

        self.assertEqual(
            result["analysis"]["total_spending"], 12586
        )

        self.assertEqual(
            result["analysis"]["total_transactions"], 12
        )

        self.assertEqual(
            len(result["recurring_expenses"]), 2
        )

        self.assertEqual(
            len(result["anomalies"]), 1
        )

        self.assertEqual(
            result["budget"]["remaining_balance"], 3162
        )


if __name__ == "__main__":
    unittest.main()