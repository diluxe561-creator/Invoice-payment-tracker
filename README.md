# PAYMENT & INVOICE TRACKER (SQLITE)

A robust CLI application for managing professional finances using an SQLite database. This tool tracks clients, manages invoice statuses (Unpaid/Partial/Paid), and handles incoming payments.

---

## 🚀 KEY FEATURES
- Relational Database: Powered by SQLite3 for reliable data storage.
- Client Management: Track client contact details and outstanding balances.
- Invoice Automation: Create invoices and automatically generate PDF copies.
- Payment Tracking: Record partial or full payments and watch invoice statuses update automatically.
- Financial Reporting: View all invoices or check which clients owe money at a glance.

---

## 🛠️ INSTALLATION

1. Ensure Python 3.x is installed.
2. Install the FPDF library for document generation:
   pip install fpdf

3. Run the script:
   python invoice_tracker.py

---

## 🖥️ HOW TO USE

1. [Add Client]: Register your clients first to generate their unique Database ID.
2. [Create Invoice]: Assign a bill to a Client ID. A PDF will be saved in the /invoices folder.
3. [Record Payment]: Enter the Invoice ID and the amount paid. The system will update the status to "Partial" or "Paid" automatically.
4. [View Clients with Balance]: Displays a list of all clients and the exact total they currently owe you.

---

## 📁 DATABASE STRUCTURE

The system uses three linked tables:
1. CLIENTS: ID, Name, Email.
2. INVOICES: ID, Client_ID, Amount, Status, Date.
3. PAYMENTS: ID, Invoice_ID, Amount, Date.



---

## 📁 FILE OUTPUTS
- /invoice_tracker.db  # Your permanent SQLite database file.
- /invoices/           # Folder where generated PDF invoices are stored.

---

## 📝 REQUIREMENTS
- Python 3.x
- sqlite3 (built-in)
- fpdf

---

Streamline your billing and stop losing track of unpaid work.
