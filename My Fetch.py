# %%
import sqlite3

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('mydatabase.sqlite')
cursor = conn.cursor()

# Create Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id TEXT PRIMARY KEY,
        active INTEGER,
        created_date TEXT,
        last_login TEXT,
        role TEXT,
        sign_up_source TEXT,
        state TEXT
    )
''')

# Create Brands table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Brands (
        brand_id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT
    )
''')

# Create Receipts table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Receipts (
        receipt_id TEXT PRIMARY KEY,
        user_id TEXT,
        brand_id TEXT,
        date_scanned TEXT,
        total_spent REAL,
        rewards_receipt_status TEXT,
        num_items INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (brand_id) REFERENCES Brands(brand_id)
    )
''')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Tables created successfully.")


# %%
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('mydatabase.sqlite')
cursor = conn.cursor()

# Insert data into Users table
users_data = [
    ('user1', 1, '2023-01-01', '2023-06-20', 'admin', 'web', 'CA'),
    ('user2', 1, '2023-02-01', '2023-06-22', 'user', 'mobile', 'NY')
]

cursor.executemany('''
    INSERT INTO Users (user_id, active, created_date, last_login, role, sign_up_source, state)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', users_data)

# Insert data into Brands table
brands_data = [
    ('brand1', 'BrandA', 'Category1'),
    ('brand2', 'BrandB', 'Category2')
]

cursor.executemany('''
    INSERT INTO Brands (brand_id, name, category)
    VALUES (?, ?, ?)
''', brands_data)

# Insert data into Receipts table
receipts_data = [
    ('receipt1', 'user1', 'brand1', '2023-05-01', 100.00, 'Accepted', 10),
    ('receipt2', 'user2', 'brand2', '2023-06-01', 200.00, 'Rejected', 20)
]

cursor.executemany('''
    INSERT INTO Receipts (receipt_id, user_id, brand_id, date_scanned, total_spent, rewards_receipt_status, num_items)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', receipts_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Data inserted successfully.")


# %%
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('mydatabase.sqlite')
cursor = conn.cursor()

# Query and print all users
cursor.execute('SELECT * FROM Users')
print("\nUsers:")
for row in cursor.fetchall():
    print(row)

# Query and print all brands
cursor.execute('SELECT * FROM Brands')
print("\nBrands:")
for row in cursor.fetchall():
    print(row)

# Query and print all receipts
cursor.execute('SELECT * FROM Receipts')
print("\nReceipts:")
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()


# %%
def query_avg_spend(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT rewards_receipt_status, AVG(total_spent) AS avg_spent
        FROM Receipts
        WHERE rewards_receipt_status IN ('Accepted', 'Rejected')
        GROUP BY rewards_receipt_status
    ''')
    rows = cursor.fetchall()
    return rows

# Execute Query 3
print("\nQuery 3: Average Spend from Receipts with 'Accepted' or 'Rejected' Status")
results_3 = query_avg_spend(conn)
for row in results_3:
    print(f"{row[0]}: ${row[1]:.2f} average spend")


# %%
def query_total_items_by_status(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT rewards_receipt_status, SUM(num_items) AS total_items
        FROM Receipts
        WHERE rewards_receipt_status IN ('Accepted', 'Rejected')
        GROUP BY rewards_receipt_status
    ''')
    rows = cursor.fetchall()
    return rows

# Execute Query 4
results_4 = query_total_items_by_status(conn)
print("\nQuery 4: Total Number of Items Purchased from Receipts with 'Accepted' or 'Rejected' Status")
for row in results_4:
    print(f"{row[0]}: {row[1]} total items")


# %%
def compare_rankings_recent_vs_previous(conn):
    # Query for recent month
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.name, COUNT(r.receipt_id) AS num_receipts
        FROM Receipts r
        JOIN Brands b ON r.brand_id = b.brand_id
        WHERE r.date_scanned >= DATE('now', '-1 month')
        GROUP BY b.name
        ORDER BY num_receipts DESC
        LIMIT 5
    ''')
    recent_month = cursor.fetchall()

    # Query for previous month
    cursor.execute('''
        SELECT b.name, COUNT(r.receipt_id) AS num_receipts
        FROM Receipts r
        JOIN Brands b ON r.brand_id = b.brand_id
        WHERE r.date_scanned >= DATE('now', '-2 month') AND r.date_scanned < DATE('now', '-1 month')
        GROUP BY b.name
        ORDER BY num_receipts DESC
        LIMIT 5
    ''')
    previous_month = cursor.fetchall()

    # Print comparison
    print("\nComparison of Rankings between Recent Month and Previous Month:")
    for i in range(5):
        brand_recent = recent_month[i][0] if i < len(recent_month) else "-"
        brand_previous = previous_month[i][0] if i < len(previous_month) else "-"
        print(f"{i+1}. Recent Month: {brand_recent}, Previous Month: {brand_previous}")

# Execute Query 2
compare_rankings_recent_vs_previous(conn)


# %%
import json

# Function to load JSON data from file
def load_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


# %%
# Function to find duplicate user IDs
def find_duplicate_user_ids(users):
    user_ids = [user['_id']['$oid'] for user in users]
    duplicate_user_ids = set([uid for uid in user_ids if user_ids.count(uid) > 1])
    return duplicate_user_ids


# %%
# Function to find brands with missing fields
def find_brands_with_issues(brands):
    brands_with_issues = [brand for brand in brands if not all(key in brand for key in ('_id', 'name', 'category'))]
    return brands_with_issues


# %%
# Function to find receipts with missing user or brand IDs
def find_receipts_with_issues(receipts):
    receipts_with_issues = [receipt for receipt in receipts if 'user_id' not in receipt or 'brand_id' not in receipt]
    return receipts_with_issues


# %%
import json

# Function to load JSON data from file
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{file_path}': {e}")
        return None

# Function to find duplicate user IDs
def find_duplicate_user_ids(users):
    user_ids = [user.get('_id', {}).get('$oid') for user in users]
    if len(user_ids) != len(set(user_ids)):
        return [uid for uid in set(user_ids) if user_ids.count(uid) > 1]
    else:
        return []

# Function to find brands with missing fields
def find_brands_with_issues(brands):
    return [brand for brand in brands if not all(key in brand for key in ('_id', 'name', 'category'))]

# Function to find receipts with missing user or brand IDs
def find_receipts_with_issues(receipts):
    return [receipt for receipt in receipts if 'user_id' not in receipt or 'brand_id' not in receipt]

# Main function to execute data quality checks
def main():
    # Load JSON files
    users = load_json_file('users.json')
    brands = load_json_file('brands.json')
    receipts = load_json_file('receipts.json')

    if not users or not brands or not receipts:
        print("Failed to load one or more JSON files. Exiting.")
        return

    # Check for duplicate user IDs
    duplicate_user_ids = find_duplicate_user_ids(users)
    if duplicate_user_ids:
        print("Duplicate User IDs:", duplicate_user_ids)
    else:
        print("No duplicate user IDs found.")

    # Check for brands with missing fields
    brands_with_issues = find_brands_with_issues(brands)
    if brands_with_issues:
        print("Brands with Missing Fields:", brands_with_issues)
    else:
        print("No brands with missing fields.")

    # Check for receipts with missing user or brand IDs
    receipts_with_issues = find_receipts_with_issues(receipts)
    if receipts_with_issues:
        print("Receipts with Missing User or Brand IDs:", receipts_with_issues)
    else:
        print("No receipts with missing user or brand IDs.")

if __name__ == "__main__":
    main()



# %%
Subject: Data Model Review and Insights

Hi Stakeholders,

I have reviewed the provided unstructured JSON data and developed a new structured relational data model to enhance data management and analytics capabilities. The new model includes Users, Brands, and Receipts tables with appropriate relationships.

I have also written SQL queries to answer the following business questions:
1. Average Spend from Receipts with 'Accepted' or 'Rejected' Status
2.  total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’

Additionally, I performed a data quality assessment and identified some issues:
1. Duplicate user IDs in the users data.
2. Missing fields in some brand records.
3. Inconsistencies in receipts data, such as missing user or brand IDs.

To address these issues, we need to:
1. Remove or merge duplicate user records.
2. Ensure all brand records have the required fields.
3. Validate and clean the receipts data.

Please let me know if you have any questions or need further details.

Best regards,
Jesse nwimo



