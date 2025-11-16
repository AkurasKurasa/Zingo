# confetti.py  (or paste into screens/game_page.py near imports)
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock
from kivy.metrics import dp
import random
from math import pi, cos, sin

class ConfettiWidget(Widget):
    """
    Pixelated confetti widget.
    - call .burst(count=80, center=None, spread=1.0, size_px=6) to spawn confetti
    - it draws small colored squares (pixel look) that fall and fade out
    """

    DEFAULT_COLORS = [
        (0.95, 0.36, 0.36),
        (0.98, 0.78, 0.35),
        (0.35, 0.78, 0.44),
        (0.29, 0.67, 0.95),
        (0.73, 0.47, 0.96),
        (1.0, 1.0, 1.0),
    ]

    class _Particle:
        def __init__(self, x, y, vx, vy, size, color, life, angular=0.0):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.size = size
            self.color = color
            self.life = life    # seconds remaining
            self.max_life = life
            self.angular = angular
            self.angle = random.uniform(0, 360)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._particles = []
        self._update_ev = None
        self.gravity = -600.0  # pixels / s^2 (negative Y goes down visually)
        self.air_drag = 0.99
        self.frame_rate = 1/60.0
        self.max_particles = 1000
        self.pixel_border = 0  # set >0 to add outline (not used by default)

    def burst(self, count=80, center=None, spread=1.0, size_px=6, colors=None, life=1.6):
        """
        Spawn a confetti burst.
        - count: number of particles
        - center: (x, y) in widget coordinates; if None uses center of widget
        - spread: how wide the angle spread is (1.0 is default lively spread)
        - size_px: side length of pixels (dp recommended)
        - colors: list of rgb tuples
        - life: seconds each particle lives
        """
        if colors is None:
            colors = ConfettiWidget.DEFAULT_COLORS

        if center is None:
            cx = self.x + self.width * 0.5
            cy = self.y + self.height * 0.6
        else:
            cx, cy = center

        size = dp(size_px)

        # limit total particles
        allowed = max(0, self.max_particles - len(self._particles))
        spawn = min(count, allowed)
        for _ in range(spawn):
            angle = random.uniform(-pi*0.9*spread, pi*0.9*spread) + random.choice([0, -pi/2, pi/2])
            speed = random.uniform(200, 800) * (0.6 + 0.8 * random.random())
            vx = cos(angle) * speed
            vy = sin(angle) * speed
            # small random offset so they don't all start at exact same pixel
            px = cx + random.uniform(-10, 10)
            py = cy + random.uniform(-6, 10)
            color = random.choice(colors)
            angular = random.uniform(-180, 180)
            p = ConfettiWidget._Particle(px, py, vx, vy, size, color, life, angular)
            self._particles.append(p)

        # make sure update scheduled
        if not self._update_ev:
            self._update_ev = Clock.schedule_interval(self._update, self.frame_rate)

    def _update(self, dt):
        # update physics
        remove = []
        for p in self._particles:
            p.vx *= self.air_drag
            # gravity acts downward in pixel coords - so subtract (we chose negative gravity)
            p.vy += self.gravity * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.angle += p.angular * dt
            p.life -= dt
            # remove if off-screen or life <= 0
            if p.life <= 0 or p.y < (self.y - 50) or p.x < (self.x - 50) or p.x > (self.x + self.width + 50):
                remove.append(p)

        for p in remove:
            try:
                self._particles.remove(p)
            except ValueError:
                pass

        # stop updates if empty
        if not self._particles:
            if self._update_ev:
                Clock.unschedule(self._update_ev)
                self._update_ev = None

        # redraw canvas
        self.canvas.clear()
        with self.canvas:
            # draw each pixel as a small rectangle; fade by life
            for p in self._particles:
                alpha = max(0.0, p.life / p.max_life)
                # slightly dim edge to simulate "pixel" block shading
                r, g, b = p.color
                Color(r, g, b, alpha)
                # Draw a rotated rectangle to add tiny visual variance
                # We keep pixelated look by drawing rectangles without smoothing.
                PushMatrix()
                rot = Rotate(angle=p.angle, origin=(p.x + p.size/2, p.y + p.size/2))
                Rectangle(pos=(p.x, p.y), size=(p.size, p.size))
                PopMatrix()
