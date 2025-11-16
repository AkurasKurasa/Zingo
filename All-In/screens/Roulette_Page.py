from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.clock import Clock
from screens.Roulette_Game import MainUI
import pygame

class RoulettePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.ui_built = False

    def on_enter(self):
        """Build MainUI once, show roulette wheel."""
        if not self.ui_built:
            ui = MainUI()  # <-- your roulette wheel
            self.add_widget(ui)  # add on top of placeholder layout
            self.ui_built = True

        # Start music
        Clock.schedule_once(self.start_music, 0.5)

    def start_music(self, dt=None):
        if hasattr(self.app, 'HEY_YA'):
            try:
                pygame.mixer.music.load(self.app.TUCA_DONKA)
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print("Failed to play music:", e)

    def on_leave(self):
        pygame.mixer.music.stop()

    def go_back_to_game(self, instance):
        game_page = self.manager.get_screen("game_page")
        game_page.continue_after_roulette()
        self.manager.current = "game_page"
