from boundary import *


class Track:
    """
        Use the boundary class to make a round track.
    """

    toile = None

    def __init__(self, x_start, y_start, x_end, y_end, nb_checkpoints, toile=None):
        """
        :param x_start:
        :param y_start:
        :param x_end:
        :param y_end:
        :param nb_checkpoints:
        """
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end

        if toile is None:
            self.toile = Track.toile
        if self.toile is None:
            raise ValueError("Toile non définie")
