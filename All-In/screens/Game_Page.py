from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.app import App

def switch_screen(instance, manager, screen_name):
    """Switch to another screen using the manager."""
    if manager and screen_name in manager.screen_names:
        manager.current = screen_name
    else:
        print(f"Screen '{screen_name}' not found in manager.")

class GamePage(Screen):
    def __init__(self, font_path, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

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
            # Align text 
            lbl.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, instance.height)))
            return lbl

        # --- Store as instance variables for later updates ---
        self.points_label = make_label("Points: 100", "left")
        self.multiplier_label = make_label("1.00x", "right")
        self.required_label = make_label("Required: 1,000,000", "left")
        self.questions_label = make_label("Questions: 1/100", "right")

        # --- Add to grid ---
        top_grid.add_widget(self.points_label)
        top_grid.add_widget(self.multiplier_label)
        top_grid.add_widget(self.required_label)
        top_grid.add_widget(self.questions_label)

        layout.add_widget(top_grid)

        # --- Question Labels ---
        self.questionNumberLabel = Label(
            text="",
            font_size=36,
            color=(1,1,1,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            font_name=font_path
        )
        layout.add_widget(self.questionNumberLabel)

        self.questionLabel = Label(
            text="",
            font_size=28,
            color=(1,1,1,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_name=font_path
        )
        layout.add_widget(self.questionLabel)

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

        self.next_question()

        self.feedback_label = Label(
            text="",
            font_size=20,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            font_name=self.app.font_path
        )
        layout.add_widget(self.feedback_label)

    def update_middle_layout(self, question_type, answer, choices):
        self.middle_layout.clear_widgets()


        if question_type == "Multiple Choice":
            self.middle_layout.cols = 2
            self.middle_layout.rows = 2
            choices.append(answer)
            for choice in choices:
                btn = self.make_option_button(str(choice), self.app.font_path)
                btn.bind(on_release=lambda instance, c=str(choice): self.submit_answer(instance, c, answer))
                self.middle_layout.add_widget(btn)

        elif question_type == "True/False":
            self.middle_layout.cols = 2
            self.middle_layout.rows = 1
            for t in ["True", "False"]:
                btn = self.make_option_button(t, self.app.font_path)
                btn.bind(on_release=lambda instance: self.submit_answer(instance, t, answer))
                self.middle_layout.add_widget(btn)

        elif question_type == "Short Answer":
            self.middle_layout.cols = 1
            self.middle_layout.rows = 2
            text_input = TextInput(
                hint_text="Type your answer here...",
                font_size=24,
                size_hint=(1,1),
                multiline=False,
                background_normal='',
                background_color=(0,0,0,0),
                foreground_color=(1,1,1,1),
                font_name=self.app.font_path
            )
            submit_btn = self.make_option_button("Submit", self.app.font_path)
            submit_btn.bind(on_release=lambda instance: self.submit_answer(instance, text_input.text, answer))
            self.middle_layout.add_widget(text_input)
            self.middle_layout.add_widget(submit_btn)

    def next_question(self):
            index = self.app.QUESTION_INDEX
            question_data = self.app.QUESTIONS[index]

            question_type = question_data['question_type']
            question = question_data['question']
            answer = question_data['answer'].strip()
            choices = question_data['choices'][0] if question_data['choices'] else None

            print(answer)

            question_number = index + 1

            self.questionNumberLabel.text = f"Question {question_number}"
            self.questionLabel.text = f"{question}"
            self.points_label.text = f"Points: {self.app.POINTS}"
            self.multiplier_label.text = f"{self.app.MULTIPLIER:.2f}x"

            self.update_middle_layout(question_type, answer, choices)

    def submit_answer(self, instance, answer, correct_answer):
        # normalise
        user = answer.strip().lower()
        correct = correct_answer.strip().lower()
        is_correct = (user == correct)

        if is_correct:
            print("Hooray!")

            # ---- update stats ----
            self.app.QUESTIONS_IN_A_ROW += 1
            points_earned = int(10 * self.app.MULTIPLIER)
            self.app.POINTS += points_earned
            self.app.MULTIPLIER += 0.05
            self.app.QUESTION_INDEX += 1

            # ---- every 5 in a row → roulette ----
            if self.app.QUESTIONS_IN_A_ROW % 5 == 0:
                self.app.root.get_screen('roulette_page').start_roulette()
                return

            self.next_question()

        else:
            print("Womp womp nigga")
            self.app.QUESTIONS_IN_A_ROW = 0          # reset streak
            self.app.MULTIPLIER = 1.0                
            self.next_question()

    def make_option_button(self, text, font_path):
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
    
        widget.bind(pos=lambda instance, val, b=border: setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))
        widget.bind(size=lambda instance, val, b=border: setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))