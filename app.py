import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import signal

curr_dir = os.path.dirname(os.path.realpath(__file__))

# Function to start recording
def start_recording():
    global recording_process
    recording_process = subprocess.Popen(["zsh", "start_recording.sh"], preexec_fn=os.setsid)
    
def stop_recording():
    global recording_process
    if recording_process:
        os.killpg(os.getpgid(recording_process.pid), signal.SIGINT)
        recording_process = None

# Function to start prediction
def start_prediction():
    model_path = filedialog.askopenfilename(title="Select a Model for Prediction")
    file_path = filedialog.askopenfilename(title="Select a File for Prediction")
    if model_path and file_path:  # Only run prediction if a file is selected
        subprocess.run(["python3", "predict.py", model_path, file_path])
    

# Creating the main window
root = tk.Tk()
root.title("Application Wrapper")
root.geometry("300x300")

# Creating the buttons
prediction_button = tk.Button(root, text="Start Prediction", command=start_prediction)
prediction_button.pack(pady=20)

recording_button = tk.Button(root, text="Start Recording", command=start_recording)
recording_button.pack(pady=20)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack(pady=20)

# Start the GUI loop
root.mainloop()
