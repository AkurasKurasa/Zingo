class WheelWidget(Widget):
    angle = NumericProperty(0.0)
    highlight = NumericProperty(None, allownone=True)
    _tex = ObjectProperty(None)
    logo_texture = ObjectProperty(None, allownone=True)

    def _redraw(self, *a):
        pil = draw_wheel_image(self.angle, size_px=700, highlight=self.highlight)
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
            cx, cy = self.center_x, self.center_y 

            if self.logo_texture:
                radius = int(700 * 0.05)
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
            ox = cx - w_a // 2  # ← NOW SAFE
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_px = 700

        self.is_spinning = False
        self.spin_speed = 0
        self.friction = 0.985
        self.min_speed = 0.25
        self._spin_event = None

        if os.path.exists(LOGO_PATH):
            try:
                img = CoreImage(LOGO_PATH)
                self.logo_texture = img.texture
            except Exception as e:
                print(f"logo error: {e}")

        self.bind(pos=self._redraw, size=self._redraw, angle=self._redraw, highlight=self._redraw, logo_texture=self._redraw)
        Clock.schedule_once(lambda dt: self._redraw(), 0.05)

    def start_spin(self):
        if self.is_spinning:
            return

        import random
        self.angle = self.angle % 360
        self.spin_speed = random.uniform(18, 26)  # initial speed
        self.is_spinning = True

        # Start animation loop
        self._spin_event = Clock.schedule_interval(self._spin_update, 0)

    def _spin_update(self, dt):
        if not self.is_spinning:
            return False

        old_angle = self.angle
        self.angle = (self.angle + self.spin_speed) % 360

        # Slow down
        self.spin_speed *= self.friction

        # Stop condition
        if self.spin_speed < self.min_speed:
            self.is_spinning = False
            self.spin_speed = 0

            # Final redraw
            Clock.schedule_once(lambda dt: self._finish_spin(), 0)
            return False

        return True
    
    def _finish_spin(self):
        from math import fmod
        final_angle = self.angle % 360.0
        winning = compute_winning_number(final_angle)

        print("WINNING NUMBER =", winning)

        # Highlight the winning segment for effect
        self.highlight = winning

        # Auto-remove highlight after 1.5 sec
        Clock.schedule_once(lambda dt: setattr(self, 'highlight', None), 1.5)

        # Callback to parent (RoulettePage)
        if hasattr(self, "on_result"):
            self.on_result(winning)

