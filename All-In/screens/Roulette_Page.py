from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App

class RoulettePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        self.app = App.get_running_app()


        # --- Congratulatory message ---
        label = Label(
            text="Congratulations!\nYou reached 5 correct answers in a row!",
            font_size=32,
            halign="center",
            valign="middle",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint_x=(0.7),
            font_name=self.app.font_path
        )

        label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        layout.add_widget(label)

        # --- Continue button ---
        continue_btn = Button(
            text="Continue",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            font_size=24,
            font_name=self.app.font_path
        )
        continue_btn.bind(on_release=self.go_back_to_game)
        layout.add_widget(continue_btn)

        self.add_widget(layout)

    def go_back_to_game(self, instance):
        game_page = self.manager.get_screen("game_page")
        game_page.continue_after_roulette()
        self.manager.current = "game_page"