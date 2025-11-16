import customtkinter as ctk
from tkinter import font, filedialog  
import os  
from PIL import Image, ImageFont
import matplotlib.font_manager as fm

ctk.set_appearance_mode("dark")
# Color theme (Change the json file for a different theme)
ctk.set_default_color_theme("All-In/Harlequin.json")

app = ctk.CTk()
app.geometry("1080x720")
app.title("AllIn")

font_dir = os.path.join(os.path.dirname(__file__), "MontserratFont")
montserrat_semibold_path = os.path.join(font_dir, "Montserrat-SemiBold.ttf")
montserrat_black_path = os.path.join(font_dir, "Montserrat-Black.ttf")

#Fonts
try:
    if not os.path.exists(montserrat_semibold_path):
        print(f"Warning: {montserrat_semibold_path} not found.")
        montserrat_semibold = ("Arial", 16) 
        montserrat_black = ("Arial", 36, "bold")  
        raise FileNotFoundError

    if not os.path.exists(montserrat_black_path):
        print(f"Warning: {montserrat_black_path} not found.")
        montserrat_semibold = ("Arial", 16)  
        montserrat_black = ("Arial", 36, "bold") 
        raise FileNotFoundError

    fm.fontManager.addfont(montserrat_semibold_path)
    fm.fontManager.addfont(montserrat_black_path)

    font_properties_semibold = fm.FontProperties(fname=montserrat_semibold_path)
    font_properties_black = fm.FontProperties(fname=montserrat_black_path)
    montserrat_semibold_name = font_properties_semibold.get_name()
    montserrat_black_name = font_properties_black.get_name()

    montserrat_semibold = (montserrat_semibold_name, 16, "normal")
    montserrat_black = (montserrat_black_name, 36, "bold")

    if montserrat_semibold_name not in font.families():
        print(f"Warning: {montserrat_semibold_name} not found.")
        montserrat_semibold = ("Arial", 16)
    if montserrat_black_name not in font.families():
        print(f"Warning: {montserrat_black_name} not found.")
        montserrat_black = ("Arial", 36, "bold")

except FileNotFoundError:
    print("Font files not found.")
    montserrat_semibold = ("Arial", 16)
    montserrat_black = ("Arial", 36, "bold")
except Exception as e:
    print(f"Font loading error: {e}")
    montserrat_semibold = ("Arial", 16)
    montserrat_black = ("Arial", 36, "bold")

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

def show_homepage():
    clear_window()

    # homepage frame 
    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Logo
    logo_label = ctk.CTkLabel(
        master=frame,
        text="AllIN",
        font=montserrat_black,  
    )
    logo_label.place(relx=0.5, rely=0.25, anchor="center")

    # Button frame 
    button_frame = ctk.CTkFrame(master=frame)
    button_frame.pack(expand=True, pady=100)

    # start icon
    start_icon_path = os.path.join(os.path.dirname(__file__), "png_icons", "start.png")
    start_image = ctk.CTkImage(light_image=Image.open(start_icon_path), dark_image=Image.open(start_icon_path), size=(24, 24)) if os.path.exists(start_icon_path) else None

    # Start Button
    start_button = ctk.CTkButton(
        master=button_frame, 
        text="Start Learning",
        width=300,  
        height=50,
        font=montserrat_semibold,  
        command=show_start_page,
        image=start_image,
        compound="left"
    )
    start_button.pack(pady=10, padx=10)

    # Create icon
    create_icon = os.path.join(os.path.dirname(__file__), "png_icons", "create.png")
    create_image = ctk.CTkImage(light_image=Image.open(create_icon), dark_image=Image.open(create_icon), size=(24, 24)) if os.path.exists(start_icon_path) else None

    # Create Flashcards Button 
    create_button = ctk.CTkButton(
        master=button_frame, 
        text="Create Flashcards",
        width=300,
        height=50,
        font=montserrat_semibold,  
        command=show_create_flashcards_page,
        image=create_image,
        compound="left"
    )
    create_button.pack(pady=10, padx=10)

    # Upload icon
    upload_icon = os.path.join(os.path.dirname(__file__), "png_icons", "upload.png")
    uplaod_image = ctk.CTkImage(light_image=Image.open(upload_icon), dark_image=Image.open(upload_icon), size=(24, 24)) if os.path.exists(start_icon_path) else None

    # Upload PDF Button 
    upload_button = ctk.CTkButton(
        master=button_frame, 
        text="Upload PDF",
        width=300,
        height=50,
        font=montserrat_semibold,  
        command=show_upload_pdf_page,
        image=uplaod_image,
        compound="left"
    )
    upload_button.pack(pady=10, padx=10)

    # Exit icon
    exit_icon = os.path.join(os.path.dirname(__file__), "png_icons", "exit.png")
    exit_image = ctk.CTkImage(light_image=Image.open(exit_icon), dark_image=Image.open(exit_icon), size=(24, 24)) if os.path.exists(start_icon_path) else None

    # Exit Button 
    exit_button = ctk.CTkButton(
        master=button_frame, 
        text="Exit",
        width=300,
        height=50,
        font=montserrat_semibold,  
        command=app.quit,
        image=exit_image,
        compound="left"
    )
    exit_button.pack(pady=10, padx=10)

def show_start_page():
    """Display the Start page."""
    clear_window()

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    title_label = ctk.CTkLabel(
        master=frame,
        text="Welcome to Start Page!",
        font=montserrat_black, 
    )
    title_label.pack(pady=50)

    # Back Button
    back_button = ctk.CTkButton(
        master=frame,
        text="Back to Home",
        width=200,
        height=40,
        font=montserrat_semibold,
        command=show_homepage
    )
    back_button.pack(pady=20)

def show_create_flashcards_page():
    """Display the Create Flashcards page."""
    clear_window()

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Title 
    title_label = ctk.CTkLabel(
        master=frame,
        text="Create Flashcards",
        font=montserrat_black,  
    )
    title_label.pack(pady=20)

    # Question input
    question_label = ctk.CTkLabel(
        master=frame,
        text="Question:",
        font=montserrat_semibold,  
    )
    question_label.pack(pady=5)
    question_entry = ctk.CTkEntry(
        master=frame,
        width=400,
        height=30,
        placeholder_text="Enter the question",
        font=montserrat_semibold 
    )
    question_entry.pack(pady=5)

    # Answer input
    answer_label = ctk.CTkLabel(
        master=frame,
        text="Answer:",
        font=montserrat_semibold,  
    )
    answer_label.pack(pady=5)
    answer_entry = ctk.CTkEntry(
        master=frame,
        width=400,
        height=30,
        placeholder_text="Enter the answer",
        font=montserrat_semibold  
    )
    answer_entry.pack(pady=5)

    save_button = ctk.CTkButton(
        master=frame,
        text="Save Flashcard",
        width=200,
        height=40,
        font=montserrat_semibold  
    )
    save_button.pack(pady=20)

    back_button = ctk.CTkButton(
        master=frame,
        text="Back to Home",
        width=200,
        height=40,
        font=montserrat_semibold,  
        command=show_homepage
    )
    back_button.pack(pady=10)

def show_upload_pdf_page():
    """Display the Upload PDF page."""
    clear_window()

    upload_frame = ctk.CTkFrame(master=app)
    upload_frame.pack(pady=10, padx=10, fill="both", expand=True)

    #App Title 
    title_label = ctk.CTkLabel(
        master=upload_frame,
        text="Upload PDF",
        font=montserrat_black,  
    )
    title_label.pack(pady=20)

    #Placeholder for selected file
    selected_file_label = ctk.CTkLabel(
        master=upload_frame,
        text="No file selected",
        font=montserrat_semibold,  
    )
    selected_file_label.pack(pady=10)

    #Upload Button (placeholder)
    upload_button = ctk.CTkButton(
        master=upload_frame,
        text="Select PDF File",
        width=200,
        height=40,
        font=montserrat_semibold  
    )
    upload_button.pack(pady=20)

    # Back Button 
    back_button = ctk.CTkButton(
        master=upload_frame,
        text="Back to Home",
        width=200,
        height=40,
        font=montserrat_semibold,  
        command=show_homepage
    )
    back_button.pack(pady=10)

show_homepage()
app.mainloop()
