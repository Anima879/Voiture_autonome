import tkinter as tk
from copy import deepcopy
from particle import Particle
from boundary import Boundary, Limit
from toile import Toile
from ray import Ray
from vehicle import Vehicle
from random import *
from IAvehicle.brain import Network
import time


def generate_random_boundary(n):
    walls = []
    for i in range(n):
        x1 = randint(0, 1000)
        x2 = randint(0, 1000)
        y1 = randint(0, 600)
        y2 = randint(0, 600)
        walls.append(Boundary(x1, y1, x2, y2))

    return walls


def generate_population(n):
    brains = []
    vehicles = []
    for i in range(n):
        brains.append(Network([5, 5, 4], 5))
        vehicles.append(Vehicle(150, 500, 10, 270))

    return brains, vehicles


def move(brain, vehicle):
    datas = [ray.len for ray in vehicle.rays]
    brain.feed_forward(datas)

    if vehicle.check_collision():
        vehicle.is_crashed = True
        d_v = ((vehicle.x - 750) ** 2 + (vehicle.y - 100) ** 2) ** 0.5
        d = ((150 - 750) ** 2 + (500 - 100) ** 2) ** 0.5
        brain.performance = d - d_v
    elif round(brain._get_layer_output(-1)[0]) == 1 and round(brain._get_layer_output(-1)[1]) == 1:
        vehicle.move(vehicle.velocity)
    elif round(brain._get_layer_output(-1)[0]) == 0 and round(brain._get_layer_output(-1)[1]) == 0:
        vehicle.move(- vehicle.velocity)
    elif round(brain._get_layer_output(-1)[0]) == 1 and round(brain._get_layer_output(-1)[1]) == 0:
        vehicle.rotate(vehicle.pas_angle)
    elif round(brain._get_layer_output(-1)[0]) == 0 and round(brain._get_layer_output(-1)[1]) == 1:
        vehicle.rotate(- vehicle.pas_angle)


def main():
    root = tk.Tk()
    root.title('Raycasting')
    master = Toile(root)
    Boundary.toile = master.toile
    Particle.toile = master.toile
    Ray.toile = master.toile
    Vehicle.toile = master.toile

    x_start = 150
    y_start = 500

    x_end = 750
    y_end = 100

    walls = [Boundary(0, 0, 1000, 0), Boundary(0, 0, 0, 600), Boundary(0, 600, 1000, 600), Boundary(1000, 0, 1000, 600)]
    walls.append(Boundary(101, 600, 100, 299))
    walls.append(Boundary(201, 600, 200, 299))
    walls.append(Boundary(100, 300, 300, 50))
    walls.append(Boundary(200, 300, 300, 150))
    walls.append(Boundary(300, 50, 800, 50))
    walls.append(Boundary(300, 150, 800, 150))

    l = Limit(751, 50, 750, 150)
    walls.append(l)

    Vehicle.walls = walls

    size_pop = 10
    brains, vehicles = generate_population(10)
    master.update()
    death_rate = 0.5
    epoch = 1000

    for i in range(epoch):
        print("Epoch : ", i)
        print("Conduite")
        count = 0
        while sum([v.is_crashed for v in vehicles]) != len(vehicles) and count < 200:
            count += 1
            for b, v in zip(brains, vehicles):
                move(b, v)
                master.update()

        brains = sorted(brains, key=lambda p: p.performance, reverse=True)
        print([brain.performance for brain in brains])
        brains = deepcopy(brains[:int(death_rate * size_pop)])

        print("Selection")
        while len(brains) <= size_pop:
            child = deepcopy(choice(brains))
            child.mutation()
            brains.append(child)

        for v in vehicles:
            v.teleport(x_start, y_start, 270)
            v.update()
            v.is_crashed = False
            master.update()


if __name__ == '__main__': main()
