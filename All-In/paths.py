# paths.py
import os

# --- Base directory ---
BASE_DIR = os.path.dirname(__file__)

# --- Resource paths ---
BG_PATH = os.path.join(BASE_DIR, "backgrounds", "allin_background.png")
FONT_PATH = os.path.join(BASE_DIR, "fonts", "PixelifySans-Regular.ttf")
QUESTIONS_CSV_PATH = os.path.join(BASE_DIR, "questions.csv")
QUESTIONS_JSON_PATH = os.path.join(BASE_DIR, "questions.json")


# --- Validate resources ---
if not os.path.exists(BG_PATH):
    raise FileNotFoundError(f"Background image not found: {BG_PATH}")

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font not found: {FONT_PATH}")
