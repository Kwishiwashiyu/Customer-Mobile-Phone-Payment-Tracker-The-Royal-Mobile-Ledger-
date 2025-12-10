# 👑 The Royal Mobile Ledger: Customer Mobile Phone Payment Tracker

A Python-based application using Tkinter for the GUI and MySQL (via XAMPP) for database management, designed to track mobile phone installment plans, payments, and overdue accounts within a feudal, medieval theme.

## 💾 Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.x:** (Ensure Python and `pip` are in your system's PATH).
2.  **XAMPP:** (To run the Apache web server and MySQL database).
3.  **Required Python Libraries:**
    ```bash
    pip install mysql-connector-python python-dateutil
    ```

## 🚀 Setup Guide

Follow these steps to set up the database and run the application.

### Step 1: Database Setup (MySQL)

The application requires a MySQL database named `TheRoyalPhoneLedger`.

1.  **Start XAMPP:** Launch the XAMPP Control Panel and click **Start** for both **Apache** and **MySQL**.

2.  **Open phpMyAdmin:** Navigate to `http://localhost/phpmyadmin` in your web browser.

3.  **Create Database:**

      * Click the **Databases** tab.
      * Enter `TheRoyalPhoneLedger` as the database name and click **Create**.

4.  **Create Tables:**

      * Click on the newly created `TheRoyalPhoneLedger` database.
      * Click the **SQL** tab and execute the following schema script to create the necessary tables (`customers`, `phones`, `installment_plans`, `payments`):

    <!-- end list -->

    ```sql
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50), last_name VARCHAR(50), contact VARCHAR(30), address TEXT
    );
    CREATE TABLE IF NOT EXISTS phones (
        phone_id INT AUTO_INCREMENT PRIMARY KEY,
        model_name VARCHAR(100), brand VARCHAR(50), price DECIMAL(10,2), stock INT
    );
    CREATE TABLE IF NOT EXISTS installment_plans (
        installment_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT, phone_id INT, purchase_date DATE, months INT, interest_rate DECIMAL(5,2),
        total_amount DECIMAL(10,2), monthly_payment DECIMAL(10,2), remaining_balance DECIMAL(10,2),
        status VARCHAR(20), FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (phone_id) REFERENCES phones(phone_id)
    );
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INT AUTO_INCREMENT PRIMARY KEY, installment_id INT, payment_date DATE,
        amount DECIMAL(10,2), remarks VARCHAR(100), FOREIGN KEY (installment_id) REFERENCES installment_plans(installment_id)
    );
    ```

### Step 2: Inject Dummy Data (Optional, but Recommended for Testing)

To test the Overdue Report feature immediately, run the provided data injector script.

1.  Place the `data_injector.py` file in the same directory as `main.py`.
2.  Run the script from your terminal:
    ```bash
    python data_injector.py
    ```

### Step 3: Run the Application

Execute the main file to launch the GUI:

```bash
python main.py
```

## 📂 Project Structure

The project follows a clean, modular structure as requested:

```
MobilePaymentTracker/
│
├── main.py                  # Entry point, GUI definition, Theme Setup
├── db.py                    # MySQL Connection Configuration
├── customers.py             # Customer CRUD (Create, Read, Update, Delete) Logic
├── phones.py                # Phone Inventory CRUD Logic
├── installments.py          # Installment Plan Creation and Management Logic
├── payments.py              # Payment Recording, History, and Overdue Check Logic
├── Data_dummy.py            # Sample Data for testing (Contains 3 customers, 2 phones, and 2 installments with payment records)
│
└── gui/
    ├── dashboard_gui.py     # Kingdom Overview and Overdue Report
    ├── customers_gui.py     # Subjects CRUD Interface
    ├── phones_gui.py        # Armory CRUD Interface
    ├── installments_gui.py  # Decrees/Loan Setup and Management
    ├── payments_gui.py      # Tribute Recording and Payment History
```

## ✨ Key Features

| Tab | Feature | Description |
| :--- | :--- | :--- |
| **🏰 Kingdom Overview** | **Overdue Report** | Automatically checks active loans against expected payment dates and flags delinquent subjects. |
| | **Stats** | Shows total subjects, active decrees, completed decrees, and total gold collected. |
| **👥 Subjects (Customers)** | **Full CRUD** | Add, View, Edit, and Delete customers. Deletion is blocked if active loans exist. |
| **⚔️ Armory (Phones)** | **Inventory Management** | Add new phone models, update stock and price. Stock is decreased upon loan creation. |
| **💰 Decrees (Installments)** | **Loan Setup** | Calculates total principal, interest, and fixed monthly payment based on terms. |
| | **Close Decree** | Manual option to complete a loan if the balance is zero. |
| **⚖️ Tribute (Payments)** | **Payment Recording** | Record a payment, update the remaining balance, and automatically mark the loan as 'Completed' if the balance reaches zero. |
| | **Payment History** | View a scroll of all past tributes paid for a selected Decree ID. |

## ⚙️ Database Configuration

The system connects to `localhost` using the default XAMPP credentials (`root` with an empty password) and the database name `MobilePaymentTracker`. This is defined in `db.py`.

```python
# db.py
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'TheRoyalPhoneLedger'
}
```
