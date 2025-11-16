# paths.py
import os

# --- Base directory ---
BASE_DIR = os.path.dirname(__file__)

# --- Resource paths ---
HOME_BG_PATH = os.path.join(BASE_DIR, "backgrounds", "homepage_bg.jpg")
GAME_BG_PATH = os.path.join(BASE_DIR, "backgrounds", "gamepage_bg.jpg")
CUSTOM_BG_PATH = os.path.join(BASE_DIR, "backgrounds", "custompage_bg.jpg")

FONT_PATH = os.path.join(BASE_DIR, "fonts", "PixelifySans-Regular.ttf")
QUESTIONS_CSV_PATH = os.path.join(BASE_DIR, "questions.csv")
QUESTIONS_JSON_PATH = os.path.join(BASE_DIR, "questions.json")

ZINGO_FILE = os.path.join(BASE_DIR, "scripts", "script.zingo")


# --- Validate resources ---
if not os.path.exists(HOME_BG_PATH):
    raise FileNotFoundError(f"Background image not found: {HOME_BG_PATH}")

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font not found: {FONT_PATH}")
