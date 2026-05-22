import subprocess
import sys
import os

# Function to install a package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = [
    "opencv-python",           # OpenCV main package
    "opencv-contrib-python",   # OpenCV contrib modules (including face recognition)
    "Pillow",                  # For image manipulation (used by PIL)
    "numpy",                   # Numpy for numerical operations
    "scikit-learn",            # Scikit-learn for machine learning utilities (like cosine similarity)
    "datetime",                # Date and time library (part of Python's standard library, no need to install)
    "csv",                     # CSV handling (part of Python's standard library, no need to install)
    "time"                     # Time module for time handling (part of Python's standard library, no need to install)
]

# Try to import each package and install if missing
for package in required_packages:
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found. Installing...")
        install(package)

print("All required packages are installed.")

# Path to your main Python script
main_script = 'gui.py'  # Replace with the name of your main script

# Check if the main script exists
if os.path.exists(main_script):
    print(f"Running {main_script}...")
    subprocess.run([sys.executable, main_script])
else:
    print(f"Error: {main_script} not found.")
