"""Synthetic neobank transaction-event producer.

Emits mock webhook payloads to a JSONL file. All data is randomly generated;
there is no real, customer, or employer data here.

The `--break` flag simulates an upstream team shipping a breaking change
(dropping the required `currency` field). Running `datacontract test` after
producing with `--break` will FAIL — which is the demonstration.

Usage:
    python src/producer.py --count 1000 --out data/transactions.jsonl
    python src/producer.py --count 1000 --out data/transactions.jsonl --break
"""

from __future__ import annotations

import argparse
import json
import os
import random
import uuid
from datetime import datetime, timedelta, timezone

CURRENCIES = ["AUD", "USD", "NZD", "GBP", "EUR"]
MERCHANTS = [
    "Corner Cafe", "Transit Authority", "Online Grocer", "Streaming Co",
    "Utility Provider", "Bookshop", "Rideshare", "Hardware Store",
]


def make_event(rng: random.Random, now: datetime, drop_currency: bool) -> dict:
    """Build a single synthetic transaction event."""
    event = {
        "transaction_id": str(uuid.uuid4()),
        "account_id": f"ACC-{rng.randint(10_000, 99_999)}",
        "amount": round(rng.uniform(-500.0, 2500.0), 2),
        "currency": rng.choice(CURRENCIES),
        "merchant": rng.choice(MERCHANTS),
        "event_timestamp": (
            now - timedelta(minutes=rng.randint(0, 23 * 60))
        ).isoformat(),
    }
    if drop_currency:
        # The breaking change: an upstream refactor silently removes a field
        # the contract declares as required.
        del event["currency"]
    return event


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=1000, help="number of events")
    parser.add_argument("--out", default="data/transactions.jsonl", help="output path")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument(
        "--break",
        dest="break_contract",
        action="store_true",
        help="simulate a breaking change: drop the required `currency` field",
    )
    args = parser.parse_args()

    rng = random.Random(args.seed)
    now = datetime.now(timezone.utc)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        for _ in range(args.count):
            fh.write(json.dumps(make_event(rng, now, args.break_contract)) + "\n")

    mode = "BREAKING (currency dropped)" if args.break_contract else "valid"
    print(f"Wrote {args.count} {mode} events to {args.out}")


if __name__ == "__main__":
    main()
