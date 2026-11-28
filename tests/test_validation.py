import unittest
from io import StringIO

from backend.transactions import load_transactions
from backend.budget import generate_budget
from backend.engine import run_finwise


class TestTransactionValidation(unittest.TestCase):

    def test_valid_transaction(self):
        csv = StringIO(
            "date,description,amount\n2026-11-01,Food,-500"
        )
        df = load_transactions(csv)
        self.assertEqual(len(df), 1)
        self.assertEqual(df["amount"].iloc[0], -500)

    def test_missing_amount(self):
        with self.assertRaises(ValueError):
            load_transactions(StringIO(
                "date,description,amount\n2026-11-01,Food,"
            ))

    def test_missing_date(self):
        with self.assertRaises(ValueError):
            load_transactions(StringIO(
                "date,description,amount\n,Food,-500"
            ))

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            load_transactions(StringIO(
                "date,description,amount\n2026-11-01,Food,abc"
            ))

    def test_infinite_amount(self):
        with self.assertRaises(ValueError):
            load_transactions(StringIO(
                "date,description,amount\n2026-11-01,Food,inf"
            ))

    def test_blank_csv(self):
        with self.assertRaises(ValueError):
            load_transactions(StringIO(""))

    def test_empty_dataset(self):
        df = load_transactions(StringIO(
            "date,description,amount\n"
        ))
        self.assertTrue(df.empty)


class TestBudgetValidation(unittest.TestCase):

    def test_budget_calculation(self):
        result = generate_budget(15000, 8000)
        self.assertEqual(result["needs_budget"], 7500)
        self.assertEqual(result["wants_budget"], 4500)
        self.assertEqual(result["savings_goal"], 3000)
        self.assertEqual(result["remaining_balance"], 7000)

    def test_overspending(self):
        result = generate_budget(5000, 8000)
        self.assertEqual(result["remaining_balance"], -3000)
        self.assertEqual(result["budget_status"], "Over Budget")

    def test_invalid_income(self):
        for value in [0, -5000, None, "abc", True,
                      float("inf"), float("nan")]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    generate_budget(value, 2000)

    def test_invalid_spending(self):
        for value in [-500, None, "abc", True,
                      float("inf"), float("nan")]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    generate_budget(15000, value)

    def test_zero_spending(self):
        result = generate_budget(15000, 0)
        self.assertEqual(result["remaining_balance"], 15000)


class TestBackendIntegration(unittest.TestCase):

    def test_expense_analysis(self):
        csv = StringIO(
            "date,description,category,amount\n"
            "2026-11-28,Food,Food,-500\n"
            "2026-11-28,Uber,Transport,-300\n"
        )
        result = run_finwise(csv, 15000)
        self.assertEqual(result["analysis"]["total_spending"], 800)
        self.assertEqual(result["budget"]["remaining_balance"], 14200)


if __name__ == "__main__":
    unittest.main()
