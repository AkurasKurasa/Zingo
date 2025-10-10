import customtkinter as ctk
from tkinter import font, filedialog  
import os  
from PIL import ImageFont


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1080x720")
app.title("AllIn")

font_dir = os.path.join(os.path.dirname(__file__), "fonts")
#font_dir = r"C:\Users\danie\OneDrive\Desktop\Documents\AllIn\static" Folder where font is saved
montserrat_regular_path = os.path.join(font_dir, "Montserrat-Regular.ttf")
montserrat_bold_path = os.path.join(font_dir, "Montserrat-Bold.ttf")

#Fonts
try:
    if os.path.exists(montserrat_regular_path):
        app.call("font", "create", "Montserrat", "-family", "Montserrat", "-file", montserrat_regular_path)
    else:
        print(f"Warning: {montserrat_regular_path} not found. Using default font.")
        montserrat_regular = ("Arial", 16) 
        montserrat_bold = ("Arial", 36, "bold")  
        raise FileNotFoundError

    if os.path.exists(montserrat_bold_path):
        app.call("font", "create", "MontserratBold", "-family", "Montserrat Bold", "-file", montserrat_bold_path)
    else:
        print(f"Warning: {montserrat_bold_path} not found. Using default font.")
        montserrat_regular = ("Arial", 16)  
        montserrat_bold = ("Arial", 36, "bold") 
        raise FileNotFoundError


    montserrat_regular = ("Montserrat", 16)
    montserrat_bold = ("Montserrat Bold", 36)
except FileNotFoundError:
    montserrat_regular = ("Arial", 16)
    montserrat_bold = ("Arial", 36, "bold")

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def show_homepage():

    clear_window()

    #homepage frame
    frame = ctk.CTkFrame(master=app, fg_color="#521515")
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    #Logo
    logo_label = ctk.CTkLabel(
        master=frame,
        text="AllIN",
        font=montserrat_bold,  
        text_color="white"
    )
    logo_label.place(relx=0.5, rely=0.25, anchor="center")

    # Button frame
    button_frame = ctk.CTkFrame(master=frame, fg_color="#521515")
    button_frame.pack(expand=True, pady=100)

    # Start Button
    start_button = ctk.CTkButton(
        master=button_frame, 
        text="Start",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=300,  
        height=50,
        font=montserrat_regular,  
        command=show_start_page
    )
    start_button.pack(pady=10, padx=10)

    # Create Flashcards Button
    create_button = ctk.CTkButton(
        master=button_frame, 
        text="Create Flashcards",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=300,
        height=50,
        font=montserrat_regular,  
        command=show_create_flashcards_page
    )
    create_button.pack(pady=10, padx=10)

    # Upload PDF Button
    upload_button = ctk.CTkButton(
        master=button_frame, 
        text="Upload PDF",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=300,
        height=50,
        font=montserrat_regular,  
        command=show_upload_pdf_page
    )
    upload_button.pack(pady=10, padx=10)

    # Exit Button
    exit_button = ctk.CTkButton(
        master=button_frame, 
        text="Exit",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=300,
        height=50,
        font=montserrat_regular,  
        command=app.quit
    )
    exit_button.pack(pady=10, padx=10)

def show_start_page():
    """Display the Start page."""
    clear_window()

    frame = ctk.CTkFrame(master=app, fg_color="#521515")
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    title_label = ctk.CTkLabel(
        master=frame,
        text="Welcome to Start Page!",
        font=montserrat_bold, 
        text_color="white"
    )
    title_label.pack(pady=50)

    # Back Button
    back_button = ctk.CTkButton(
        master=frame,
        text="Back to Home",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=200,
        height=40,
        font=montserrat_regular,
        command=show_homepage
    )
    back_button.pack(pady=20)

def show_create_flashcards_page():
    """Display the Create Flashcards page."""
    clear_window()

    flashcard_frame = ctk.CTkFrame(master=app, fg_color="#521515")
    flashcard_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Title
    title_label = ctk.CTkLabel(
        master=flashcard_frame,
        text="Create Flashcards",
        font=montserrat_bold,  
        text_color="white"
    )
    title_label.pack(pady=20)

    # Question input
    question_label = ctk.CTkLabel(
        master=flashcard_frame,
        text="Question:",
        font=montserrat_regular,  
        text_color="white"
    )
    question_label.pack(pady=5)
    question_entry = ctk.CTkEntry(
        master=flashcard_frame,
        width=400,
        height=30,
        placeholder_text="Enter the question",
        font=montserrat_regular 
    )
    question_entry.pack(pady=5)

    # Answer input
    answer_label = ctk.CTkLabel(
        master=flashcard_frame,
        text="Answer:",
        font=montserrat_regular,  
        text_color="white"
    )
    answer_label.pack(pady=5)
    answer_entry = ctk.CTkEntry(
        master=flashcard_frame,
        width=400,
        height=30,
        placeholder_text="Enter the answer",
        font=montserrat_regular  
    )
    answer_entry.pack(pady=5)

    #Save Button (placeholder)
    save_button = ctk.CTkButton(
        master=flashcard_frame,
        text="Save Flashcard",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=200,
        height=40,
        font=montserrat_regular  
    )
    save_button.pack(pady=20)

    #Back Button
    back_button = ctk.CTkButton(
        master=flashcard_frame,
        text="Back to Home",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=200,
        height=40,
        font=montserrat_regular,  
        command=show_homepage
    )
    back_button.pack(pady=10)

def show_upload_pdf_page():
    """Display the Upload PDF page."""
    clear_window()

    upload_frame = ctk.CTkFrame(master=app, fg_color="#521515")
    upload_frame.pack(pady=10, padx=10, fill="both", expand=True)

    #App Title
    title_label = ctk.CTkLabel(
        master=upload_frame,
        text="Upload PDF",
        font=montserrat_bold,  
        text_color="white"
    )
    title_label.pack(pady=20)

    #Placeholder for selected file
    selected_file_label = ctk.CTkLabel(
        master=upload_frame,
        text="No file selected",
        font=montserrat_regular,  
        text_color="white"
    )
    selected_file_label.pack(pady=10)

    #Upload Button (placeholder)
    upload_button = ctk.CTkButton(
        master=upload_frame,
        text="Select PDF File",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=200,
        height=40,
        font=montserrat_regular  
    )
    upload_button.pack(pady=20)

    # Back Button
    back_button = ctk.CTkButton(
        master=upload_frame,
        text="Back to Home",
        fg_color=("#1E1E1E"),
        text_color="white",
        width=200,
        height=40,
        font=montserrat_regular,  
        command=show_homepage
    )
    back_button.pack(pady=10)


show_homepage()

app.mainloop()
