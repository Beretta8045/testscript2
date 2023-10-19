from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import sha256_crypt
import random
import string
import secrets
import mysql.connector

app = Flask(__name)
app.secret_key = secrets.token_hex(32)  # Set a secret key for session management

# Function to check if a user is logged in
def is_logged_in():
    return 'logged_in' in session

# Database configuration (replace with your MySQL database details)
db_config = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'your_database',
}

# License Key Generation
def generate_license_key():
    key_length = 20  # Adjust the length as needed
    characters = string.ascii_letters + string.digits
    license_key = ''.join(random.choice(characters) for _ in range(key_length))
    return license_key

# Routes
@app.route("/", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = mysql.connector.connect(**db_config)
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
            # Generate and store the license key
            license_key = generate_license_key()
            
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO licenses (license_key) VALUES (%s)", (license_key,))
            connection.commit()
            connection.close()
            
            return render_template("index.html", license_key=license_key)
        
        return render_template("index.html")
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
