from kivy.config import Config
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle, Color, Line
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.core.text import Label as CoreLabel
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup 
from kivy.clock import Clock
import os
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image

import os

# ------------------- Paths -------------------
bg_path = os.path.join(os.path.dirname(__file__), "backgrounds", "homepage_bg.jpg")
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
    def __init__(self, question_type="Short Answer", **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

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

        top_grid.add_widget(make_label("Points: 100", "left"))
        top_grid.add_widget(make_label("1.25x", "right"))
        top_grid.add_widget(make_label("Required: 1,000,000", "left"))
        top_grid.add_widget(make_label("Questions: 1/100", "right"))

        layout.add_widget(top_grid)

        # --- Question Labels ---
        questionNumberLabel = Label(
            text="Question 1",
            font_size=36,
            color=(1,1,1,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.75},
            font_name=font_path
        )
        layout.add_widget(questionNumberLabel)

        questionLabel = Label(
            text="What is the capital of France?",
            font_size=28,
            color=(1,1,1,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_name=font_path
        )
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

        # --- Build middle layout based on question_type ---
        self.update_middle_layout(question_type)

    def update_middle_layout(self, question_type):
        self.middle_layout.clear_widgets()

        if question_type == "Multiple Choice":
            self.middle_layout.cols = 2
            self.middle_layout.rows = 2
            for i in range(1,5):
                btn = self.make_option_button(f"Option {i}")
                self.middle_layout.add_widget(btn)

        elif question_type == "True/False":
            self.middle_layout.cols = 2
            self.middle_layout.rows = 1
            for t in ["True", "False"]:
                btn = self.make_option_button(t)
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
                font_name=font_path
            )
            submit_btn = self.make_option_button("Submit")
            self.middle_layout.add_widget(text_input)
            self.middle_layout.add_widget(submit_btn)

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

# ------------------- Custom Page Example -------------------
class CustomPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # --- Title label ---
        titleLabel = Label(
            text="CUSTOM",
            font_size=32,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.1, 'center_y': 0.92},
            font_name=font_path,
        )
        layout.add_widget(titleLabel)

        # --- Sub-label ---
        createQuestionLabel = Label(
            text="Create Questions",
            font_size=24,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.145, 'center_y': 0.83},
            font_name=font_path,
        )
        layout.add_widget(createQuestionLabel)

        # --- Spinner setup ---
        spinner_values = ("Multiple Choice", "True/False", "Short Answer")
        spinner_text = "Select Question Type"

        def fit_spinner_width(texts, font_name, font_size=16, padding=40):
            longest = max(texts, key=len)
            label = CoreLabel(text=longest, font_name=font_name, font_size=font_size)
            label.refresh()
            text_width = label.texture.size[0]
            return text_width + dp(padding)

        spinner_width = fit_spinner_width(spinner_values + (spinner_text,), font_path)

        questionTypeSpinner = Spinner(
            text=spinner_text,
            values=spinner_values,
            pos_hint={'center_x': 0.145, 'center_y': 0.73},
            size_hint=(None, None),
            size=(spinner_width, dp(32)),
            font_name=font_path,
            font_size=16,
            background_normal='',
            background_down='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )

        # --- Spinner border ---
        with questionTypeSpinner.canvas.before:
            Color(1, 1, 1, 1)
            spinner_border = Line(rectangle=(0, 0, 0, 0), width=1.5)

        def update_spinner_border(*_):
            spinner_border.rectangle = (
                questionTypeSpinner.x,
                questionTypeSpinner.y,
                questionTypeSpinner.width,
                questionTypeSpinner.height,
            )

        questionTypeSpinner.bind(pos=update_spinner_border, size=update_spinner_border)
        layout.add_widget(questionTypeSpinner)

        # --- Question label ---
        questionLabel = Label(
            text="Question:",
            font_size=20,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.085, 'center_y': 0.63},
            font_name=font_path,
        )
        layout.add_widget(questionLabel)

        # --- Calculate input size based on hint text ---
        questionInput_hint_text = "Enter question here..."
        questionInputLabel = CoreLabel(text=questionInput_hint_text, font_name=font_path, font_size=16)
        questionInputLabel.refresh()
        text_width, text_height = questionInputLabel.texture.size

        questionInput_width = text_width + dp(100)   # add padding
        questionInput_height = text_height + dp(12) # add vertical padding

        # --- Text input box ---
        questionInput = TextInput(
            hint_text=questionInput_hint_text,
            multiline=False,
            size_hint=(None, None),
            size=(questionInput_width, questionInput_height),
            pos_hint={'center_x': 0.185, 'center_y': 0.56},
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),   # transparent
            foreground_color=(1, 1, 1, 1),   # white text
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(1, 1, 1, 0.4),
            font_name=font_path,
            font_size=16,
        )

        # --- White border for input ---
        with questionInput.canvas.before:
            Color(1, 1, 1, 1)
            questionInput_border = Line(rectangle=(0, 0, 0, 0), width=1.5)

        def update_questionInput_border(*_):
            questionInput_border.rectangle = (
                questionInput.x,
                questionInput.y,
                questionInput.width,
                questionInput.height,
            )

        questionInput.bind(pos=update_questionInput_border, size=update_questionInput_border)
        layout.add_widget(questionInput)

        # --- Answer label ---
        answerLabel = Label(
            text="Answer:",
            font_size=20,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.08, 'center_y': 0.45},
            font_name=font_path,
        )
        layout.add_widget(answerLabel)

        # --- Answer input box ---
        # --- Calculate input size based on hint text ---
        answerInput_hint_text = "Enter answer here..."
        answerInputLabel = CoreLabel(text=questionInput_hint_text, font_name=font_path, font_size=16)
        answerInputLabel.refresh()
        text_width, text_height = answerInputLabel.texture.size

        answerInput_width = text_width + dp(100)   # add padding
        answerInput_height = text_height + dp(12) # add vertical padding

        # --- Text input box ---
        answerInput = TextInput(
            hint_text=answerInput_hint_text,
            multiline=False,
            size_hint=(None, None),
            size=(answerInput_width, answerInput_height),
            pos_hint={'center_x': 0.185, 'center_y': 0.38},
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),   # transparent
            foreground_color=(1, 1, 1, 1),   # white text
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(1, 1, 1, 0.4),
            font_name=font_path,
            font_size=16,
        )

        # --- White border for input ---
        with answerInput.canvas.before:
            Color(1, 1, 1, 1)
            answerInput_border = Line(rectangle=(0, 0, 0, 0), width=1.5)

        def update_answerInput_border(*_):
            answerInput_border.rectangle = (
                answerInput.x,
                answerInput.y,
                answerInput.width,
                answerInput.height,
            )

        answerInput.bind(pos=update_answerInput_border, size=update_answerInput_border)
        layout.add_widget(answerInput)

        def on_save_question(instance):
            self.successLabel.text = "Question successfully saved!"

        # --- Create button label to auto-fit size ---
        save_question_text = "Save Question"
        saveQuestionLabel = CoreLabel(text=save_question_text, font_name=font_path, font_size=16)
        saveQuestionLabel.refresh()
        text_width, text_height = saveQuestionLabel.texture.size

        save_question_btn_width = text_width + dp(60)   # horizontal padding
        save_question_btn_height = text_height + dp(12) # vertical padding

        # --- Button with white background and black text (no border) ---
        save_question_btn = Button(
            text=save_question_text,
            size_hint=(None, None),
            size=(save_question_btn_width, save_question_btn_height),
            pos_hint={'center_x': 0.128, 'center_y': 0.25},
            background_normal='',
            background_down='',
            background_color=(1, 1, 1, 1),  # white background
            color=(0, 0, 0, 1),             # black text
            font_name=font_path,
            font_size=16,
        )

        save_question_btn.bind(on_release=on_save_question)

        layout.add_widget(save_question_btn)

        # --- Answer label ---
        self.successLabel = Label(
            text="",
            font_size=20,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.18, 'center_y': 0.15},
            font_name=font_path,
        )
        layout.add_widget(self.successLabel)
        
        # --- Sub-label ---
        importLabel = Label(
            text="Import",
            font_size=24,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.65, 'center_y': 0.83},
            font_name=font_path,
        )
        layout.add_widget(importLabel)

        # --- Upload PDF Button ---
        show_filechooser_btn = Button(
            text="Upload PDF",
            size_hint=(None, None),
            size=(dp(125), dp(35)),
            pos_hint={'center_x': 0.68, 'center_y': 0.74},
            background_normal='',
            background_down='',
            background_color=(0, 0, 0, 0),  # transparent
            color=(1, 1, 1, 1),             # white text
            font_size=16,
            font_name=font_path
        )

        # --- White border for button ---
        with show_filechooser_btn.canvas.before:
            Color(1, 1, 1, 1)
            btn_border = Line(rectangle=(show_filechooser_btn.x, show_filechooser_btn.y,
                                        show_filechooser_btn.width, show_filechooser_btn.height),
                            width=1.5)

        def update_btn_border(*args):
            btn_border.rectangle = (
                show_filechooser_btn.x,
                show_filechooser_btn.y,
                show_filechooser_btn.width,
                show_filechooser_btn.height
            )

        show_filechooser_btn.bind(pos=update_btn_border, size=update_btn_border)
        show_filechooser_btn.bind(on_release=self.open_file_chooser)
        layout.add_widget(show_filechooser_btn)

        self.upload_status_label = Label(
            text="No files selected",
            font_size=16,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.67, 'center_y': 0.6},
            font_name=font_path,
            size_hint=(None, None),
        )
        # Measure text size dynamically
        self.upload_status_label.texture_update()
        self.upload_status_label.width = self.upload_status_label.texture_size[0] + dp(10)  # add small padding
        self.upload_status_label.height = self.upload_status_label.texture_size[1]
        self.upload_status_label.halign = "left"
        self.upload_status_label.valign = "middle"
        layout.add_widget(self.upload_status_label)

        # --- Back button ---
        back_btn = Button(
            text="Back",
            size=(120, 50),
            size_hint=(None, None),
            pos_hint={'x': 0.02, 'y': 0.02},
            background_normal='',
            background_color=(0, 0, 0, 0),
            font_name=font_path,
            font_size=28,
        )
        back_btn.bind(on_release=lambda instance: switch_screen(instance, self.manager, "start_page"))
        layout.add_widget(back_btn)

        self.add_widget(layout)
    
    def open_file_chooser(self, instance):
        content = FileChooserPopup(select_callback=self.files_chosen)
        popup = Popup(
            title="Select files",
            content=content,
            size_hint=(0.9, 0.9)
        )
        content.parent_popup = popup
        popup.open()

    def files_chosen(self, filepaths):
        self.upload_status_label.text = "Selected files:\n" + "\n".join(filepaths)
        

# --------- File Chooser Popup -------------
class FileChooserPopup(FloatLayout):
    def __init__(self, select_callback, **kwargs):
        super().__init__(**kwargs)
        self.select_callback = select_callback

        # FileChooserIconView with multiselect
        self.file_chooser = FileChooserIconView(
            size_hint=(0.95, 0.75),
            pos_hint={'x':0.025, 'y':0.2},
            multiselect=True
        )
        self.add_widget(self.file_chooser)

        # Up button
        self.up_button = Button(
            text="Up",
            size_hint=(0.2, 0.08),
            pos_hint={'x':0.025, 'y':0.1}
        )
        self.up_button.bind(on_release=self.go_up)
        self.add_widget(self.up_button)

        # Select button
        self.select_button = Button(
            text="Select",
            size_hint=(0.35, 0.08),
            pos_hint={'x':0.3, 'y':0.1}
        )
        self.select_button.bind(on_release=self.select_files)
        self.add_widget(self.select_button)

        # Close button
        self.close_button = Button(
            text="Close",
            size_hint=(0.2, 0.08),
            pos_hint={'x':0.7, 'y':0.1}
        )
        self.close_button.bind(on_release=self.close_popup)
        self.add_widget(self.close_button)

    def go_up(self, instance):
        parent = os.path.dirname(self.file_chooser.path)
        if parent:
            self.file_chooser.path = parent

    def select_files(self, instance):
        selection = self.file_chooser.selection
        if selection:
            accessible_files = []
            for f in selection:
                try:
                    os.stat(f)
                    accessible_files.append(f)
                except Exception as e:
                    print(f"Cannot access file {f}: {e}")
            if accessible_files:
                self.select_callback(accessible_files)
                self.parent_popup.dismiss()
        else:
            print("No files selected")

    def close_popup(self, instance):
        self.parent_popup.dismiss()

# ------------------- App ------------------
class AllInApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartPage(name="start_page"))
        sm.add_widget(GamePage(name="game_page"))
        sm.add_widget(CustomPage(name="custom_page"))
        return sm

if __name__ == "__main__":
    AllInApp().run()
