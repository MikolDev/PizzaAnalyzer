from os import getenv, makedirs
from dotenv import load_dotenv
from pyodbc import connect
import csv
import matplotlib.pyplot as plt

global cursor


def connect_to_db():
    load_dotenv()
    conn = connect(getenv("SQL_CONNECTION_STRING"))
    return conn.cursor()


def get_all_ingredients(pizza_name):
    cursor.execute(
        f'select recipes.ingredient from recipes join menu on recipes.pizza = menu.pizza where menu.pizza = ?',
        pizza_name
    )
    ingredients = cursor.fetchall()
    print(f"--- INGREDIENTS pizza = {pizza_name} ---")
    for row in ingredients:
        print(row.ingredient)
    print("----------------------------------")


def get_pizzas_by_country(country):
    cursor.execute("SELECT pizza, price FROM MENU WHERE country = ?", country)
    rows = cursor.fetchall()

    if not rows:
        print("No pizzas for such country")

    print(f"--- PIZZAS country = {country} ---")
    for row in rows:
        print(row.pizza, row.price)
    print("----------------------------------")

    makedirs('./figures', exist_ok=True)
    filename = f'figures/pizzas_from_{country}.csv'

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Pizza Name', 'Price'])
        for row in rows:
            writer.writerow([row.pizza, row.price])


def basic_queries():
    cursor.execute("select pizza from menu order by pizza asc")
    pizza_names = cursor.fetchall()

    print("--- PIZZA NAMES ALPHABETICALLY ---")
    for row in pizza_names:
        print(row.pizza)
    print("----------------------------------")

    cursor.execute("select count(pizza) as count from menu")
    pizza_count = cursor.fetchone()
    if pizza_count:
        print(f'--- PIZZA COUNT: {pizza_count.count} ---')

    get_all_ingredients('americano')

    get_pizzas_by_country('Italy')


def ask_for_ingredient():
    ingredient = input("Specify the ingredient name: ")
    cursor.execute(
        'select menu.pizza from menu join recipes on menu.pizza = recipes.pizza where recipes.ingredient = ?',
        ingredient)

    rows = cursor.fetchall()

    if not rows:
        print("No pizza found for specified ingredient")
        return

    print(f"--- PIZZA NAMES FOR INGREDIENT {ingredient} ---")
    for row in rows:
        print(row.pizza)
    print("----------------------------------")


def ask_for_price():
    correct = True
    price = 0
    while correct:
        price = input("Specify price: ")
        try:
            price = float(price)
            correct = False
        except ValueError:
            print("Wrong input. Specify float value for price.")

    cursor.execute('select pizza, price from menu where price >= ?', price)

    rows = cursor.fetchall()

    if not rows:
        print("No pizza found for specified price")
        return

    print(f"--- PIZZA NAMES FOR PRICE {price} ---")
    for row in rows:
        print(row.pizza, row.price)
    print("----------------------------------")


def draw_chart():
    cursor.execute("SELECT pizza, price FROM MENU")
    results = cursor.fetchall()

    pizza_names = [row.pizza for row in results]
    pizza_prices = [float(row.price) for row in results]

    cursor.execute("SELECT AVG(price) as avg_price FROM MENU")
    avg_price = float(cursor.fetchone().avg_price)

    plt.figure(figsize=(12, 6))
    plt.bar(pizza_names, pizza_prices, color='orange')
    plt.axhline(y=avg_price, color='orange', linestyle='--')
    plt.text(
        x=len(pizza_names) - 1,
        y=avg_price + 0.1,
        s=f'{avg_price}',
    )
    plt.grid(axis='both', linestyle='-', alpha=0.5)

    plt.title('Pizza prices')
    plt.xlabel('Pizza')
    plt.ylabel('Price')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    makedirs('./figures', exist_ok=True)
    filename = 'figures/pizza_prices_comparison.svg'
    plt.savefig(filename, format='svg')


if __name__ == '__main__':
    cursor = connect_to_db()
    basic_queries()
    ask_for_ingredient()
    ask_for_price()
    draw_chart()
