# screens/Roulette_Kv.py
from kivy.lang import Builder

KV = '''
<RoulettePage>:
    name: "roulette_page"
    BoxLayout:
        orientation: 'vertical'
        padding: [30, 20, 30, 20]
        spacing: 20

        # MAIN ROULETTE — FULL SPACE
        MainUI:
            id: main_ui
            balance: root.initial_balance
            size_hint: 1, 1

        # CLEAN EXIT BUTTON
        Button:
            text: "Collect & Exit"
            font_name: app.font_path if app.font_path else "Roboto"
            font_size: '18sp'
            size_hint: 0.4, None
            height: 60
            pos_hint: {'center_x': 0.5}
            background_normal: ''
            background_color: 0.1, 0.6, 0.1, 1
            color: 1, 1, 1, 1
            on_release: root.collect_and_exit()


# FULLY RESPONSIVE MAINUI — NO FIXED HEIGHTS
<MainUI>:
    orientation: 'horizontal'
    padding: [20, 15, 20, 15]
    spacing: 20
    canvas.before:
        Color:
            rgba: 0.06, 0.06, 0.08, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # LEFT: WHEEL + INPUT
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.58
        spacing: 15

        Label:
            text: "ALL-IN ROULETTE"
            font_name: "PixelFont"
            font_size: '32sp'
            size_hint_y: None
            height: self.texture_size[1] + 20
            color: 1, 0.9, 0.5, 1
            text_size: self.width, None

        WheelWidget:
            id: wheel
            size_hint_y: 1

        BoxLayout:
            size_hint_y: None
            height: 70
            spacing: 12
            TextInput:
                id: bet_input
                hint_text: "Bet amount"
                font_name: "PixelFont"
                input_filter: 'int'
                multiline: False
                size_hint_x: 0.7
                font_size: '20sp'
                text: str(root.bet_amount)
                background_color: 0.07, 0.07, 0.08, 1
                foreground_color: 1, 1, 1, 1
                cursor_color: 1, 1, 1, 1
                padding: [15, 15]
            Button:
                text: "Place\\nNumber"
                font_name: "PixelFont"
                font_size: '16sp'
                halign: 'center'
                valign: 'middle'
                background_normal: ''
                background_color: 0.25, 0.05, 0.4, 1
                color: 1, 1, 1, 1
                on_release: root.prepare_number_bet()
            Button:
                text: "Clear"
                font_name: "PixelFont"
                font_size: '16sp'
                background_normal: ''
                background_color: 1.0, 0.3, 0.1, 1
                color: 1, 1, 1, 1
                on_release: root.clear_last_bet()

    # RIGHT: BETTING BOARD
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.42
        spacing: 15

        # BALANCE
        BoxLayout:
            size_hint_y: None
            height: 55
            spacing: 15
            Label:
                text: "Balance: P" + str(int(root.balance))
                font_name: "PixelFont"
                font_size: '22sp'
                color: 0.4, 1, 0.5, 1
                halign: 'left'
            Label:
                text: "Bets: " + str(len(root.bets))
                font_name: "PixelFont"
                font_size: '18sp'
                color: 1, 1, 1, 1

        # COLOR BETS
        GridLayout:
            cols: 2
            spacing: 10
            size_hint_y: None
            height: 120
            Button:
                text: "RED"
                font_name: "PixelFont"
                font_size: '18sp'
                background_normal: ''
                background_color: 0.9, 0.1, 0.1, 1
                on_release: root.place_color_bet('red')
            Button:
                text: "BLACK"
                font_name: "PixelFont"
                font_size: '18sp'
                background_normal: ''
                background_color: 0.15, 0.15, 0.18, 1
                on_release: root.place_color_bet('black')
            Button:
                text: "ODD"
                font_name: "PixelFont"
                font_size: '18sp'
                background_normal: ''
                background_color: 0.1, 0.7, 0.1, 1
                on_release: root.place_color_bet('odd')
            Button:
                text: "EVEN"
                font_name: "PixelFont"
                font_size: '18sp'
                background_normal: ''
                background_color: 0.1, 0.4, 0.9, 1
                on_release: root.place_color_bet('even')

        # NUMBER GRID — RESPONSIVE
        GridLayout:
            id: num_grid
            cols: 3
            spacing: 12
            size_hint_y: 1
            padding: [5, 10]

        # SPIN + RESULT
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: 180
            spacing: 12
            Button:
                text: "SPIN THE WHEEL"
                font_name: "PixelFont"
                font_size: '24sp'
                size_hint_y: None
                height: 70
                background_color: 0.95, 0.2, 0.2, 1
                on_release: root.spin_wheel()
            Label:
                id: result_label
                text: root.last_result
                font_name: "PixelFont"
                font_size: '16sp'
                color: 1, 1, 1, 1
                size_hint_y: None
                height: 70
                text_size: self.width, None
                halign: 'center'
            Label:
                text: "Recent Results"
                font_name: "PixelFont"
                font_size: '14sp'
                color: 0.8, 0.8, 0.8, 1
                size_hint_y: None
                height: 20
            ScrollView:
                size_hint_y: None
                height: 60
                Label:
                    id: history_label
                    text: root.history_text
                    font_name: "PixelFont"
                    font_size: '13sp'
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
                    color: 0.9, 0.9, 0.9, 1
'''

Builder.load_string(KV)