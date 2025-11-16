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
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.app import App
from kivy.clock import Clock
from utils.zingo_engine import ZingoEngine
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
    def __init__(self, bg_path, font_path, **kwargs):
        super().__init__(**kwargs)
        self.bg_path = bg_path
        self.font_path = font_path

        self.app = App.get_running_app()

        # Create a layout and attach it
        self.layout = FloatLayout()
        self.add_widget(self.layout) 

        self._build_background()
        self._build_headers()
        self._build_spinner()
        self._build_inputs()
        self._build_buttons()

    # ---------------------------
    # UI BUILDERS
    # ---------------------------

    def _build_background(self) -> None:
        """Set the background image with transparency."""
        with self.layout.canvas:
            Color(1, 1, 1, 0.25)
            self.bg_rect = Rectangle(source=self.bg_path, pos=(0, 0), size=Window.size)
        Window.bind(on_resize=self.update_rect)


    def _build_headers(self) -> None:
        """Create static and dynamic labels."""

        # --- Static labels ---
        self.titleLabel = self.create_label("CUSTOM", {'center_x': 0.1, 'center_y': 0.92}, 32)
        self.createQuestionLabel = self.create_label("Create Questions", {'center_x': 0.145, 'center_y': 0.83}, 24)
        self.questionLabel = self.create_label("Question:", {'center_x': 0.093, 'center_y': 0.63}, 20)
        self.answerLabel = self.create_label("Answer:", {'center_x': 0.087, 'center_y': 0.45}, 20)

        # --- Dynamic labels ---
        self.successLabel = self.create_label("", {'center_x': 0.8, 'center_y': 0.07}, 20)
        self.importLabel = self.create_label("Import", {'center_x': 0.65, 'center_y': 0.83}, 24)
        self.uploadStatusLabel = self.create_label("No files selected", {'center_x': 0.67, 'center_y': 0.6}, 16, auto_size=True)


    def _build_spinner(self) -> None:
        """Create question type spinner with border."""
        spinner_values = ("Short Answer", "Multiple Choice", "True/False")
        self.spinner_text = "Short Answer"

        spinner_width = self.fit_widget_width(spinner_values + (self.spinner_text,), self.font_path)

        self.questionTypeSpinner = Spinner(
            text=self.spinner_text,
            values=spinner_values,
            pos_hint={'center_x': 0.12, 'center_y': 0.73},
            size_hint=(None, None),
            size=(spinner_width, dp(32)),
            font_name=self.font_path,
            font_size=16,
            background_normal='',
            background_down='',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )

        self.add_border(self.questionTypeSpinner)
        self.layout.add_widget(self.questionTypeSpinner)
        self.questionTypeSpinner.bind(text=self.update_answer_inputs)


    def _build_inputs(self) -> None:
        """Create question and answer inputs and dynamic container."""
        # Question input
        self.questionInput = self.create_text_input("Enter question here...", {'center_x': 0.185, 'center_y': 0.56})
        self.layout.add_widget(self.questionInput)

        # Answer input
        self.answerInput = self.create_text_input("Enter answer here...", {'center_x': 0.18, 'center_y': 0.38})

        # Container for dynamic answer inputs
        self.answer_container = FloatLayout()
        self.layout.add_widget(self.answer_container)
        self.answer_container.add_widget(self.answerInput)

        # Initialize dynamic inputs for spinner selection
        self.update_answer_inputs(self.questionTypeSpinner, self.spinner_text)


    def _build_buttons(self) -> None:
        """Create all main buttons with optional borders."""

        # --- Save Question Button ---
        def on_save(instance):
            if self.questionTypeSpinner.text in ["Short Answer", "True/False"]:
                if not self.questionInput.text or not self.answerInput.text:
                    self.successLabel.text = "Please fill in all fields."
                    return
            elif self.questionTypeSpinner.text == "Multiple Choice":
                if not self.questionInput.text or any(not i.text.strip() for i in self.answer_inputs):
                    self.successLabel.text = "Please fill in all fields."
                    return

            question_type = self.questionTypeSpinner.text
            question = self.questionInput.text

            if question_type == "Multiple Choice":
                initial_choices = [i.text.strip() for i in self.answer_inputs if i.text.strip()]
                answer = initial_choices[0] if initial_choices else ""
                choices = [random.sample(initial_choices, len(initial_choices))]
                for input_box in self.answer_inputs:
                    input_box.text = ""
            elif question_type == "True/False":
                answer = self.answer_dropdown.text if self.answer_dropdown.text != "Select Answer" else ""
                choices = ["True", "False"]
            else:
                answer = self.answerInput.text.strip()
                choices = None

            data = self.load_questions_data()
            data.append({"question_type": question_type, "question": question, "answer": answer, "choices": choices})
            self.save_questions_data(data)

            self.app.load_questions()
            self.questionInput.text = ""
            self.answerInput.text = ""
            self.successLabel.text = "Question successfully saved!"

        self.create_button("saveQuestionBtn", "Save Question", {'center_x': 0.128, 'center_y': 0.2}, on_release=on_save)

        # --- Upload PDF Button ---
        self.create_button("uploadBtn", "Upload PDF", {'center_x': 0.68, 'center_y': 0.74},
                        bg_color=(0, 0, 0, 0), text_color=(1, 1, 1, 1), on_release=self.open_file_chooser)

        # --- Show Questions Button ---
        self.create_button("showQuestionsBtn", "Show Questions", {'center_x': 0.7, 'center_y': 0.35},
                        bg_color=(0, 0, 0, 0), text_color=(1, 1, 1, 1), on_release=self.show_questions_popup)

        # --- Back Button (no border) ---
        self.create_button("backBtn", "Back", {'x': 0.035, 'y': 0.05}, font_size=28, width_padding=0, height_padding=0,
                        bg_color=(0, 0, 0, 0), text_color=(1, 1, 1, 1), auto_size=True,
                        on_release=lambda inst: switch_screen(inst, self.manager, "start_page"),
                        add_border_flag=False)


    # ---------------------------
    # HELPER FUNCTIONS
    # ---------------------------

    def create_label(self, text, pos_hint=None, font_size=20, color=(1,1,1,1), auto_size=False):
        """Create a Label, optionally auto-size, and add to layout."""
        label = Label(text=text, font_size=font_size, color=color, font_name=self.font_path, pos_hint=pos_hint)
        self.layout.add_widget(label)

        if auto_size:
            label.size_hint = (None, None)
            label.texture_update()
            label.width = label.texture_size[0] + dp(10)
            label.height = label.texture_size[1]
            label.halign = "left"
            label.valign = "middle"
        return label


    def create_text_input(self, hint_text, pos_hint):
        """Create a bordered TextInput and bind focus clearing."""
        label = CoreLabel(text=hint_text, font_name=self.font_path, font_size=16)
        label.refresh()
        width, height = label.texture.size
        width += dp(100)
        height += dp(12)

        ti = TextInput(
            hint_text=hint_text,
            multiline=False,
            size_hint=(None, None),
            size=(width, height),
            pos_hint=pos_hint,
            background_normal='',
            background_active='',
            background_color=(0,0,0,0),
            foreground_color=(1,1,1,1),
            cursor_color=(1,1,1,1),
            hint_text_color=(1,1,1,0.4),
            font_name=self.font_path,
            font_size=16,
        )

        self.add_border(ti)
        ti.bind(focus=self.clear_success_label)
        return ti


    def create_button(self, attr_name, text, pos_hint=None, font_size=16, width_padding=60, height_padding=12,
                    bg_color=(1,1,1,1), text_color=(0,0,0,1), auto_size=True, on_release=None,
                    add_border_flag=True):
        """Create a Button with optional border."""
        if auto_size:
            label = CoreLabel(text=text, font_name=self.font_path, font_size=font_size)
            label.refresh()
            btn_width = label.texture.size[0] + dp(width_padding)
            btn_height = label.texture.size[1] + dp(height_padding)
        else:
            btn_width, btn_height = dp(125), dp(35)

        btn = Button(
            text=text,
            size_hint=(None, None),
            size=(btn_width, btn_height),
            pos_hint=pos_hint,
            background_normal='',
            background_down='',
            background_color=bg_color,
            color=text_color,
            font_name=self.font_path,
            font_size=font_size,
        )

        if on_release:
            btn.bind(on_release=on_release)

        self.layout.add_widget(btn)
        setattr(self, attr_name, btn)
        if add_border_flag:
            self.add_border(btn)
        return btn


    def add_border(self, widget, color=(1,1,1,1), width=1.5):
        """Add a rectangle border to a widget and update on resize/move."""
        with widget.canvas.before:
            Color(*color)
            widget.border_line = Line(width=width)

        def update(*_):
            widget.border_line.rectangle = (widget.x, widget.y, widget.width, widget.height)

        widget.bind(pos=update, size=update)
        update()


    def fit_widget_width(self, texts, font_name, font_size=16, padding=40):
        """Calculate dp width to fit the longest text."""
        longest = max(texts, key=len)
        label = CoreLabel(text=longest, font_name=font_name, font_size=font_size)
        label.refresh()
        return label.texture.size[0] + dp(padding)


    def load_questions_data(self):
        """Load JSON questions safely."""
        try:
            with open(self.app.QUESTIONS_JSON_PATH, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []


    def save_questions_data(self, data):
        """Save JSON questions."""
        with open(self.app.QUESTIONS_JSON_PATH, 'w') as f:
            json.dump(data, f, indent=4)


    # ---------------------------
    # EVENTS
    # ---------------------------

    def update_rect(self, instance, width, height):
        self.bg_rect.size = (width, height)

    # ---------------------------
    # HELPERS
    # ---------------------------

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
        if not filepaths:
            print("No file selected.")
            return

        # -------------------------------
        # Load existing questions FIRST
        # -------------------------------
        try:
            with open(self.app.QUESTIONS_JSON_PATH, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            existing_data = []

        # Build a fast lookup set for duplicate detection
        # normalized questions only
        existing_questions_set = {
            self.normalize_text(q["question"]).lower()
            for q in existing_data
            if "question" in q
        }

        all_pdf_text = ""

        # -------------------------------
        # Read each PDF
        # -------------------------------
        for filepath in filepaths:
            if not filepath.lower().endswith(".pdf"):
                print(f"Skipped non-PDF file: {filepath}")
                continue

            try:
                doc = fitz.open(filepath)
                extracted = ""

                for page in doc:
                    txt = page.get_text("text")
                    if txt.strip():
                        extracted += txt + "\n"

                doc.close()
                all_pdf_text += extracted + "\n"

            except Exception as e:
                print(f"Error reading {filepath}: {e}")

        # Normalize text
        all_pdf_text = all_pdf_text.replace("\r\n", "\n").strip()

        # -------------------------------------------------------
        # Extract all Question + Answer blocks from the PDF text
        # -------------------------------------------------------
        pattern = r"Question\s*\d*:\s*(.*?)\nAnswer:\s*(.*?)(?=\nQuestion|\Z)"
        matches = re.findall(pattern, all_pdf_text, flags=re.DOTALL)

        new_questions_added = 0

        # -------------------------------
        # Process each extracted QA block
        # -------------------------------
        for question_text, answer_block in matches:

            cleaned_q = self.normalize_text(question_text).lower()

            # Skip duplicates
            if cleaned_q in existing_questions_set:
                print(f"Skipped duplicate: {question_text}")
                continue

            # Process answers
            answers = [self.normalize_text(a) for a in answer_block.split(",") if a.strip()]
            answer = answers[0]

            # Determine question type
            if len(answers) > 1:
                qtype = "Multiple Choice"
                choices = answers[:]      # copy list
                random.shuffle(choices)   # shuffle the MCQs
            elif answer in ("True", "False"):
                qtype = "True/False"
                choices = ["True", "False"]
            else:
                qtype = "Short Answer"
                choices = None

            # Append NEW question only
            new_item = {
                "question_type": qtype,
                "question": self.normalize_text(question_text),
                "answer": answer,
                "choices": [choices] if choices else [None]
            }

            existing_data.append(new_item)
            existing_questions_set.add(cleaned_q)
            new_questions_added += 1

        # -------------------------------
        # Save updated questions.json
        # -------------------------------
        with open(self.app.QUESTIONS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        # Refresh app data
        self.app.load_questions()

        print(f"Imported {new_questions_added} new unique questions.")
        print("Total questions:", len(existing_data))


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
