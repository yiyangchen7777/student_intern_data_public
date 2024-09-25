import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('student_intern_data.db')
cursor = conn.cursor()

# Step 1: Delete all existing rows from the Intakes table
cursor.execute('DELETE FROM Intakes')

# Step 2: Insert new rows into the Intakes table
intakes_data = [
    ('1 - Semester 2 2021', 'finish'),
    ('2 - Summer 2021/2022', 'finish'),
    ('3 - Semester 1 2022', 'finish'),
    ('4 - Semester 2 2022', 'finish'),
    ('5 - Summer 2022/2023', 'finish'),
    ('6 - Semester 1 2023', 'finish'),
    ('7 - Semester 2 2023', 'finish'),
    ('8 - Summer 2023/2024', 'finish'),
    ('9 - Semester 1 2024', 'finish'),
    ('10 - Semester 2 2024', 'current'),
    ('11 - Summer 2024/2025', 'new')
]

cursor.executemany('''
    INSERT INTO Intakes (name, status)
    VALUES (?, ?)
''', intakes_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Intakes table has been cleared and updated.")
