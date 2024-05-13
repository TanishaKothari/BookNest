from flask import Flask, flash, render_template, redirect, session, request
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from utilities import apology, login_required
from flask_session import Session
from datetime import date

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect('booknest.db')
cursor = con.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
    author TEXT, genres TEXT)''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usersdb (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, 
    hash TEXT NOT NULL)''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS wishlist (user_id INTEGER, book_id INTEGER, book_name TEXT,
    FOREIGN KEY (user_id) REFERENCES usersdb(id), FOREIGN KEY (book_id) REFERENCES books(id))''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reading_history (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
    book_id INTEGER, book_name TEXT, date_read DATE, feedback TEXT,
    FOREIGN KEY (user_id) REFERENCES usersdb(id), FOREIGN KEY (book_id) REFERENCES books(id))''')

cursor.close()
con.close()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    con = sqlite3.connect('booknest.db')
    cursor = con.cursor()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        cursor.execute("SELECT * FROM usersdb WHERE username = ?", (request.form.get("username"),))
        rows = cursor.fetchall()

        cursor.close()
        con.close()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            print(rows)
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    con = sqlite3.connect('booknest.db')
    cursor = con.cursor()

    if request.method == "POST":
        # Get user inputs from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate inputs
        if not username:
            return apology("Username cannot be blank.")
        if cursor.execute("SELECT * FROM usersdb WHERE username = ?", (username,)).fetchone() is not None:
            return apology("Username already exists.")
        if not password or not confirmation:
            return apology("Password fields cannot be blank.")
        if password != confirmation:
            return apology("Passwords do not match.")

        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO usersdb (username, hash) VALUES(?, ?)", (username, hashed_password))
        con.commit()
        return redirect("/login")

    cursor.close()
    con.close()
    return render_template("register.html")


@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    user_preferences = {
        "title": request.form.get("title"),
        "genre": request.form.get("genre"),
        "author": request.form.get("author")
    }

    books = search_books(user_preferences)
    return render_template('search.html', books=books)


@app.route("/add_to_wishlist", methods=["GET", "POST"])
@login_required
def add_to_wishlist():
    user_id = session["user_id"]
    book_id = request.form.get("book_id")
    book_name = request.form.get("book_name")
    # Check if the book ID is valid
    if not book_id or not book_name:
        return apology("Invalid book ID")
    
    con = sqlite3.connect('booknest.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO wishlist (user_id, book_id, book_name) VALUES (?, ?, ?)", (user_id, book_id, book_name))
    con.commit()
    cursor.close()
    con.close()
    flash("Added to Wishlist")
    return redirect("/")


@app.route('/wishlist')
@login_required
def wishlist():
    con = sqlite3.connect('booknest.db')
    cursor = con.cursor()

    # Get the user's wishlist from the database
    cursor.execute("SELECT * FROM wishlist WHERE user_id = ?", (session["user_id"],))
    user_wishlist = cursor.fetchall()

    cursor.close()
    con.close()

    return render_template('wishlist.html', wishlist=user_wishlist)


@app.route("/add_to_reading_history", methods=["POST"])
@login_required
def add_to_reading_history():
    user_id = session["user_id"]
    book_id = request.form.get("book_id")
    book_name = request.form.get("book_name")
    feedback = request.form.get("feedback")
    # Check if the book ID is valid
    if not book_id or not book_name:
        return apology("Invalid book")
    
    con = sqlite3.connect('booknest.db')
    cursor = con.cursor()

    # Check if the book already exists in the user's reading history
    cursor.execute("SELECT * FROM reading_history WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # If the book already exists, update the feedback
        cursor.execute("UPDATE reading_history SET feedback = ? WHERE id = ?", (feedback, existing_entry[0]))
    else:
        flash("Marked as Read")
        cursor.execute("INSERT INTO reading_history (user_id, book_id, book_name, date_read, feedback) VALUES (?, ?, ?, ?, ?)", (user_id, book_id, book_name, date.today(), feedback))
    con.commit()
    
    cursor.execute("DELETE FROM wishlist WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    con.commit()

    cursor.close()
    con.close()
    return redirect("/")


@app.route('/reading_history')
@login_required
def reading_history():
    con = sqlite3.connect('booknest.db')
    cursor = con.cursor()

    # Get the user's reading history from the database
    cursor.execute("SELECT book_id, book_name, date_read FROM reading_history WHERE user_id = ? ORDER BY date_read DESC", (session["user_id"],))
    user_reading_history = cursor.fetchall()

    cursor.close()
    con.close()

    return render_template('reading_history.html', reading_history=user_reading_history)


@app.route('/recommendations')
@login_required
def recommendations():
    con = sqlite3.connect('booknest.db')
    cursor = con.cursor()

    # Generate recommendations based on genres
    # Get the user's liked books from the database
    cursor.execute("SELECT book_id FROM reading_history WHERE user_id = ? AND (feedback = 'Liked' OR feedback IS NULL)", (session["user_id"],))
    liked_books = cursor.fetchall()

    for liked_book in liked_books:
        # Get the genres of the liked book
        cursor.execute("SELECT genres FROM books WHERE id = ?", (liked_book[0],))
        liked_genres = cursor.fetchone()[0].split(', ')

    # Get the user's reading history from the database
    cursor.execute("SELECT * FROM reading_history WHERE user_id = ?", (session["user_id"],))
    user_reading_history = cursor.fetchall()

    # Extract book ids from reading history
    user_reading_ids = [row[2] for row in user_reading_history]

    recommended_books = []

    # Search for books with at least one genre in common with the liked book
    for genre in liked_genres:
        similar_books = search_books({"genre": genre})
        for book in similar_books:
            # Check if the book is not already in the recommendations list and not already read by the user
            if book not in recommended_books and book[0] not in user_reading_ids:
                recommended_books.append(book)

    # Get top 10 most popular books
    cursor.execute("SELECT book_id, COUNT(*) as cnt FROM reading_history GROUP BY book_id ORDER BY cnt DESC LIMIT 10")
    popular_books_data = cursor.fetchall()

    popular_books = []

    for popular_book_data in popular_books_data:
        cursor.execute("SELECT * FROM books WHERE id = ?", (popular_book_data[0],))
        popular_book = cursor.fetchone()
        popular_books.append(popular_book)

    cursor.close()
    con.close()

    return render_template('recommendations.html', recommended_books=recommended_books, popular_books=popular_books)


def search_books(user_preferences):
    # Build the SQL query based on user preferences
    con = sqlite3.connect('booknest.db')
    cursor = con.cursor()

    query = "SELECT * FROM books WHERE"
    params = []

    if user_preferences.get("title"):
        query += " title LIKE ? AND"
        params.append('%' + user_preferences["title"] + '%')

    if user_preferences.get("genre"):
        query += " genres LIKE ? AND"
        params.append('%' + user_preferences["genre"] + '%')

    if user_preferences.get("author"):
        query += " author LIKE ? AND"
        params.append('%' + user_preferences["author"] + '%')

    # Remove the trailing "AND" from the query
    query = query[:-4]

    # Execute the query
    cursor.execute(query, params)
    found_books = cursor.fetchall()

    cursor.close()
    con.close()
    
    return found_books

if __name__ == '__main__':
    app.run(debug=True)