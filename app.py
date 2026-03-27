from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_NAME = "database.db"


# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            duration INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            movie_id INTEGER NOT NULL,
            seats INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            booking_date TEXT NOT NULL,
            FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
        )
    """)

    # Check if movies already exist
    cursor.execute("SELECT COUNT(*) FROM movies")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_movies = [
            ("Avengers Endgame", "Action", 181, 250),
            ("Pushpa 2", "Drama", 165, 220),
            ("KGF Chapter 2", "Action", 168, 240),
            ("Frozen 2", "Animation", 103, 180),
            ("Jawan", "Thriller", 169, 260),
            ("Pathaan", "Action", 146, 230),
            ("3 Idiots", "Comedy", 170, 200),
            ("Dangal", "Sports", 161, 210),
            ("Bahubali 2", "Epic", 167, 270),
            ("Inception", "Sci-Fi", 148, 300)
        ]

        cursor.executemany(
            "INSERT INTO movies (title, genre, duration, price) VALUES (?, ?, ?, ?)",
            sample_movies
        )

        conn.commit()

    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- MOVIES PAGE ----------------
@app.route("/movies")
def movies_page():
    return render_template("movies.html")


# ---------------- BOOKINGS PAGE ----------------
@app.route("/bookings")
def bookings_page():
    return render_template("bookings.html")


# ---------------- API: GET MOVIES ----------------
@app.route("/api/movies", methods=["GET"])
def get_movies():
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return jsonify([dict(movie) for movie in movies])


# ---------------- API: ADD MOVIE ----------------
@app.route("/api/movies", methods=["POST"])
def add_movie():
    data = request.json

    title = data.get("title")
    genre = data.get("genre")
    duration = data.get("duration")
    price = data.get("price")

    if not title or not genre or not duration or not price:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO movies (title, genre, duration, price) VALUES (?, ?, ?, ?)",
        (title, genre, duration, price)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Movie Added Successfully"})


# ---------------- API: UPDATE MOVIE ----------------
@app.route("/api/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    data = request.json

    title = data.get("title")
    genre = data.get("genre")
    duration = data.get("duration")
    price = data.get("price")

    conn = get_db_connection()
    conn.execute("""
        UPDATE movies 
        SET title=?, genre=?, duration=?, price=?
        WHERE movie_id=?
    """, (title, genre, duration, price, movie_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Movie Updated Successfully"})


# ---------------- API: DELETE MOVIE ----------------
@app.route("/api/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM movies WHERE movie_id=?", (movie_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Movie Deleted Successfully"})


# ---------------- API: CREATE BOOKING ----------------
@app.route("/api/bookings", methods=["POST"])
def create_booking():
    data = request.json

    customer_name = data.get("customer_name")
    movie_id = data.get("movie_id")
    seats = data.get("seats")

    if not customer_name or not movie_id or not seats:
        return jsonify({"error": "All booking fields required"}), 400

    conn = get_db_connection()
    movie = conn.execute("SELECT price FROM movies WHERE movie_id=?", (movie_id,)).fetchone()

    if movie is None:
        conn.close()
        return jsonify({"error": "Movie Not Found"}), 404

    total_amount = movie["price"] * int(seats)
    booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn.execute("""
        INSERT INTO bookings (customer_name, movie_id, seats, total_amount, booking_date)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_name, movie_id, seats, total_amount, booking_date))

    conn.commit()
    conn.close()

    return jsonify({"message": "Booking Successful", "total_amount": total_amount})


# ---------------- API: GET BOOKINGS ----------------
@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    conn = get_db_connection()
    bookings = conn.execute("""
        SELECT bookings.booking_id, bookings.customer_name, movies.title, bookings.seats,
               bookings.total_amount, bookings.booking_date
        FROM bookings
        JOIN movies ON bookings.movie_id = movies.movie_id
    """).fetchall()

    conn.close()
    return jsonify([dict(b) for b in bookings])


# ---------------- API: DELETE BOOKING ----------------
@app.route("/api/bookings/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM bookings WHERE booking_id=?", (booking_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Booking Deleted Successfully"})


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    init_db()  # Auto create DB + insert sample data
    app.run(debug=True)