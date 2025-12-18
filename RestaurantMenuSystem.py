import sqlite3
from datetime import datetime


# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return sqlite3.connect("restaurant.db")


# ---------------- CREATE TABLES & DETAILED SEED ----------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (category_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        quantity INTEGER,
        order_date TEXT,
        total_price REAL,
        FOREIGN KEY (item_id) REFERENCES menu_items (item_id)
    )
    """)

    # Seed initial data if tables are empty
    cur.execute("SELECT COUNT(*) FROM categories")
    if cur.fetchone()[0] == 0:
        # Define Categories and Items
        data = {
            "Juice": [("Orange", 60), ("Pappaya", 50), ("Musambi", 70), ("Watermelon", 50)],
            "Desserts": [("Falooda", 150), ("Vanilla Icecream", 80), ("Pista Icecream", 90), ("Butterscotch", 100)],
            "Rice Items": [("Mandhi", 250), ("Biriyani", 180), ("Rice", 60), ("Fried Rice", 150)],
            "Curry Items": [("Butter Chicken", 220), ("Chilli Chicken", 200), ("Kadai Chicken", 210),
                            ("Gobi Manchurian", 160), ("Paneer Butter Masala", 190)]
        }

        for cat_name, items in data.items():
            cur.execute("INSERT INTO categories (category_name) VALUES (?)", (cat_name,))
            cat_id = cur.lastrowid
            for item_name, price in items:
                cur.execute("INSERT INTO menu_items (name, price, category_id) VALUES (?, ?, ?)",
                            (item_name, price, cat_id))

    conn.commit()
    conn.close()


# ---------------- STAFF / CHEF SECTION ----------------
def staff_menu():
    while True:
        print("\n--- STAFF / CHEF CONTROL PANEL ---")
        print("1. Add New Category")
        print("2. Add New Menu Item")
        print("3. View Full Menu Report")
        print("4. Back to Main Menu")

        choice = input("Select option: ")
        if choice == "1":
            add_category()
        elif choice == "2":
            add_menu_item()
        elif choice == "3":
            view_full_menu()
        elif choice == "4":
            break


def add_category():
    name = input("Enter new category name: ").strip().title()
    if not name: return
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (category_name) VALUES (?)", (name,))
        conn.commit()
        print(f"Category '{name}' added!")
    except:
        print("Category already exists.")
    finally:
        conn.close()


def add_menu_item():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories")
    cats = cur.fetchall()
    print("\nCategories:")
    for c in cats: print(f"{c[0]}. {c[1]}")
    try:
        cat_id = int(input("Select Category ID: "))
        name = input("Item Name: ").strip().title()
        price = float(input("Price: ₹"))
        cur.execute("INSERT INTO menu_items (name, price, category_id) VALUES (?, ?, ?)", (name, price, cat_id))
        conn.commit()
        print(f"'{name}' added successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


# ---------------- CUSTOMER SECTION ----------------
def view_full_menu():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.category_name, m.item_id, m.name, m.price 
        FROM menu_items m JOIN categories c ON m.category_id = c.category_id
        ORDER BY c.category_name
    """)
    rows = cur.fetchall()
    current_cat = ""
    print("\n--- RESTAURANT MENU ---")
    for row in rows:
        if row[0] != current_cat:
            current_cat = row[0]
            print(f"\n[{current_cat.upper()}]")
        print(f"  ID:{row[1]:<3} {row[2]:<20} ₹{row[3]}")
    conn.close()


def place_order():
    conn = get_connection()
    cur = conn.cursor()

    # Show categories for user to pick from
    cur.execute("SELECT * FROM categories")
    cats = cur.fetchall()
    print("\n--- WHAT WOULD YOU LIKE TO ORDER? ---")
    for c in cats: print(f"{c[0]}. {c[1]}")
    print("0. View All Items")

    try:
        cat_choice = int(input("Select Category ID: "))
        if cat_choice == 0:
            view_full_menu()
        else:
            cur.execute("SELECT item_id, name, price FROM menu_items WHERE category_id = ?", (cat_choice,))
            items = cur.fetchall()
            if not items:
                print("No items in this category.")
                return
            print("\nItems in this category:")
            for item in items:
                print(f"ID:{item[0]:<3} {item[1]:<20} ₹{item[2]}")

        item_id = int(input("\nEnter Item ID to buy: "))
        qty = int(input("Enter Quantity: "))

        cur.execute("SELECT name, price FROM menu_items WHERE item_id = ?", (item_id,))
        res = cur.fetchone()

        if res and qty > 0:
            name, price = res
            total = price * qty
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute("INSERT INTO orders (item_id, quantity, order_date, total_price) VALUES (?, ?, ?, ?)",
                        (item_id, qty, date, total))
            conn.commit()
            print(f"\n✅ SUCCESS: Ordered {qty}x {name}. Total: ₹{total}")
        else:
            print("Invalid Item ID or Quantity.")
    except ValueError:
        print("Please enter valid numbers.")
    finally:
        conn.close()


# ---------------- MAIN ----------------
def main():
    create_tables()
    while True:
        print("\n================================")
        print("  RESTAURANT MANAGEMENT SYSTEM")
        print("================================")
        print("1. Customer (Order Food)")
        print("2. Staff / Chef (Manage Menu)")
        print("3. Exit")

        role = input("Choice: ")
        if role == "1":
            place_order()
        elif role == "2":
            staff_menu()
        elif role == "3":
            break
        else:
            print("Try again.")


if __name__ == "__main__":
    main()