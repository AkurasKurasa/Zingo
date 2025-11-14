# main.py
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.lang import Builder
from PIL import Image

from screens.Start_Page import StartPage
from screens.Game_Page import GamePage
from screens.Custom_Page import CustomPage
from screens.Roulette_Page import RoulettePage
from screens.roulette_kivy import KV 


import paths
import json

# --- Window setup ---
img = Image.open(paths.BG_PATH)
img_width, img_height = img.size
Config.set('graphics', 'width', str(img_width))
Config.set('graphics', 'height', str(img_height))
Config.set('graphics', 'resizable', '0')
Window.size = (img_width, img_height)
# --- Global KV Config ---
Builder.load_string(KV)

class AllInApp(App):

    # --- CONVERTED TO KIVY PROPERTIES ---
    POINTS = NumericProperty(100)
    QUESTIONS_IN_A_ROW = NumericProperty(0)

    # CONSTANTS 
    QUESTION_INDEX = 0
    REQUIRED_POINTS = 1_000_000
    MULTIPLIER = 1
    
    # PATHS
    font_path = paths.FONT_PATH
    QUESTIONS_JSON_PATH = paths.QUESTIONS_JSON_PATH
    QUESTIONS = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.load_questions()
    
    def load_questions(self):
        """Loads questions from the specified JSON file into self.QUESTIONS."""
        try:
            with open(self.QUESTIONS_JSON_PATH, 'r') as file:
                data = json.load(file)
                questions = []
                for obj in data:
                    question = {
                        'question_type': obj['question_type'],
                        'question': obj['question'],
                        'answer': obj['answer'],
                        'choices': obj.get('choices') 
                    }
                    questions.append(question)
                
                self.QUESTIONS = questions
        except FileNotFoundError:
            print(f"Error: Question file not found at {self.QUESTIONS_JSON_PATH}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.QUESTIONS_JSON_PATH}")


    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartPage(name="start_page", bg_path=paths.BG_PATH, font_path=paths.FONT_PATH))
        sm.add_widget(GamePage(name="game_page", font_path=paths.FONT_PATH))
        sm.add_widget(CustomPage(name="custom_page", font_path=paths.FONT_PATH))
        sm.add_widget(RoulettePage(name="roulette_page"))
        return sm

if __name__ == "__main__":
    AllInApp().run()
