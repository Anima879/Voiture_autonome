import math as m
from ray import Ray


class Particle:
    toile = None

    def __init__(self, x, y, toile=None):
        self.x = x
        self.y = y
        if toile is None:
            self.toile = Particle.toile
        if self.toile is None:
            raise ValueError('Toile non définie')

        self.rays = []
        for i in range(0, 360, 15):
            theta = m.radians(i)
            self.rays.append(Ray(self, [m.cos(theta), m.sin(theta)]))

        self.gobj = self.toile.create_oval(x - 5, y - 5, x + 5, y + 5, fill='white')

    def update(self, walls):
        """
            Update object on the canvas
        :return:
        """
        self.toile.delete(self.gobj)
        self.gobj = self.toile.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill='white')
        for ray in self.rays:
            ray.update(walls)
