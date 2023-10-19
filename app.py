from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
import psycopg2
import random
import string

app = Flask(__name)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# ... (previous code for the Flask app)

# Function to check if a user is logged in
def is_logged_in():
    return 'logged_in' in session

@app.route("/", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = psycopg2.connect(
            database="your_database",
            user="your_user",
            password="your_password",
            host="your_database_host",
            port="your_database_port"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        connection.close()

        if user_data and sha256_crypt.verify(password, user_data[0]):
            session['logged_in'] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/index", methods=["GET", "POST"])
def index():
    if is_logged_in():
        if request.method == "POST":
            # ... (license key generation and database storage as before)
        return render_template("index.html")
    else:
        return redirect(url_for("login"))

# ... (rest of the code for the Flask app)

if __name__ == "__main__":
    app.run(debug=True)
