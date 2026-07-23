from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import base64
import uuid
from risk_engine import get_score, get_risk_level
from risk_engine import add_event
from risk_engine import (
    add_event,
    get_score,
    get_risk_level,
    get_events
)


app = Flask(__name__)

app.secret_key = "online_exam_secret_key"

DATABASE = "database.db"
LOG_FILE = "events.log"


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

        user=session["user"],
        risk_score=get_score(),
        risk_level=get_risk_level()

    )


# ==============================
# Logout
# ==============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ----------------------------
# Browser Event Logging
# ----------------------------

@app.route("/log_event", methods=["POST"])
def log_event():

    data = request.get_json()
    event = data.get("event")

    # Assign points based on the event
    if event == "Tab Switched":
        add_event(event, 3)

    elif event == "Window Lost Focus":
        add_event(event, 2)

    elif event == "Right Click Detected":
        add_event(event, 1)

    elif event in ["Copy Attempt", "Ctrl + C"]:
        add_event(event, 2)

    elif event in ["Paste Attempt", "Ctrl + V"]:
        add_event(event, 2)

    elif event == "Developer Tools Attempt":
        add_event(event, 5)

    from datetime import datetime

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}\n"
        )

    return jsonify({"status": "success"})

# ----------------------------
# Live Dashboard API
# ----------------------------

@app.route("/dashboard_data")
def dashboard_data():

    return jsonify({

        "score": get_score(),

        "level": get_risk_level(),

        "events": get_events()

    })

# ==============================
# Run Flask
# ==============================

if __name__ == "__main__":

    app.run(debug=True)
