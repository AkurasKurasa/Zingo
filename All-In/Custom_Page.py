from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.filechooser import FileChooserListView
import os

# --- Font Setup ---
font_path = os.path.join(os.path.dirname(__file__), "fonts", "PixelifySans-Regular.ttf")
if not os.path.exists(font_path):
    font_path = 'Roboto' 

def switch_screen(instance, screen_manager, target_screen):
    screen_manager.current = target_screen

def add_white_border(widget, width=1.5):
    with widget.canvas.before:
        Color(1, 1, 1, 1)
        border = Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=width)
    widget.bind(pos=lambda instance, val, b=border: setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))
    widget.bind(size=lambda instance, val, b=border: setattr(b, 'rectangle', (instance.x, instance.y, instance.width, instance.height)))

def _make_textinput(hint, height):
    ti = TextInput(
        hint_text=hint, multiline=True, size_hint_y=None, height=height,
        background_normal="", background_color=(0,0,0,0),
        foreground_color=(1,1,1,1), cursor_color=(1,1,1,1),
        hint_text_color=(1,1,1,0.4),
        font_name=font_path, font_size=16
    )
    add_white_border(ti)
    return ti

def _make_button(text, size):
    btn = Button(
        text=text, size_hint=(None, None), size=size, pos_hint={'center_x':0.5},
        background_normal="", background_color=(0,0,0,0),
        color=(1,1,1,1), font_name=font_path, font_size=18
    )
    add_white_border(btn)
    return btn

def _make_spinner():
    class CustomSpinnerOption(SpinnerOption):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.background_normal = ""
            self.background_color = (0.1,0.1,0.1,1)
            self.color = (1,1,1,1)
            self.font_name = font_path
            self.font_size = 16
    spinner = Spinner(
        text="Short Answer",
        values=("Multiple Choice", "True/False", "Short Answer"),
        size_hint_x=0.5,
        font_name=font_path, font_size=16,
        background_normal="", background_color=(0,0,0,0),
        color=(1,1,1,1),
        option_cls=CustomSpinnerOption
    )
    add_white_border(spinner)
    return spinner

class CustomPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        root = FloatLayout()

        with root.canvas.before:
            Color(0.05,0.05,0.05,1)
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda inst,val: setattr(self.bg_rect, 'pos', val))
        root.bind(size=lambda inst,val: setattr(self.bg_rect, 'size', val))

        scroll_view = ScrollView(
            size_hint=(0.9,0.95),
            pos_hint={"center_x":0.5, "center_y":0.5},
            bar_width=dp(8), scroll_type=['bars','content'], do_scroll_x=False
        )
        main_layout = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=dp(15),
            padding=[dp(10),dp(10),dp(10),dp(20)]
        )
        main_layout.bind(minimum_height=main_layout.setter("height"))

        main_layout.add_widget(Label(text="CUSTOM", font_name=font_path, font_size=32,
                                     color=(1,1,1,1), size_hint_y=None, height=dp(40)))
        main_layout.add_widget(Label(text="Create Questions", font_name=font_path, font_size=24,
                                     color=(1,1,1,1), size_hint_y=None, height=dp(30)))

        # Question Type
        qtype_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        qtype_layout.add_widget(Label(text="Select Question Type:", font_name=font_path, font_size=20,
                                      color=(1,1,1,1), size_hint_x=0.5))
        self.questionTypeSpinner = _make_spinner()
        qtype_layout.add_widget(self.questionTypeSpinner)
        main_layout.add_widget(qtype_layout)

        # Question & Answer Inputs
        main_layout.add_widget(Label(text="Question Text:", font_name=font_path, font_size=20,
                                     color=(1,1,1,1), size_hint_y=None, height=dp(30)))
        self.questionInput = _make_textinput("Enter your question text here...", dp(100))
        main_layout.add_widget(self.questionInput)

        main_layout.add_widget(Label(text="Correct Answer:", font_name=font_path, font_size=20,
                                     color=(1,1,1,1), size_hint_y=None, height=dp(30)))
        self.answerInput = _make_textinput("Enter the correct answer...", dp(80))
        main_layout.add_widget(self.answerInput)

        # Multiple Choice Inputs
        self.mc_box = BoxLayout(orientation='vertical', size_hint_y=None, height=0, spacing=dp(10))
        self.mc_answers = []
        for i in range(4):
            mc_input = _make_textinput(f"Option {chr(65+i)}...", dp(50))
            mc_input.opacity = 0
            mc_input.disabled = True
            mc_input.height = 0
            self.mc_answers.append(mc_input)
            self.mc_box.add_widget(mc_input)
        main_layout.add_widget(self.mc_box)

        # Buttons
        self.save_btn = _make_button("Save Question", (dp(200), dp(50)))
        self.save_btn.bind(on_release=self.save_question)
        main_layout.add_widget(self.save_btn)

        # Upload PDF button
        self.upload_btn = _make_button("Upload PDF", (dp(200), dp(50)))
        self.upload_btn.bind(on_release=self.open_pdf_popup)
        main_layout.add_widget(self.upload_btn)

        # Success Label
        self.successLabel = Label(text="", font_name=font_path, font_size=18,
                                  color=(0,1,0,1), size_hint_y=None, height=dp(30))
        main_layout.add_widget(self.successLabel)

        scroll_view.add_widget(main_layout)
        root.add_widget(scroll_view)

        # Back Button
        back_btn = _make_button("Back", (dp(120), dp(45)))
        back_btn.pos_hint = {"x":0.02,"y":0.02}
        back_btn.bind(on_release=lambda i: switch_screen(i, self.manager, "start_page"))
        root.add_widget(back_btn)

        self.add_widget(root)

        self.questionTypeSpinner.bind(text=self.update_question_type)
        self.update_question_type(None, self.questionTypeSpinner.text)

    def update_question_type(self, instance, q_type):
        is_mc = q_type == "Multiple Choice"
        self.mc_box.height = dp(4*50 + 3*10) if is_mc else 0
        for mc_input in self.mc_answers:
            mc_input.opacity = 1 if is_mc else 0
            mc_input.disabled = not is_mc
            mc_input.height = dp(50) if is_mc else 0
            if not is_mc:
                mc_input.text = ""

    def save_question(self, instance):
        q_text = self.questionInput.text.strip()
        a_text = self.answerInput.text.strip()
        q_type = self.questionTypeSpinner.text
        app = App.get_running_app()

        if not q_text:
            self.show_error("Question text is required!")
            return
        if not a_text and q_type != "True/False":
            self.show_error("Correct answer is required!")
            return

        question_data = {"text":q_text,"type":q_type,"correct_answer":a_text,"answers":[]}

        if q_type == "Multiple Choice":
            options = [mc.text.strip() for mc in self.mc_answers]
            if any(not o for o in options):
                self.show_error("Please fill all 4 options for Multiple Choice!")
                return
            if a_text not in options:
                self.show_error("Correct answer must match one of the 4 options!")
                return
            question_data["answers"] = options
        elif q_type == "True/False":
            question_data["answers"] = ["True","False"]

        app.custom_questions.append(question_data)
        self.clear_inputs()
        self.successLabel.text = f"Question saved! Total: {len(app.custom_questions)}"
        Clock.schedule_once(lambda dt: setattr(self.successLabel,'text',''),3)

    def show_error(self, msg):
        self.successLabel.text = msg
        self.successLabel.color = (1,0,0,1)
        Clock.schedule_once(lambda dt: setattr(self.successLabel,'text',''),3)

    def clear_inputs(self):
        self.questionInput.text = ""
        self.answerInput.text = ""
        for mc in self.mc_answers: mc.text = ""

    def open_pdf_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        chooser = FileChooserListView(filters=['*.pdf'], size_hint=(1,0.9))
        content.add_widget(chooser)
        btn = Button(text="Select PDF", size_hint=(1,0.1))
        content.add_widget(btn)

        popup = Popup(title="Select PDF File", content=content, size_hint=(0.9,0.9))
        btn.bind(on_release=lambda x: self.load_pdf(chooser.path, chooser.selection, popup))
        popup.open()

    def load_pdf(self, path, selection, popup):
        if selection:
            self.successLabel.text = f"Loaded PDF: {os.path.basename(selection[0])}"
            self.successLabel.color = (0,1,0,1)
            # TODO: Parse PDF and extract questions if needed
        popup.dismiss()
        Clock.schedule_once(lambda dt: setattr(self.successLabel,'text',''),3)
