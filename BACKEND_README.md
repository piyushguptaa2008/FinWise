# FinWise — Backend Documentation

**Developer:** Niraj Manoj Chauhan

## Implemented Features

- CSV transaction processing
- Automatic expense categorization
- Category-wise spending analysis
- Monthly recurring expense detection
- Unusual spending detection
- 50/30/20 budget calculation
- Integrated backend engine
- Automated integration test

## Installation

```bash
pip install -r requirements.txt
```

## Backend Integration

```python
from backend.engine import run_finwise

result = run_finwise("data/transactions.csv", 15000)
```

## Output Keys

- `transactions`
- `analysis`
- `recurring_expenses`
- `anomalies`
- `budget`

## Testing

```bash
python -m unittest discover -s tests -v
```

## Test Results

- Transactions processed: 12
- Total expenses: ₹12,586
- Recurring payments detected: 2
- Unusual expenses detected: 1
- Automated tests: 1/1 passed

## Current Limitations

- Supports positive expense amounts.
- Requires date, description and amount columns.
- Uses keyword-based categorization.
- Budget calculations use the latest transaction month.
- AI and frontend integration are pending.
- Further real-world data testing is required.