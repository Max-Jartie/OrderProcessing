from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

db_path = '/app/drivers.db'

# HTML шаблон для страницы заказа
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Система заказа</title>
</head>
<body>
    <h1>Заказ поездки</h1>
    <form action="/select-driver" method="post">
        <label>Откуда:</label><br>
        <input type="text" name="from_address" required><br>
        <label>Куда:</label><br>
        <input type="text" name="to_address" required><br>
        <label>Класс авто:</label><br>
        <select name="car_class">
            <option value="economy">Эконом</option>
            <option value="comfort">Комфорт</option>
            <option value="business">Бизнес</option>
        </select><br><br>
        <input type="submit" value="Выбрать водителя">
    </form>

    {% if drivers %}
    <h2>Доступные водители:</h2>
    <form action="/confirm-order" method="post">
        <input type="hidden" name="from_address" value="{{ from_address }}">
        <input type="hidden" name="to_address" value="{{ to_address }}">
        <input type="hidden" name="car_class" value="{{ car_class }}">
        {% for driver in drivers %}
        <input type="radio" name="driver_id" value="{{ driver[0] }}" required> {{ driver[1] }} (Рейтинг: {{ driver[2] }})<br>
        {% endfor %}
        <br>
        <input type="submit" value="Подтвердить заказ">
    </form>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/select-driver', methods=['POST'])
def select_driver():
    from_address = request.form['from_address']
    to_address = request.form['to_address']
    car_class = request.form['car_class']

    # Укажите путь напрямую
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, rating FROM drivers WHERE status = 'available' AND car_class = ?", (car_class,))
    drivers = cursor.fetchall()
    conn.close()

    return render_template_string(HTML_PAGE, drivers=drivers, from_address=from_address, to_address=to_address, car_class=car_class)


@app.route('/confirm-order', methods=['POST'])
def confirm_order():
    from_address = request.form['from_address']
    to_address = request.form['to_address']
    car_class = request.form['car_class']
    driver_id = request.form['driver_id']

    # Укажите путь напрямую
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Обновление статуса водителя
    cursor.execute("UPDATE drivers SET status = 'busy' WHERE id = ?", (driver_id,))
    conn.commit()
    conn.close()

    # Для простоты, цена фиксирована на основе класса авто
    prices = {'economy': 500, 'comfort': 1000, 'business': 2000}
    price = prices.get(car_class, 500)

    return f"<h1>Ваш заказ подтверждён!</h1><p>Цена: {price} рублей</p><a href='/'>Назад</a>"

if __name__ == "__main__":
    print("Запуск Flask-сервера...")
    app.run(host="0.0.0.0", port=5000, debug=True)