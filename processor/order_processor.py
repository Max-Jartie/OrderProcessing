import time
import redis
import json
import sqlite3
import logging
import traceback

logging.basicConfig(
    level=logging.INFO,
    filename='order_processor.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

r = redis.Redis(host='redis', port=6379, db=0)
db_path = '/app/drivers.db'

def process_order(order_data):
    try:
        order = json.loads(order_data)
        logging.info(f"Обрабатывается заказ: {order}")

        if 'driver_id' not in order or 'driver_status' not in order:
            logging.warning(f"Заказ {order.get('order_id', 'неизвестен')} не содержит driver_id или driver_status.")
            return

        allowed_statuses = ["available", "assigned", "busy", "offline"]
        if order['driver_status'] not in allowed_statuses:
            logging.error(f"Неверный статус водителя: {order['driver_status']} для заказа {order.get('order_id', 'неизвестен')}.")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT status FROM drivers WHERE id = ?", (order['driver_id'],))
        row = cursor.fetchone()
        old_status = row[0] if row else None

        if not row:
            logging.warning(f"Водитель с ID {order['driver_id']} не найден для заказа {order.get('order_id', 'неизвестен')}.")
            return

        cursor.execute("UPDATE drivers SET status = ? WHERE id = ?", (order['driver_status'], order['driver_id']))
        conn.commit()

        logging.info(f"Статус водителя {order['driver_id']} изменён с {old_status} на {order['driver_status']} для заказа {order.get('order_id', 'неизвестен')}.")
    except sqlite3.IntegrityError as e:
        logging.error(f"Ошибка целостности базы данных: {e}, traceback: {traceback.format_exc()}")
    except sqlite3.OperationalError as e:
        logging.error(f"Операционная ошибка базы данных: {e}, traceback: {traceback.format_exc()}")
    except sqlite3.Error as e:
        logging.error(f"Ошибка базы данных: {e}, traceback: {traceback.format_exc()}")
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования JSON: {order_data}, traceback: {traceback.format_exc()}")
    except Exception as e:
        logging.exception(f"Произошла непредвиденная ошибка: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

while True:
    try:
        result = r.blpop('orders', timeout=5)
        if result:
            message = result[1]
            process_order(message)
        else:
            logging.info("Очередь заказов пуста. Ожидание...")
    except redis.exceptions.ConnectionError as e:
        logging.error(f"Ошибка подключения к Redis: {e}")
        time.sleep(5)
    except Exception as e:
        logging.exception(f"Произошла непредвиденная ошибка: {e}")
