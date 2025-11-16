import customtkinter as ctk
import random, math
from PIL import Image, ImageDraw, ImageFont, ImageTk

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("Elegant Roulette Wheel 🎡")
app.geometry("500x650")

# Roulette numbers (European layout)
numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27,
    13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1,
    20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

colors = ["#136f63" if n == 0 else "#e63946" if i % 2 == 0 else "#2b2d42" for i, n in enumerate(numbers)]

canvas_size = 400
wheel_canvas = ctk.CTkCanvas(app, width=canvas_size, height=canvas_size, bg="#1a1b26", highlightthickness=0)
wheel_canvas.pack(pady=20)

center = canvas_size // 2
radius = 180
angle = 0.0
spinning = False

try:
    font = ImageFont.truetype("arial.ttf", 14)
except:
    font = ImageFont.load_default()

def draw_wheel(current_angle):
    """Draws the roulette wheel rotated by current_angle degrees."""
    wheel = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wheel)
    num_slices = len(numbers)
    slice_angle = 360 / num_slices

    for i, (n, color) in enumerate(zip(numbers, colors)):
        start_angle = i * slice_angle + current_angle
        end_angle = start_angle + slice_angle
        draw.pieslice(
            [center - radius, center - radius, center + radius, center + radius],
            start=start_angle, end=end_angle,
            fill=color, outline="#1a1b26", width=2
        )

        # Draw number text
        text_angle = math.radians(start_angle + slice_angle / 2)
        text_x = center + math.cos(text_angle) * (radius - 30)
        text_y = center + math.sin(text_angle) * (radius - 30)
        text = str(n)
        bbox = draw.textbbox((0, 0), text, font=font)
        draw.text(
            (text_x - bbox[2] / 2, text_y - bbox[3] / 2),
            text, font=font, fill="white"
        )

    # Pointer now at the top (upward)
    pointer = [
        (center, center - radius - 5),      # Top middle
        (center - 10, center - radius + 25),  # Top-left
        (center + 10, center - radius + 25)   # Top-right
    ]
    draw.polygon(pointer, fill="yellow")

    return ImageTk.PhotoImage(wheel)

def get_winning_number(final_angle):
    """Determine which number the upward pointer (90°) lands on."""
    num_slices = len(numbers)
    slice_angle = 360 / num_slices
    # Adjust to pointer at 90° (top)
    adjusted = (90 - final_angle - (slice_angle / 2)) % 360
    index = int(adjusted // slice_angle) % num_slices
    return numbers[index]

def spin():
    global spinning, angle
    if spinning:
        return

    spinning = True
    spin_button.configure(state="disabled")
    result_label.configure(text="Spinning...")

    total_spins = random.uniform(5, 8) * 360
    deceleration_factor = random.uniform(0.97, 0.985)
    speed = 50.0

    def animate():
        nonlocal total_spins, speed
        global angle, spinning

        wheel_canvas.delete("all")
        wheel_img = draw_wheel(angle)
        wheel_canvas.create_image(center, center, image=wheel_img)
        wheel_canvas.image = wheel_img

        angle = (angle + speed) % 360
        total_spins -= speed
        speed *= deceleration_factor

        if speed > 0.3:
            app.after(16, animate)
        else:
            final_number = get_winning_number(angle)
            result_label.configure(text=f"🎯 Result: {final_number}")
            spin_button.configure(state="normal")
            spinning = False

    animate()

# UI setup
spin_button = ctk.CTkButton(app, text="SPIN 🎰", width=200, height=50, fg_color="#00bfa6", command=spin)
spin_button.pack(pady=20)

result_label = ctk.CTkLabel(app, text="Ready to spin!", font=("Arial", 18, "bold"), text_color="#FFD700")
result_label.pack(pady=10)

# Initial wheel
initial_img = draw_wheel(angle)
wheel_canvas.create_image(center, center, image=initial_img)
wheel_canvas.image = initial_img

app.mainloop()
