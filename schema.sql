DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS movies;

CREATE TABLE movies (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    duration INTEGER NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    movie_id INTEGER NOT NULL,
    seats INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    booking_date TEXT NOT NULL,
    FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
);