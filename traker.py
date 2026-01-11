import sqlite3
from datetime import datetime
from fpdf import FPDF
import os

# --- Database Setup ---
conn = sqlite3.connect("invoice_tracker.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    amount REAL,
    status TEXT,
    date TEXT,
    FOREIGN KEY(client_id) REFERENCES clients(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    amount REAL,
    date TEXT,
    FOREIGN KEY(invoice_id) REFERENCES invoices(id)
)
""")

conn.commit()

# --- Functions ---
def add_client():
    name = input("Client Name: ")
    email = input("Client Email: ")
    c.execute("INSERT INTO clients (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    print(f"Client '{name}' added successfully!\n")

def create_invoice():
    client_id = int(input("Client ID: "))
    amount = float(input("Invoice Amount: "))
    date = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO invoices (client_id, amount, status, date) VALUES (?, ?, ?, ?)",
              (client_id, amount, "Unpaid", date))
    conn.commit()
    invoice_id = c.lastrowid
    print("Invoice created successfully!\n")
    generate_pdf_invoice(invoice_id)

def record_payment():
    invoice_id = int(input("Invoice ID: "))
    amount = float(input("Payment Amount: "))
    date = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO payments (invoice_id, amount, date) VALUES (?, ?, ?)",
              (invoice_id, amount, date))

    # Update invoice status
    c.execute("SELECT SUM(amount) FROM payments WHERE invoice_id = ?", (invoice_id,))
    total_paid = c.fetchone()[0] or 0
    c.execute("SELECT amount FROM invoices WHERE id = ?", (invoice_id,))
    invoice_amount = c.fetchone()[0]

    status = "Paid" if total_paid >= invoice_amount else "Partial"
    c.execute("UPDATE invoices SET status = ? WHERE id = ?", (status, invoice_id))

    conn.commit()
    print("Payment recorded successfully!\n")

def view_invoices():
    c.execute("""
    SELECT invoices.id, clients.name, invoices.amount, invoices.status, invoices.date
    FROM invoices
    JOIN clients ON invoices.client_id = clients.id
    """)
    invoices = c.fetchall()
    print("\n--- All Invoices ---")
    for inv in invoices:
        print(f"ID: {inv[0]}, Client: {inv[1]}, Amount: {inv[2]}, Status: {inv[3]}, Date: {inv[4]}")
    print()

def view_clients():
    c.execute("SELECT * FROM clients")
    clients = c.fetchall()
    print("\n--- All Clients ---")
    for client in clients:
        # Calculate total due
        c.execute("""
        SELECT SUM(amount) - IFNULL((SELECT SUM(amount) FROM payments WHERE payments.invoice_id = invoices.id), 0)
        FROM invoices WHERE client_id = ?
        """, (client[0],))
        balance_due = c.fetchone()[0] or 0
        print(f"ID: {client[0]}, Name: {client[1]}, Email: {client[2]}, Balance Due: {balance_due}")
    print()

def generate_pdf_invoice(invoice_id):
    c.execute("""
    SELECT invoices.id, clients.name, clients.email, invoices.amount, invoices.status, invoices.date
    FROM invoices
    JOIN clients ON invoices.client_id = clients.id
    WHERE invoices.id = ?
    """, (invoice_id,))
    inv = c.fetchone()
    if not inv:
        print("Invoice not found!")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "INVOICE", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Invoice ID: {inv[0]}", ln=True)
    pdf.cell(0, 10, f"Client: {inv[1]}", ln=True)
    pdf.cell(0, 10, f"Email: {inv[2]}", ln=True)
    pdf.cell(0, 10, f"Date: {inv[5]}", ln=True)
    pdf.cell(0, 10, f"Status: {inv[4]}", ln=True)
    pdf.ln(10)

    pdf.cell(0, 10, f"Amount Due: ${inv[3]:.2f}", ln=True)

    if not os.path.exists("invoices"):
        os.makedirs("invoices")
    filename = f"invoices/invoice_{inv[0]}.pdf"
    pdf.output(filename)
    print(f"PDF Invoice generated: {filename}\n")

# --- Main Menu ---
while True:
    print("=== Payment & Invoice Tracker ===")
    print("1. Add Client")
    print("2. Create Invoice")
    print("3. Record Payment")
    print("4. View Invoices")
    print("5. View Clients with Balance")
    print("6. Exit")

    choice = input("Select an option: ")

    if choice == "1":
        add_client()
    elif choice == "2":
        create_invoice()
    elif choice == "3":
        record_payment()
    elif choice == "4":
        view_invoices()
    elif choice == "5":
        view_clients()
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Try again.\n")