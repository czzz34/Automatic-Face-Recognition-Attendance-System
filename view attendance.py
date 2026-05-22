from flask import Flask, render_template, request, redirect, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management and flashing messages

ADMIN_CREDENTIALS = {"username": "admin", "password": "1234"}  # Teacher login credentials

def get_unique_names():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM attendance")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

def get_attendance_records(search_name=None, search_month=None, search_roll=None):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    query = "SELECT * FROM attendance WHERE 1=1"
    params = []

    if search_name:
        query += " AND name = ?"
        params.append(search_name)
    if search_month:
        query += " AND month = ?"
        params.append(search_month)
    if search_roll:
        query += " AND roll_number = ?"
        params.append(search_roll)

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    conn.close()
    return data

def delete_attendance_record(roll_number, day, month, year):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM attendance WHERE roll_number = ? AND day = ? AND month = ? AND year = ?",
        (roll_number, day, month, year)
    )
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check for admin (teacher) credentials
        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            session['role'] = 'teacher'
            return redirect('/dashboard')

        # Check for student credentials
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM attendance WHERE name = ? AND roll_number = ?", (username, password))
        student = cursor.fetchone()
        conn.close()

        if student:
            session['role'] = 'student'
            session['username'] = username
            session['roll_number'] = password
            return redirect('/dashboard')

        flash("Invalid credentials. Please try again.", "error")
        return redirect('/')

    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'role' not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect('/')

    role = session['role']
    if role == 'teacher':
        # Teachers can see all records
        search_name = request.args.get('search_name')
        search_month = request.args.get('search_month')
        search_roll = request.args.get('search_roll')
        unique_names = get_unique_names()
        data = get_attendance_records(search_name, search_month, search_roll)
    elif role == 'student':
        # Students can only see their own records
        unique_names = []
        search_name = session['username']
        search_month = request.args.get('search_month')
        search_roll = session['roll_number']
        data = get_attendance_records(search_name, search_month, search_roll)

    return render_template(
        'meme.html',
        data=data,
        unique_names=unique_names,
        role=role
    )

@app.route('/delete', methods=['POST'])
def delete_record():
    if 'role' not in session or session['role'] != 'teacher':
        flash("You are not authorized to delete records.", "error")
        return redirect('/dashboard')

    roll_number = request.form.get('roll_number')
    day = request.form.get('day')
    month = request.form.get('month')
    year = request.form.get('year')

    delete_attendance_record(roll_number, day, month, year)
    flash("Record successfully deleted.", "success")
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
