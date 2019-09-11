from boundary import Limit


class Ray:
    toile = None

    def __init__(self, particle, dir, toile=None):
        """

        :param particle: object which the ray is attached to
        :param dir:
        :param toile:
        """
        self.particle = particle
        self.dir = dir
        self.vec = self.toile.create_line(particle.x, particle.y, particle.x + self.dir[0] * 10,
                                          particle.y + self.dir[1] * 10, fill='white')
        self.shown = False
        self.lines = []
        self.pts = []

        self.len = 0

        if toile is None:
            self.toile = Ray.toile
        if self.toile is None:
            raise ValueError('Toile non définie')

    def __del__(self):
        self.toile.delete(self.vec)
        for elt in self.lines:
            self.toile.delete(elt)

    def cast(self, wall):
        if isinstance(wall, Limit):
            return
        den = (wall.x1 - wall.x2) * (self.particle.y - (self.particle.y + self.dir[1])) - (wall.y1 - wall.y2) * (
                self.particle.x - (self.particle.x + self.dir[0]))
        if den == 0:
            return

        t = ((wall.x1 - self.particle.x) * (self.particle.y - (self.particle.y + self.dir[1])) - (
                wall.y1 - self.particle.y) * (
                     self.particle.x - (self.particle.x + self.dir[0]))) / den
        u = - ((wall.x1 - wall.x2) * (wall.y1 - self.particle.y) - (wall.y1 - wall.y2) * (
                wall.x1 - self.particle.x)) / den

        if u > 0 and 0 < t < 1:
            pt = [wall.x1 + t * (wall.x2 - wall.x1), wall.y1 + t * (wall.y2 - wall.y1)]
            self.pts.append(pt)
        else:
            return

    def find_closest(self):
        closest = None
        record = -1
        for pt in self.pts:
            d = ((self.particle.x - pt[0]) ** 2 + (self.particle.y - pt[1]) ** 2) ** 0.5
            if d < record or record == -1:
                record = d
                closest = pt
        return closest

    def draw(self, pt):
        if pt is not None:
            self.len = ((self.particle.x - pt[0]) ** 2 + (self.particle.y - pt[1]) ** 2) ** 0.5
            if self.shown:
                self.lines.append(self.toile.create_line(self.particle.x, self.particle.y, pt[0], pt[1], fill='white'))

    def update(self, walls):
        self.toile.delete(self.vec)
        for elt in self.lines:
            self.toile.delete(elt)
        self.vec = self.toile.create_line(self.particle.x, self.particle.y, self.particle.x + self.dir[0] * 10,
                                          self.particle.y + self.dir[1] * 10, fill='white')
        self.pts = []

        for wall in walls:
            self.cast(wall)
        self.draw(self.find_closest())
