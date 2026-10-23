import os
import tempfile
import unittest
from unittest.mock import patch

import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = os.path.join(self.temp_dir.name, "finops.db")
        self.path_patcher = patch.object(database, "DB_PATH", self.db_path)
        self.path_patcher.start()
        database.create_database()

    def tearDown(self):
        self.path_patcher.stop()
        self.temp_dir.cleanup()

    def test_upsert_updates_existing_date_service(self):
        database.upsert_cost("2026-01-01", "Amazon EC2", 1.25)
        database.upsert_cost("2026-01-01", "Amazon EC2", 2.50)
        with database.get_connection() as conn:
            rows = conn.execute("SELECT date, service, cost_usd FROM daily_costs").fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["cost_usd"], 2.50)

    def test_distinct_services_are_kept(self):
        database.upsert_cost("2026-01-01", "Amazon EC2", 1.25)
        database.upsert_cost("2026-01-01", "Amazon S3", 0.25)
        with database.get_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM daily_costs").fetchone()[0]
        self.assertEqual(count, 2)


if __name__ == "__main__":
    unittest.main()
