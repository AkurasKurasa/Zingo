# main.py
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from PIL import Image

from screens.Start_Page import StartPage
from screens.Game_Page import GamePage
from screens.Custom_Page import CustomPage
from screens.Roulette_Page import RoulettePage

from dataclasses import dataclass
import paths
import json

# --- Window setup ---
img = Image.open(paths.HOME_BG_PATH)
img_width, img_height = img.size
Config.set('graphics', 'width', str(img_width))
Config.set('graphics', 'height', str(img_height))
Config.set('graphics', 'resizable', '0')
Window.size = (img_width, img_height)

# --- Data Structures ---
@dataclass
class Question:
    question_type: str
    question: str
    answer: str
    choices: list | None = None

class AllInApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Game States
        self.QUESTIONS = []
        self.QUESTION_INDEX = 0
        self.POINTS = 100 
        self.REQUIRED_POINTS = 102
        self.MULTIPLIER = 1
        self.QUESTIONS_IN_A_ROW = 0

        # PATHS
        self.font_path = paths.FONT_PATH
        self.QUESTIONS_JSON_PATH = paths.QUESTIONS_JSON_PATH

        # HELPER FUNCTIONS
        self.load_csv = self.load_questions

        self.load_questions()
    
    def load_questions(self):
        with open(paths.QUESTIONS_JSON_PATH, 'r') as file:
            data = json.load(file)
            questions = []
            for obj in data:
                question = {
                    'question_type': obj['question_type'],
                    'question': obj['question'],
                    'answer': obj['answer'],
                    'choices': obj['choices'] if 'choices' in obj else None
                }
            
                questions.append(question)
            
            self.QUESTIONS = questions

    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartPage(name="start_page", bg_path=paths.HOME_BG_PATH, font_path=paths.FONT_PATH))
        sm.add_widget(GamePage(name="game_page", bg_path=paths.GAME_BG_PATH, font_path=paths.FONT_PATH))
        sm.add_widget(CustomPage(name="custom_page", bg_path=paths.CUSTOM_BG_PATH ,font_path=paths.FONT_PATH))
        sm.add_widget(RoulettePage(name="roulette_page"))
        return sm

if __name__ == "__main__":
    AllInApp().run()
