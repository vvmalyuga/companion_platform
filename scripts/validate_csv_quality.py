from pathlib import Path
import csv
import re


def rows(name):
    with (Path("data/csv") / name).open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

bookings = rows("bookings.csv")
companions = rows("companions.csv")
users = rows("users.csv")
booking_ids = [row["booking_id"] for row in bookings]
assert len(booking_ids) == len(set(booking_ids))
assert all(1 <= int(row["rating"]) <= 5 for row in bookings)
assert all(row["booking_date"] for row in bookings)
assert all(18 <= int(row["age"]) <= 100 for row in companions)
assert all(float(row["price_per_hour"]) > 0 for row in companions)
assert all(re.match(r"^[^@]+@[^@]+\.[^@]+$", row["email"]) for row in users)
assert all(row["role"] in ["customer", "companion"] for row in users)
print("CSV quality checks passed")
