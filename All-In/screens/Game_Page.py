# screens/game_page.py
from functools import partial
from typing import Optional, Iterable, List, Any

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from utils.zingo_engine import ZingoEngine


from widgets.confetti import ConfettiWidget
import random


def switch_screen(instance, manager, screen_name: str) -> None:
    """Safe screen switch helper (keeps previous behavior)."""
    if manager and screen_name in manager.screen_names:
        manager.current = screen_name
    else:
        print(f"Screen '{screen_name}' not found in manager.")


class GamePage(Screen):
    """
    Clean, refactored GamePage.

    Constructor signature kept the same: GamePage(bg_path, font_path, **kwargs)
    """

    def __init__(self, bg_path: str, font_path: str, **kwargs):
        super().__init__(**kwargs)

        self.bg_path = bg_path
        self.font_path = font_path
        self.zingo_engine = ZingoEngine()

        # Application/state reference
        self.app = App.get_running_app()

        # Root layout
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Build UI pieces
        self._build_background()
        self._build_header()
        self._build_question_labels()
        self._build_middle_area()
        self._build_back_button()
        self._build_feedback_and_flash()
        self._build_confetti()

        # Ensure background resizes on window change
        Window.bind(on_resize=self.update_rect)

        # Start with first question
        Clock.schedule_once(lambda dt: self.next_question(), 0)

    # ---------------------------
    # UI BUILDERS
    # ---------------------------

    def _build_background(self) -> None:
        with self.layout.canvas:
            Color(1, 1, 1, 0.15)
            self.bg_rect = Rectangle(source=self.bg_path, pos=(0, 0), size=Window.size)

    def _build_header(self) -> None:
        """Top 2x2 header showing points, multiplier, required, and question count."""
        def make_label(text: str, halign: str) -> Label:
            lbl = Label(
                text=text,
                font_size=20,
                color=(1, 1, 1, 1),
                font_name=self.font_path,
                halign=halign,
                valign='middle',
                size_hint=(1, 1),
            )
            lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, instance.height)))
            return lbl

        top_grid = GridLayout(
            cols=2,
            rows=2,
            size_hint=(0.9, None),
            height=75,
            pos_hint={'center_x': 0.5, 'top': 1},
            spacing=[10, 5],
            padding=[10, 20, 10, 10]
        )

        self.points_label = make_label(f"Points: {self.app.POINTS}", "left")
        self.multiplier_label = make_label(f"{self.app.MULTIPLIER}x", "right")
        self.required_label = make_label(f"Required: {self.app.REQUIRED_POINTS}", "left")
        self.questions_label = make_label("Questions: 1/100", "right")

        for w in (self.points_label, self.multiplier_label, self.required_label, self.questions_label):
            top_grid.add_widget(w)

        self.layout.add_widget(top_grid)

    def _build_question_labels(self) -> None:
        self.questionNumberLabel = Label(
            text="",
            font_size=36,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            font_name=self.font_path
        )
        self.questionLabel = Label(
            text="",
            font_size=28,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            font_name=self.font_path
        )
        self.layout.add_widget(self.questionNumberLabel)
        self.layout.add_widget(self.questionLabel)

    def _build_middle_area(self) -> None:
        """Container for answer widgets (multiple choice / T/F / short answer)."""
        self.middle_layout = GridLayout(
            cols=2,
            rows=2,
            size_hint=(0.8, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            spacing=[15, 15],
            padding=[10, 10, 10, 10]
        )
        self.layout.add_widget(self.middle_layout)

    def _build_back_button(self) -> None:
        self.back_btn = Button(
            text="Back",
            size=(120, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.02, 'y': 0.05},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=self.font_path,
            font_size=28
        )
        self.back_btn.bind(on_release=self.reset_and_back)
        self.layout.add_widget(self.back_btn)

    def _build_feedback_and_flash(self) -> None:
        self.feedback_label = Label(
            text="",
            font_size=20,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            font_name=self.font_path
        )
        self.flash_label = Label(
            text="",
            font_size=50,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name=self.font_path,
            opacity=0
        )
        self.layout.add_widget(self.feedback_label)
        self.layout.add_widget(self.flash_label)

    def _build_confetti(self) -> None:
        self.confetti = ConfettiWidget(size_hint=(1, 1))
        self.layout.add_widget(self.confetti)

    # ---------------------------
    # Geometry / events
    # ---------------------------

    def update_rect(self, instance, width: int, height: int) -> None:
        """Called on window resize (keeps background filling window)."""
        self.bg_rect.size = (width, height)

    # ---------------------------
    # UI Utilities
    # ---------------------------

    def make_option_button(self, text: str) -> Button:
        """Button factory used for answer options. Adds a white border for style."""
        btn = Button(
            text=text,
            font_size=24,
            size_hint=(1, 1),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            font_name=self.font_path
        )
        self.add_white_border(btn)
        return btn

    def add_white_border(self, widget: Any) -> None:
        """Add a white rectangle border around a widget and keep it updated on resize/pos changes."""
        with widget.canvas.before:
            Color(1, 1, 1, 1)
            border = Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=1.5)

        widget.bind(pos=lambda instance, val, b=border:
                    setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))
        widget.bind(size=lambda instance, val, b=border:
                    setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))

    # ---------------------------
    # Game flow helpers
    # ---------------------------

    def hide_all_widgets(self) -> None:
        """Hide everything except flash_label and confetti (used during flash / finished state)."""
        for widget in list(self.layout.children):
            if widget not in (self.flash_label, self.confetti):
                widget.opacity = 0

    def show_all_widgets(self) -> None:
        for widget in list(self.layout.children):
            if widget not in (self.flash_label, self.confetti):
                widget.opacity = 1

    def reset_game_state(self) -> None:
        """Reset game-related app state to defaults — centralizes the values."""
        self.app.QUESTION_INDEX = 0
        self.app.POINTS = 100
        self.app.MULTIPLIER = 1.0
        self.app.QUESTIONS_IN_A_ROW = 0

    def advance_question(self, delay: float = 1.0) -> None:
        """Advance to next question gracefully with scheduling."""
        if not self.app.QUESTIONS:
            return

        self.app.QUESTION_INDEX = (self.app.QUESTION_INDEX + 1) % len(self.app.QUESTIONS)
        Clock.schedule_once(lambda dt: self.next_question(), delay)

    # ---------------------------
    # Question rendering & input handling
    # ---------------------------

    def update_middle_layout(self, question_type: str, correct_answer: str, choices: Optional[Iterable]) -> None:
        """Render the middle area depending on question type."""
        self.middle_layout.clear_widgets()

        if question_type.lower() in ("multiple choice", "multiple_choice", "mcq"):
            # ensure choices is a plain list
            opts = list(choices) if choices else []
            # shuffle choices deterministically each time
            random.shuffle(opts)

            self.middle_layout.cols = 2
            self.middle_layout.rows = 2

            for choice in opts:
                choice_text = str(choice)
                btn = self.make_option_button(choice_text)
                # Use partial to avoid late binding bugs
                btn.bind(on_release=partial(self._on_option_selected, choice_text, correct_answer))
                self.middle_layout.add_widget(btn)

        elif question_type.lower() in ("true/false", "true_false", "tf"):
            self.middle_layout.cols = 2
            self.middle_layout.rows = 1
            for t in ("True", "False"):
                btn = self.make_option_button(t)
                btn.bind(on_release=partial(self._on_option_selected, t, correct_answer))
                self.middle_layout.add_widget(btn)

        elif question_type.lower() in ("short answer", "short_answer", "short"):
            self.middle_layout.cols = 1
            self.middle_layout.rows = 2

            text_input = TextInput(
                hint_text="Type your answer here...",
                font_size=24,
                size_hint=(1, 1),
                multiline=False,
                background_normal='',
                background_color=(0, 0, 0, 0),
                foreground_color=(1, 1, 1, 1),
                font_name=self.font_path
            )
            submit_btn = self.make_option_button("Submit")
            submit_btn.bind(on_release=partial(self._on_option_selected_from_textinput, text_input, correct_answer))
            self.middle_layout.add_widget(text_input)
            self.middle_layout.add_widget(submit_btn)

        else:
            # Unknown question type — show as short-answer fallback
            self.middle_layout.cols = 1
            self.middle_layout.rows = 1
            fallback = Label(text="Unsupported question type", font_size=20)
            self.middle_layout.add_widget(fallback)

    def _on_option_selected(self, user_answer: str, correct_answer: str, *args) -> None:
        """Handler for option buttons (MCQ / TF)."""
        self.submit_answer(user_answer, correct_answer)

    def _on_option_selected_from_textinput(self, text_input: TextInput, correct_answer: str, *args) -> None:
        self.submit_answer(text_input.text.strip(), correct_answer)

    def next_question(self) -> None:
        """Load and render the current question index."""
        # Guard: no questions
        if not getattr(self.app, 'QUESTIONS', None):
            self.hide_all_widgets()
            self.flash_label.text = "No questions available"
            self.flash_label.opacity = 1
            self.back_btn.opacity = 1
            self.back_btn.disabled = False
            return

        # normalize index
        if self.app.QUESTION_INDEX >= len(self.app.QUESTIONS):
            self.app.QUESTION_INDEX = 0

        idx = self.app.QUESTION_INDEX
        qdata = self.app.QUESTIONS[idx]

        # qdata may be dict-like or dataclass-like; handle both
        def get_field(obj, key, default=None):
            if isinstance(obj, dict):
                return obj.get(key, default)
            return getattr(obj, key, default)

        question_type = str(get_field(qdata, 'question_type', '')).strip()
        question_text = str(get_field(qdata, 'question', '')).strip()
        answer = str(get_field(qdata, 'answer', '')).strip()
        # choices could be a list or nested; handle previous format gracefully:
        raw_choices = get_field(qdata, 'choices', None)
        # If choices saved like [[...]] (previous code used choices[0]), try to normalize:
        if isinstance(raw_choices, list) and raw_choices and isinstance(raw_choices[0], list):
            choices = raw_choices[0]
        else:
            choices = raw_choices

        # Update UI labels
        self.questionNumberLabel.text = f"Question {idx + 1}"
        self.questionLabel.text = question_text
        self.points_label.text = f"Points: {self.app.POINTS}"
        self.multiplier_label.text = f"{self.app.MULTIPLIER:.2f}x"

        # Render inputs/options
        self.update_middle_layout(question_type, answer, choices)

    # ---------------------------
    # Answer handling & scoring
    # ---------------------------

    def submit_answer(self, user_answer: str, correct_answer: str) -> None:
        """Centralized answer processing and UI reactions."""
        user = (user_answer or "").strip()
        correct = (correct_answer or "").strip()

        if user == correct:
            self._process_correct()
        else:
            self._process_incorrect()

        # Move to next question (unless we returned due to final win)
        # If a final-state was triggered, we don't advance here.
        if self.app.POINTS < self.app.REQUIRED_POINTS:
            self.advance_question(delay=1.0)

    def _process_correct(self) -> None:
        """Handle correct answer: update state, show feedback, check conditions."""
        print("Correct")

        self.app.POINTS += 1
        self.app.MULTIPLIER += 0.05
        self.app.QUESTIONS_IN_A_ROW += 1

        # Reached required points: finish / celebrate
        if self.app.POINTS >= self.app.REQUIRED_POINTS:
            self.hide_all_widgets()
            self.flash_label.text = "Congratulations!"
            self.flash_label.opacity = 1

            # Confetti burst near bottom center
            cx = self.layout.width * 0.5
            cy = self.layout.height * 0.05
            self.confetti.burst(count=150, center=(cx, cy), spread=1.4, size_px=8, life=1.8)

            # ensure back button still usable
            self.back_btn.opacity = 1
            self.back_btn.disabled = False
            self.middle_layout.disabled = True
            return

        # Not finished: temporary flash
        self.flash_result("Correct!", duration=1.0)

        # If streak triggers roulette
        if self.app.QUESTIONS_IN_A_ROW >= 5:
            self.app.QUESTIONS_IN_A_ROW = 0
            # go to roulette after a brief pause
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'roulette_page'), 1.0)

    def _process_incorrect(self) -> None:
        print("Wrong")
        self.app.QUESTIONS_IN_A_ROW = 0
        self.flash_result("Wrong!", duration=1.0)

    # ---------------------------
    # Flash helpers
    # ---------------------------

    def flash_result(self, message: str, duration: float = 1.0) -> None:
        """Temporarily hide UI, show a full-screen flash message, then restore UI."""
        self.hide_all_widgets()
        self.middle_layout.disabled = True

        self.flash_label.text = message
        self.flash_label.opacity = 1

        def finish_flash(dt: float) -> None:
            self.flash_label.opacity = 0
            self.show_all_widgets()
            self.middle_layout.disabled = False

        Clock.schedule_once(finish_flash, duration)

    def hide_flash(self) -> None:
        self.flash_label.opacity = 0

    # ---------------------------
    # Navigation & flow
    # ---------------------------

    def reset_and_back(self, instance=None) -> None:
        """Reset state/UI and return to start page."""
        self.reset_game_state()
        self.show_all_widgets()
        self.middle_layout.disabled = False
        self.flash_label.opacity = 0
        self.next_question()
        switch_screen(instance, self.manager, "start_page")

    def continue_after_roulette(self) -> None:
        """Called by roulette page to continue the game flow."""
        self.next_question()
