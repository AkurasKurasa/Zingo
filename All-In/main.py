import tkinter as tk
from tkinter import filedialog, messagebox

# Create the main window
root = tk.Tk()
root.title("All In")
root.geometry("800x500")
root.config(bg="#751f1b")  # dark red background

# Create a darker frame to simulate the inner panel
frame = tk.Frame(root, bg="#5e1513", bd=20, relief="flat")
frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=400)

# Title Label
title_label = tk.Label(frame, text="All In", font=("Arial", 36, "bold"), bg="#5e1513", fg="white")
title_label.pack(pady=40)

# Button styling helper
def make_button(parent, text, command, bg_color, fg_color):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 18, "bold"),
        bg=bg_color,
        fg=fg_color,
        activebackground="#3a0c0b",
        activeforeground="white",
        relief="flat",
        width=15,
        height=1
    )

# Button commands
def start_game():
    messagebox.showinfo("Start", "Game started!")

def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        messagebox.showinfo("Uploaded", f"PDF Uploaded:\n{file_path}")

def exit_app():
    root.destroy()

# Buttons
make_button(frame, "Start", start_game, "#751f1b", "white").pack(pady=10)
make_button(frame, "Upload PDF", upload_pdf, "black", "white").pack(pady=10)
make_button(frame, "Exit", exit_app, "#751f1b", "white").pack(pady=10)

# Run the application
root.mainloop()
