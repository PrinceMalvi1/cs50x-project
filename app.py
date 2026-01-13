from flask import Flask, render_template, request, redirect, session, g, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

# --------------------
# CONFIGURATION
# --------------------
app = Flask(__name__)
app.secret_key = "cs50travel"
DATABASE = "database.db"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# --------------------
# DATABASE HELPERS
# --------------------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cur = db.cursor()
    # STUDENTS
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            school TEXT,
            route TEXT,
            photo TEXT
        )
    ''')
    # FEES
    cur.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            month TEXT,
            amount REAL,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')
    # ATTENDANCE
    cur.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')
    # VEHICLES
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_no TEXT,
            driver_name TEXT,
            route TEXT
        )
    ''')
    # FUEL LOG
    cur.execute('''
        CREATE TABLE IF NOT EXISTS fuel_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            date TEXT,
            fuel_type TEXT,
            amount_liters REAL,
            cost REAL,
            FOREIGN KEY(vehicle_id) REFERENCES vehicles(id)
        )
    ''')
    db.commit()

# Initialize DB on start
with app.app_context():
    init_db()

# --------------------
# ROUTES
# --------------------

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect("/dashboard")
        else:
            message = "Invalid Username or Password!"
    return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    db = get_db()
    cur = db.cursor()
    # Dashboard metrics
    cur.execute("SELECT COUNT(*) as total_students FROM students")
    total_students = cur.fetchone()["total_students"]
    cur.execute("SELECT COUNT(*) as total_vehicles FROM vehicles")
    total_vehicles = cur.fetchone()["total_vehicles"]
    cur.execute("SELECT SUM(amount) as total_fees FROM fees")
    total_fees = cur.fetchone()["total_fees"] or 0
    cur.execute("SELECT SUM(cost) as total_fuel FROM fuel_log")
    total_fuel = cur.fetchone()["total_fuel"] or 0
    return render_template("dashboard.html",
                           total_students=total_students,
                           total_vehicles=total_vehicles,
                           total_fees=total_fees,
                           total_fuel=total_fuel)

# --------------------
# STUDENTS
# --------------------
@app.route("/students")
def students():
    if "user" not in session:
        return redirect("/")
    cur = get_db().cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    return render_template("students.html", students=students)

@app.route("/add_student", methods=["GET","POST"])
def add_student():
    if "user" not in session:
        return redirect("/")
    if request.method == "POST":
        name = request.form["name"]
        school = request.form["school"]
        route = request.form["route"]
        photo_file = request.files.get("photo")
        if photo_file and photo_file.filename != "":
            filename = secure_filename(photo_file.filename)
            photo_file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = None
        cur = get_db().cursor()
        cur.execute("INSERT INTO students (name, school, route, photo) VALUES (?, ?, ?, ?)",
                    (name, school, route, filename))
        cur.connection.commit()
        return redirect("/students")
    return render_template("add_students.html")

# --------------------
# FEES
# --------------------
@app.route("/fees")
def fees():
    if "user" not in session:
        return redirect("/")
    cur = get_db().cursor()
    cur.execute('''
        SELECT fees.id, students.name, fees.month, fees.amount, fees.status
        FROM fees JOIN students ON fees.student_id = students.id
    ''')
    fees = cur.fetchall()
    return render_template("fees.html", fees=fees)

@app.route("/add_fee", methods=["GET","POST"])
def add_fee():
    if "user" not in session:
        return redirect("/")
    cur = get_db().cursor()
    if request.method == "POST":
        student_id = request.form["student_id"]
        month = request.form["month"]
        amount = request.form["amount"]
        status = request.form["status"]
        cur.execute("INSERT INTO fees (student_id, month, amount, status) VALUES (?, ?, ?, ?)",
                    (student_id, month, amount, status))
        cur.connection.commit()
        return redirect("/fees")
    cur.execute("SELECT id, name FROM students")
    students = cur.fetchall()
    return render_template("add_fee.html", students=students)

# --------------------
# ATTENDANCE
# --------------------
@app.route("/attendance")
def attendance():
    if "user" not in session:
        return redirect("/")
    cur = get_db().cursor()
    cur.execute('''
        SELECT attendance.id, students.name, attendance.date, attendance.status
        FROM attendance JOIN students ON attendance.student_id = students.id
    ''')
    attendance = cur.fetchall()
    return render_template("attendance.html", attendance=attendance)

@app.route("/mark_attendance", methods=["GET","POST"])
def mark_attendance():
    if "user" not in session:
        return redirect("/")
    cur = get_db().cursor()
    if request.method == "POST":
        student_id = request.form["student_id"]
        date = request.form["date"]
        status = request.form["status"]
        cur.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                    (student_id, date, status))
        cur.connection.commit()
        return redirect("/attendance")
    cur.execute("SELECT id, name FROM students")
    students = cur.fetchall()
    return render_template("mark_attendance.html", students=students)

# --------------------
# VEHICLES
# --------------------
@app.route("/vehicles")
def vehicles():
    if "user" not in session:
        return redirect("/")
    cur = get_db().cursor()
    cur.execute("SELECT * FROM vehicles")
    vehicles = cur.fetchall()
    cur.execute('''
        SELECT fuel_log.id, vehicles.vehicle_no, fuel_log.date, fuel_log.fuel_type, fuel_log.amount_liters, fuel_log.cost
        FROM fuel_log JOIN vehicles ON fuel_log.vehicle_id = vehicles.id
    ''')
    fuel_entries = cur.fetchall()
    return render_template("vehicles.html", vehicles=vehicles, fuel_entries=fuel_entries)

@app.route("/add_vehicle", methods=["GET","POST"])
def add_vehicle():
    if "user" not in session:
        return redirect("/")
    if request.method == "POST":
        vehicle_no = request.form["vehicle_no"]
        driver_name = request.form["driver_name"]
        route = request.form["route"]
        cur = get_db().cursor()
        cur.execute("INSERT INTO vehicles (vehicle_no, driver_name, route) VALUES (?, ?, ?)",
                    (vehicle_no, driver_name, route))
        cur.connection.commit()
        return redirect("/vehicles")
    return render_template("add_vehicle.html")

@app.route("/add_fuel", methods=["GET","POST"])
def add_fuel():
    if "user" not in session:
        return redirect("/")
    cur = get_db().cursor()
    if request.method == "POST":
        vehicle_id = request.form["vehicle_id"]
        date = request.form["date"]
        fuel_type = request.form["fuel_type"]
        amount = request.form["amount"]
        cost = request.form["cost"]
        cur.execute("INSERT INTO fuel_log (vehicle_id, date, fuel_type, amount_liters, cost) VALUES (?, ?, ?, ?, ?)",
                    (vehicle_id, date, fuel_type, amount, cost))
        cur.connection.commit()
        return redirect("/vehicles")
    cur.execute("SELECT id, vehicle_no FROM vehicles")
    vehicles = cur.fetchall()
    return render_template("add_fuel.html", vehicles=vehicles)

                                                                                                                                                                                                                                                                         # --------------------
                                                                                                                                                                                                                                                                    # RUN APP
                                                                                                                                                                                                                                                                            # --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)