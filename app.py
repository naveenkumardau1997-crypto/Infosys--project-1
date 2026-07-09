from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import base64
import uuid

app = Flask(__name__)

app.secret_key = "online_exam_secret_key"

DATABASE = "database.db"


# ==============================
# Create Database
# ==============================

def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS candidates(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT,

        email TEXT UNIQUE,

        mobile TEXT,

        password TEXT,

        photo TEXT

    )

    """)

    conn.commit()

    conn.close()


create_database()


# ==============================
# Home Page
# ==============================

@app.route("/")
def home():

    return render_template("index.html")


# ==============================
# Register
# ==============================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        password = request.form.get("password")
        photo = request.form.get("photo")

        hashed_password = generate_password_hash(password)

        photo_path = ""

        if photo:

            try:

                header, encoded = photo.split(",", 1)

                image_data = base64.b64decode(encoded)

                filename = f"{uuid.uuid4().hex}.png"

                upload_folder = os.path.join("static", "uploads")

                os.makedirs(upload_folder, exist_ok=True)

                filepath = os.path.join(upload_folder, filename)

                with open(filepath, "wb") as image_file:

                    image_file.write(image_data)

                photo_path = filepath

            except Exception as e:

                print("Photo Error:", e)

        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()

        try:

            cursor.execute("""

            INSERT INTO candidates
            (fullname,email,mobile,password,photo)

            VALUES(?,?,?,?,?)

            """,(

                fullname,
                email,
                mobile,
                hashed_password,
                photo_path

            ))

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return "Email Already Exists"

        conn.close()

        return redirect("/")

    return render_template("register.html")

# ==============================
# Login
# ==============================

@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM candidates WHERE email=?",

        (email,)

    )

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[4], password):

        session["user"] = {

            "id": user[0],
            "name": user[1],
            "email": user[2],
            "mobile": user[3],
            "photo": user[5]

        }

        return redirect("/dashboard")

    return """
    <h2 style='font-family:Arial;text-align:center;color:red;margin-top:100px;'>
    Invalid Email or Password
    </h2>

    <center>
        <a href="/">Go Back</a>
    </center>
    """

# ==============================
# Dashboard
# ==============================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/")

    return render_template(

        "dashboard.html",

        user=session["user"]

    )


# ==============================
# Logout
# ==============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==============================
# Run Flask
# ==============================

if __name__ == "__main__":

    app.run(debug=True)