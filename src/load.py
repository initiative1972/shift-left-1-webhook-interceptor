"""Load synthetic transaction events (JSONL) into a local DuckDB warehouse.

This is the 'ingestion' step. It deliberately does NOT validate the data — the
data contract does that, via `datacontract test`, in CI. The loader's job is just
to land whatever the producer emitted into the `transactions` table, so that a
breaking change actually reaches the warehouse boundary and is caught there.

Usage:
    python src/load.py --in data/transactions.jsonl --db data/warehouse.duckdb
"""

from __future__ import annotations

import argparse
import os

import duckdb


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="infile", default="data/transactions.jsonl")
    parser.add_argument("--db", dest="db", default="data/warehouse.duckdb")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.db) or ".", exist_ok=True)

    con = duckdb.connect(args.db)
    con.execute("DROP TABLE IF EXISTS transactions")
    # read_json_auto infers the schema from the JSONL. If the producer dropped
    # `currency`, the column simply won't exist — and the contract test will fail
    # on the missing required field.
    con.execute(
        "CREATE TABLE transactions AS "
        "SELECT * FROM read_json_auto(?, format='newline_delimited')",
        [args.infile],
    )
    rows = con.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    cols = [c[0] for c in con.execute("DESCRIBE transactions").fetchall()]
    con.close()

    print(f"Loaded {rows} rows into {args.db} (table: transactions)")
    print(f"Columns: {', '.join(cols)}")


if __name__ == "__main__":
    main()
