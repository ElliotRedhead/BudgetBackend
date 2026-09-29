"""Read and write expenses as CSV with columns date, name, category, cost (£)."""

import csv
import io
from decimal import Decimal, InvalidOperation

from expenses.serializers import ExpenseSerializer

CSV_COLUMNS = ["date", "name", "category", "cost"]
MAX_IMPORT_BYTES = 1024 * 1024


def write_expenses_csv(expenses, stream):
    """Write expenses to a text stream, with cost in pounds."""
    writer = csv.writer(stream)
    writer.writerow(CSV_COLUMNS)
    for expense in expenses:
        writer.writerow(
            [
                expense.date.date().isoformat(),
                expense.name,
                expense.category,
                f"{Decimal(expense.cost) / 100:.2f}",
            ]
        )


def _pounds_to_pence(value):
    """Convert "12.34" to 1234 exactly, or return None if it isn't money."""
    try:
        pounds = Decimal(value.strip().lstrip("£"))
    except InvalidOperation, AttributeError:
        return None
    pence = pounds * 100
    return int(pence) if pence == pence.to_integral_value() else None


def parse_expenses_csv(uploaded_file):
    """Validate every row, returning (serializers, errors keyed by row number)."""
    text = io.TextIOWrapper(uploaded_file, encoding="utf-8-sig")
    reader = csv.DictReader(text)
    missing_columns = set(CSV_COLUMNS) - set(reader.fieldnames or [])
    if missing_columns:
        return [], {1: {"columns": [f"Missing: {', '.join(sorted(missing_columns))}"]}}

    row_serializers, row_errors = [], {}
    # Row 1 is the header, so data starts on row 2.
    for row_number, row in enumerate(reader, start=2):
        pence = _pounds_to_pence(row["cost"])
        if pence is None:
            row_errors[row_number] = {"cost": ["Enter an amount like 12.34."]}
            continue
        row_serializer = ExpenseSerializer(
            data={
                "date": row["date"],
                "name": row["name"],
                "category": row["category"] or "other",
                "cost": pence,
            }
        )
        if row_serializer.is_valid():
            row_serializers.append(row_serializer)
        else:
            row_errors[row_number] = row_serializer.errors
    return row_serializers, row_errors
