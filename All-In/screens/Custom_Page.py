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
from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.app import App
from kivy.clock import Clock
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
        spinner_values = ("Multiple Choice", "True/False", "Short Answer")
        spinner_text = "Select Question Type"

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
        layout.add_widget(self.questionInput)

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
        _update_answerInput_border()
        layout.add_widget(self.answerInput)

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

        def on_save_question(instance):
            self.successLabel.text = "Question successfully saved!"

            question_type = self.questionTypeSpinner.text
            question = self.questionInput.text
            answer_text = self.answerInput.text.split(',')

            if self.questionTypeSpinner.text == "Multiple Choice":
                answer = answer_text[0]
                choices = [answer_text[1:]]
            elif self.questionTypeSpinner.text == "True/False":
                answer = answer_text[0]
                choices = ["True", "False"]
            else:
                answer = answer_text[0]
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


        save_question_btn.bind(on_release=on_save_question)
        layout.add_widget(save_question_btn)

        # --- Success label ---
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

    # ---------------------------
    # Popup to show saved questions
    # ---------------------------
    def show_questions_popup(self, instance=None):
        app = App.get_running_app()
        questions = app.QUESTIONS

        # --- Main container ---
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # --- Scrollable area ---
        scroll = ScrollView(size_hint=(1, 0.85))
        inner_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        inner_layout.bind(minimum_height=inner_layout.setter('height'))

        # --- Popup (create early so it's in scope) ---
        popup = Popup(
            title="All Questions",
            size_hint=(0.7, 0.8),
            auto_dismiss=False,
        )

        # --- Helper function to update numbering ---
        def update_question_numbers():
            for i, container in enumerate(reversed(inner_layout.children)):
                for widget in container.walk():
                    if isinstance(widget, Label):
                        text_parts = widget.text.split('.', 1)
                        if len(text_parts) > 1:
                            widget.text = f"[b]{i + 1}.[/b]{text_parts[1]}"
                        break

        # --- Function to remove question ---
        def remove_question(question, question_container):
            try:
                with open(self.app.QUESTIONS_JSON_PATH, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                question_clean = question.strip().lower()
                deleted = False

                for i, item in enumerate(data):
                    if item.get('question', '').strip().lower() == question_clean:
                        del data[i]
                        deleted = True
                        print(f"Deleted question: '{question}'")
                        break

                if not deleted:
                    print(f"No question found matching: '{question}'")

                # Save changes
                with open(self.app.QUESTIONS_JSON_PATH, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)

                # Remove the question visually from the layout
                inner_layout.remove_widget(question_container)

                # Update numbering visually
                update_question_numbers()

            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"JSON error: {e}")

            self.app.load_questions()

        # --- Populate questions ---
        for idx, q in enumerate(questions):
            question_container = BoxLayout(orientation='vertical', size_hint_y=None)

            # Row for label and delete button
            row = BoxLayout(size_hint_y=None, height=dp(60), spacing=10, padding=[10, 5, 10, 5])

            # Label
            question_label = Label(
                text=f"[b]{idx + 1}.[/b] {q.get('question', '')}",
                markup=True,
                halign="left",
                valign="middle",
                text_size=(dp(400), None),
                color=(1, 1, 1, 1)
            )
            question_label.bind(
                size=lambda *_: setattr(question_label, 'text_size', (question_label.width - dp(10), None))
            )

            # Delete button
            delete_btn = Button(
                text="X",
                size_hint=(None, None),
                size=(dp(35), dp(35)),
                background_normal='',
                background_color=(1, 0, 0, 0.8),
                color=(1, 1, 1, 1),
            )
            delete_btn.bind(on_release=lambda instance, q_text=q.get('question', ''), qc=question_container: remove_question(q_text, qc))

            row.add_widget(question_label)
            row.add_widget(delete_btn)
            question_container.add_widget(row)

            # Separator line
            separator = Widget(size_hint_y=None, height=dp(1))
            with separator.canvas.after:
                Color(1, 1, 1, 0.3)
                line = Line(points=[])

            def update_separator(*_):
                x, y = separator.x + dp(10), separator.y
                w = separator.width - dp(20)
                line.points = [x, y, x + w, y]

            separator.bind(pos=update_separator, size=update_separator)
            question_container.add_widget(separator)
            inner_layout.add_widget(question_container)

        scroll.add_widget(inner_layout)
        main_layout.add_widget(scroll)

        # Close button
        close_btn = Button(
            text="Close",
            size_hint=(1, 0.15),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_name=app.font_path
        )
        close_btn.bind(on_release=lambda *_: popup.dismiss())
        main_layout.add_widget(close_btn)

        popup.content = main_layout
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

                for question_text, answer_text in matches:
                    question = question_text.strip()
                    answer_text = answer_text.split(',')

                    if len(answer_text) > 1:
                        question_type = "Multiple Choice"
                        answer = answer_text[0]
                        choices = [answer_text[1:]]
                    elif answer_text[0] in ["True", "False"]:
                        question_type = "True/False"
                        answer = answer_text[0]
                        choices = ["True", "False"]
                    else:
                        question_type = "Short Answer"
                        answer = answer_text[0]
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
