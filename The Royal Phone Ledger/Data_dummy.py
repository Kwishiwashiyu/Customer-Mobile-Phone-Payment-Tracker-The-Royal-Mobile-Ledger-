import mysql.connector
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Import DB_CONFIG from db.py
try:
    from db import DB_CONFIG
except ImportError:
    # Fallback config if db.py is not run from the same environment
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'TheRoyalPhoneLedger'
    }

def insert_dummy_data():
    """Inserts dummy data for testing purposes."""
    
    config = DB_CONFIG.copy()
    config['database'] = 'TheRoyalPhoneLedger'

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("Connected to database. Injecting test data...")

        # --- Clear existing data (for clean runs) ---
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE payments")
        cursor.execute("TRUNCATE TABLE installment_plans")
        cursor.execute("TRUNCATE TABLE customers")
        cursor.execute("TRUNCATE TABLE phones")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        # 1. Insert Customers (Subjects)
        customers_data = [
            ("Sir", "Lancelot", "555-1001", "Camelot Keep"), # ID 1 (On time)
            ("Lady", "Guinevere", "555-1002", "Royal Chambers"), # ID 2
            ("Lord", "Mordred", "555-1003", "Dark Tower") # ID 3 (Overdue)
        ]
        cursor.executemany("INSERT INTO customers (first_name, last_name, contact, address) VALUES (%s, %s, %s, %s)", customers_data)

        # 2. Insert Phones (Weapons)
        phones_data = [
            ("Royal Scrying Orb X", "G-Apple", 1200.00, 5),  # ID 1
            ("King's Tablet Pro", "S-Samsung", 850.00, 10)   # ID 2
        ]
        cursor.executemany("INSERT INTO phones (model_name, brand, price, stock) VALUES (%s, %s, %s, %s)", phones_data)
        
        # 3. Insert Installment Plans (Decrees)
        today = date.today()
        
        # --- Loan 1: Lancelot (On time) ---
        # Purchased 2 months ago. Should have 2 payments made.
        date_loan1 = today - timedelta(days=60) 
        # Total: 1260.00. Monthly (12 months): 105.00
        cursor.execute("""
            INSERT INTO installment_plans (customer_id, phone_id, purchase_date, months, interest_rate, total_amount, monthly_payment, remaining_balance, status) 
            VALUES (1, 1, %s, 12, 5.00, 1260.00, 105.00, 1260.00, 'Active')
        """, (date_loan1,))
        loan1_id = cursor.lastrowid
        
        # Make 2 payments (on time)
        cursor.execute("INSERT INTO payments (installment_id, payment_date, amount) VALUES (%s, %s, %s)", (loan1_id, date_loan1 + timedelta(days=30), 105.00))
        cursor.execute("INSERT INTO payments (installment_id, payment_date, amount) VALUES (%s, %s, %s)", (loan1_id, date_loan1 + timedelta(days=60), 105.00))
        cursor.execute("UPDATE installment_plans SET remaining_balance = 1050.00 WHERE installment_id = %s", (loan1_id,))

        # --- Loan 2: Mordred (Overdue) ---
        # Purchased 3 months ago. Should have 3 payments.
        date_loan2 = today - timedelta(days=90) 
        # Total: 884.00. Monthly (10 months): 88.40
        cursor.execute("""
            INSERT INTO installment_plans (customer_id, phone_id, purchase_date, months, interest_rate, total_amount, monthly_payment, remaining_balance, status) 
            VALUES (3, 2, %s, 10, 4.00, 884.00, 88.40, 884.00, 'Active')
        """, (date_loan2,))
        loan2_id = cursor.lastrowid

        # Make only 1 payment (2 payments missed, as of today)
        cursor.execute("INSERT INTO payments (installment_id, payment_date, amount) VALUES (%s, %s, %s)", (loan2_id, date_loan2 + timedelta(days=30), 88.40))
        cursor.execute("UPDATE installment_plans SET remaining_balance = 795.60 WHERE installment_id = %s", (loan2_id,))
        
        conn.commit()
        print("Data injection complete. You can now run main.py.")

    except mysql.connector.Error as err:
        print(f"Error during data injection: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":

    insert_dummy_data()
