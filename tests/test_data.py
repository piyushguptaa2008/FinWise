import csv
from pathlib import Path

file_path = Path(__file__).resolve().parents[1] / "data" / "transactions.csv"

income = 0
expenses = 0
transactions = 0
categories = {}

with open(file_path, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        amount = float(row["amount"])
        category = row["category"]
        transactions += 1

        if amount > 0:
            income += amount
        else:
            expenses += abs(amount)
            categories[category] = categories.get(category, 0) + abs(amount)

balance = income - expenses

print("FinWise - Data Testing")
print("-------------------------")
print("Total Transactions:", transactions)
print("Total Income: Rs.", income)
print("Total Expenses: Rs.", expenses)
print("Remaining Balance: Rs.", balance)

print("\nCategory-wise Expenses:")

for category, amount in categories.items():
    print(category, ":", amount)

print("\nData loaded successfully!")