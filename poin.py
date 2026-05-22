import os
import cv2
import numpy as np
import datetime
import sqlite3
import csv
import time
from PIL import Image

# Automatically get the current working directory
base_dir = os.getcwd()

# Paths to the face data folder and detected faces folder within the current directory
face_data_dir = os.path.join(base_dir, 'faces')
detected_faces_dir = os.path.join(base_dir, 'detected_faces')

# Create detected faces directory if it doesn't exist
if not os.path.exists(detected_faces_dir):
    os.makedirs(detected_faces_dir)

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize the face recognizer (LBPH)
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Database setup
db_connection = sqlite3.connect("attendance.db")
db_cursor = db_connection.cursor()

# Create a table for attendance records if it doesn't already exist
db_cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    roll_number INTEGER,
    name TEXT,
    day TEXT,
    month TEXT,
    year TEXT,
    time TEXT,
    PRIMARY KEY (roll_number, day, month, year)
)
''')
db_connection.commit()

def extract_name_and_roll_number(full_name):
    if "_" in full_name:
        name, roll_number_str = full_name.rsplit('_', 1)
        try:
            roll_number = int(roll_number_str)
            return name, roll_number
        except ValueError:
            print(f"Error: Could not convert roll number '{roll_number_str}' to an integer.")
            return full_name, None
    else:
        print(f"Error: No roll number found in '{full_name}'.")
        return full_name, None

def mark_attendance(name, roll_number):
    now = datetime.datetime.now()
    day = now.strftime("%d")
    month = now.strftime("%m")
    year = now.strftime("%Y")
    time_12hr = now.strftime("%I:%M %p")

    # Check if already marked in the database
    db_cursor.execute('''
    SELECT * FROM attendance WHERE roll_number = ? AND day = ? AND month = ? AND year = ?
    ''', (roll_number, day, month, year))
    marked_today = db_cursor.fetchone() is not None

    if not marked_today:
        # Insert into database
        db_cursor.execute('''
        INSERT INTO attendance (roll_number, name, day, month, year, time)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (roll_number, name, day, month, year, time_12hr))
        db_connection.commit()

        # Append to CSV file
        csv_file = 'attendance.csv'
        headers = ['Roll Number', 'Name', 'Day', 'Month', 'Year', 'Time']

        # Check if file exists and write header only if it's a new file
        write_header = not os.path.exists(csv_file)

        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(headers)
            writer.writerow([roll_number, name, day, month, year, time_12hr])

        print(f"Attendance marked for {name} (Roll Number: {roll_number}) at {time_12hr} on {day}/{month}/{year}")
    else:
        print(f"{name} (Roll Number: {roll_number}) is already marked present for today.")

def get_images_and_labels():
    face_samples = []
    ids = []
    names = {}
    current_id = 0

    for name in os.listdir(face_data_dir):
        folder_path = os.path.join(face_data_dir, name)
        if not os.path.isdir(folder_path):
            continue

        for image_file in os.listdir(folder_path):
            if image_file.endswith('.jpg'):
                image_path = os.path.join(folder_path, image_file)
                img = Image.open(image_path).convert('L')
                img_np = np.array(img, 'uint8')

                face_id = current_id
                face_samples.append(img_np)
                ids.append(face_id)

        names[current_id] = name
        current_id += 1

    return face_samples, ids, names

faces, ids, names = get_images_and_labels()
recognizer.train(faces, np.array(ids))

def detect_and_recognize_faces():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    fps_start_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fps_end_time = time.time()
        time_diff = fps_end_time - fps_start_time
        fps = 1 / time_diff if time_diff > 0 else 0
        fps_start_time = fps_end_time

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            confidence_scaled = confidence / 100.0

            if confidence_scaled < 0.6:
                full_name = names.get(id_, "Unknown")
                name, roll_number = extract_name_and_roll_number(full_name)

                if name != "Unknown" and roll_number is not None:
                    mark_attendance(name, roll_number)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} ({confidence_scaled:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            else:
                name = "Unknown"
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                unknown_face = gray[y:y+h, x:x+w]
                cv2.imwrite(os.path.join(detected_faces_dir, f"Unknown_{timestamp}.jpg"), unknown_face)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, f"Unknown ({confidence_scaled:.2f})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2)

        cv2.imshow('Attendance System', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_and_recognize_faces()
    db_connection.close()
