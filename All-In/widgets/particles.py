# particles.py (or paste near your other widgets)

from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock
from kivy.metrics import dp
import random
from math import pi, cos, sin

class ParticlesWidget(Widget):
    """
    Falling particle effect widget.
    Use for losing effect:
        self.particles.burst(count=80, center=(cx, cy), size_px=6, life=1.8)
    """

    DEFAULT_COLORS = [
        (0.2, 0.0, 0.0),  # dark red
        (0.1, 0.1, 0.1),  # dark gray
        (0.3, 0.0, 0.0),  # crimson
    ]

    class _Particle:
        def __init__(self, x, y, vx, vy, size, color, life, angular=0.0):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.size = size
            self.color = color
            self.life = life
            self.max_life = life
            self.angular = angular
            self.angle = random.uniform(0, 360)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._particles = []
        self._update_ev = None
        self.gravity = 300.0      # positive = fall downward
        self.air_drag = 0.96
        self.frame_rate = 1/60.0
        self.max_particles = 1000

    def burst(self, count=80, center=None, size_px=6, colors=None, life=1.8):
        """Spawn falling particles"""
        if colors is None:
            colors = self.DEFAULT_COLORS

        if center is None:
            cx = self.x + self.width * 0.5
            cy = self.y + self.height
        else:
            cx, cy = center

        size = dp(size_px)

        # limit total particles
        allowed = max(0, self.max_particles - len(self._particles))
        spawn = min(count, allowed)
        for _ in range(spawn):
            # mostly downward spread
            angle = random.uniform(-pi/4, pi/4) + pi  # downward ±45°
            speed = random.uniform(150, 500)
            vx = cos(angle) * speed
            vy = sin(angle) * speed
            px = cx + random.uniform(-20, 20)
            py = cy
            color = random.choice(colors)
            angular = random.uniform(-180, 180)
            p = self._Particle(px, py, vx, vy, size, color, life, angular)
            self._particles.append(p)

        if not self._update_ev:
            self._update_ev = Clock.schedule_interval(self._update, self.frame_rate)

    def _update(self, dt):
        remove = []
        for p in self._particles:
            p.vx *= self.air_drag
            p.vy += self.gravity * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.angle += p.angular * dt
            p.life -= dt
            if p.life <= 0 or p.y < (self.y - 50) or p.x < (self.x - 50) or p.x > (self.x + self.width + 50):
                remove.append(p)

        for p in remove:
            try:
                self._particles.remove(p)
            except ValueError:
                pass

        if not self._particles:
            if self._update_ev:
                Clock.unschedule(self._update_ev)
                self._update_ev = None

        # redraw canvas
        self.canvas.clear()
        with self.canvas:
            for p in self._particles:
                alpha = max(0.0, p.life / p.max_life)
                r, g, b = p.color
                Color(r, g, b, alpha)
                PushMatrix()
                rot = Rotate(angle=p.angle, origin=(p.x + p.size/2, p.y + p.size/2))
                Rectangle(pos=(p.x, p.y), size=(p.size, p.size))
                PopMatrix()
