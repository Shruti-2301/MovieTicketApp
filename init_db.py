import sqlite3

with open("schema.sql", "r") as f:
    schema = f.read()

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.executescript(schema)

# Insert sample movies
cursor.execute("INSERT INTO movies (title, genre, duration, price) VALUES (?, ?, ?, ?)",
               ("Avengers", "Action", 180, 250))

cursor.execute("INSERT INTO movies (title, genre, duration, price) VALUES (?, ?, ?, ?)",
               ("Frozen", "Animation", 120, 180))

cursor.execute("INSERT INTO movies (title, genre, duration, price) VALUES (?, ?, ?, ?)",
               ("Inception", "Sci-Fi", 150, 300))

conn.commit()
conn.close()

print("Database Initialized Successfully!")