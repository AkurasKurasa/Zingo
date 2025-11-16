# screens/Roulette_Page.py
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

# --- KV LAYOUT ---
Builder.load_string('''
<RoulettePage>:
    name: "roulette_page"
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 8
        BoxLayout:
            size_hint_y: None
            height: 540
            MainUI:
                id: main_ui
                balance: root.initial_balance
                size_hint: None, None
                size: self.parent.size
        Button:
            text: "Collect & Exit"
            font_name: app.font_path if app.font_path else "Roboto"
            font_size: '20sp'
            size_hint_x: None
            width: 180
            height: 44
            pos_hint: {'center_x': 0.5}
            background_normal: ''
            background_color: 0, 0, 0, 1
            color: 1, 1, 1, 1
            on_release: root.collect_and_exit()
''')

class RoulettePage(Screen):
    initial_balance = NumericProperty(100)
    main_ui = ObjectProperty(None)
    _original_size = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        # SAVE ORIGINAL SIZE BEFORE SWITCH
        self._original_size = Window.size

        Window.size = (800, 600)

        app = App.get_running_app()
        self.initial_balance = app.POINTS

    def on_enter(self):
        self.main_ui = self.ids.main_ui

    def collect_and_exit(self):
        if self.main_ui:
            winnings = int(self.main_ui.balance)
            app = App.get_running_app()
            app.POINTS = winnings

            if winnings >= app.REQUIRED_POINTS:
                self.show_congrats()
                return

        self._restore_and_go_back()

    def _restore_and_go_back(self):
        if self._original_size:
            Window.size = self._original_size
        if self.manager:
            self.manager.current = "game_page"

    def show_congrats(self):
        from kivy.uix.label import Label
        from kivy.animation import Animation

        self.ids.main_ui.opacity = 0
        exit_btn = self.children[0].children[0]
        exit_btn.disabled = True
        exit_btn.opacity = 0

        congrats = Label(
            text="[b]CONGRATULATIONS![/b]\nYou reached the required points!",
            markup=True,
            font_size='32sp',
            color=(1, 0.9, 0.2, 1),
            font_name=App.get_running_app().font_path,
            halign='center',
            valign='middle',
            size_hint=(1, 1)
        )
        self.add_widget(congrats)
        anim = Animation(opacity=1, duration=1.0)
        anim.start(congrats)

        Clock.schedule_once(lambda dt: self._final_exit(), 4.0)

    def _final_exit(self):
        if self._original_size:
            Window.size = self._original_size
        if self.manager:
            self.manager.current = "start_page"