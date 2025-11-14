from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from screens.roulette_kivy import MainUI, KV # Import MainUI and KV

class RoulettePage(Screen):
    
    roulette_game = ObjectProperty(None) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.main_layout = FloatLayout()
        self.add_widget(self.main_layout)

    def on_enter(self, *args):
        self.main_layout.clear_widgets()
        self.app.QUESTIONS_IN_A_ROW = 0 
        
        initial_balance = self.app.POINTS 
        
        # --- Roulette Game Widget ---
        self.roulette_game = MainUI(
            balance=initial_balance,
            # Add size_hint back to maximize it within RoulettePage
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 1) # <--- USE (1, 1) HERE
        )
        self.main_layout.add_widget(self.roulette_game)
        
        # Collect & Exit Button 
        exit_btn = Button(
            text="Collect Winnings & Exit",
            size_hint=(0.3, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0.02},
            font_size=20,
            font_name=self.app.font_path,
            background_color=(0.1, 0.4, 0.8, 1)
        )
        exit_btn.bind(on_release=self.go_back_to_game)
        self.main_layout.add_widget(exit_btn)
        
    def go_back_to_game(self, instance):
        if self.roulette_game:
             final_balance = self.roulette_game.balance
             self.app.POINTS = int(final_balance)
             print(f"Roulette event ended. New points: {self.app.POINTS}")
             self.main_layout.clear_widgets()
             self.roulette_game = None 

        self.manager.current = "game_page"