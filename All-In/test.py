import customtkinter as ctk
from PIL import Image
import os

app = ctk.CTk()
app.geometry("800x600")
app.title("Image Test")

# ✅ Adjust this path
bg_path = os.path.join(os.path.dirname(__file__), "backgrounds", "homepage_bg.jpg")
print("Looking for:", bg_path)
print("Exists?", os.path.exists(bg_path))

if os.path.exists(bg_path):
    try:
        img = Image.open(bg_path)
        print("Image loaded:", img.size)
    except Exception as e:
        print("Image open failed:", e)
else:
    print("❌ Image not found! Check your folder structure.")
    app.mainloop()
    exit()

# ✅ Create CTkImage (True size)
bg_image_raw = Image.open(bg_path)
true_width, true_height = bg_image_raw.size

bg_image = ctk.CTkImage(
    light_image=bg_image_raw,
    dark_image=bg_image_raw,
    size=(true_width, true_height)
)
# ✅ Show image
label = ctk.CTkLabel(app, image=bg_image, text="")
label.image = bg_image
label.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()
