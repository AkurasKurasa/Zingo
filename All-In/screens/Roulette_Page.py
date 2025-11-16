# screens/Roulette_Page.py
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder

# --- kv layout for roulette page ---
Builder.load_string('''
<RoulettePage>:
    name: "roulette_page"
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 8

        # --- fixed-height container for the ORIGINAL roulette UI ---
        BoxLayout:
            size_hint_y: None
            height: 540   # 500px wheel + 40px controls = perfect fit
            MainUI:
                id: main_ui
                balance: root.initial_balance
                size_hint: None, None
                size: self.parent.size   # fill the 540px box

        # --- collect & exit button (below everything) ---
        Button:
            text: "Collect & Exit"
            font_name: app.font_path if app.font_path else "Roboto"
            font_size: '16sp'
            size_hint_x: None          
            width: 180                 
            height: 44                 
            pos_hint: {'center_x': 0.5} # ← centered
            background_normal: ''
            background_color: 0, 0, 0, 1
            color: 1, 1, 1, 1
            on_release: root.collect_and_exit()
''')

class RoulettePage(Screen):
    initial_balance = NumericProperty(100)
    main_ui = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_roulette = None
        self.end_roulette = None

    def on_enter(self):
        """called when screen is shown."""
        if self.start_roulette:
            self.start_roulette()
        self.main_ui = self.ids.main_ui

    def collect_and_exit(self):
        """update points and return to quiz."""
        if self.main_ui:
            winnings = int(self.main_ui.balance)
            from kivy.app import App
            app = App.get_running_app()
            app.POINTS = winnings
        if self.end_roulette:
            self.end_roulette()