import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Define file paths for the source and input audio
SOURCE_VOICE_FILE = "source_voice.wav"  # Pre-recorded voice template (e.g., passphrase)
USER_VOICE_FILE = "user_input_voice.wav"  # User input audio for comparison

# Function to extract MFCC features from the audio file
def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, sr=16000)  # Load and resample to 16kHz
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Extract 13 MFCC features
    return np.mean(mfcc.T, axis=0)  # Return average MFCCs for the audio

# Function to compare two audio files using cosine similarity on MFCC features
def compare_audio(file1, file2):
    mfcc1 = extract_mfcc(file1)
    mfcc2 = extract_mfcc(file2)
    similarity = cosine_similarity([mfcc1], [mfcc2])
    return similarity[0][0]

# Function to handle user registration (recording the source voice)
def register_user():
    messagebox.showinfo("Registration", "Please upload your passphrase file to register.")
    file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    if file_path:
        # Save the uploaded file as the source voice template
        os.rename(file_path, SOURCE_VOICE_FILE)
        messagebox.showinfo("Registration", "Passphrase registered successfully! ✔️")
    else:
        messagebox.showerror("Registration Error", "No file selected. Please try again.")

# Function to handle user authentication (comparing input voice with source voice)
def authenticate_user():
    if not os.path.exists(SOURCE_VOICE_FILE):
        messagebox.showerror("Authentication Error", "No passphrase registered. Please register first. ❌")
        return

    messagebox.showinfo("Authentication", "Please upload your voice file to authenticate.")
    file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    if file_path:
        # Save the uploaded file as the user input voice
        os.rename(file_path, USER_VOICE_FILE)

        # Compare the source voice and the uploaded voice
        similarity = compare_audio(SOURCE_VOICE_FILE, USER_VOICE_FILE)
        print(f"Voice similarity: {similarity}")

        if similarity > 0.8:  # Threshold for voice match (adjust as necessary)
            messagebox.showinfo("Authentication", "Authentication successful! ✔️")
        else:
            messagebox.showerror("Authentication Error", "Authentication failed. Voice did not match. ❌")
    else:
        messagebox.showerror("Authentication Error", "No file selected. Please try again.")

# GUI setup using Tkinter
def create_gui():
    window = tk.Tk()
    window.title("Voice Authentication System")
    window.geometry("400x400")
    window.configure(bg="#F4A6C5")  # Reddish Pink background color

    # Header
    header = tk.Label(window, text="Voice Authentication", font=("Helvetica", 18, "bold"), fg="white", bg="#F4A6C5")
    header.pack(pady=20)

    # Register Button
    register_button = tk.Button(window, text="Register Voice", font=("Helvetica", 12), bg="#C04F7C", fg="white", command=register_user)
    register_button.pack(pady=10)

    # Authenticate Button
    authenticate_button = tk.Button(window, text="Authenticate", font=("Helvetica", 12), bg="#C04F7C", fg="white", command=authenticate_user)
    authenticate_button.pack(pady=10)

    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
