from turtle import pd
import unittest
from backend.engine import run_finwise


class TestFinWise(unittest.TestCase):

    def test_backend(self):
        result = run_finwise(
            "data/transactions.csv", 15000
        )

        analysis = result["analysis"]

        self.assertEqual(analysis["total_spending"], 15590)
        self.assertEqual(analysis["total_income"], 21500)
        self.assertEqual(analysis["net_balance"], 5910)
        self.assertEqual(analysis["total_transactions"], 40)
        self.assertEqual(analysis["expense_transactions"], 37)
        self.assertEqual(analysis["income_transactions"], 3)

        self.assertEqual(
            result["budget"]["total_spending"], 8106
        )

        self.assertEqual(
            result["budget"]["remaining_balance"], 6894
        )

        self.assertEqual(
            len(result["recurring_expenses"]), 14
        )

        self.assertEqual(
            len(result["anomalies"]), 2
        )

        for item in result["recurring_expenses"]:
            self.assertGreater(item["total_amount"], 0)

        for item in result["anomalies"]:
            self.assertGreater(item["amount"], 0)
    def test_category_preservation(self):
        import pandas as pd
        from backend.categorizer import categorize_transactions

        df = pd.read_csv("data/transactions.csv")
        result = categorize_transactions(df)

        self.assertTrue(
            df["category"].equals(result["category"])
        )


if __name__ == "__main__":
    unittest.main()
