# screens/roulette_kivy.py
import os
import random
import math
from functools import partial
import kivy
kivy.require("2.1.0")

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import (NumericProperty, StringProperty, ListProperty,
                             ObjectProperty, BooleanProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation
from PIL import Image, ImageDraw, ImageFont
from kivy.core.image import Image as CoreImage
from paths import FONT_PATH

# --- config ---
LOGO_PATH = "All-In/png_icons/allin_roulette_center.png"
PIXEL_FONT_NAME = "PixelFont"
try:
    if os.path.exists(FONT_PATH):
        LabelBase.register(name=PIXEL_FONT_NAME, fn_regular=FONT_PATH)
        PIL_FONT = ImageFont.truetype(FONT_PATH, 24)
    else:
        LabelBase.register(name=PIXEL_FONT_NAME, fn_regular=None)
        PIL_FONT = ImageFont.load_default()
except Exception:
    LabelBase.register(name=PIXEL_FONT_NAME, fn_regular=None)
    PIL_FONT = ImageFont.load_default()

STARTING_BALANCE = 500
BET_DEFAULT = 50
NUMBERS = list(range(1, 13))
SEG_COUNT = len(NUMBERS)
SLICE_ANGLE = 360.0 / SEG_COUNT
RED_SET = {1, 3, 5, 7, 9, 11}
BLACK_SET = set(NUMBERS) - RED_SET
PAYOUT_NUMBER = 10
PAYOUT_COLOR = 2

# --- wheel image (no hub) ---
def draw_wheel_image(angle_deg: float, size_px: int = 700, highlight: int = None):
    im = Image.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    cx, cy = size_px // 2, size_px // 2
    radius = int(size_px * 0.42)

    draw.ellipse((cx - radius - 8, cy - radius - 8,
                  cx + radius + 8, cy + radius + 8),
                 fill=(20, 20, 20), outline=(50, 50, 50))

    for i, n in enumerate(NUMBERS):
        start = i * SLICE_ANGLE + angle_deg
        end = start + SLICE_ANGLE
        fill = (230, 40, 52) if n in RED_SET else (28, 28, 31)

        if highlight == n:
            draw.pieslice((cx - radius - 6, cy - radius - 6,
                           cx + radius + 6, cy + radius + 6),
                          start, end, fill=(255, 210, 100))

        draw.pieslice((cx - radius, cy - radius,
                       cx + radius, cy + radius),
                      start, end, fill=fill, outline=(0, 0, 0))

        mid_angle = math.radians(start + SLICE_ANGLE / 2)
        tx = cx + math.cos(mid_angle) * (radius - 38)
        ty = cy + math.sin(mid_angle) * (radius - 38)
        txt = str(n)

        try:
            font = ImageFont.truetype(FONT_PATH, 24)
        except Exception:
            font = PIL_FONT

        w, h = draw.textbbox((0, 0), txt, font=font)[2:4]

        if highlight == n:
            draw.text((tx - w/2 + 2, ty - h/2 + 2), txt, font=font, fill=(0, 0, 0))
            draw.text((tx - w/2, ty - h/2), txt, font=font, fill=(255, 250, 200))
        else:
            draw.text((tx - w/2, ty - h/2), txt, font=font, fill=(240, 240, 240))

    return im

# --- winning number (bottom pointer) ---
def compute_winning_number(final_angle: float):
    a = final_angle % 360.0
    rel = (270.0 - a) % 360.0
    idx = int(rel // SLICE_ANGLE) % SEG_COUNT
    return NUMBERS[idx]

# --- wheel widget ---
class WheelWidget(Widget):
    angle = NumericProperty(0.0)
    highlight = NumericProperty(None, allownone=True)
    _tex = ObjectProperty(None)
    logo_texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_px = 700

        if os.path.exists(LOGO_PATH):
            try:
                img = CoreImage(LOGO_PATH)
                self.logo_texture = img.texture
            except Exception as e:
                print(f"logo error: {e}")

        self.bind(pos=self._redraw, size=self._redraw,
                  angle=self._redraw, highlight=self._redraw,
                  logo_texture=self._redraw)
        Clock.schedule_once(lambda dt: self._redraw(), 0.05)

    def _redraw(self, *a):
        pil = draw_wheel_image(self.angle, size_px=self.size_px, highlight=self.highlight)
        data = pil.tobytes()
        w, h = pil.size
        if not self._tex:
            self._tex = Texture.create(size=(w, h), colorfmt='rgba')
            self._tex.flip_vertical()
        self._tex.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')

        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(texture=self._tex, pos=self.pos, size=self.size)

            if self.logo_texture:
                cx, cy = self.center_x, self.center_y
                radius = int(self.size_px * 0.05)
                from kivy.graphics import StencilPush, StencilUse, StencilUnUse, StencilPop, Ellipse
                StencilPush()
                Ellipse(pos=(cx - radius, cy - radius), size=(radius*2, radius*2))
                StencilUse()
                logo_sz = radius * 2
                Rectangle(texture=self.logo_texture,
                          pos=(cx - logo_sz//2, cy - logo_sz//2),
                          size=(logo_sz, logo_sz))
                StencilUnUse()
                StencilPop()

            top = self.top
            arrow = [[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0]]
            scale = 7
            w_a = len(arrow[0]) * scale
            h_a = len(arrow) * scale
            ox = cx - w_a // 2
            oy = top - h_a - 8

            Color(0, 0, 0, 0.6)
            for y, row in enumerate(arrow):
                for x, p in enumerate(row):
                    if p:
                        Rectangle(pos=(ox + x*scale + 2, oy + y*scale + 2), size=(scale, scale))
            Color(1.0, 0.9, 0.2, 1)
            for y, row in enumerate(arrow):
                for x, p in enumerate(row):
                    if p:
                        Rectangle(pos=(ox + x*scale, oy + y*scale), size=(scale, scale))

# --- kv layout ---
KV = '''
<MainUI>:
    orientation: 'horizontal'
    padding: 12
    spacing: 12
    canvas.before:
        Color:
            rgba: 0.07,0.07,0.09,1
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.6
        padding: 8
        spacing: 8
        Label:
            text: "ALL-IN ROULETTE"
            font_name: "PixelFont"
            font_size: '28sp'
            size_hint_y: None
            height: 36
            color: 1,0.9,0.5,1
        WheelWidget:
            id: wheel
            size_hint_y: 0.85
        BoxLayout:
            size_hint_y: 0.12
            spacing: 8
            TextInput:
                id: bet_input
                hint_text: "Bet\\namount"
                font_name: "PixelFont"
                input_filter: 'int'
                multiline: False
                size_hint_x: 0.8
                font_size: '18sp'
                text: str(root.bet_amount)
                background_color: 0.07, 0.07, 0.08, 1
                foreground_color: 1, 1, 1, 1
                cursor_color: 1, 1, 1, 1
            Button:
                text: "Place Number Bet"
                font_name: "PixelFont"
                font_size: '15sp'
                background_normal: ''
                background_color: 0.2, 0.05, 0.35, 1
                color: 1, 1, 1, 1
                on_release: root.prepare_number_bet()
            Button:
                text: "Clear Last Bet"
                font_name: "PixelFont"
                font_size: '15sp'
                background_normal: ''
                background_color: 1.0, 0.4, 0.1, 1
                color: 1, 1, 1, 1
                on_release: root.clear_last_bet()
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.4
        padding: 8
        spacing: 8
        BoxLayout:
            size_hint_y: None
            height: 48
            spacing: 8
            Label:
                text: "Balance: P" + str(root.balance)
                font_name: "PixelFont"
                font_size: '20sp'
                color: 0.5,1,0.6,1
            Label:
                text: "Current Bets: " + str(len(root.bets))
                font_name: "PixelFont"
                font_size: '16sp'
                color: 1,1,1,1
        BoxLayout:
            size_hint_y: None
            height: 42
            spacing: 6
            Button:
                text: "Bet\\nRED"
                font_name: "PixelFont"
                font_size: '15sp'
                halign: 'center'
                valign: 'middle'
                background_normal: ''
                background_color: 0.9, 0.1, 0.1, 1
                color: 1, 1, 1, 1
                on_release: root.place_color_bet('red')
            Button:
                text: "Bet\\nBLACK"
                font_name: "PixelFont"
                font_size: '15sp'
                halign: 'center'
                valign: 'middle'
                background_normal: ''
                background_color: 0.15, 0.15, 0.18, 1
                color: 1, 1, 1, 1
                on_release: root.place_color_bet('black')
            Button:
                text: "Bet\\nODD"
                font_name: "PixelFont"
                font_size: '15sp'
                halign: 'center'
                valign: 'middle'
                background_normal: ''
                background_color: 0.1, 0.7, 0.1, 1
                color: 1, 1, 1, 1
                on_release: root.place_color_bet('odd')
            Button:
                text: "Bet\\nEVEN"
                font_name: "PixelFont"
                font_size: '15sp'
                halign: 'center'
                valign: 'middle'
                background_normal: ''
                background_color: 0.1, 0.3, 0.8, 1
                color: 1, 1, 1, 1
                on_release: root.place_color_bet('even')
        GridLayout:
            id: num_grid
            cols: 4          # ← CHANGED FROM 3 TO 4
            rows: 3          # ← NEW: explicit 3 rows
            spacing: 6
            size_hint_y: 0.5
            row_default_height: 50
            row_force_default: True
            col_default_width: 70
            col_force_default: True
            padding: 4
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: 180
            spacing: 8
            Button:
                text: "SPIN"
                font_name: "PixelFont"
                font_size: '20sp'
                size_hint_y: None
                height: 56
                background_color: 0.9,0.2,0.2,1
                on_release: root.spin_wheel()
            Label:
                id: result_label
                text: root.last_result
                font_name: "PixelFont"
                font_size: '14sp'
                color: 1,1,1,1
                size_hint_y: None
                height: 60
                text_size: self.width, None
            Label:
                text: "History"
                font_name: "PixelFont"
                font_size: '14sp'
                size_hint_y: None
                height: 20
            ScrollView:
                size_hint_y: None
                height: 40
                do_scroll_x: False
                Label:
                    id: history_label
                    text: root.history_text
                    font_name: "PixelFont"
                    font_size: '12sp'
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None
'''

# --- main ui ---
class MainUI(BoxLayout):
    balance = NumericProperty(STARTING_BALANCE)
    bet_amount = NumericProperty(BET_DEFAULT)
    bets = ListProperty([])
    last_result = StringProperty("Place your bets!")
    history_text = StringProperty("")
    spinning = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._post_init, 0.05)

    def _post_init(self, dt):
        grid = self.ids.num_grid
        grid.clear_widgets()
        for n in NUMBERS:
            bg = (1, 0.12, 0.18, 1) if n in RED_SET else (0.07, 0.07, 0.08, 1)
            btn = Button(
                text=str(n),
                font_name=PIXEL_FONT_NAME,
                font_size='18sp',
                background_normal='',
                background_color=bg,
                shorten=True,
                max_lines=1,
                halign='center',
                valign='middle'
            )
            btn.bind(size=btn.setter('text_size'))
            btn.bind(on_release=partial(self.prepare_number_bet_with_n, n))
            grid.add_widget(btn)

        self.wheel_widget = self.ids.get('wheel', None)
        if self.wheel_widget:
            self.wheel_widget.angle = 0
            self.wheel_widget._redraw()

    def _get_bet_amount_from_input(self):
        try:
            val = int(self.ids.bet_input.text.strip())
            return val if val > 0 else int(self.bet_amount)
        except Exception:
            return int(self.bet_amount)

    def prepare_number_bet_with_n(self, n, *a):
        amt = self._get_bet_amount_from_input()
        if amt > self.balance:
            self.last_result = "Not enough balance for that bet."
            return
        self.bets.append({'type':'number','numbers':[n],'amount':amt})
        self.balance -= amt
        self.last_result = f"Bet placed: {n} for P{amt}"
        self._update_history(f"Bet {n} P{amt}")

    def prepare_number_bet(self, *a):
        txt = self.ids.bet_input.text.strip()
        if not txt.isdigit():
            self.last_result = "Enter a number (1-12)."
            return
        n = int(txt)
        if n not in NUMBERS:
            self.last_result = "Number must be 1–12."
            return
        amt = self._get_bet_amount_from_input()
        if amt > self.balance:
            self.last_result = "Not enough balance."
            return
        self.bets.append({'type':'number','numbers':[n],'amount':amt})
        self.balance -= amt
        self.last_result = f"Bet placed: {n} for P{amt}"
        self._update_history(f"Bet {n} P{amt}")

    def place_color_bet(self, ctype):
        amt = self._get_bet_amount_from_input()
        if amt > self.balance:
            self.last_result = "Not enough balance."
            return
        if ctype == 'red':
            nums = [n for n in NUMBERS if n in RED_SET]
        elif ctype == 'black':
            nums = [n for n in NUMBERS if n in BLACK_SET]
        elif ctype == 'odd':
            nums = [n for n in NUMBERS if n % 2 == 1]
        else:
            nums = [n for n in NUMBERS if n % 2 == 0]
        self.bets.append({'type':'color','numbers':nums,'amount':amt,'choice':ctype})
        self.balance -= amt
        self.last_result = f"Bet placed: {ctype.upper()} P{amt}"
        self._update_history(f"Bet {ctype} P{amt}")

    def clear_last_bet(self):
        if not self.bets:
            self.last_result = "No bets to clear."
            return
        last = self.bets.pop()
        self.balance += last['amount']
        self.last_result = f"Cleared last bet. Refunded P{last['amount']}"
        self._update_history("Cleared last bet")

    def _update_history(self, msg):
        hist = self.history_text.splitlines()
        hist.insert(0, msg)
        self.history_text = "\n".join(hist[:6])

    def spin_wheel(self):
        if self.spinning or not self.bets:
            if not self.bets:
                self.last_result = "Place at least one bet."
            return
        self.spinning = True
        self.last_result = "Spinning..."
        spins = random.randint(4, 7)
        offset = random.uniform(0, 360)
        target = self.wheel_widget.angle + spins * 360 + offset
        anim = Animation(angle=target, duration=5, t='out_quad')
        anim.bind(on_complete=lambda *args: self._on_spin_complete())
        anim.start(self.wheel_widget)

    def _on_spin_complete(self):
        winner = compute_winning_number(self.wheel_widget.angle % 360)
        self._on_spin_result(winner)
        self.spinning = False

    def _on_spin_result(self, winner):
        self.wheel_widget.highlight = winner
        self.wheel_widget._redraw()
        total_win = 0
        total_bet = sum(b['amount'] for b in self.bets)
        for bet in self.bets:
            if winner in bet['numbers']:
                mult = PAYOUT_NUMBER if bet['type'] == 'number' else PAYOUT_COLOR
                total_win += bet['amount'] * mult
        net = total_win - total_bet
        self.balance += total_win
        if net > 0:
            self.last_result = f"Result: {winner} — YOU WON P{net}!"
            self._update_history(f"WIN {winner} +P{net}")
        elif net < 0:
            self.last_result = f"Result: {winner} — You lost P{abs(net)}."
            self._update_history(f"LOSE {winner} -P{abs(net)}")
        else:
            self.last_result = f"Result: {winner} — Break even."
            self._update_history(f"EVEN {winner}")
        self.bets = []
        Clock.schedule_once(lambda dt: self._clear_highlight(), 1.0)

    def _clear_highlight(self):
        self.wheel_widget.highlight = None
        self.wheel_widget._redraw()

# --- app ---
class RouletteApp(App):
    def build(self):
        Builder.load_string(KV)
        return MainUI()

if __name__ == "__main__":
    RouletteApp().run()