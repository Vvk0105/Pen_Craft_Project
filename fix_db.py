import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Find invalid foreign keys
cursor.execute("SELECT * FROM pen_chatrequest WHERE master_id NOT IN (SELECT id FROM auth_user);")
invalid_rows = cursor.fetchall()

# Print invalid rows
print("Invalid rows in pen_chatrequest:")
for row in invalid_rows:
    print(row)

# Fix invalid foreign keys (choose one of the following options)

# Option 1: Update invalid entries (replace 1 with a valid user_id from auth_user table)
# cursor.execute("UPDATE pen_chatrequest SET master_id = 1 WHERE master_id NOT IN (SELECT id FROM auth_user);")

# Option 2: Delete invalid entries
cursor.execute("DELETE FROM pen_chatrequest WHERE master_id NOT IN (SELECT id FROM auth_user);")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Invalid foreign keys fixed.")
