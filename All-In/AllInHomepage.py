import customtkinter
from tkinter import Canvas
from PIL import Image, ImageTk

# Homepage for AllIn
app = customtkinter.CTk()
app.geometry("1080x720")
app.title("AllIn")

frame = customtkinter.CTkFrame(master=app, fg_color="#521515")
frame.pack(pady=10, padx=10, fill="both", expand=True)

logo_container = customtkinter.CTkFrame(master=frame, fg_color="#521515")
logo_container.pack(fill="x")

# Logo
logo_label = customtkinter.CTkLabel(
    master=frame,
    text="AllIN",
    font=("Arial", 48, "bold"),
    text_color="white"
)
logo_label.place(relx=0.5, rely=0.25, anchor="center")

# Button frame
button_frame = customtkinter.CTkFrame(master=frame, fg_color="#521515")
button_frame.pack(expand=True)

# Start Button
start_button = customtkinter.CTkButton(
    master=button_frame, 
    text="Start",
    fg_color=("#1E1E1E"),
    text_color="white",
    width=300,  
    height=50   
)
start_button.pack(pady=10, padx=10)

# Create Flashcards
create_button = customtkinter.CTkButton(
    master=button_frame, 
    text="Create Flashcards",
    fg_color=("#1E1E1E"),
    text_color="white",
    width=300,
    height=50
)
create_button.pack(pady=10, padx=10)

# Upload PDF
upload_button = customtkinter.CTkButton(
    master=button_frame, 
    text="Upload PDF",
    fg_color=("#1E1E1E"),
    text_color="white",
    width=300,
    height=50
)
upload_button.pack(pady=10, padx=10)

# Exit
exit_button = customtkinter.CTkButton(
    master=button_frame, 
    text="Exit",
    fg_color=("#1E1E1E"),
    text_color="white",
    width=300,
    height=50
)
exit_button.pack(pady=10, padx=10)

app.mainloop()
