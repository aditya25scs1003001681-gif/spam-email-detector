import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import tkinter as tk
from datetime import datetime


# ---------------- ML MODEL ----------------

data = pd.read_csv("spam.csv")

X = data["text"]
y = data["label"]

vectorizer = CountVectorizer()
X_vector = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vector, y)


# ---------------- FUNCTIONS ----------------

def save_history(msg, result):

    with open("history.txt", "a") as f:
        time = datetime.now()
        f.write(f"{time} | {msg} | {result}\n")


def check_spam():

    msg = entry.get()

    if msg == "":
        result_label.config(text="Enter message", fg="orange")
        return

    msg_vec = vectorizer.transform([msg])
    result = model.predict(msg_vec)[0]

    if result == "spam":

        result_label.config(
            text="SPAM DETECTED ❌",
            fg="red"
        )

        save_history(msg, "spam")

    else:

        result_label.config(
            text="NOT SPAM ✅",
            fg="green"
        )

        save_history(msg, "ham")


def clear_text():

    entry.delete(0, tk.END)
    result_label.config(text="")


# ---------------- LOGIN ----------------

def login():

    user = username.get()
    pas = password.get()

    if user == "admin" and pas == "1234":

        login_window.destroy()
        main_window()

    else:

        login_msg.config(text="Wrong login", fg="red")


# ---------------- MAIN WINDOW ----------------

def main_window():

    global entry, result_label

    root = tk.Tk()
    root.title("Spam Email Detection System")
    root.geometry("600x400")
    root.configure(bg="#111")

    title = tk.Label(
        root,
        text="AI Spam Email Detection",
        font=("Arial", 18, "bold"),
        bg="#111",
        fg="white"
    )
    title.pack(pady=10)

    entry = tk.Entry(
        root,
        width=50,
        font=("Arial", 12)
    )
    entry.pack(pady=10)

    tk.Button(
        root,
        text="Check",
        bg="blue",
        fg="white",
        width=10,
        command=check_spam
    ).pack(pady=5)

    tk.Button(
        root,
        text="Clear",
        bg="gray",
        fg="white",
        width=10,
        command=clear_text
    ).pack(pady=5)

    result_label = tk.Label(
        root,
        text="",
        font=("Arial", 14, "bold"),
        bg="#111"
    )
    result_label.pack(pady=20)

    root.mainloop()


# ---------------- LOGIN WINDOW ----------------

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x250")

tk.Label(login_window, text="Login", font=("Arial", 16)).pack(pady=10)

username = tk.Entry(login_window)
username.pack(pady=5)
username.insert(0, "admin")

password = tk.Entry(login_window, show="*")
password.pack(pady=5)
password.insert(0, "1234")

tk.Button(
    login_window,
    text="Login",
    command=login
).pack(pady=10)

login_msg = tk.Label(login_window, text="")
login_msg.pack()

login_window.mainloop()
