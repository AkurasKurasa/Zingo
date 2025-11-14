# screens/custom_page.py
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.app import App
from kivy.clock import Clock
import unicodedata
import random
import json
import fitz
import re
import os


def switch_screen(instance, manager, screen_name):
    """Switch to another screen using the manager."""
    if manager and screen_name in manager.screen_names:
        manager.current = screen_name
    else:
        print(f"Screen '{screen_name}' not found in manager.")


class CustomPage(Screen):
    def __init__(self, font_path, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        # keep app instance available across methods
        self.app = App.get_running_app()

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
        spinner_values = ("Short Answer", "Multiple Choice", "True/False")
        spinner_text = "Short Answer"

        def fit_spinner_width(texts, font_name, font_size=16, padding=40):
            longest = max(texts, key=len)
            label = CoreLabel(text=longest, font_name=font_name, font_size=font_size)
            label.refresh()
            text_width = label.texture.size[0]
            return text_width + dp(padding)

        spinner_width = fit_spinner_width(spinner_values + (spinner_text,), font_path)

        self.questionTypeSpinner = Spinner(
            text=spinner_text,
            values=spinner_values,
            pos_hint={'center_x': 0.12, 'center_y': 0.73},
            size_hint=(None, None),
            size=(spinner_width, dp(32)),
            font_name=font_path,
            font_size=16,
            background_normal='',
            background_down='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )

        # --- Spinner border (create empty line and update later) ---
        with self.questionTypeSpinner.canvas.before:
            Color(1, 1, 1, 1)
            self._spinner_border = Line(width=1.5)

        def _update_spinner_border(*_):
            self._spinner_border.rectangle = (
                self.questionTypeSpinner.x,
                self.questionTypeSpinner.y,
                self.questionTypeSpinner.width,
                self.questionTypeSpinner.height,
            )

        self.questionTypeSpinner.bind(pos=_update_spinner_border, size=_update_spinner_border)
        _update_spinner_border()
        layout.add_widget(self.questionTypeSpinner)        

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
        self.questionInput = TextInput(
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


        with self.questionInput.canvas.before:
            Color(1, 1, 1, 1)
            self._question_input_border = Line(width=1.5)

        def _update_questionInput_border(*_):
            self._question_input_border.rectangle = (
                self.questionInput.x,
                self.questionInput.y,
                self.questionInput.width,
                self.questionInput.height,
            )

        self.questionInput.bind(pos=_update_questionInput_border, size=_update_questionInput_border)
        _update_questionInput_border()
        self.questionInput.bind(focus=self.clear_success_label)
        layout.add_widget(self.questionInput)

        # --- Answer label ---
        answerLabel = Label(
            text="Answer:",
            font_size=20,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.075, 'center_y': 0.45},
            font_name=font_path,
        )
        layout.add_widget(answerLabel)

        # --- Answer input box ---
        answerInput_hint_text = "Enter answer here..."
        answerInputLabel = CoreLabel(text=answerInput_hint_text, font_name=font_path, font_size=16)
        answerInputLabel.refresh()
        text_width, text_height = answerInputLabel.texture.size

        answerInput_width = text_width + dp(100)   # add padding
        answerInput_height = text_height + dp(12) # add vertical padding

        self.answerInput = TextInput(
            hint_text=answerInput_hint_text,
            multiline=False,
            size_hint=(None, None),
            size=(answerInput_width, answerInput_height),
            pos_hint={'center_x': 0.18, 'center_y': 0.38},
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),   # transparent
            foreground_color=(1, 1, 1, 1),   # white text
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(1, 1, 1, 0.4),
            font_name=font_path,
            font_size=16,
        )

        with self.answerInput.canvas.before:
            Color(1, 1, 1, 1)
            self._answer_input_border = Line(width=1.5)


        def _update_answerInput_border(*_):
            self._answer_input_border.rectangle = (
                self.answerInput.x,
                self.answerInput.y,
                self.answerInput.width,
                self.answerInput.height,
            )

        self.answerInput.bind(pos=_update_answerInput_border, size=_update_answerInput_border)
        self.answerInput.bind(focus=self.clear_success_label)
        _update_answerInput_border()
        # --- Container to hold answer inputs dynamically ---
        self.answer_container = FloatLayout()
        layout.add_widget(self.answer_container)

        self.answer_container.add_widget(self.answerInput)

        self.update_answer_inputs(self.questionTypeSpinner, spinner_text)


        # Bind spinner event
        self.questionTypeSpinner.bind(text=self.update_answer_inputs)

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
            pos_hint={'center_x': 0.128, 'center_y': 0.2},
            background_normal='',
            background_down='',
            background_color=(1, 1, 1, 1),  # white background
            color=(0, 0, 0, 1),             # black text
            font_name=font_path,
            font_size=16,
        )

        def on_save_question(instance):

            # --- Update Fields and States ---

            if self.questionTypeSpinner.text in ["Short Answer", "True/False"]:

                if self.questionInput.text == "" or self.answerInput.text == "":
                    self.successLabel.text = "Please fill in all fields."
                    return

            if self.questionTypeSpinner.text == "Multiple Choice":

                if self.questionInput.text == "" or any(not i.text.strip() for i in self.answer_inputs):
                    self.successLabel.text = "Please fill in all fields."
                    return


            # --- Save Question to JSON ---
            question_type = self.questionTypeSpinner.text
            question = self.questionInput.text

            if self.questionTypeSpinner.text == "Multiple Choice":
                initial_choices = [i.text.strip() for i in self.answer_inputs if i.text.strip()]
                answer = initial_choices[0] if initial_choices else ""
                choices = [random.sample(initial_choices, len(initial_choices))]

                for input_box in self.answer_inputs:
                    input_box.text = ""

            elif self.questionTypeSpinner.text == "True/False":
                answer = self.answer_dropdown.text if self.answer_dropdown.text != "Select Answer" else ""
                choices = ["True", "False"]
            else:
                answer = self.answerInput.text.strip()
                choices = None

            try:
                with open(self.app.QUESTIONS_JSON_PATH, 'r') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                data = []  

            new_question = {
                "question_type": question_type,
                "question": question,
                "answer": answer,
                "choices": choices
            }

            data.append(new_question)

            with open(self.app.QUESTIONS_JSON_PATH, 'w') as file:
                json.dump(data, file, indent=4)

            self.app.load_questions()

            self.answerInput.text = ""
            self.questionInput.text = ""
            self.successLabel.text = "Question successfully saved!"


        save_question_btn.bind(on_release=on_save_question)
        layout.add_widget(save_question_btn)

        # --- Success label ---
        self.successLabel = Label(
            text="",
            font_size=20,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.8, 'center_y': 0.07},
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

        # --- White border for upload button (create line and update) ---
        with show_filechooser_btn.canvas.before:
            Color(1, 1, 1, 1)
            self._upload_btn_border = Line(width=1.5)

        def _update_upload_btn_border(*_):
            self._upload_btn_border.rectangle = (
                show_filechooser_btn.x,
                show_filechooser_btn.y,
                show_filechooser_btn.width,
                show_filechooser_btn.height
            )

        show_filechooser_btn.bind(pos=_update_upload_btn_border, size=_update_upload_btn_border)
        _update_upload_btn_border()
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

        # --- Show Questions Button ---
        show_questions_btn = Button(
            text="Show Questions",
            size_hint=(None, None),
            size=(dp(125), dp(35)),
            pos_hint={'center_x': 0.68, 'center_y': 0.35},
            background_normal='',
            background_down='',
            background_color=(0, 0, 0, 0),  # transparent
            color=(1, 1, 1, 1),             # white text
            font_size=16,
            font_name=font_path
        )

        # --- White border for show questions button ---
        with show_questions_btn.canvas.before:
            Color(1, 1, 1, 1)
            self._show_btn_border = Line(width=1.5)

        def _update_show_btn_border(*_):
            self._show_btn_border.rectangle = (
                show_questions_btn.x,
                show_questions_btn.y,
                show_questions_btn.width,
                show_questions_btn.height
            )

        show_questions_btn.bind(pos=_update_show_btn_border, size=_update_show_btn_border)
        _update_show_btn_border()
        # show questions should open the questions popup, not file chooser
        show_questions_btn.bind(on_release=self.show_questions_popup)
        layout.add_widget(show_questions_btn)

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

    def normalize_text(self, s):
        if not s:
            return ""
        # Normalize unicode
        s = unicodedata.normalize("NFKD", s)
        # Replace curly quotes with straight quotes
        s = s.replace("’", "'").replace("‘", "'")
        s = s.replace("“", '"').replace("”", '"')
        # Strip spaces/newlines
        return s.strip()

    def clear_success_label(self, instance, value):
            if value:  # Only when the TextInput gains focus
                self.successLabel.text = ""

    def update_answer_inputs(self, spinner, text):
        """Switch between single and multiple answer input fields."""
        self.answer_container.clear_widgets()
        font_path = App.get_running_app().font_path

        # -------------------------------
        # MULTIPLE CHOICE
        # -------------------------------
        if text == "Multiple Choice":
            self.answer_inputs = []
            y_positions = [0.38, 0.38, 0.305, 0.305]
            x_positions = [0.115, 0.280, 0.115, 0.280]
            labels = ["Correct Answer", "Choice 1", "Choice 2", "Choice 3"]

            for i, y in enumerate(y_positions):
                input_box = TextInput(
                    hint_text=labels[i],
                    multiline=False,
                    size_hint=(None, None),
                    size=(dp(125), dp(25)),
                    pos_hint={'center_x': x_positions[i], 'center_y': y},
                    background_normal='',
                    background_active='',
                    background_color=(0, 0, 0, 0),
                    foreground_color=(1, 1, 1, 1),
                    cursor_color=(1, 1, 1, 1),
                    hint_text_color=(1, 1, 1, 0.4),
                    font_name=font_path,
                    font_size=16,
                )

                # Add white border
                with input_box.canvas.before:
                    Color(1, 1, 1, 1)
                    input_box.border_line = Line(width=1.5)

                def update_border(instance, *_):
                    if hasattr(instance, 'border_line'):
                        instance.border_line.rectangle = (instance.x, instance.y, instance.width, instance.height)

                input_box.bind(pos=update_border, size=update_border)
                input_box.bind(focus=self.clear_success_label)
                Clock.schedule_once(lambda dt, inst=input_box: update_border(inst), 0)

                self.answer_inputs.append(input_box)
                self.answer_container.add_widget(input_box)

        # -------------------------------
        # TRUE / FALSE (turn into dropdown)
        # -------------------------------
        elif text == "True/False":
            self.answer_dropdown = Spinner(
                text="Select Answer",
                values=("True", "False"),
                size_hint=(None, None),
                size=(dp(125), dp(30)),
                pos_hint={'center_x': 0.115, 'center_y': 0.38},
                font_size=16,
                font_name=font_path,
                background_normal='',
                background_down='',
                background_color=(0, 0, 0, 0),
                color=(1, 1, 1, 1),
            )

            # Add white border
            with self.answer_dropdown.canvas.before:
                Color(1, 1, 1, 1)
                self.answer_dropdown.border_line = Line(width=1.5)

            def update_border_tf(*_):
                self.answer_dropdown.border_line.rectangle = (
                    self.answer_dropdown.x,
                    self.answer_dropdown.y,
                    self.answer_dropdown.width,
                    self.answer_dropdown.height,
                )

            self.answer_dropdown.bind(pos=update_border_tf, size=update_border_tf)
            update_border_tf()

            # Put spinner on screen
            self.answer_container.add_widget(self.answer_dropdown)

        # -------------------------------
        # SHORT ANSWER (default text input)
        # -------------------------------
        else:
            self.answer_container.add_widget(self.answerInput)

        

    # ---------------------------
    # Popup to show saved questions
    # ---------------------------
    def show_questions_popup(self, instance=None):
        app = App.get_running_app()
        questions = app.QUESTIONS

        # --- Popup container ---
        popup = Popup(
            title="",
            size_hint=(0.75, 0.82),
            background='',    # remove default
            background_color=(0, 0, 0, 0.6),
            auto_dismiss=False,
            separator_height=0
        )

        # --- Card container ---
        card = BoxLayout(
            orientation='vertical',
            padding=dp(12),
            spacing=dp(12),
            size_hint=(1, 1)
        )

        # Background + border
        with card.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            card.bg_rect = Rectangle(pos=card.pos, size=card.size)

            Color(1, 1, 1, 1)  # WHITE border
            card.border = Line(rectangle=(card.x, card.y, card.width, card.height), width=1.4)

        def update_card(*_):
            card.bg_rect.pos = card.pos
            card.bg_rect.size = card.size
            card.border.rectangle = (card.x, card.y, card.width, card.height)

        card.bind(pos=update_card, size=update_card)

        # --- Title ---
        title_label = Label(
            text="[b]ALL QUESTIONS[/b]",
            markup=True,
            font_size="22sp",
            size_hint=(1, None),
            height=dp(35),
            halign="center",
            valign="middle",
            font_name=app.font_path,
            color=(1, 1, 1, 1),
        )
        title_label.bind(size=lambda *_: setattr(title_label, "text_size", (title_label.width, None)))
        card.add_widget(title_label)

        # --- Scroll area ---
        scroll = ScrollView(size_hint=(1, 0.82))

        inner = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(5), dp(5)],
            size_hint_y=None,
        )
        inner.bind(minimum_height=inner.setter("height"))

        # Update numbering
        def update_question_numbers():
            ordered = inner.children[::-1]  # correct top-to-bottom order
            for i, container in enumerate(ordered):
                row = container.children[-1]
                label = row.children[-1]
                raw = label.text.split('.', 1)[-1].strip()
                label.text = f"[b]{i+1}.[/b] {raw}"

        # Remove question
        def remove_question(q_text, container):
            try:
                with open(self.app.QUESTIONS_JSON_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                q_clean = q_text.strip().lower()
                data = [q for q in data if q.get("question", "").strip().lower() != q_clean]

                with open(self.app.QUESTIONS_JSON_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

                inner.remove_widget(container)
                update_question_numbers()

            except Exception as e:
                print("JSON error:", e)

            self.app.load_questions()

        # --- Populate questions ---
        for idx, q in enumerate(questions):
            container = BoxLayout(
                orientation="vertical",
                size_hint_y=None
            )

            row = BoxLayout(
                size_hint_y=None,
                height=dp(55),
                spacing=dp(10),
                padding=[dp(10), dp(5), dp(10), dp(5)]
            )

            # Label
            question_label = Label(
                text=f"[b]{idx+1}.[/b] {q.get('question', '')}",
                markup=True,
                halign="left",
                valign="middle",
                font_name=app.font_path,
                color=(1, 1, 1, 1),
            )
            question_label.bind(
                size=lambda inst, val: setattr(inst, "text_size", (val[0] - dp(15), None))
            )

            # Delete button
            delete_btn = Button(
                text="x",
                size_hint=(None, None),
                size=(dp(32), dp(32)),
                background_normal='',
                background_color=(0.9, 0.2, 0.2, 0.8),
                color=(1, 1, 1, 1),
                font_size="16sp",
                font_name=app.font_path
            )
            delete_btn.bind(
                on_release=lambda inst, qt=q.get('question', ''), c=container: remove_question(qt, c)
            )

            row.add_widget(question_label)
            row.add_widget(delete_btn)
            container.add_widget(row)

            inner.add_widget(container)

        scroll.add_widget(inner)
        card.add_widget(scroll)

        # --- Close button ---
        close_btn = Button(
            text="[b]CLOSE[/b]",
            markup=True,
            size_hint=(1, None),
            height=dp(50),
            background_normal='',
            background_color=(0.25, 0.25, 0.25, 1),
            color=(1, 1, 1, 1),
            font_size="18sp",
            font_name=app.font_path
        )
        close_btn.bind(on_release=lambda *_: popup.dismiss())
        card.add_widget(close_btn)

        popup.content = card
        popup.open()



    # ---------------------------
    # File chooser and PDF import
    # ---------------------------
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

        if not filepaths:
            print("No file selected.")
            return

        for filepath in filepaths:
            if not filepath.lower().endswith(".pdf"):
                print(f"Skipped non-PDF file: {filepath}")
                continue

            try:
                doc = fitz.open(filepath)
                text = ""
                for page in doc:
                    text += page.get_text("text")
                doc.close()

                print(f"\n--- PDF Content ({filepath}) ---\n")

                # Normalize newlines (handles both \n and \r\n)
                normalized_text = text.strip().replace("\r\n", "\n")

                # Use regex to find all Question + Answer pairs
                pattern = r"Question\s*\d*:\s*(.*?)\nAnswer:\s*(.*?)(?=\nQuestion|\Z)"
                matches = re.findall(pattern, normalized_text, flags=re.DOTALL)

                for question_text, answer_block in matches:

                    # Normalize text BEFORE using it
                    question = self.normalize_text(question_text)

                    # Split answers then normalize each one
                    split_answers = [self.normalize_text(a) for a in answer_block.split(',')]

                    answer = split_answers[0]  # correct answer is always first

                    # Determine question type
                    if len(split_answers) > 1:
                        question_type = "Multiple Choice"
                        choices = [random.sample(split_answers, len(split_answers))]

                    elif answer in ["True", "False"]:
                        question_type = "True/False"
                        choices = ["True", "False"]

                    else:
                        question_type = "Short Answer"
                        choices = None

                    try:
                        with open(self.app.QUESTIONS_JSON_PATH, 'r') as file:
                            data = json.load(file)
                    except (FileNotFoundError, json.JSONDecodeError):
                        data = []  

                    new_question = {
                        "question_type": question_type,
                        "question": question,
                        "answer": answer,
                        "choices": choices
                    }

                    data.append(new_question)

                    with open(self.app.QUESTIONS_JSON_PATH, 'w') as file:
                        json.dump(data, file, indent=4)

                self.app.load_questions()

                # Show results in console
                for q in self.app.QUESTIONS:
                    print(q)

            except Exception as e:
                print(f"Error reading {filepath}: {e}")


# --------- File Chooser Popup -------------
class FileChooserPopup(FloatLayout):
    def __init__(self, select_callback, **kwargs):
        super().__init__(**kwargs)
        self.select_callback = select_callback

        # FileChooserIconView with multiselect
        self.file_chooser = FileChooserIconView(
            size_hint=(0.95, 0.75),
            pos_hint={'x': 0.025, 'y': 0.2},
            multiselect=True
        )
        self.add_widget(self.file_chooser)

        # Up button
        self.up_button = Button(
            text="Up",
            size_hint=(0.2, 0.08),
            pos_hint={'x': 0.025, 'y': 0.1}
        )
        self.up_button.bind(on_release=self.go_up)
        self.add_widget(self.up_button)

        # Select button
        self.select_button = Button(
            text="Select",
            size_hint=(0.35, 0.08),
            pos_hint={'x': 0.3, 'y': 0.1}
        )
        self.select_button.bind(on_release=self.select_files)
        self.add_widget(self.select_button)

        # Close button
        self.close_button = Button(
            text="Close",
            size_hint=(0.2, 0.08),
            pos_hint={'x': 0.7, 'y': 0.1}
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
                # dismiss parent popup if present
                if hasattr(self, "parent_popup"):
                    self.parent_popup.dismiss()
        else:
            print("No files selected")

    def close_popup(self, instance):
        if hasattr(self, "parent_popup"):
            self.parent_popup.dismiss()
