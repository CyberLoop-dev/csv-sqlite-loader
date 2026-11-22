import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path
from main import infer_type, load_csv, quote_identifier

class LoaderTests(unittest.TestCase):
    def test_infers_integer_real_and_text(self):
        self.assertEqual(infer_type(["1", "2"]), "INTEGER")
        self.assertEqual(infer_type(["1.5", "2"]), "REAL")
        self.assertEqual(infer_type(["a", "2"]), "TEXT")

    def test_imports_rows_and_nulls(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            database = Path(directory) / "data.db"
            source.write_text("id,price,note\n1,2.5,hello\n2,,\n", encoding="utf-8")
            result = load_csv(source, database, "items")
            self.assertEqual(result["rows"], 2)
            with sqlite3.connect(database) as connection:
                rows = connection.execute('SELECT id, price, note FROM "items" ORDER BY id').fetchall()
            self.assertEqual(rows, [(1, 2.5, "hello"), (2, None, None)])

    def test_existing_table_requires_replace(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            database = Path(directory) / "data.db"
            source.write_text("id\n1\n", encoding="utf-8")
            load_csv(source, database, "items")
            with self.assertRaises(ValueError):
                load_csv(source, database, "items")
            load_csv(source, database, "items", replace=True)

    def test_identifier_is_quoted(self):
        self.assertEqual(quote_identifier('a"b'), '"a""b"')

    def test_duplicate_headers_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            source.write_text("id,id\n1,2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_csv(source, Path(directory) / "data.db", "items")

if __name__ == "__main__":
    unittest.main()
