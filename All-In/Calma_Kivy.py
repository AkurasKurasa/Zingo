from kivy.config import Config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color, Line
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
from kivy.uix.filechooser import FileChooserListView
import os
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from Custom_Page import CustomPage

import os

# ------------------- Paths -------------------
bg_path = os.path.join(os.path.dirname(__file__), "backgrounds", "homepagebg.png")
if not os.path.exists(bg_path):
    raise FileNotFoundError(f"Background image not found: {bg_path}")

font_path = os.path.join(os.path.dirname(__file__), "fonts", "PixelifySans-Regular.ttf")
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font not found: {font_path}")

# ------------------- Window Size -------------------
img = Image.open(bg_path)
img_width, img_height = img.size

Config.set('graphics', 'width', str(img_width))
Config.set('graphics', 'height', str(img_height))
Config.set('graphics', 'resizable', '0')
Window.size = (img_width, img_height)

# ------------------- Reusable Function -------------------
def switch_screen(instance, screen_manager, target_screen):
    screen_manager.current = target_screen

# ------------------- Screens -------------------
class StartPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # Background
        with layout.canvas:
            Color(1, 1, 1, 0.5)
            self.bg_rect = Rectangle(source=bg_path, pos=(0, 0), size=Window.size)
        Window.bind(on_resize=self.update_rect)

        # Title
        self.label = Label(
            text="All-In",
            font_size=81,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'top': 0.75},
            font_name=font_path
        )
        layout.add_widget(self.label)

        # Start button
        self.start_btn = Button(
            text="Start",
            size=(150, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.02, 'y': 0.25},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=font_path,
            font_size=32
        )
        self.start_btn.bind(on_release=lambda instance: switch_screen(instance, self.manager, "game_page"))
        layout.add_widget(self.start_btn)

        # Custom button
        self.custom_btn = Button(
            text="Custom",
            size=(150, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.03, 'y': 0.18},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=font_path,
            font_size=32
        )
        self.custom_btn.bind(on_release=lambda instance: switch_screen(instance, self.manager, "custom_page"))
        layout.add_widget(self.custom_btn)

        # Quit button
        self.quit_btn = Button(
            text="Quit",
            size=(150, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.0025, 'y': 0.11},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=font_path,
            font_size=32
        )
        self.quit_btn.bind(on_release=lambda x: App.get_running_app().stop())
        layout.add_widget(self.quit_btn)

        self.add_widget(layout)

    def update_rect(self, instance, width, height):
        self.bg_rect.size = (width, height)

# ------------------- Game Page -------------------
class GamePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_question_index = 0
        self.points = 0
        # multiplier increases with correct streak, but cap to avoid runaway points
        self.multiplier = 1.0
        self.BASE_POINTS = 100
        self.MAX_MULTIPLIER = 3.0
        self.correct_streak = 0
        # questions_answered will reflect number of UNIQUE correctly answered questions
        self.questions_answered = 0
        self.correctly_answered = set()
        self.incorrect_questions = []  # Store indices of incorrectly answered questions
        self.questions_queue = []  # Store the sequence of questions to ask
        layout = FloatLayout()
        self.layout = layout  # Store reference to layout

        # --- Top GridLayout (2x2) ---
        top_grid = GridLayout(
            cols=2,
            rows=2,
            size_hint=(0.9, 0.1),
            pos_hint={'center_x': 0.5, 'top': 1},
            spacing=[10, 20],
            padding=[10, 50, 10, 10]
        )

        def make_label(text, halign):
            lbl = Label(
                text=text,
                font_size=20,
                color=(1,1,1,1),
                font_name=font_path,
                halign=halign,
                valign='middle'
            )
            lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            return lbl

        self.points_label = make_label("Points: 0", "left")
        self.multiplier_label = make_label("1.00x", "right")
        self.required_label = make_label("Required: 0", "left")
        self.questions_label = make_label("Questions: 0/0", "right")

        top_grid.add_widget(self.points_label)
        top_grid.add_widget(self.multiplier_label)
        top_grid.add_widget(self.required_label)
        top_grid.add_widget(self.questions_label)

        layout.add_widget(top_grid)

        # --- Question Labels ---
        questionNumberLabel = Label(
            # start with no questions
            text="Question 0/0",
            font_size=36,
            color=(1,1,1,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            font_name=font_path
        )
        self.question_number_label_ref = questionNumberLabel
        layout.add_widget(questionNumberLabel)

        questionLabel = Label(
            text="No questions yet. Add questions in Custom.",
            font_size=28,
            color=(1,1,1,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_name=font_path
        )
        self.question_label_ref = questionLabel
        layout.add_widget(questionLabel)

        # --- Middle layout placeholder ---
        self.middle_layout = GridLayout(
            cols=2,
            rows=2,
            size_hint=(0.8, 0.25),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            spacing=[15, 15],
            padding=[10, 10, 10, 10]
        )
        layout.add_widget(self.middle_layout)

        # --- Back Button ---
        back_btn = Button(
            text="Back",
            size=(120, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.02, 'y': 0.02},
            background_normal='',
            background_color=(0,0,0,0),
            font_name=font_path,
            font_size=28
        )
        back_btn.bind(on_release=lambda instance: switch_screen(instance, self.manager, "start_page"))
        layout.add_widget(back_btn)

        self.add_widget(layout)

        # Initialize with empty question
        self.update_middle_layout()

    def on_enter(self):
        # This is called when the screen is entered
        app = App.get_running_app()
        # Reset per-entry transient state
        self.current_question_index = 0
        self.points = 0
        self.multiplier = 1.0
        self.correct_streak = 0
        self.incorrect_questions = []
        self.questions_queue = []
        self.correctly_answered = set()
        self.questions_answered = 0
        if app.custom_questions:
            # Initialize the questions queue with sequential indices
            self.questions_queue = list(range(len(app.custom_questions)))
            # show first question
            self.show_question(self.current_question_index)
        else:
            # no questions: show placeholder
            self.question_number_label_ref.text = "Question 0/0"
            self.question_label_ref.text = "No questions yet. Add questions in Custom."
            self.middle_layout.clear_widgets()
            # add a placeholder button to indicate no questions
            placeholder = Button(text='No questions', font_size=20, size_hint=(1,1), background_normal='', background_color=(0,0,0,0), color=(1,1,1,1), font_name=font_path)
            self.add_white_border(placeholder)
            self.middle_layout.add_widget(placeholder)
        # update required points based on number of questions
        total_questions = len(app.custom_questions)
        required = total_questions * self.BASE_POINTS
        self.required_label.text = f"Required: {required:,}"
    
    def show_question(self, index):
        app = App.get_running_app()
        if not app.custom_questions:
            return
        
        question = app.custom_questions[index]
        
        # Update question text
        self.question_label_ref.text = question['text']
        
        # Update question number
        total_questions = len(app.custom_questions)
        self.question_number_label_ref.text = f"Question {index + 1}/{total_questions}"
        
        # Update score display
        self.questions_label.text = f"Questions: {self.questions_answered}/{total_questions}"
        self.points_label.text = f"Points: {self.points}"
        self.multiplier_label.text = f"{self.multiplier:.2f}x"
        # update required points dynamically (one base point-per-question target)
        required = total_questions * self.BASE_POINTS
        self.required_label.text = f"Required: {required:,}"

        self.current_question = question  # Store current question
        self.update_middle_layout(question_type=question['type'], answers=question.get('answers', []))

    def check_answer(self, answer):
        if not hasattr(self, 'current_question'):
            return
        
        is_correct = False
        
        if self.current_question['type'] == "Multiple Choice":
            is_correct = answer == self.current_question['correct_answer']
        elif self.current_question['type'] == "True/False":
            is_correct = answer.lower() == self.current_question['correct_answer'].lower()
        elif self.current_question['type'] == "Short Answer":
            # For short answer, handle the TextInput widget's text
            if hasattr(self, 'answer_input'):
                user_answer = self.answer_input.text
            else:
                user_answer = answer # Fallback, should use answer_input.text
            is_correct = user_answer.lower().strip() == self.current_question['correct_answer'].lower().strip()
            
        if is_correct:
            # Only count the question once as answered
            first_time = self.current_question_index not in self.correctly_answered
            if first_time:
                self.correctly_answered.add(self.current_question_index)
            self.questions_answered = len(self.correctly_answered)

            self.correct_streak += 1
            self.multiplier = 1.0 + (self.correct_streak * 0.05)
            # cap multiplier to avoid runaway scoring
            mult = min(self.multiplier, self.MAX_MULTIPLIER)
            points_earned = int(self.BASE_POINTS * mult)
            self.points += points_earned

            # If this was an incorrect question that was answered correctly, remove it
            if self.current_question_index in self.incorrect_questions:
                try:
                    self.incorrect_questions.remove(self.current_question_index)
                except ValueError:
                    pass
        else:
            self.correct_streak = 0
            self.multiplier = 1.0
            # Add the question to incorrect_questions if not already there
            if self.current_question_index not in self.incorrect_questions:
                self.incorrect_questions.append(self.current_question_index)

        # Update question/score labels
        total_questions = len(App.get_running_app().custom_questions)
        self.questions_label.text = f"Questions: {self.questions_answered}/{total_questions}"
        self.points_label.text = f"Points: {self.points}"
        self.multiplier_label.text = f"{self.multiplier:.2f}x"

        # Check for completion: all questions answered correctly
        if total_questions > 0 and len(self.correctly_answered) >= total_questions:
            # Game over - all correct
            self.end_game()
            return

        # Otherwise move to next
        self.next_question(None)
        
    def next_question(self, instance):
        app = App.get_running_app()
        if not app.custom_questions:
            return
            
        total_questions = len(app.custom_questions)
        
        # If this was the last question in the queue (or we are reviewing incorrect ones)
        if self.current_question_index >= total_questions - 1:
            # Check if there are still incorrect questions to re-ask
            if self.incorrect_questions:
                # Find the next question to ask among the incorrect ones
                try:
                    current_idx_in_incorrect = self.incorrect_questions.index(self.current_question_index)
                    if current_idx_in_incorrect < len(self.incorrect_questions) - 1:
                        # Move to the next incorrect question
                        self.current_question_index = self.incorrect_questions[current_idx_in_incorrect + 1]
                    else:
                        # Reached the end of the incorrect list, wrap back to start
                        self.current_question_index = self.incorrect_questions[0]
                except ValueError:
                    # Current question was correctly answered and removed, start from the first incorrect one
                    self.current_question_index = self.incorrect_questions[0]
            else:
                # All questions answered correctly, start over from beginning
                self.current_question_index = 0
        else:
            # Move to the next question in sequential order
            self.current_question_index += 1
            
        self.show_question(self.current_question_index)
        
    def prev_question(self, instance):
        app = App.get_running_app()
        if not app.custom_questions:
            return
            
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question(self.current_question_index)

    def update_middle_layout(self, question_type="Short Answer", answers=None):
        self.middle_layout.clear_widgets()

        if question_type == "Multiple Choice":
            self.middle_layout.cols = 2
            self.middle_layout.rows = 2
            if answers and len(answers) >= 4:
                for answer in answers[:4]:
                    btn = self.make_option_button(answer)
                    btn.bind(on_release=lambda x, a=answer: self.check_answer(a))
                    self.middle_layout.add_widget(btn)
            else:
                for i in range(1,5):
                    btn = self.make_option_button(f"Option {i}")
                    self.middle_layout.add_widget(btn)

        elif question_type == "True/False":
            self.middle_layout.cols = 2
            self.middle_layout.rows = 1
            for t in ["True", "False"]:
                btn = self.make_option_button(t)
                btn.bind(on_release=lambda x, a=t: self.check_answer(a))
                self.middle_layout.add_widget(btn)

        elif question_type == "Short Answer":
            self.middle_layout.cols = 1
            self.middle_layout.rows = 2
            self.answer_input = TextInput(
                hint_text="Type your answer here...",
                font_size=24,
                size_hint=(1, 0.7),
                multiline=False,
                background_normal='',
                background_color=(0,0,0,0),
                foreground_color=(1,1,1,1),
                cursor_color=(1,1,1,1),
                font_name=font_path
            )

            submit_btn = self.make_option_button("Submit")
            submit_btn.bind(on_release=lambda x: self.check_answer(None)) 
            self.middle_layout.add_widget(self.answer_input)
            self.middle_layout.add_widget(submit_btn)

    def end_game(self):
        # show a simple popup and return to start page
        popup = Popup(title='Game Complete',
                      content=Label(text='All questions answered correctly!', font_name=font_path),
                      size_hint=(0.6, 0.4))
        popup.open()
        # Optionally navigate back to start after a short delay
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'start_page'), 2)

    def make_option_button(self, text):
        btn = Button(
            text=text,
            font_size=24,
            size_hint=(1,1),
            background_normal='',
            background_color=(0,0,0,0),
            color=(1,1,1,1),
            font_name=font_path
        )
        self.add_white_border(btn)
        return btn

    def add_white_border(self, widget):
        with widget.canvas.before:
            Color(1,1,1,1)
            border = Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=1.5)
        # Update border on move/resize
        widget.bind(pos=lambda instance, val, b=border: setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))
        widget.bind(size=lambda instance, val, b=border: setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))


    from Custom_Page import CustomPage

# ------------------- Main App -------------------
class AllInApp(App):
    custom_questions = []

    def build(self):
        # Default questions for initial testing (commented out)
        # Uncomment or populate this list to start with preloaded questions.
        # self.custom_questions = [
        #     {'text': 'What is the capital of France?', 'type': 'Short Answer', 'correct_answer': 'Paris', 'answers': []},
        #     {'text': 'Is the sky usually blue?', 'type': 'True/False', 'correct_answer': 'True', 'answers': ['True', 'False']},
        #     {'text': 'Which of these is a vegetable?', 'type': 'Multiple Choice', 'correct_answer': 'Carrot', 'answers': ['Apple', 'Carrot', 'Banana', 'Grape']},
        # ]
        # Start with no questions so the user can add them via the Custom page
        self.custom_questions = []
        
        self.sm = ScreenManager()
        self.sm.add_widget(StartPage(name='start_page'))
        self.sm.add_widget(CustomPage(name='custom_page'))
        self.sm.add_widget(GamePage(name='game_page'))

        return self.sm

if __name__ == '__main__':
    AllInApp().run()