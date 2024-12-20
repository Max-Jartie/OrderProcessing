import unittest
import sqlite3

class TestDatabase(unittest.TestCase):
    def test_connection(self):
        conn = sqlite3.connect("drivers.db/drivers.db")
        self.assertIsNotNone(conn)
        conn.close()

    def test_driver_insertion(self):
        conn = sqlite3.connect("drivers.db/drivers.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO drivers (name, rating, status, car_class) VALUES (?, ?, ?, ?)",
            ("Тестовый Водитель", 4.5, "available", "econom"),
        )
        conn.commit()
        cursor.execute("SELECT * FROM drivers WHERE name = 'Тестовый Водитель'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        conn.close()
