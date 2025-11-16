# screens/start_page.py
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.app import App

def switch_screen(instance, screen_manager, target_screen):
    screen_manager.current = target_screen

class StartPage(Screen):
    def __init__(self, bg_path, font_path, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background
        with layout.canvas:
            Color(0.2, 0, 0.7, 0.9)
            self.bg_rect = Rectangle(source=bg_path, pos=(0, 0), size=Window.size)
        Window.bind(on_resize=self.update_rect)

        # Title
        self.label = Label(
            text="All-In",
            font_size=81,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'top': 1.15},
            font_name=font_path
        )
        
        layout.add_widget(self.label)

        # Start
        start_btn = Button(
            text="Start",
            size=(150, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.02, 'y': 0.25},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=font_path,
            font_size=32
        )
        start_btn.bind(on_release=lambda instance: switch_screen(instance, self.manager, "game_page"))
        layout.add_widget(start_btn)

        # Custom
        custom_btn = Button(
            text="Custom",
            size=(150, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.03, 'y': 0.18},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=font_path,
            font_size=32
        )
        custom_btn.bind(on_release=lambda instance: switch_screen(instance, self.manager, "custom_page"))
        layout.add_widget(custom_btn)

        # Quit
        quit_btn = Button(
            text="Quit",
            size=(150, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.0025, 'y': 0.11},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=font_path,
            font_size=32
        )
        quit_btn.bind(on_release=lambda x: App.get_running_app().stop())
        layout.add_widget(quit_btn)

        self.add_widget(layout)

    def update_rect(self, instance, width, height):
        self.bg_rect.size = (width, height)
