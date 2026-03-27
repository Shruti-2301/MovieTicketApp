// ---------------- MOVIES ----------------

let editMovieId = null;

function loadMovies() {
    fetch("/api/movies")
        .then(res => res.json())
        .then(data => {
            let table = document.getElementById("movieTable");
            table.innerHTML = "";

            data.forEach(movie => {
                table.innerHTML += `
                    <tr>
                        <td>${movie.movie_id}</td>
                        <td>${movie.title}</td>
                        <td>${movie.genre}</td>
                        <td>${movie.duration} min</td>
                        <td>₹${movie.price}</td>
                        <td>
                            <button onclick="editMovie(${movie.movie_id}, '${movie.title}', '${movie.genre}', ${movie.duration}, ${movie.price})">Edit</button>
                            <button onclick="deleteMovie(${movie.movie_id})">Delete</button>
                        </td>
                    </tr>
                `;
            });
        });
}

function addMovie() {
    let title = document.getElementById("title").value;
    let genre = document.getElementById("genre").value;
    let duration = document.getElementById("duration").value;
    let price = document.getElementById("price").value;

    if (title === "" || genre === "" || duration === "" || price === "") {
        alert("Please fill all fields!");
        return;
    }

    fetch("/api/movies", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: title,
            genre: genre,
            duration: duration,
            price: price
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        clearMovieForm();
        loadMovies();
    });
}

function editMovie(id, title, genre, duration, price) {
    editMovieId = id;

    document.getElementById("title").value = title;
    document.getElementById("genre").value = genre;
    document.getElementById("duration").value = duration;
    document.getElementById("price").value = price;

    document.getElementById("movieBtn").innerText = "Update Movie";
    document.getElementById("movieBtn").setAttribute("onclick", "updateMovie()");
}

function updateMovie() {
    let title = document.getElementById("title").value;
    let genre = document.getElementById("genre").value;
    let duration = document.getElementById("duration").value;
    let price = document.getElementById("price").value;

    if (title === "" || genre === "" || duration === "" || price === "") {
        alert("Please fill all fields!");
        return;
    }

    fetch(`/api/movies/${editMovieId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: title,
            genre: genre,
            duration: duration,
            price: price
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);

        clearMovieForm();
        loadMovies();
    });
}

function clearMovieForm() {
    editMovieId = null;

    document.getElementById("title").value = "";
    document.getElementById("genre").value = "";
    document.getElementById("duration").value = "";
    document.getElementById("price").value = "";

    document.getElementById("movieBtn").innerText = "Add Movie";
    document.getElementById("movieBtn").setAttribute("onclick", "addMovie()");
}

function deleteMovie(movie_id) {
    fetch(`/api/movies/${movie_id}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadMovies();
    });
}


// ---------------- BOOKINGS ----------------

function loadMovieDropdown() {
    fetch("/api/movies")
        .then(res => res.json())
        .then(data => {
            let dropdown = document.getElementById("movieDropdown");
            dropdown.innerHTML = `<option value="">-- Select Movie --</option>`;

            data.forEach(movie => {
                dropdown.innerHTML += `
                    <option value="${movie.movie_id}">
                        ${movie.title} (₹${movie.price})
                    </option>
                `;
            });
        });
}

function bookTicket() {
    let customer_name = document.getElementById("customer_name").value;
    let movie_id = document.getElementById("movieDropdown").value;
    let seats = document.getElementById("seats").value;

    if (customer_name === "" || movie_id === "" || seats === "") {
        alert("Please fill all booking fields!");
        return;
    }

    fetch("/api/bookings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            customer_name: customer_name,
            movie_id: movie_id,
            seats: seats
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert("Booking Successful! Total Amount: ₹" + data.total_amount);

            document.getElementById("customer_name").value = "";
            document.getElementById("movieDropdown").value = "";
            document.getElementById("seats").value = "";

            loadBookings();
        }
    });
}

function loadBookings() {
    fetch("/api/bookings")
        .then(res => res.json())
        .then(data => {
            let table = document.getElementById("bookingTable");
            table.innerHTML = "";

            data.forEach(b => {
                table.innerHTML += `
                    <tr>
                        <td>${b.booking_id}</td>
                        <td>${b.customer_name}</td>
                        <td>${b.title}</td>
                        <td>${b.seats}</td>
                        <td>₹${b.total_amount}</td>
                        <td>${b.booking_date}</td>
                        <td>
                            <button onclick="deleteBooking(${b.booking_id})">Cancel</button>
                        </td>
                    </tr>
                `;
            });
        });
}

function deleteBooking(booking_id) {
    fetch(`/api/bookings/${booking_id}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadBookings();
    });
}