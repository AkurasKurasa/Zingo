# screens/start_page.py
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.app import App


class StartPage(Screen):
    def __init__(self, bg_path, font_path, **kwargs):
        super().__init__(**kwargs)

        self.bg_path = bg_path
        self.font_path = font_path

        # Main layout container
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        self._add_background()
        self._add_title()
        self._add_buttons()

    # ============================================================
    #                           UI ELEMENTS
    # ============================================================

    def _add_background(self):
        """Add and auto-resize background image."""
        with self.layout.canvas:
            Color(1, 1, 1, 0.5)
            self.bg_rect = Rectangle(source=self.bg_path, size=Window.size, pos=(0, 0))

        Window.bind(on_resize=self._update_bg_size)

    def _add_title(self):
        """Add main title label."""
        title = Label(
            text="All-In",
            font_size=81,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'top': 1.15},
            font_name=self.font_path
        )
        self.layout.add_widget(title)

    def _add_buttons(self):
        """Create and place Start, Custom, Quit buttons."""
        buttons = [
            ("Start",  0.02, 0.30, lambda: self._go_to("game_page")),
            ("Custom", 0.03, 0.20, lambda: self._go_to("custom_page")),
            ("Quit",   0.0025, 0.10, lambda: App.get_running_app().stop())
        ]

        for text, x_pos, y_pos, callback in buttons:
            self.layout.add_widget(self._make_button(text, x_pos, y_pos, callback))

    # ============================================================
    #                           HELPERS
    # ============================================================

    def _make_button(self, text: str, x_pos: float, y_pos: float, callback):
        """Reusable button with hover arrow."""
        btn = Button(
            text=text,
            size=(150, 50),
            size_hint=(None, None),
            pos_hint={'x': x_pos, 'y': y_pos},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=self.font_path,
            font_size=32
        )

        # Store original text
        btn.base_text = text

        # Bind click
        btn.bind(on_release=lambda *args: callback())

        # Bind hover detection
        Window.bind(mouse_pos=lambda *args: self._on_hover(btn, args[1]))

        return btn

    def _on_hover(self, btn, mouse_pos):
        """Adds '>' on hover and removes it when not hovered."""
        if not btn.get_parent_window():
            return  # Ignore if button is not displayed yet

        inside = btn.collide_point(*btn.to_widget(*mouse_pos))

        if inside:
            if not btn.text.startswith("> "):
                btn.text = f"> {btn.base_text}"
        else:
            btn.text = btn.base_text


    def _go_to(self, screen_name: str):
        """Screen switching shortcut."""
        if self.manager:
            self.manager.current = screen_name

    # ============================================================
    #                           EVENTS
    # ============================================================

    def _update_bg_size(self, instance, width, height):
        """Handle window resizes."""
        self.bg_rect.size = (width, height)
