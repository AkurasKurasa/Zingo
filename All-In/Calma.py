import customtkinter as ctk
from tkinter import font, filedialog, messagebox
import os
from PIL import Image, ImageSequence, ImageDraw, ImageFont, ImageTk
import matplotlib.font_manager as fm
import random
import warnings

app = ctk.CTk()
app.geometry("800x450")
app.title("All-In")
app.resizable(True, True)


def homepage():
    # --- Clear previous widgets ---
    for widget in app.winfo_children():
        widget.destroy()

    # --- Load and darken the background image ---
    bg_path = os.path.join(os.path.dirname(__file__), "backgrounds", "homepage_bg.jpg")
    if not os.path.exists(bg_path):
        print("❌ Background image not found at:", bg_path)
        return

    # Load image and convert to RGBA
    bg_image_raw = Image.open(bg_path).convert("RGBA")

    # Create black background same size as image
    black_bg = Image.new("RGBA", bg_image_raw.size, (0, 0, 0, 255))

    # Blend the image with the black background (25% opacity)
    opacity = 0.25
    bg_image_dim = Image.blend(black_bg, bg_image_raw, opacity)

    # Convert to CTkImage
    true_width, true_height = bg_image_raw.size
    bg_image = ctk.CTkImage(
        light_image=bg_image_dim,
        dark_image=bg_image_dim,
        size=(true_width, true_height)
    )

    # --- Background Label (non-resizing) ---
    bg_label = ctk.CTkLabel(app, text="", image=bg_image)
    bg_label.image = bg_image
    bg_label.place(relx=0.5, rely=0.5, anchor="center")

    # --- Title ---
    title = ctk.CTkLabel(
        master=app,
        text="All-IN",
        font=("Montserrat Black", 72),
        text_color="#00FFC6"
    )
    title.place(relx=0.5, rely=0.15, anchor="center")

    # --- Menu Buttons ---
    menu_frame = ctk.CTkFrame(master=app, fg_color="transparent")
    menu_frame.place(relx=0.5, rely=0.55, anchor="center")

    button_kwargs = {
        "master": menu_frame,
        "width": 300,
        "height": 50,
        "corner_radius": 12,
        "fg_color": "#1F2833",
        "hover_color": "#00FFC6",
        "font": ("Montserrat SemiBold", 18),
        "text_color": "#C5C6C7",
    }

    ctk.CTkButton(**button_kwargs, text="Start Game", command=game_page).pack(pady=12)
    ctk.CTkButton(**button_kwargs, text="Create Questions", command=custom_page).pack(pady=12)

    exit_button_kwargs = button_kwargs.copy()
    exit_button_kwargs.update({"fg_color": "#661111", "hover_color": "#FF5555", "command": app.quit})
    ctk.CTkButton(**exit_button_kwargs, text="Exit").pack(pady=12)

def game_page():
    pass

def custom_page():
    pass

# HELPER FUNCTIONS

def clear_window():
    for widget in app.winfo_children():
        widget.destroy()
        

homepage()
app.mainloop()