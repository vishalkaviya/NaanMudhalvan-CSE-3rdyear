import tkinter as tk
import speech_recognition as sr
import random
import emoji
from tkinter import filedialog

# Function to recognize speech from a selected audio file
def recognize_speech(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        # Use Google Web Speech API to recognize the speech
        speech_text = recognizer.recognize_google(audio_data)
        print(f"Recognized Speech: {speech_text}")
        return speech_text
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio."
    except sr.RequestError:
        return "Sorry, there was an error with the speech recognition service."

# Function to extract number from text
def extract_number_from_text(text):
    words = text.split()  # Split the text into words
    print(f"Words extracted: {words}")
    # Try to find the first word that can be converted into an integer
    for word in words:
        try:
            return int(word)  # Try to convert each word into an integer
        except ValueError:
            continue  # If it can't be converted, skip it
    return None  # Return None if no valid number is found

# Function to check if the recognized number matches the generated random number
def check_guess():
    # Get the audio file selected by the user
    audio_file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])  # Open file dialog to browse audio
    
    if not audio_file:  # If no file is selected, show a message
        result_label.config(text="No audio file selected. Please try again.", fg='red')
        return
    
    # Get the recognized number from the audio file
    recognized_text = recognize_speech(audio_file)
    result_label.config(text=f"Recognized Text: {recognized_text}", fg="blue")  # Show recognized text in GUI for debugging
    
    # Extract the number from the recognized text
    recognized_number = extract_number_from_text(recognized_text)
    
    if recognized_number is None:
        result_label.config(text="Could not recognize a valid number! Try again.", fg='red')
        return
    
    # Generate a random number between 1 and 10
    random_number = random.randint(1, 10)
    
    # Compare the recognized number with the random number
    if recognized_number == random_number:
        result_label.config(text=f"You win! 🎉 Correctly guessed! \nThe random number was {random_number}.", fg='green')
        emoji_label.config(text=emoji.emojize(":trophy:"))  # Trophy emoji for winning
    else:
        result_label.config(text=f"Sorry, you lose! 😞 The random number was {random_number}. Try again!", fg='red')
        emoji_label.config(text=emoji.emojize(":cross_mark:"))  # Cross mark emoji for losing

# Create the main window
window = tk.Tk()
window.title("Speech Recognition Game")
window.geometry("500x350")
window.configure(bg="#FF8C8C")  # Pinkish-red background color

# Add an emoji as a label in the GUI
emoji_label = tk.Label(window, text=emoji.emojize(":question:"), font=("Arial", 50), bg="#FF8C8C")
emoji_label.pack(pady=20)

# Add a title label with a fancy font
title_label = tk.Label(window, text="Guess the Number Game", font=("Helvetica", 24), bg="#FF8C8C", fg="white")
title_label.pack(pady=10)

# Add a button to start the speech recognition and check the guess
check_button = tk.Button(window, text="Start Game", font=("Arial", 14), bg="#FF4C4C", fg="white", command=check_guess)
check_button.pack(pady=20)

# Add a label to display the result
result_label = tk.Label(window, text="Make your guess!", font=("Arial", 16), bg="#FF8C8C", fg="white")
result_label.pack(pady=20)

# Run the GUI loop
window.mainloop()
