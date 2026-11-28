
from contextvars import ContextVar
from contextlib import contextmanager
from io import StringIO
from pathlib import Path

DEFAULT_DATA_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "transactions.csv"
)

_transaction_data = ContextVar(
    "transaction_data",
    default=None
)


@contextmanager
def transaction_context(transactions=None):

    if transactions is not None:
        csv_data = transactions.copy(deep=True).to_csv(
            index=False
        )
    else:
        csv_data = None

    token = _transaction_data.set(csv_data)

    try:
        yield
    finally:
        _transaction_data.reset(token)


def get_transaction_source():

    csv_data = _transaction_data.get()

    if csv_data is None:
        return str(DEFAULT_DATA_FILE)

    return StringIO(csv_data)
