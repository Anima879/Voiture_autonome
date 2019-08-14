class Boundary:
    nbr_instance = 0
    toile = None

    def __init__(self, x1, y1, x2, y2, width=0, toile=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.length = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        self.color = 'red'
        if toile is None:
            self.toile = Boundary.toile
        if self.toile is None:
            raise ValueError('Aucune toile définie')

        if width == 0:
            self.gobj = self.toile.create_line(x1, y1, x2, y2, fill=self.color)

        self.id = Boundary.nbr_instance
        Boundary.nbr_instance += 1


class Limit(Boundary):
    nbr_instance = 0
    toile = Boundary.toile

    def __init__(self, x1, y1, x2, y2, width=0, toile=None):
        Boundary.__init__(self, x1, y1, x2, y2, width, toile)
        self.color = 'blue'
        self.toile.delete(self.gobj)
        self.gobj = self.toile.create_line(x1, y1, x2, y2, fill=self.color)
