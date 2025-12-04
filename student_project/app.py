
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ================= LOGIN PAGE ====================
@app.route("/", methods=["GET", "POST"])   # "/" → Login Page
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        # Simple login check
        if user == "admin" and pwd == "1234":
            return redirect("/home")  # After login → Home
        else:
            return render_template("login.html", message="Invalid Credentials!")

    return render_template("login.html")


# ================= HOME PAGE ======================
@app.route("/home")
def home():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    data = c.fetchall()
    conn.close()

    return render_template("index.html", students=data)


# ================= ADD STUDENT ====================
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        mob = request.form["mob"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO students (name, email, course, mob) VALUES (?, ?, ?, ?)",
                  (name, email, course, mob))
        conn.commit()
        conn.close()

        return redirect("/home")

    return render_template("add_student.html")


# ================= INIT DATABASE ==================
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        course TEXT,
        mob TEXT
    )
    """)
    conn.commit()
    conn.close()


init_db()


# ================= RUN APP =======================
if __name__ == "__main__":
    app.run(debug=True)
