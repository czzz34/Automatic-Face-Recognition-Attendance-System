import tkinter as tk
import subprocess
import os
from tkinter import messagebox
from PIL import Image, ImageTk

# Variable to track the processes
processes = {
    "view_records_admin_user": None,
    "view_records_user": None,
    "mark_attendance": None,
    "add_face": None
}

def terminate_process(process_key):
    """Terminate the process associated with a given key."""
    if processes[process_key]:
        try:
            processes[process_key].terminate()
            processes[process_key].wait(timeout=1)  # Wait for process to terminate
            processes[process_key] = None
        except Exception as e:
            processes[process_key].kill()  # Force kill if terminate fails
            processes[process_key] = None
            messagebox.showerror("Error", f"Failed to terminate {process_key}: {e}")

def mark_attendance():
    terminate_process("mark_attendance")
    try:
        processes["mark_attendance"] = subprocess.Popen(['python', 'poin.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to mark attendance: {e}")

def add_face():
    terminate_process("add_face")
    try:
        processes["add_face"] = subprocess.Popen(['python', 'attendance.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add face: {e}")

def toggle_view_records_admin_user():
    if processes["view_records_admin_user"] is None:
        # Start the process for admin/user view
        try:
            processes["view_records_admin_user"] = subprocess.Popen(['python', 'view attendance.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            btn_view_records_admin_user.config(bg="green", text="Stop View Records (Admin/User)")
            messagebox.showinfo("Server Status", "Server is running on the local network.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start view records (admin/user): {e}")
            processes["view_records_admin_user"] = None
    else:
        # Stop the process for admin/user view
        terminate_process("view_records_admin_user")
        btn_view_records_admin_user.config(bg="white", text="View Records (Admin/User)")

def toggle_view_records_user():
    if processes["view_records_user"] is None:
        # Start the process for user-only view
        try:
            processes["view_records_user"] = subprocess.Popen(['python', 'view attendance2.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            btn_view_records_user.config(bg="green", text="Stop View Records (User)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start view records (user): {e}")
            processes["view_records_user"] = None
    else:
        # Stop the process for user-only view
        terminate_process("view_records_user")
        btn_view_records_user.config(bg="white", text="View Records (User)")

def exit_program():
    """Terminate all processes and exit the program."""
    for key in processes:
        terminate_process(key)
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Attendance System")

# Set the window size
root.geometry("900x800")

# Load and set the background image
try:
    background_image = Image.open("att.png")
    background_image = background_image.resize((900, 800), Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
    bg_image = ImageTk.PhotoImage(background_image)

    # Create a label to hold the background image
    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load background image: {e}")

# Create buttons for the GUI
btn_mark_attendance = tk.Button(root, text="Mark Attendance", command=mark_attendance, width=30, bg="white")
btn_mark_attendance.pack(pady=10)

btn_add_face = tk.Button(root, text="Add Face", command=add_face, width=30, bg="white")
btn_add_face.pack(pady=10)

btn_view_records_admin_user = tk.Button(root, text="View Records (Admin/User)", command=toggle_view_records_admin_user, width=30, bg="white")
btn_view_records_admin_user.pack(pady=10)

btn_view_records_user = tk.Button(root, text="View Records (User)", command=toggle_view_records_user, width=30, bg="white")
btn_view_records_user.pack(pady=10)

btn_exit = tk.Button(root, text="Exit", command=exit_program, width=20, bg="white")
btn_exit.pack(pady=10)

# Start the main event loop
root.mainloop()
