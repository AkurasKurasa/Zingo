import customtkinter as ctk
from tkinter import font, filedialog, messagebox
import os
from PIL import Image, ImageSequence, ImageDraw, ImageFont, ImageTk
import matplotlib.font_manager as fm
import random
import warnings

warnings.filterwarnings("ignore", message="CTkLabel Warning")

ctk.set_appearance_mode("dark")
# Color theme
ctk.set_default_color_theme("../Anthracite.json")

app = ctk.CTk()
app.geometry("1025x550")
app.title("All-In")
app.resizable(False, False)

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

def homepage():
    clear_window()

    # --- Background ---
    bg_frame = ctk.CTkFrame(app, fg_color="#0B0C10")
    bg_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # --- Title (neon effect) ---
    title_shadow = ctk.CTkLabel(
        master=app,
        text="All-IN",
        font=("Montserrat Black", 72),
        text_color="#004B4B"
    )
    title_shadow.place(relx=0.5, rely=0.203, anchor="center")

    title = ctk.CTkLabel(
        master=app,
        text="All-IN",
        font=("Montserrat Black", 72),
        text_color="#00FFC6"
    )
    title.place(relx=0.5, rely=0.2, anchor="center")

    # --- Menu Frame (glass effect) ---
    menu_frame = ctk.CTkFrame(
        master=app,
        fg_color=("#11141C", "#11141C"),
        corner_radius=20,
        border_width=1,
        border_color="#1F2833"
    )
    menu_frame.place(relx=0.5, rely=0.55, anchor="center")

    # --- Load Icons ---
    def load_icon(filename):
        path = os.path.join(os.path.dirname(__file__), "png_icons", filename)
        if os.path.exists(path):
            return ctk.CTkImage(
                light_image=Image.open(path),
                dark_image=Image.open(path),
                size=(24, 24)
            )
        return None

    create_icon = load_icon("create.png")
    exit_icon = load_icon("exit.png")

    # --- Buttons ---
    button_kwargs = {
        "master": menu_frame,
        "width": 300,
        "height": 50,
        "corner_radius": 12,
        "fg_color": "#1F2833",
        "hover_color": "#00FFC6",
        "font": ("Montserrat SemiBold", 18),
        "text_color": "#C5C6C7",
        "compound": "left"
    }

    start_button = ctk.CTkButton(
        **button_kwargs,
        text="Start Game",
        command=show_quiz
    )
    start_button.pack(pady=12, padx=10)

    create_button = ctk.CTkButton(
        **button_kwargs,
        text="Create Questions",
        image=create_icon,
        command=show_create_flashcards_page
    )
    create_button.pack(pady=12, padx=10)

    exit_button_kwargs = button_kwargs.copy()
    exit_button_kwargs["fg_color"] = "#661111"
    exit_button_kwargs["hover_color"] = "#FF5555"

    exit_button = ctk.CTkButton(
        **exit_button_kwargs,
        text="Exit",
        image=exit_icon,
        command=app.quit
    )
    exit_button.pack(pady=12, padx=10)

    # --- Footer ---
    footer = ctk.CTkLabel(
        master=app,
        text="v1.0 — by All-IN Studios",
        font=("Montserrat Medium", 12),
        text_color="#6B6E70"
    )
    footer.place(relx=0.5, rely=0.95, anchor="center")



def start_game_page():
    pass

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

    # Allow resizing for this page
    app.resizable(True, True)

    # --- Main Frame ---
    frame = ctk.CTkFrame(master=app, fg_color="transparent")
    frame.pack(pady=30, padx=50, fill="both", expand=True)

    # --- TITLE ---
    ctk.CTkLabel(
        frame,
        text="Custom",
        font=montserrat_black,
        justify="center"
    ).pack(anchor="center", pady=(0, 30))

    # --- MAIN CONTENT WRAPPER (Two Columns) ---
    content_frame = ctk.CTkFrame(frame, fg_color="transparent")
    content_frame.pack(fill="both", expand=True)

    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    # =====================================================
    # LEFT COLUMN: CREATE QUESTION
    # =====================================================
    left_col = ctk.CTkFrame(content_frame, fg_color="#111217", corner_radius=15)
    left_col.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    ctk.CTkLabel(left_col, text="🧠 Create Question", font=montserrat_semibold).pack(
        anchor="w", pady=(15, 10), padx=15
    )

    question_types = ["Question-Answer", "True-or-False", "Multiple-Choice"]
    question_type_var = ctk.StringVar(value=question_types[0])

    # --- Question Type Dropdown ---
    ctk.CTkLabel(left_col, text="Question Type:", font=montserrat_semibold).pack(anchor="w", padx=15, pady=(0, 5))
    ctk.CTkOptionMenu(
        left_col,
        values=question_types,
        variable=question_type_var,
        command=lambda choice: render_dynamic_inputs(choice),
        width=250
    ).pack(anchor="w", padx=15, pady=(0, 15))

    # --- Dynamic Inputs ---
    dynamic_frame = ctk.CTkFrame(left_col, fg_color="transparent")
    dynamic_frame.pack(anchor="w", fill="x", padx=15, pady=(0, 15))

    def render_dynamic_inputs(q_type):
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        global current_question_entry, current_answer_entry

        # Question input
        ctk.CTkLabel(dynamic_frame, text="Question:", font=montserrat_semibold).pack(anchor="w", pady=(5, 0))
        current_question_entry = ctk.CTkEntry(
            dynamic_frame, width=350, height=35, placeholder_text="Enter the question"
        )
        current_question_entry.pack(anchor="w", pady=(0, 10))

        # Answer inputs (depending on type)
        if q_type == "Question-Answer":
            ctk.CTkLabel(dynamic_frame, text="Answer:", font=montserrat_semibold).pack(anchor="w", pady=(5, 0))
            current_answer_entry = ctk.CTkEntry(
                dynamic_frame, width=350, height=35, placeholder_text="Enter the answer"
            )
            current_answer_entry.pack(anchor="w", pady=(0, 5))

        elif q_type == "True-or-False":
            ctk.CTkLabel(dynamic_frame, text="Answer:", font=montserrat_semibold).pack(anchor="w", pady=(5, 0))
            bool_var = ctk.StringVar(value="True")
            current_answer_entry = bool_var
            ctk.CTkSwitch(
                dynamic_frame,
                text="True / False",
                variable=bool_var,
                onvalue="True",
                offvalue="False",
            ).pack(anchor="w", pady=(3, 5))

        elif q_type == "Multiple-Choice":
            ctk.CTkLabel(dynamic_frame, text="Correct Answer:", font=montserrat_semibold).pack(anchor="w", pady=(5, 0))
            current_answer_entry = ctk.CTkEntry(
                dynamic_frame, width=350, height=35, placeholder_text="Enter the correct answer"
            )
            current_answer_entry.pack(anchor="w", pady=(0, 10))

            ctk.CTkLabel(dynamic_frame, text="Other Choices:", font=montserrat_semibold).pack(anchor="w", pady=(5, 3))
            for i in range(3):
                ctk.CTkEntry(
                    dynamic_frame, width=350, height=35, placeholder_text=f"Enter choice {i+1}"
                ).pack(anchor="w", pady=(3, 3))

    render_dynamic_inputs(question_type_var.get())

    # --- Save button ---
    ctk.CTkButton(
        left_col, text="💾 Save Flashcard", width=200, height=40, command=save_flashcard
    ).pack(anchor="w", padx=15, pady=(10, 20))

    # =====================================================
    # RIGHT COLUMN: IMPORT SECTION
    # =====================================================
    right_col = ctk.CTkFrame(content_frame, fg_color="#111217", corner_radius=15)
    right_col.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

    ctk.CTkLabel(right_col, text="📄 Import", font=montserrat_semibold).pack(anchor="w", pady=(15, 10), padx=15)

    uploaded_pdfs = []

    def upload_pdfs():
        nonlocal uploaded_pdfs
        file_paths = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
        if file_paths:
            uploaded_pdfs = list(file_paths)
            filenames = [os.path.basename(f) for f in uploaded_pdfs]
            display_text = (
                f"✅ {len(filenames)} PDFs uploaded:\n" +
                "\n".join(filenames[:5]) +
                (f"\n...and {len(filenames)-5} more" if len(filenames) > 5 else "")
            )
            pdf_label.configure(text=display_text, justify="left")
        else:
            pdf_label.configure(text="❌ No PDFs selected")

    ctk.CTkButton(
        right_col, text="📤 Upload PDFs", width=200, height=40, command=upload_pdfs
    ).pack(anchor="w", padx=15, pady=(5, 10))

    pdf_label = ctk.CTkLabel(right_col, text="No PDFs uploaded yet", font=montserrat_semibold, justify="left")
    pdf_label.pack(anchor="w", padx=15, pady=(5, 30))

    # --- Back button ---
    ctk.CTkButton(frame, text="⬅ Back to Home", width=220, height=40, command=show_homepage).pack(anchor="center", pady=(30, 10))

homepage()

app.mainloop()
