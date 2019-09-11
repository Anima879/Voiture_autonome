from copy import deepcopy
from vehicle.particle import Particle
from boundary import Boundary, Limit
from toile import Toile
from vehicle.ray import Ray
from vehicle.vehicle import Vehicle
from track import Track
from random import *
from IAvehicle.brain import Network
from setup.setup import *
import matplotlib.pyplot as plt
import time


def generate_random_boundary(n):
    """
        Generate n random boundaries
    :param n: {int}
    :return: {list} List of boundaries created
    """
    walls = []
    for i in range(n):
        x1 = randint(0, 1000)
        x2 = randint(0, 1000)
        y1 = randint(0, 600)
        y2 = randint(0, 600)
        walls.append(Boundary(x1, y1, x2, y2))

    return walls


def generate_population(n):
    """
        Generate initial population.
        Brain at index i control vehicle at index i
    :param n: {int} Size of the population
    :return: {list, list} Lists of brains and vehicles created.
    """
    brains = []
    vehicles = []
    for i in range(n):
        brains.append(Network([5, 5, 2], 5))
        v = Vehicle(150, 500, 10, 270)
        vehicles.append(v)

    return brains, vehicles


def move(brain, vehicle):
    """
        brain move its vehicle
    :param brain:
    :param vehicle:
    :return:
    """
    datas = [ray.len for ray in vehicle.rays]
    brain.feed_forward(datas)

    if vehicle.check_collision():
        vehicle.is_crashed = True
    elif round(brain.get_layer_output(-1)[0]) == 1 and round(brain.get_layer_output(-1)[1]) == 1:
        vehicle.move(vehicle.velocity)
    elif round(brain.get_layer_output(-1)[0]) == 0 and round(brain.get_layer_output(-1)[1]) == 0:
        vehicle.move(- vehicle.velocity)
    elif round(brain.get_layer_output(-1)[0]) == 1 and round(brain.get_layer_output(-1)[1]) == 0:
        vehicle.rotate(vehicle.pas_angle)
    elif round(brain.get_layer_output(-1)[0]) == 0 and round(brain.get_layer_output(-1)[1]) == 1:
        vehicle.rotate(- vehicle.pas_angle)


def compute_fitness(vehicle, brain):
    # apply a malus if vehicle crashed into a wall.
    crashed_malus = 100
    if vehicle.is_crashed:
        brain.performance = len(vehicle.passed_checkpoint) * vehicle.distance - crashed_malus
    else:
        brain.performance = len(vehicle.passed_checkpoint) * vehicle.distance


def main():
    root = tk.Tk()
    root.title('Raycasting')

    # Setup windows, WIP.
    # setup = Setup(root)
    # setup.mainloop()
    # setup.destroy()

    master = Toile(root)

    # Share master.toile's pointer for every object which needs it therefore it can alter the "toile".
    Boundary.toile = master.toile
    Particle.toile = master.toile
    Ray.toile = master.toile
    Vehicle.toile = master.toile
    Track.toile = master.toile

    # Start of the vehicles
    x_start = 150
    y_start = 500
    master.toile.create_oval(x_start - 3, y_start - 3, x_start + 3, y_start + 3, fill='red')

    # Extern boundaries
    walls = [Boundary(0, 0, 1000, 0), Boundary(0, 0, 0, 600), Boundary(0, 600, 1000, 600), Boundary(1000, 0, 1000, 600)]

    # Track(x_start, y_start, 100, 25)

    # Handmade track
    walls.append(Boundary(101, 600, 100, 299))
    walls.append(Boundary(201, 550, 200, 299))
    walls.append(Boundary(100, 300, 300, 50))
    walls.append(Boundary(200, 300, 300, 150))
    walls.append(Boundary(300, 50, 800, 50))
    walls.append(Boundary(300, 150, 700, 150))
    walls.append(Boundary(800, 50, 900, 300))
    walls.append(Boundary(700, 150, 750, 300))
    walls.append(Boundary(900, 300, 750, 500))
    walls.append(Boundary(750, 300, 650, 450))
    walls.append(Boundary(750, 500, 500, 550))
    walls.append(Boundary(650, 450, 500, 500))
    walls.append(Boundary(500, 500, 201, 550))
    walls.append(Boundary(500, 550, 201, 600))

    checkpoints = [Limit(100, 299, 200, 299), Limit(301, 150, 300, 50), Limit(800, 50, 700, 150),
                   Limit(900, 300, 750, 300), Limit(750, 500, 650, 450), Limit(500, 550, 501, 500),
                   Limit(201, 550, 201, 600)]

    # Share walls' pointer so Vehicle can "see" the walls
    Vehicle.walls = walls + checkpoints

    size_pop = 10
    brains, vehicles = generate_population(size_pop)
    # Initialization of the canvas
    master.update()
    death_rate = 0.5
    epoch = 10000

    # master.mainloop()
    for i in range(epoch):
        print("Epoch : ", i)
        print("Conduite")
        clock = 300
        while sum([v.is_crashed for v in vehicles]) != len(vehicles) and clock != 0:
            clock -= 1
            for b, v in zip(brains, vehicles):
                if not v.is_crashed:
                    move(b, v)
                    # Reset clock if a checkpoint is passed
                    if v.has_passed_checkpoint:
                        v.has_passed_checkpoint = False
                        clock = 300
                    master.update()

        print("Selection")
        for b, v in zip(brains, vehicles):
            compute_fitness(v, b)

        brains = sorted(brains, key=lambda p: p.performance, reverse=True)

        print([brain.performance for brain in brains])
        brains = deepcopy(brains[:int(death_rate * size_pop)])

        print("Reproduction")
        while len(brains) <= size_pop:
            child = deepcopy(choice(brains))
            child.mutation()
            brains.append(child)

        for v in vehicles:
            v.teleport(x_start, y_start, 270)
            v.passed_checkpoint = []
            v.update()
            v.is_crashed = False
            master.update()


if __name__ == '__main__': main()
