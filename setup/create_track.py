import tkinter as tk
from tkinter import messagebox, filedialog


class TrackCreator(tk.Frame):
    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.grid()
        self.toile = tk.Canvas(self, width=1000, height=600, bg="black")
        self.toile.grid(row=0, columnspan=2)

        self.btn_confirm = tk.Button(self, text='Confirmer', command=self.confirm)
        self.btn_confirm.grid(column=1, row=1)

        self.btn_cancel = tk.Button(self, text='Annuler')
        self.btn_cancel.grid(column=0, row=1)

    def confirm(self):
        pass
