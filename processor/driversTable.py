import sqlite3
import os

db_file = "/app/drivers.db"

def create_drivers_table():
    conn = None  # Инициализируем переменную conn
    try:
        # Проверяем, существует ли база данных
        if not os.path.exists(db_file):
            print(f"Создание базы данных {db_file}")

        # Открываем соединение с базой данных
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Создаем таблицу, если её нет
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating REAL NOT NULL,
            status TEXT NOT NULL,
            car_class TEXT NOT NULL
        )
        """)
        conn.commit()
        print(f"Таблица 'drivers' создана в базе данных {db_file}")

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")

    finally:
        # Закрываем соединение
        if conn:
            conn.close()


def insert_test_data():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Добавляем тестовые данные
        test_data = [
            # Эконом
            ('Иван Иванов', 4.7, 'available', 'economy'),
            ('Петр Смирнов', 4.5, 'available', 'economy'),
            ('Ольга Соколова', 4.6, 'busy', 'economy'),
            ('Наталья Васильева', 4.8, 'available', 'economy'),

            # Комфорт
            ('Алексей Кузнецов', 4.9, 'available', 'comfort'),
            ('Екатерина Морозова', 4.8, 'busy', 'comfort'),
            ('Михаил Орлов', 4.7, 'available', 'comfort'),
            ('Светлана Никифорова', 4.9, 'available', 'comfort'),

            # Бизнес
            ('Дмитрий Федоров', 4.9, 'available', 'business'),
            ('Сергей Михайлов', 4.8, 'available', 'business'),
            ('Анастасия Романова', 5.0, 'busy', 'business'),
            ('Владимир Тихонов', 4.7, 'available', 'business'),
        ]

        cursor.executemany("""
        INSERT INTO drivers (name, rating, status, car_class)
        VALUES (?, ?, ?, ?)
        """, test_data)
        conn.commit()
        print("Тестовые данные успешно добавлены.")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных: {e}")

    finally:
        if conn:
            conn.close()



if __name__ == "__main__":
    create_drivers_table()
    insert_test_data()
