import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

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


class MainPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Label
        self.label = Label(
            text="No file selected",
            size_hint=(0.95, 0.1),
            pos_hint={'x':0.025, 'y':0.9}
        )
        self.add_widget(self.label)

        # Open FileChooser button
        self.open_btn = Button(
            text="Open File Chooser",
            size_hint=(0.3, 0.08),
            pos_hint={'x':0.35, 'y':0.8}
        )
        self.open_btn.bind(on_release=self.open_file_chooser)
        self.add_widget(self.open_btn)

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
        self.label.text = "Selected files:\n" + "\n".join(filepaths)


class MyApp(App):
    def build(self):
        return MainPage()


if __name__ == "__main__":
    MyApp().run()
