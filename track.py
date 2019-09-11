from boundary import *
import math as m
from random import randint, uniform


class Track:
    """
        Use the boundary class to make a round track.
    """

    toile = None

    def __init__(self, x_center, y_center, radius, noise, toile=None):
        """
        :param x_start:
        :param y_start:
        :param x_end:
        :param y_end:
        :param nb_checkpoints:
        """
        self.x_center = x_center
        self.y_center = y_center
        self.checkpoints = []

        if toile is None:
            self.toile = Track.toile
        if self.toile is None:
            raise ValueError("Toile non définie")

        # Génération du circuit
        for angle in self.frange(0, 2 * m.pi, m.radians(20)):
            if randint(0, 1) == 0:
                radius += randint(0, noise)
            else:
                radius -= randint(0, noise)

            x = radius * m.cos(angle) + x_center
            y = radius * m.sin(angle) + y_center

            self.toile.create_oval(x + 2, y + 2, x - 2, y - 2, fill='white')

        print(self.checkpoints)

    @staticmethod
    def frange(x, y, jump):
        while x < y:
            yield x
            x += jump
