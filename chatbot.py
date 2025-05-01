import os
import requests
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

MODEL = "openai/gpt-3.5-turbo"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://mentalhealthchatbot.example",
    "X-Title": "Mental Health Chatbot",
    "Content-Type": "application/json"
}

mood_history = []
chat_y = 40  # initial y-coordinate

# API Communication
def get_ai_response(user_message):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a supportive and empathetic mental health chatbot."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        return f"[Error {response.status_code}] {response.text}"

# Mood Detection
def detect_mood(message):
    message = message.lower()
    if any(word in message for word in ["sad", "depressed", "cry", "unhappy"]):
        return "Sad"
    elif any(word in message for word in ["happy", "joy", "glad", "excited"]):
        return "Happy"
    elif any(word in message for word in ["angry", "mad", "furious"]):
        return "Angry"
    else:
        return "Neutral"

# Send a message
def send_message():
    user_message = user_entry.get()
    if user_message.strip() == "":
        return

    mood = detect_mood(user_message)
    mood_history.append(mood)

    display_message("You", user_message, color="#a53860", align="left")  # Neon Cyan
    user_entry.delete(0, tk.END)

    bot_response = get_ai_response(user_message)

    display_message("Bot", bot_response, color="#f27059", align="right")  # Neon Pink

# Display floating messages properly
def display_message(sender, message, color="#FFFFFF", align="left"):
    global chat_y
    text = f"{sender}: {message}"

    chars_per_line = 70  # rough estimate
    num_lines = (len(text) // chars_per_line) + 1

    if align == "left":
        x = 40
    else:
        x = 760

    canvas.create_text(
        x, chat_y,
        anchor="nw" if align == "left" else "ne",
        text=text,
        fill=color,
        font=("Helvetica", 14, "bold"),
        width=700  # wrap text width
    )

    chat_y += num_lines * 30  # move down based on text size

# Mood Graph Popup
def show_mood_graph():
    if not mood_history:
        messagebox.showinfo("Mood Graph", "No mood data yet! Start chatting first.")
        return

    moods = {"Happy": 0, "Sad": 0, "Angry": 0, "Neutral": 0}
    for mood in mood_history:
        moods[mood] += 1

    labels = list(moods.keys())
    values = list(moods.values())

    plt.style.use('dark_background')
    plt.figure(figsize=(7,5))
    plt.bar(labels, values, color=["lime", "cyan", "magenta", "grey"])
    plt.title("🌌 Your Emotional Journey")
    plt.xlabel("Mood")
    plt.ylabel("Occurrences")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("🛸 Mental Health Chatbot (Galaxy Edition)")
root.geometry("800x800")
root.resizable(False, False)

# Load Background Image
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=800, height=800)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# User Entry
user_entry = tk.Entry(root, font=("Helvetica", 14), bg="#ffa9da", fg="white", insertbackground="white", bd=0)
user_entry.place(x=20, y=700, width=600, height=40)
user_entry.bind("<Return>", lambda event=None: send_message())

# Send Button
send_button = tk.Button(root, text="🚀 Send", command=send_message, font=("Helvetica", 12),
                        bg="#8e44ad", fg="white", activebackground="#9b59b6", bd=0)
send_button.place(x=640, y=700, width=130, height=40)

# Mood Graph Button
mood_button = tk.Button(root, text="📈 Mood Graph", command=show_mood_graph, font=("Helvetica", 12),
                        bg="#f27059", fg="white", activebackground="#1abc9c", bd=0)
mood_button.place(x=320, y=750, width=150, height=40)

root.mainloop()
