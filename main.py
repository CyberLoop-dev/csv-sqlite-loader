from __future__ import annotations
import argparse
import csv
import json
import math
import sqlite3
from pathlib import Path

def quote_identifier(value: str) -> str:
    if not value or not value.strip():
        raise ValueError("SQL identifiers cannot be empty")
    return '"' + value.replace('"', '""') + '"'

def infer_type(values: list[str | None]) -> str:
    present = [value.strip() for value in values if value is not None and value.strip() != ""]
    if not present:
        return "TEXT"
    try:
        for value in present:
            int(value)
        return "INTEGER"
    except ValueError:
        pass
    try:
        for value in present:
            number = float(value)
            if not math.isfinite(number):
                return "TEXT"
        return "REAL"
    except ValueError:
        return "TEXT"

def convert_value(value: str | None, kind: str):
    if value is None or value == "":
        return None
    if kind == "INTEGER":
        return int(value)
    if kind == "REAL":
        return float(value)
    return value

def load_csv(csv_path: str | Path, db_path: str | Path, table: str, replace: bool = False) -> dict:
    table_sql = quote_identifier(table)
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        if not columns:
            raise ValueError("CSV must contain a header row")
        if any(not column or not column.strip() for column in columns):
            raise ValueError("CSV column names cannot be empty")
        if len(set(columns)) != len(columns):
            raise ValueError("CSV column names must be unique")
        rows = list(reader)
    if any(None in row for row in rows):
        raise ValueError("A row contains more fields than the header")
    kinds = {column: infer_type([row.get(column) for row in rows]) for column in columns}
    column_sql = ", ".join(f"{quote_identifier(column)} {kinds[column]}" for column in columns)
    placeholders = ", ".join("?" for _ in columns)
    insert_sql = f"INSERT INTO {table_sql} VALUES ({placeholders})"
    with sqlite3.connect(db_path) as connection:
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ).fetchone()
        if exists and not replace:
            raise ValueError(f"Table {table!r} already exists; pass replace=True to replace it")
        if exists:
            connection.execute(f"DROP TABLE {table_sql}")
        connection.execute(f"CREATE TABLE {table_sql} ({column_sql})")
        values = [
            tuple(convert_value(row.get(column), kinds[column]) for column in columns)
            for row in rows
        ]
        if values:
            connection.executemany(insert_sql, values)
    return {"table": table, "rows": len(rows), "columns": kinds}

def main() -> int:
    parser = argparse.ArgumentParser(description="Import a CSV file into a local SQLite database.")
    parser.add_argument("csv_file")
    parser.add_argument("database")
    parser.add_argument("--table", default="data")
    parser.add_argument("--replace", action="store_true", help="Replace the target table if it exists")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    try:
        result = load_csv(args.csv_file, args.database, args.table, args.replace)
    except (OSError, csv.Error, sqlite3.Error, ValueError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Imported {result['rows']} rows into table {result['table']!r}.")
        for column, kind in result["columns"].items():
            print(f"  {column}: {kind}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
