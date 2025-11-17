# paths.py
import os

# --- Base directory ---
BASE_DIR = os.path.dirname(__file__)

# --- Resource paths ---
HOME_BG_PATH = os.path.join(BASE_DIR, "backgrounds", "Start_Page_Final_BG.jpg")
GAME_BG_PATH = os.path.join(BASE_DIR, "backgrounds", "Game_Page_Final_BG.jpg")
CUSTOM_BG_PATH = os.path.join(BASE_DIR, "backgrounds", "Custom_Page_Final_BG.jpg")

ALL_IN_LOGO = os.path.join(BASE_DIR, "backgrounds", "All-In_Logo.png")

FONT_PATH = os.path.join(BASE_DIR, "fonts", "PixelifySans-Regular.ttf")
QUESTIONS_CSV_PATH = os.path.join(BASE_DIR, "questions.csv")
QUESTIONS_JSON_PATH = os.path.join(BASE_DIR, "questions.json")

UPDATE_POINTS_ZINGO = os.path.join(BASE_DIR, "scripts", "update_points.zingo")
UPDATE_MULTIPLIER_ZINGO = os.path.join(BASE_DIR, "scripts", "update_multiplier.zingo")
UPDATE_QUESTIONS_INDEX = os.path.join(BASE_DIR, "scripts", "update_questions_index.zingo")

HEY_YA = os.path.join(BASE_DIR, "audio", "Hey_Ya.mp3")
SODA_POP = os.path.join(BASE_DIR, "audio", "Soda_Pop.mp3")
MY_DISCO = os.path.join(BASE_DIR, "audio", "My_Disco.mp3")
TUCA_DONKA = os.path.join(BASE_DIR, "audio", "TUCA_DONKA.mp3")
CORRECT = os.path.join(BASE_DIR, "audio", "correct.mp3")
WRONG = os.path.join(BASE_DIR, "audio", "wrong.mp3")

# --- Validate resources ---
if not os.path.exists(HOME_BG_PATH):
    raise FileNotFoundError(f"Background image not found: {HOME_BG_PATH}")

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font not found: {FONT_PATH}")
