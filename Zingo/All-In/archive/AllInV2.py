import customtkinter as ctk
from tkinter import font, filedialog, messagebox
import os
from PIL import Image, ImageFont
import matplotlib.font_manager as fm
import random

ctk.set_appearance_mode("dark")
# Color theme
ctk.set_default_color_theme("All-In/Anthracite.json")

app = ctk.CTk()
app.geometry("1080x720")
app.title("All-In")

# Data
flashcards = []
current_flashcard_index = 0
current_question_entry = None 
current_answer_entry = None 
selected_file_path = None 
# Quiz State Variables
current_quiz_index = 0
current_correct_answer = ""
current_quiz_entry = None # Modified to track the input Entry widget

# FONTS

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
    print("Font files not found. Using default fonts.")
    montserrat_semibold = ("Arial", 16)
    montserrat_black = ("Arial", 36, "bold")
except Exception as e:
    print(f"Font loading error: {e}. Using default fonts.")
    montserrat_semibold = ("Arial", 16)
    montserrat_black = ("Arial", 36, "bold")

# Main app window clearing

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()

# Functionalities

def save_flashcard():
    
    global current_question_entry, current_answer_entry

    question = current_question_entry.get().strip()
    answer = current_answer_entry.get().strip()

    if question and answer:
        flashcards.append({"question": question, "answer": answer})
        # Clear 
        current_question_entry.delete(0, 'end')
        current_answer_entry.delete(0, 'end')
        messagebox.showinfo("Success", f"Flashcard saved! Total flashcards: {len(flashcards)}")
    else:
        messagebox.showerror("Error", "Please enter both a question and an answer.")

def select_pdf_file(selected_file_label):
    """Opens a file dialog for PDF selection and updates the label."""
    global selected_file_path
    filepath = filedialog.askopenfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if filepath:
        selected_file_path = filepath
        filename = os.path.basename(filepath)
        selected_file_label.configure(text=f"Selected: {filename}")
        messagebox.showinfo("File Selected", f"PDF selected: {filename}")
    else:
        selected_file_path = None
        selected_file_label.configure(text="No file selected")

def process_pdf():
    #Temp PDF Processing
    global selected_file_path
    if selected_file_path:
        print(f"Processing PDF at: {selected_file_path}")
        messagebox.showinfo("Processing", "PDF processing started. (This is a placeholder for actual extraction/flashcard generation).")
    else:
        messagebox.showerror("Error", "Please select a PDF file first.")

def update_flashcard_display(question_label, answer_label, next_button, prev_button, flip_button):
    """Updates the display with the current flashcard's question."""
    global current_flashcard_index

    if not flashcards:
        question_label.configure(text="No Flashcards Available 😔")
        answer_label.configure(text="Go back and create some!")
        next_button.configure(state="disabled")
        prev_button.configure(state="disabled")
        flip_button.configure(state="disabled")
        return

    flip_button.configure(text="Flip Card")
    flashcard = flashcards[current_flashcard_index]
    question_label.configure(text=flashcard['question'])
    answer_label.configure(text="Click 'Flip Card' for Answer") 

    next_button.configure(state="normal" if current_flashcard_index < len(flashcards) - 1 else "disabled")
    prev_button.configure(state="normal" if current_flashcard_index > 0 else "disabled")
    flip_button.configure(state="normal")

def navigate_flashcard(direction, question_label, answer_label, next_button, prev_button, flip_button):
    # Moves Flashcards
    global current_flashcard_index
    new_index = current_flashcard_index + direction

    if 0 <= new_index < len(flashcards):
        current_flashcard_index = new_index
        update_flashcard_display(question_label, answer_label, next_button, prev_button, flip_button)

def flip_flashcard(answer_label, flip_button):
    """Toggles the display between question and answer."""
    flashcard = flashcards[current_flashcard_index]
    
    if answer_label.cget("text") == flashcard['answer']:
        answer_label.configure(text="Click 'Flip Card' for Answer")
        flip_button.configure(text="Flip Card")
    else:
        answer_label.configure(text=flashcard['answer'])
        flip_button.configure(text="Hide Answer")

# Quiz Function

def check_answer_input(feedback_label, next_q_button, check_button):
    """Checks the user's typed answer against the correct answer."""
    global current_quiz_entry, current_correct_answer
    
    if current_quiz_entry is None:
        return
        
    user_answer = current_quiz_entry.get().strip()
    
    if not user_answer:
        feedback_label.configure(text="Please type your answer.", text_color="yellow")
        return

    if user_answer.lower() == current_correct_answer.lower():
        feedback_label.configure(text="Correct! 🎉", text_color="green")
    else:
        feedback_label.configure(text=f"Incorrect. The answer was: {current_correct_answer}", text_color="red")
        
    next_q_button.configure(state="normal")
    check_button.configure(state="disabled")

def advance_quiz(quiz_frame):
    global current_quiz_index
    current_quiz_index += 1
    update_quiz_display(quiz_frame)

def update_quiz_display(frame):
    global current_quiz_index, current_correct_answer, current_quiz_entry

    for widget in frame.winfo_children():
        widget.destroy()

    if not flashcards:
        ctk.CTkLabel(frame, text="No Flashcards Available for Quiz 😔", font=montserrat_black).pack(pady=50)
        ctk.CTkButton(frame, text="Back to Home", font=montserrat_semibold, command=show_homepage).pack(pady=20)
        return

    if current_quiz_index >= len(flashcards):
        ctk.CTkLabel(frame, text="Quiz Finished! Well Done! 🎉", font=montserrat_black).pack(pady=50)
        ctk.CTkButton(frame, text="Start Again", font=montserrat_semibold, command=show_quiz).pack(pady=20)
        ctk.CTkButton(frame, text="Back to Home", font=montserrat_semibold, command=show_homepage).pack(pady=10)
        return

    card = flashcards[current_quiz_index]
    question = card['question']
    current_correct_answer = card['answer']

    # Title/Progress
    ctk.CTkLabel(
        frame,
        text=f"Question {current_quiz_index + 1}/{len(flashcards)}",
        font=montserrat_semibold
    ).pack(pady=(10, 5))

    # Question Display
    ctk.CTkLabel(
        frame,
        text=question,
        font=montserrat_black,
        wraplength=700,
        justify="center"
    ).pack(pady=(5, 30))

    # User Input Field
    question_label = ctk.CTkLabel(
        frame,
        text="Your Answer:",
        font=montserrat_semibold,
    )
    question_label.pack(pady=5)
    
    answer_entry = ctk.CTkEntry(
        frame,
        width=400,
        height=40,
        placeholder_text="Type your answer here",
        font=montserrat_semibold
    )
    answer_entry.pack(pady=5)
    current_quiz_entry = answer_entry # Store reference globally for check_answer_input

    # Feedback Label
    feedback_label = ctk.CTkLabel(frame, text="", font=montserrat_semibold)
    feedback_label.pack(pady=20)

    # Control Frame for Buttons
    control_frame = ctk.CTkFrame(frame, fg_color="transparent")
    control_frame.pack(pady=10)
    
    # Next Question Button 
    next_q_button = ctk.CTkButton(
        control_frame,
        text="Next Question",
        width=200,
        height=40,
        font=montserrat_semibold,
        command=lambda: advance_quiz(frame),
        state="disabled"
    )
    next_q_button.grid(row=0, column=1, padx=10)

    # Check Button
    check_button = ctk.CTkButton(
        control_frame,
        text="Check Answer",
        width=200,
        height=40,
        font=montserrat_semibold,
        command=lambda: check_answer_input(feedback_label, next_q_button, check_button)
    )
    check_button.grid(row=0, column=0, padx=10)

    # Back to Home Button
    ctk.CTkButton(
        frame,
        text="Back to Home",
        width=200,
        height=40,
        font=montserrat_semibold,
        command=show_homepage
    ).pack(pady=30)
    

def show_quiz():
    """Display the Quiz page."""
    global current_quiz_index
    clear_window()
    current_quiz_index = 0

    quiz_frame = ctk.CTkFrame(master=app)
    quiz_frame.pack(pady=10, padx=10, fill="both", expand=True)

    title_label = ctk.CTkLabel(
        master=quiz_frame,
        text="Flashcard Quiz (Input Mode)",
        font=montserrat_black,
    )
    title_label.pack(pady=20)
    
    # Frame for dynamic question/options
    question_container = ctk.CTkFrame(quiz_frame, fg_color="transparent")
    question_container.pack(pady=10, fill="x", expand=True)

    update_quiz_display(question_container)

# PAGE DISPLAY FUNCTIONS

def show_homepage():
    clear_window()

    # homepage frame
    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Logo
    logo_label = ctk.CTkLabel(
        master=frame,
        text="All-IN",
        font=montserrat_black,
    )
    logo_label.place(relx=0.5, rely=0.15, anchor="center")

    # Button frame
    button_frame = ctk.CTkFrame(master=frame)
    button_frame.pack(expand=True, pady=100)

    # start icon
    start_icon_path = os.path.join(os.path.dirname(__file__), "png_icons", "start.png")
    start_image = ctk.CTkImage(light_image=Image.open(start_icon_path), dark_image=Image.open(start_icon_path), size=(24, 24)) if os.path.exists(start_icon_path) else None

    # Start Learning Button (Reviewer)
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
    create_image = ctk.CTkImage(light_image=Image.open(create_icon), dark_image=Image.open(create_icon), size=(24, 24)) if os.path.exists(create_icon) else None

    # Start Quiz Button 
    quiz_button = ctk.CTkButton(
        master=button_frame,
        text="Start Quiz",
        width=300,
        height=50,
        font=montserrat_semibold,
        command=show_quiz,
        compound="left"
    )
    quiz_button.pack(pady=10, padx=10)
    
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
    upload_image = ctk.CTkImage(light_image=Image.open(upload_icon), dark_image=Image.open(upload_icon), size=(24, 24)) if os.path.exists(upload_icon) else None

    # Upload PDF Button
    upload_button = ctk.CTkButton(
        master=button_frame,
        text="Upload PDF",
        width=300,
        height=50,
        font=montserrat_semibold,
        command=show_upload_pdf_page,
        image=upload_image,
        compound="left"
    )
    upload_button.pack(pady=10, padx=10)

    # Exit icon
    exit_icon = os.path.join(os.path.dirname(__file__), "png_icons", "exit.png")
    exit_image = ctk.CTkImage(light_image=Image.open(exit_icon), dark_image=Image.open(exit_icon), size=(24, 24)) if os.path.exists(exit_icon) else None

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
    """Display the Start page with Flashcard Reviewer."""
    global current_flashcard_index
    clear_window()
    current_flashcard_index = 0 # Reset index when entering the review page

    frame = ctk.CTkFrame(master=app)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    title_label = ctk.CTkLabel(
        master=frame,
        text="Flashcard Review",
        font=montserrat_black,
    )
    title_label.pack(pady=20)

    # Flashcard Display Frame
    card_frame = ctk.CTkFrame(master=frame, width=500, height=300, corner_radius=10)
    card_frame.pack(pady=20, padx=20, fill="x")
    card_frame.pack_propagate(False) 

    question_label = ctk.CTkLabel(
        master=card_frame,
        text="",
        font=montserrat_black,
        wraplength=450,
        justify="center"
    )
    question_label.pack(pady=(50, 10))

    answer_label = ctk.CTkLabel(
        master=card_frame,
        text="",
        font=montserrat_semibold,
        wraplength=450,
        justify="center"
    )
    answer_label.pack(pady=10)

    # Control Frame
    control_frame = ctk.CTkFrame(master=frame)
    control_frame.pack(pady=10)

    # Flip Button
    flip_button = ctk.CTkButton(
        master=control_frame,
        text="Flip Card",
        width=150,
        height=40,
        font=montserrat_semibold,
        command=lambda: flip_flashcard(answer_label, flip_button)
    )
    flip_button.grid(row=0, column=1, padx=10)

    # Navigation Buttons
    prev_button = ctk.CTkButton(
        master=control_frame,
        text="< Previous",
        width=150,
        height=40,
        font=montserrat_semibold,
        command=lambda: navigate_flashcard(-1, question_label, answer_label, next_button, prev_button, flip_button)
    )
    prev_button.grid(row=0, column=0, padx=10)

    next_button = ctk.CTkButton(
        master=control_frame,
        text="Next >",
        width=150,
        height=40,
        font=montserrat_semibold,
        command=lambda: navigate_flashcard(1, question_label, answer_label, next_button, prev_button, flip_button)
    )
    next_button.grid(row=0, column=2, padx=10)

    # Initial display update
    update_flashcard_display(question_label, answer_label, next_button, prev_button, flip_button)

    # Back Button
    back_button = ctk.CTkButton(
        master=frame,
        text="Back to Home",
        width=200,
        height=40,
        font=montserrat_semibold,
        command=show_homepage
    )
    back_button.pack(pady=50)

def show_create_flashcards_page():
    """Display the Create Flashcards page."""
    global current_question_entry, current_answer_entry
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
    current_question_entry = question_entry # Store reference

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
    current_answer_entry = answer_entry # Store reference

    # Save button (now functional)
    save_button = ctk.CTkButton(
        master=frame,
        text="Save Flashcard",
        width=200,
        height=40,
        font=montserrat_semibold,
        command=save_flashcard # Link to new function
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

    # App Title
    title_label = ctk.CTkLabel(
        master=upload_frame,
        text="Upload PDF",
        font=montserrat_black,
    )
    title_label.pack(pady=20)

    # Placeholder for selected file
    selected_file_label = ctk.CTkLabel(
        master=upload_frame,
        text="No file selected",
        font=montserrat_semibold,
    )
    selected_file_label.pack(pady=10)

    select_button = ctk.CTkButton(
        master=upload_frame,
        text="Select PDF File",
        width=200,
        height=40,
        font=montserrat_semibold,
        command=lambda: select_pdf_file(selected_file_label)
    )
    select_button.pack(pady=20)

    # Non-functional Process pDF
    process_button = ctk.CTkButton(
        master=upload_frame,
        text="Process PDF",
        width=200,
        height=40,
        font=montserrat_semibold,
        command=process_pdf
    )
    process_button.pack(pady=10)

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
