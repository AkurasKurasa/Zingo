from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.lang import Builder
from PIL import Image
from screens.roulette_kivy import KV
from screens.Start_Page import StartPage
from screens.Game_Page import GamePage
from screens.Custom_Page import CustomPage
from screens.Roulette_Page import RoulettePage

import paths
import json


# --- original quiz window size ---
img = Image.open(paths.BG_PATH)
img_width, img_height = img.size
Window.size = (img_width, img_height)   

# --- load roulette kv string ---
Builder.load_string(KV)


class AllInApp(App):

    # --- reactive kivy properties ---
    POINTS = NumericProperty(100)
    QUESTIONS_IN_A_ROW = NumericProperty(0)

    # --- non-reactive constants ---
    QUESTION_INDEX = 0
    REQUIRED_POINTS = 1_000_000
    MULTIPLIER = 1

    # --- paths ---
    font_path = paths.FONT_PATH
    QUESTIONS_JSON_PATH = paths.QUESTIONS_JSON_PATH
    QUESTIONS = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_questions()

        # --- save quiz size ---
        self._quiz_size = (img_width, img_height)

        # --- roulette natural size: 800x600  ---
        self._roulette_size = (800, 600)

    # --- load questions from json file ---
    def load_questions(self):
        """loads questions into self.QUESTIONS."""
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
            print(f"error: question file not found at {self.QUESTIONS_JSON_PATH}")
        except json.JSONDecodeError:
            print(f"error: invalid json format in {self.QUESTIONS_JSON_PATH}")

    # --- switch to roulette ---
    def switch_to_roulette(self):
        """sets window to 800x600 and opens roulette_page."""
        print(f"[debug] opening roulette at {self._roulette_size}")
        Window.size = self._roulette_size
        self.root.transition = NoTransition()
        self.root.current = "roulette_page"

    # --- return to quiz ---
    def switch_back_from_roulette(self):
        """restores quiz window size."""
        print(f"[debug] restoring quiz size: {self._quiz_size}")
        Window.size = self._quiz_size
        self.root.current = "game_page"

    # --- build screen manager ---
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartPage(name="start_page", bg_path=paths.BG_PATH, font_path=paths.FONT_PATH))
        sm.add_widget(GamePage(name="game_page", font_path=paths.FONT_PATH))
        sm.add_widget(CustomPage(name="custom_page", font_path=paths.FONT_PATH))

        # --- inject callbacks ---
        rp = RoulettePage(name="roulette_page")
        rp.start_roulette = self.switch_to_roulette
        rp.end_roulette = self.switch_back_from_roulette
        # --- pass initial balance from current points ---
        rp.initial_balance = int(self.POINTS)
        sm.add_widget(rp)

        return sm


if __name__ == "__main__":
    AllInApp().run()