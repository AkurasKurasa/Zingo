# screens/game_page.py
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from widgets.confetti import ConfettiWidget
import random


def switch_screen(instance, manager, screen_name):
    if manager and screen_name in manager.screen_names:
        manager.current = screen_name
    else:
        print(f"Screen '{screen_name}' not found in manager.")


class GamePage(Screen):

    def __init__(self, font_path, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.app = App.get_running_app()

        # --- Top GridLayout (2x2) ---
        top_grid = GridLayout(
            cols=2,
            rows=2,
            size_hint=(0.9, None),
            height=75,
            pos_hint={'center_x': 0.5, 'top': 1},
            spacing=[10, 5],
            padding=[10, 20, 10, 10]
        )

        def make_label(text, halign):
            lbl = Label(
                text=text,
                font_size=20,
                color=(1, 1, 1, 1),
                font_name=font_path,
                halign=halign,
                valign='middle',
                size_hint=(1, 1),
            )
            lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, instance.height)))
            return lbl

        self.points_label = make_label(f"Points: {self.app.POINTS}", "left")
        self.multiplier_label = make_label(f"{self.app.MULTIPLIER}x", "right")
        self.required_label = make_label(f"Required: {self.app.REQUIRED_POINTS}", "left")
        self.questions_label = make_label("Questions: 1/100", "right")

        top_grid.add_widget(self.points_label)
        top_grid.add_widget(self.multiplier_label)
        top_grid.add_widget(self.required_label)
        top_grid.add_widget(self.questions_label)

        self.layout.add_widget(top_grid)

        # --- Question labels ---
        self.questionNumberLabel = Label(
            text="",
            font_size=36,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            font_name=font_path
        )
        self.layout.add_widget(self.questionNumberLabel)

        self.questionLabel = Label(
            text="",
            font_size=28,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_name=font_path
        )
        self.layout.add_widget(self.questionLabel)

        # --- Middle self.layout ---
        self.middle_layout = GridLayout(
            cols=2,
            rows=2,
            size_hint=(0.8, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            spacing=[15, 15],
            padding=[10, 10, 10, 10]
        )
        self.layout.add_widget(self.middle_layout)

        # --- Back Button ---
        self.back_btn = Button(
            text="Back",
            size=(120, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.02, 'y': 0.02},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=font_path,
            font_size=28
        )
        self.back_btn.bind(on_release=self.reset_and_back)
        self.layout.add_widget(self.back_btn)

        # Info label
        self.feedback_label = Label(
            text="",
            font_size=20,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            font_name=font_path
        )
        self.layout.add_widget(self.feedback_label)

        # --- FULL-SCREEN FLASH OVERLAY ---
        self.flash_label = Label(
            text="",
            font_size=50,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name=font_path,
            opacity=0
        )
        self.layout.add_widget(self.flash_label)

        # --- CONFETTI WIDGET ---
        self.confetti = ConfettiWidget(size_hint=(1, 1))
        self.layout.add_widget(self.confetti)

        self.add_widget(self.layout)

        # Load first question
        self.next_question()

    # --- FLASH FUNCTIONS ---
    def flash_result(self, message, duration=1.0):
        self.hide_all_widgets()
        self.middle_layout.disabled = True

        self.flash_label.text = message
        self.flash_label.opacity = 1

        def finish_flash(dt):
            self.flash_label.opacity = 0
            self.show_all_widgets()
            self.middle_layout.disabled = False  

        Clock.schedule_once(finish_flash, duration)


    def reset_and_back(self, instance):
        # Reset all game state
        self.app.QUESTION_INDEX = 0
        self.app.POINTS = 100
        self.app.MULTIPLIER = 1.0
        self.app.QUESTIONS_IN_A_ROW = 0
        self.end_of_questions = False

        # Reset UI
        self.show_all_widgets()
        self.middle_layout.disabled = False
        self.flash_label.opacity = 0

        # Load first question
        self.next_question()

        # Go back to start page
        switch_screen(instance, self.manager, "start_page")


    def hide_flash(self):
        self.flash_label.opacity = 0

    # --------------------------------------------------------------------

    def update_middle_layout(self, question_type, answer, choices):
        self.middle_layout.clear_widgets()

        if question_type == "Multiple Choice":
            self.middle_layout.cols = 2
            self.middle_layout.rows = 2

            choices = random.sample(choices, len(choices))

            for choice in choices:
                btn = self.make_option_button(str(choice), self.app.font_path)
                btn.bind(on_release=lambda instance, c=str(choice): self.submit_answer(instance, c, answer))
                self.middle_layout.add_widget(btn)

        elif question_type == "True/False":
            self.middle_layout.cols = 2
            self.middle_layout.rows = 1

            for t in ["True", "False"]:
                btn = self.make_option_button(t, self.app.font_path)
                btn.bind(on_release=lambda instance, x=t: self.submit_answer(instance, x, answer))
                self.middle_layout.add_widget(btn)

        elif question_type == "Short Answer":
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
                font_name=self.app.font_path
            )

            submit_btn = self.make_option_button("Submit", self.app.font_path)
            submit_btn.bind(on_release=lambda instance: self.submit_answer(instance, text_input.text, answer))

            self.middle_layout.add_widget(text_input)
            self.middle_layout.add_widget(submit_btn)

    def next_question(self):
        # If there are no questions, just show back button
        if not self.app.QUESTIONS:
            self.hide_all_widgets()
            self.flash_label.text = "No questions available"
            self.flash_label.opacity = 1
            self.back_btn.opacity = 1
            self.back_btn.disabled = False
            return

        # Loop index back to 0 if it exceeds the number of questions
        if self.app.QUESTION_INDEX >= len(self.app.QUESTIONS):
            self.app.QUESTION_INDEX = 0

        index = self.app.QUESTION_INDEX
        question_data = self.app.QUESTIONS[index]

        question_type = question_data['question_type']
        question = question_data['question']
        answer = question_data['answer'].strip()
        choices = question_data['choices'][0] if question_data['choices'] else None

        question_number = index + 1

        self.questionNumberLabel.text = f"Question {question_number}"
        self.questionLabel.text = f"{question}"
        self.points_label.text = f"Points: {self.app.POINTS}"
        self.multiplier_label.text = f"{self.app.MULTIPLIER:.2f}x"

        self.update_middle_layout(question_type, answer, choices)


    # --------------------------------------------------------------------

    def submit_answer(self, instance, answer, correct_answer):
        if answer == correct_answer:
            print("Correct")
            self.app.POINTS += 1
            self.app.MULTIPLIER += 0.05
            self.app.QUESTIONS_IN_A_ROW += 1

            # Check if reached required points
            if self.app.POINTS >= self.app.REQUIRED_POINTS:
                self.hide_all_widgets()

                self.flash_label.text = "🎉 Congratulations! 🎉"
                self.flash_label.opacity = 1

                # CONFETTI BURST FROM BOTTOM CENTER
                cx = self.layout.width * 0.5
                cy = self.layout.height * 0.05    # near bottom

                self.confetti.burst(
                    count=150,
                    center=(cx, cy),
                    spread=1.4,
                    size_px=8,
                    life=1.8
                )

                # keep back button usable
                self.back_btn.opacity = 1
                self.back_btn.disabled = False

                self.middle_layout.disabled = True
                return

            else:
                # Show temporary "Correct!" flash
                self.flash_result("Correct!", 1.0)

            # Optional: go to roulette after streak
            if self.app.QUESTIONS_IN_A_ROW >= 5:
                self.app.QUESTIONS_IN_A_ROW = 0
                Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'roulette_page'), 1.0)

        else:
            print("Wrong")
            self.flash_result("Wrong!", 1.0)

        # Move to next question
        self.app.QUESTION_INDEX += 1

        # Loop back to start if reached the end
        if self.app.QUESTION_INDEX >= len(self.app.QUESTIONS):
            self.app.QUESTION_INDEX = 0

        Clock.schedule_once(lambda dt: self.next_question(), 1.0)

    def hide_all_widgets(self):
        for widget in self.layout.children:
            if widget not in (self.flash_label, self.confetti):
                widget.opacity = 0

    def show_all_widgets(self):
        for widget in self.layout.children:
            if widget not in (self.flash_label, self.confetti):
                widget.opacity = 1

    def make_option_button(self, text, font_path):
        btn = Button(
            text=text,
            font_size=24,
            size_hint=(1, 1),
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            font_name=font_path
        )
        self.add_white_border(btn)
        return btn

    def add_white_border(self, widget):
        with widget.canvas.before:
            Color(1, 1, 1, 1)
            border = Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=1.5)

        widget.bind(pos=lambda instance, val, b=border:
                    setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))
        widget.bind(size=lambda instance, val, b=border:
                    setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))

    def continue_after_roulette(self):
        self.next_question()
