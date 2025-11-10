from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App
from kivy.graphics import Color, Line
import os
import random

# Font fallback
font_path = os.path.join(os.path.dirname(__file__), "fonts", "PixelifySans-Regular.ttf")
if not os.path.exists(font_path):
    font_path = "Roboto"

def switch_screen(instance, screen_manager, target_screen):
    screen_manager.current = target_screen

class GamePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_index = 0
        self.points = 0
        self.multiplier = 1.0
        self.streak = 0
        self.time_per_question = 15
        self.remaining_time = self.time_per_question
        self.timer_event = None
        self.questions_queue = []

        root = FloatLayout()
        self.add_widget(root)

        # --- Top Info Labels ---
        self.top_grid = GridLayout(
            cols=2, rows=2, size_hint=(0.9, 0.1),
            pos_hint={'center_x':0.5, 'top':1}, spacing=[10,10], padding=[10,10,10,10]
        )

        self.points_label = Label(text="Points: 0", font_name=font_path, font_size=20, color=(1,1,1,1))
        self.multiplier_label = Label(text="Multiplier: 1.0x", font_name=font_path, font_size=20, color=(1,1,1,1))
        self.required_label = Label(text="Required: 0", font_name=font_path, font_size=20, color=(1,1,1,1))
        self.questions_label = Label(text="Questions: 0/0", font_name=font_path, font_size=20, color=(1,1,1,1))

        self.top_grid.add_widget(self.points_label)
        self.top_grid.add_widget(self.multiplier_label)
        self.top_grid.add_widget(self.required_label)
        self.top_grid.add_widget(self.questions_label)
        root.add_widget(self.top_grid)

        # --- Question Label ---
        self.question_label = Label(
            text="No questions loaded.", font_name=font_path, font_size=28, color=(1,1,1,1),
            size_hint=(0.9,0.2), pos_hint={'center_x':0.5,'center_y':0.7}, halign='center', valign='middle'
        )
        self.question_label.bind(size=self.question_label.setter('text_size'))
        root.add_widget(self.question_label)

        # --- Answer Buttons Container ---
        self.answers_layout = GridLayout(cols=2, rows=2, spacing=dp(10),
                                         size_hint=(0.8,0.3), pos_hint={'center_x':0.5,'center_y':0.45})
        root.add_widget(self.answers_layout)

        # --- Timer Label ---
        self.timer_label = Label(text=f"Time: {self.time_per_question}", font_name=font_path, font_size=24,
                                 color=(1,0.8,0,1), size_hint=(0.2,0.1), pos_hint={'center_x':0.9,'center_y':0.9})
        root.add_widget(self.timer_label)

        # --- Back Button ---
        back_btn = Button(text="Back", size_hint=(None,None), size=(dp(120),dp(45)),
                          pos_hint={'x':0.02,'y':0.02}, background_normal='', background_color=(0,0,0,0),
                          font_name=font_path, font_size=22)
        back_btn.bind(on_release=lambda i: switch_screen(i, self.manager, "start_page"))
        root.add_widget(back_btn)

    def on_enter(self):
        app = App.get_running_app()
        self.questions_queue = list(range(len(app.custom_questions)))
        random.shuffle(self.questions_queue)
        self.current_index = 0
        self.points = 0
        self.multiplier = 1.0
        self.streak = 0
        self.show_question()

    def show_question(self):
        app = App.get_running_app()
        if not self.questions_queue:
            self.question_label.text = "No questions available."
            return
        q_idx = self.questions_queue[self.current_index]
        question = app.custom_questions[q_idx]
        self.current_question = question

        self.question_label.text = question['text']
        self.questions_label.text = f"Questions: {self.current_index+1}/{len(app.custom_questions)}"
        self.required_label.text = f"Required: {len(app.custom_questions)*100}"

        self.display_answers(question)
        self.start_timer()

    def display_answers(self, question):
        self.answers_layout.clear_widgets()
        options = question.get('answers', [question['correct_answer']])
        random.shuffle(options)
        for opt in options:
            btn = Button(text=opt, font_name=font_path, font_size=20,
                         background_normal='', background_color=(0,0,0,0), color=(1,1,1,1))
            btn.bind(on_release=lambda i, opt=opt: self.check_answer(opt))
            self.answers_layout.add_widget(btn)

    def start_timer(self):
        self.remaining_time = self.time_per_question
        self.timer_label.text = f"Time: {self.remaining_time}"
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.countdown, 1)

    def countdown(self, dt):
        self.remaining_time -= 1
        self.timer_label.text = f"Time: {self.remaining_time}"
        if self.remaining_time <= 0:
            self.timer_event.cancel()
            self.check_answer(None)

    def check_answer(self, answer):
        if self.timer_event:
            self.timer_event.cancel()
        correct_answer = self.current_question['correct_answer']
        correct = (answer and answer.strip().lower() == correct_answer.strip().lower())

        if correct:
            self.streak += 1
            self.multiplier = min(1 + 0.05*self.streak, 3.0)
            self.points += int(100*self.multiplier)
        else:
            self.streak = 0
            self.multiplier = 1.0

        self.points_label.text = f"Points: {self.points}"
        self.multiplier_label.text = f"Multiplier: {self.multiplier:.2f}x"

        # Feedback
        self.answers_layout.clear_widgets()
        feedback = Label(text="Correct!" if correct else f"Wrong! ({correct_answer})",
                         font_name=font_path, font_size=32,
                         color=(0,1,0,1) if correct else (1,0,0,1))
        self.answers_layout.add_widget(feedback)

        Clock.schedule_once(lambda dt: self.next_question(), 1.5)

    def next_question(self):
        self.current_index += 1
        app = App.get_running_app()
        if self.current_index >= len(app.custom_questions):
            self.question_label.text = f"Quiz Finished!\nTotal Points: {self.points}"
            self.answers_layout.clear_widgets()
            self.timer_label.text = ""
        else:
            self.show_question()
