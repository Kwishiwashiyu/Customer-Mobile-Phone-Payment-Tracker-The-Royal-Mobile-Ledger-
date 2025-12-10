from db import get_connection

def add_phone(model, price, stock):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO phones (model_name, price, stock) VALUES (%s, %s, %s)"
        cursor.execute(sql, (model, price, stock))
        conn.commit()
        conn.close()

def get_all_phones():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT phone_id, model_name, price, stock FROM phones")
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

def get_phone_price_stock(phone_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT price, stock FROM phones WHERE phone_id = %s", (phone_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    return None

# Update Phone Function
def update_phone(phone_id, model, price, stock):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE phones SET model_name = %s, price = %s, stock = %s WHERE phone_id = %s"
        cursor.execute(sql, (model, price, stock, phone_id))
        conn.commit()
        conn.close()

# Delete Phone Function
def delete_phone(phone_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Check for active dependent records (Installments)
            cursor.execute("SELECT COUNT(*) FROM installment_plans WHERE phone_id = %s AND status = 'Active'", (phone_id,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False, "Cannot delete Weapon! Active Decrees (Installments) are linked to this model."
            
            sql = "DELETE FROM phones WHERE phone_id = %s"
            cursor.execute(sql, (phone_id,))
            conn.commit()
            conn.close()
            return True, "Weapon scrapped from the Armory."
        except Exception as e:
            conn.close()
            return False, f"Error deleting: {e}"
    return False, "Database connection failed."