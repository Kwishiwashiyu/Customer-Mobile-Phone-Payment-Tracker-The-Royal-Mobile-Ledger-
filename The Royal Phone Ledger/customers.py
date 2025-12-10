from db import get_connection

def add_customer(first, last, contact):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO customers (first_name, last_name, contact) VALUES (%s, %s, %s)"
        cursor.execute(sql, (first, last, contact))
        conn.commit()
        conn.close()

def get_all_customers():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, first_name, last_name, contact FROM customers")
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

# Update Customer Function
def update_customer(customer_id, first, last, contact):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE customers SET first_name = %s, last_name = %s, contact = %s WHERE customer_id = %s"
        cursor.execute(sql, (first, last, contact, customer_id))
        conn.commit()
        conn.close()

# Delete Customer Function
def delete_customer(customer_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Check for active dependent records (Installments)
            cursor.execute("SELECT COUNT(*) FROM installment_plans WHERE customer_id = %s", (customer_id,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return False, "Cannot banish Subject! Active Decrees (Installments) are linked to this ID."
            
            sql = "DELETE FROM customers WHERE customer_id = %s"
            cursor.execute(sql, (customer_id,))
            conn.commit()
            conn.close()
            return True, "Subject banished from the Realm."
        except Exception as e:
            conn.close()
            return False, f"Error deleting: {e}"
    return False, "Database connection failed."