import os
import cv2
import numpy as np
import datetime
import time

# Automatically get the current working directory
base_dir = os.getcwd()

# Paths to the face data folder and detected faces folder within the current directory
face_data_dir = os.path.join(base_dir, 'faces')
detected_faces_dir = os.path.join(base_dir, 'detected_faces')

# Create detected faces directory if it doesn't exist
if not os.path.exists(detected_faces_dir):
    os.makedirs(detected_faces_dir)

# Prompt the user for name and roll number
name = input("Enter your name: ").lower()
roll_number = input("Enter your roll number: ")

# Combine name and roll number to create a unique folder name
folder_name = f"{name}_{roll_number}"

# Path for the user's face folder
user_face_folder = os.path.join(face_data_dir, folder_name)

# Create the user's face folder if it doesn't exist
if not os.path.exists(user_face_folder):
    os.makedirs(user_face_folder)
    print(f"Folder '{folder_name}' created successfully!")
else:
    print(f"Folder '{folder_name}' already exists.")

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Set a limit on the number of images per face
MAX_IMAGES_PER_FACE = 30

def detect_and_capture_faces():
    capture_count = 0
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while capture_count < MAX_IMAGES_PER_FACE:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Detect faces using the face cascade
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Instructions for capturing images
            cv2.putText(frame, "Press 'P' to capture image", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Display the frame
        cv2.imshow('Face Capture', frame)

        # Wait for key press
        key = cv2.waitKey(1) & 0xFF

        # Capture image on 'P' key press
        if key == ord('p') and len(faces) > 0:
            for (x, y, w, h) in faces:
                if capture_count < MAX_IMAGES_PER_FACE:
                    # Save grayscale images
                    face_image = gray[y:y + h, x:x + w]
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    cv2.imwrite(os.path.join(user_face_folder, f"{name}_{timestamp}_{capture_count + 1}.jpg"), face_image)
                    capture_count += 1
                    print(f"Captured {capture_count}/{MAX_IMAGES_PER_FACE} images for {name}.")
                if capture_count >= MAX_IMAGES_PER_FACE:
                    break

        # Quit on 'Q' key press
        if key == ord('q'):
            print("Exiting...")
            break

    print(f"Finished capturing {capture_count} images for {name}.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_and_capture_faces()
