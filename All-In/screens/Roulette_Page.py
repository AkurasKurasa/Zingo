from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from screens.Roulette_Game import MainUI
import pygame

from kivy.core.window import Window

# Set window width and height (width, height)

class RoulettePage(Screen):
    initial_balance = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.ui_built = False

        # -------------------------
        # Python version of KV layout
        # -------------------------
        root_layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=8
        )

        # Top container (540 height)
        self.top_box = BoxLayout(
            size_hint_y=None,
            height=540
        )

        # Placeholder until UI is built
        self.main_ui_container = BoxLayout()
        self.top_box.add_widget(self.main_ui_container)

        # Button section
        collect_btn = Button(
            text="Collect & Exit",
            font_name=self.app.font_path if hasattr(self.app, "font_path") else "Roboto",
            font_size="20sp",
            size_hint_x=None,
            width=180,
            height=44,
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        collect_btn.bind(on_release=lambda *_: self.collect_and_exit())

        # Add widgets into page
        root_layout.add_widget(self.top_box)
        root_layout.add_widget(collect_btn)

        self.add_widget(root_layout)

    # ----------------------------
    # Build roulette wheel once
    # ----------------------------

    def on_enter(self):
        # Save original size
        self._original_size = Window.size

        if not self.ui_built:
            ui = MainUI()
            self.main_ui_container.clear_widgets()
            self.main_ui_container.add_widget(ui)
            self.ids_main_ui = ui
            self.ui_built = True

        # Set balance
        self.initial_balance = self.app.POINTS
        self.ids_main_ui.balance = self.initial_balance

    def on_leave(self):
        pygame.mixer.music.stop()

        # Restore original window size
        if hasattr(self, "_original_size"):
            Window.size = self._original_size

            # Schedule update_rect for GamePage after resize
            def resize_callback(dt):
                game_page = self.manager.get_screen("game_page")
                if hasattr(game_page, "update_rect"):
                    game_page.update_rect(Window, *Window.size)
                    # Also force UI labels to reposition if needed
                    game_page.show_all_widgets()

            Clock.schedule_once(resize_callback, 0.05)  # small delay ensures Window.size applied





    # ----------------------------
    # MUSIC CONTROL
    # ----------------------------
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

    # ----------------------------
    # EXIT BUTTON
    # ----------------------------
    def collect_and_exit(self):
        ui = self.ids_main_ui
        self.app.POINTS = ui.balance
        pygame.mixer.music.stop()
        self.manager.current = "game_page"

        
