import mysql.connector
from tkinter import messagebox

# Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'TheRoyalPhoneLedger'
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Vault Error", f"Could not open the Royal Vault: {err}")
        return None