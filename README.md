

---

# Automatic Face Recognition Attendance System

An automated attendance management system that utilizes computer vision to recognize faces and log attendance in real-time. The project features a dual-layer storage system (CSV and SQLite) and provides a secure Flask-powered web dashboard for users to review their records without risking data manipulation.

---


---

## 🚀 Desktop GUI Features (gui.py)

The main desktop application serves as the control panel for the system. It offers **5 primary operations**:

1. **Mark Attendance:** Activates the camera loop using OpenCV to detect enrolled faces and automatically log timestamps.
2. **Add Face:** Captures a sequence of images for a new user, associates them with a unique ID, and updates the recognition model.
3. **View Records (Admin):** Requires administrative login credentials. Grants full read and write access (PUSH / POST / DELETE) to modify, correct, or update attendance logs directly.
4. **View Records (User - Read-Only):** A strict read-only mode that locks out any data-modifying actions. Users can only perform GET requests, entirely eliminating the risk of accidental or unauthorized data manipulation.
5. **Start Web Server:** Launches the local background Flask utility to host the remote monitoring dashboard.

---

## 📊 Dual-Database Storage

To ensure data redundancy and quick access speeds, attendance entries are written simultaneously to two different formats:

* **attendance.db (SQLite):** Handles relational user profiling, login credentials, and structured logs for the Flask application.
* **attendance.csv (Comma-Separated Values):** Serves as a clean, lightweight flat-file backup that can be instantly opened in Microsoft Excel or Google Sheets for manual reporting.

---

## 🌐 Flask Web Dashboard

The project includes an embedded web server running on **Flask**.

* **Secure Access:** Employees or students can connect to the dashboard over the local network via their web browser.
* **Isolated Session:** After a secure login, users can review their personal chronological attendance history.
* **Zero-Tamper Design:** The web route explicitly blocks database write permissions for standard user sessions, ensuring logs remain completely safe and accurate.

---

## 📦 Prerequisites & Installation

### 1. Core Dependencies

Make sure you have Python installed alongside a working C++ compiler (required for some face recognition math packages).

### 2. Install Required Packages

```bash
pip install opencv-python flask numpy

```

*(Note: Add any additional packages you are importing, such as face_recognition, dlib, or specific GUI libraries like PyQt5).*

---

## 🏁 How to Use

1. **Enroll Users:** Open the desktop interface, select **Add Face**, and enter the user details to build the image training set.
2. **Run Attendance Mode:** Select **Mark Attendance** during check-in hours to let the webcam scan and log incoming faces.
3. **Launch the Dashboard:** Start the Flask application to allow team members to view their logs securely from their own devices.
