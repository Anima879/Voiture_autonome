import math as m
from ray import Ray


class Vehicle:
    toile = None
    pas_angle = 1
    walls = None

    def __init__(self, x, y, r, heading, fov=180, toile=None):
        if toile is None:
            self.toile = Vehicle.toile
        if self.toile is None:
            raise ValueError('Toile non définie')

        self.x = x
        self.y = y
        self.r = r
        self.fov = fov
        self.heading = heading
        self.velocity = 5
        self.rays = []
        self.is_crashed = False

        for angle in self.frange(heading - fov / 2, heading + fov / 2, 45):
            angle = m.radians(angle)
            ray = Ray(self, [m.cos(angle), m.sin(angle)])
            ray.update(Vehicle.walls)
            self.rays.append(ray)

        self.gobj = self.toile.create_oval(x - r, y - r, x + r, y + r, fill='white')
        self.direction = self.toile.create_line(self.x, self.y, self.x + 1.5 * r * m.cos(m.radians(heading)), self.y +
                                                1.5 * r * m.sin(m.radians(heading)), fill='white', arrow='last')
        self.toile.bind_all("<Key>", self.user_move)

    def user_move(self, evt):
        if evt.char == "z":
            self.move(self.velocity)
        elif evt.char == "s":
            self.move(- self.velocity)
        elif evt.char == "q":
            self.rotate(- Vehicle.pas_angle)
        elif evt.char == "d":
            self.rotate(Vehicle.pas_angle)

        self.update()

    def move(self, dl):
        angle = m.radians(self.heading)
        dx = dl * m.cos(angle)
        dy = dl * m.sin(angle)
        self.x += dx
        self.y += dy
        self.toile.move(self.gobj, dx, dy)
        self.update()

    def teleport(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading
        self.toile.delete(self.gobj, self.direction)
        self.gobj = self.toile.create_oval(x - self.r, y - self.r, x + self.r, y + self.r, fill='white')
        self.direction = self.toile.create_line(self.x, self.y, self.x + 1.5 * self.r * m.cos(m.radians(heading)), self.y +
                                                1.5 * self.r * m.sin(m.radians(heading)), fill='white', arrow='last')

    def rotate(self, d_theta):
        self.heading += d_theta
        self.update()

    def check_collision(self):
        for wall in Vehicle.walls:
            # Unitary vector u director of the line
            ux = (wall.x2 - wall.x1) / wall.length
            uy = (wall.y2 - wall.y1) / wall.length

            d = ((self.x - wall.x1) * ux + (self.y - wall.y1) * uy) / m.sqrt(ux ** 2 + uy ** 2)
            xh = wall.x1 + d / m.sqrt(ux ** 2 + uy ** 2) * ux
            yh = wall.y1 + d / m.sqrt(ux ** 2 + uy ** 2) * uy

            # Distance between center of the circle to the line
            d = ((self.x - xh) ** 2 + (self.y - yh) ** 2) ** 0.5

            between = False
            if wall.x1 != wall.x2:
                x_min = min(wall.x1, wall.x2)
                x_max = max(wall.x1, wall.x2)
                if x_min <= xh <= x_max:
                    between = True
            else:
                y_min = min(wall.y1, wall.y2)
                y_max = min(wall.y1, wall.y2)
                if y_min <= yh <= y_max:
                    between = True

            if self.r > d and between:
                return True
        return False

    def update(self):
        self.toile.delete(self.direction)
        self.direction = self.toile.create_line(self.x, self.y, self.x + 1.5 * self.r * m.cos(m.radians(self.heading)),
                                                self.y +
                                                1.5 * self.r * m.sin(m.radians(self.heading)), fill='white',
                                                arrow='last')
        if Vehicle.walls is not None:
            for ray in self.rays:
                self.toile.delete(ray)
            self.rays = []
            for angle in self.frange(self.heading - self.fov / 2, self.heading + self.fov / 2, 45):
                angle = m.radians(angle)
                ray = Ray(self, [m.cos(angle), m.sin(angle)])
                ray.update(Vehicle.walls)
                self.rays.append(ray)

    @staticmethod
    def frange(x, y, jump):
        while x <= y:
            yield x
            x += jump
