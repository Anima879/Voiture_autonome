import tkinter as tk
from tkinter import messagebox, filedialog
from setup.create_track import *


class Setup(tk.Frame):
    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.grid()
        tk.Label(self, text="Forme du véhicule :").grid(column=0, row=0)
        list_options = ('Rond', '')
        self.vehicle_shape = tk.StringVar()
        self.vehicle_shape.set(list_options[0])
        tk.OptionMenu(self, self.vehicle_shape, *list_options).grid(column=0, row=1)

        self.fov_value = tk.Scale(self, orient='horizontal', from_=0, to=360, resolution=5, length=100,
                                  label='FOV')
        self.fov_value.grid(column=0, row=2)

        self.btn_create_new_track = tk.Button(self, text="Nouveau circuit", command=self.create)
        self.btn_create_new_track.grid(column=1, row=0, padx=10)

        self.btn_open_track = tk.Button(self, text="Ouvrir un circuit", command=self.load)
        self.btn_open_track.grid(column=2, row=0, padx=10)

        self.track_name = tk.StringVar(value="None")
        self.label_name_track = tk.Label(self, textvariable=self.track_name)
        self.label_name_track.grid(column=1, row=1, columnspan=2)

        self.btn_launch = tk.Button(self, text="Confirmer", command=self.launch)
        self.btn_launch.grid(column=2, row=2)

    def launch(self):
        """
            Launch simulation according to settings.
        :return:
        """
        if messagebox.askokcancel('Confirmer ?', 'Voulez-vous lancer la simulation ? \n'):
            self.quit()
        else:
            return

    def load(self):
        """
            Open window for loading a track file.
        :return:
        """
        path = filedialog.askopenfilename(
            initialdir='C:/Users/eloim/Documents/Programmation/Python/raycasting/setup/tracks')
        self.track_name.set(path)

    def create(self):
        """
            Open window for creating a new track file and save it.
        :return:
        """
        root = tk.Tk()
        root.title("Création d'un circuit")

        wd = TrackCreator(root)
        wd.mainloop()
        wd.destroy()
