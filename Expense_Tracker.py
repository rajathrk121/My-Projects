import sqlite3
connect=sqlite3.connect('expensee.db')
c=connect.cursor()
c.execute("""  
CREATE TABLE IF NOT EXISTS EXPENSETRACKER
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
Amount REAL NOT NULL,
Category TEXT NOT NULL,
Date TEXT NOT NULL,
Description TEXT 
);
""")
connect.commit()

def add_expense():
    amount=float(input("Enter expense amount: "))
    print("Select Category \n1 For Food \n2 For Petrol \n3 For Investment \n4 For Travel \n5 For Other")
    choice=int(input("Enter your choice:"))

    if choice==1:
        Category = "Food"
    elif choice==2:
        Category = "Petrol"
    elif choice==3:
        Category = "Investment"
    elif choice==4:
        Category = "Travel"
    elif choice==5:
        Category = "Other"
    else:
        print("Invalid choice")
        return
    Date=input("Enter the date of your expense(DD-MM-YYYY format): ")
    Description=input("Enter the description of your expense: ")

    c.execute("""
    INSERT INTO EXPENSETRACKER (Amount,Category ,Date,Description)
    VALUES(?,?,?,?)""",(amount,Category,Date,Description))

    connect.commit()

    print("Expense added successfully")

def view_expense():
    c.execute("SELECT * FROM EXPENSETRACKER")
    records=c.fetchall()

    if not records:
        print("No Expenses found \n")
        return

    print("All Expenses")
    print("-"*60)
    for row in records:
        print(f"ID:{row[0]} | Amount:{row[1]} | Category:{row[2]} | Date:{row[3]} | Decription:{row[4]}")
    print()

def delete_expense():
    expense_id=int(input("Enter expense id you want to delete: "))
    c.execute("SELECT * FROM EXPENSETRACKER WHERE ID=?", (expense_id,))
    record=c.fetchone()

    if not record:
        print("No such Expenses found \n")
        return

    if record:
        c.execute("DELETE FROM EXPENSETRACKER WHERE ID = ?",  (expense_id,))

        connect.commit()
        print("Expense Deleted Successfully")

    else:
        print("Expense Not Found")


def monthly_report():
    month=int(input("Enter month: "))
    year=int(input("Enter year: "))

    pattern = f"{year}-{month:02d}-%"

    c.execute("SELECT * FROM  EXPENSETRACKER WHERE DATE LIKE ? ", (pattern,)   )

    records=c.fetchall()

    if not records:
        print("NO Expenses found \n")
        return

    total = 0
    print(f"Expense for {month} {year}:")
    print("-" * 60)
    for row in records:

        print(f"ID:{row[0]} | Amount:{row[1]} | Category:{row[2]} | Date:{row[3]} | Decription:{row[4]}")

        total += row[1]

    print("-" * 60)
    print(f"Total Expense Amount for {month} {year} : {total}")

def menu():
    while True:
        choice=int(input("Enter your choice: "))
        if choice==1:
            add_expense()
        elif choice==2:
            view_expense()
        elif choice==3:
            delete_expense()
        elif choice==4:
            monthly_report()
        elif choice == 5:
            print("Exiting program...")
            break
        else:
            print("Invalid choice")



menu()
connect.close()
