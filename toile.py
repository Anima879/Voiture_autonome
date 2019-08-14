import tkinter as tk


class Toile(tk.Frame):
    dimension = (1000, 600)

    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, width=Toile.dimension[0], height=Toile.dimension[1], **kwargs)
        self.grid()
        self.toile = tk.Canvas(self, width=Toile.dimension[0], height=Toile.dimension[1], bg='black')
        self.toile.grid()

        # Attributes :
        self.mouse_pos = [0, 0]

        # Bind:
        self.toile.bind("<Motion>", self.motion)
        self.toile.bind("<Key>", self.move)

    def motion(self, evt):
        self.mouse_pos = [evt.x, evt.y]

    def move(self, evt):
        print(evt.char)
