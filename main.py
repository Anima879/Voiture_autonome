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
import matplotlib.pyplot as plt


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
    """
        Generate initial population.
        Brain at index i control vehicle at index i
    :param n:
    :return:
    """
    brains = []
    vehicles = []
    for i in range(n):
        brains.append(Network([5, 5, 4], 5))
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


def compute_fitness(vehicle, brain, x_start, y_start, x_end, y_end):
    d_v = ((vehicle.x - x_end) ** 2 + (vehicle.y - y_end) ** 2) ** 0.5
    d = ((x_start - x_end) ** 2 + (y_start - y_end) ** 2) ** 0.5
    crashed_malus = 100
    if vehicle.is_crashed:
        brain.performance = len(vehicle.passed_checkpoint) * vehicle.distance - crashed_malus
    else:
        brain.performance = len(vehicle.passed_checkpoint) * vehicle.distance


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

    d_start_end = ((150 - 750)**2 + (500 - 100)**2)**0.5

    # Extern boundaries
    walls = [Boundary(0, 0, 1000, 0), Boundary(0, 0, 0, 600), Boundary(0, 600, 1000, 600), Boundary(1000, 0, 1000, 600)]

    # Track
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

    Vehicle.walls = walls + checkpoints

    size_pop = 10
    brains, vehicles = generate_population(size_pop)
    master.update()
    death_rate = 0.5
    epoch = 10000

    # datas
    best_distance_each_epoch = []
    mean_distance_each_epoch = []

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
                        print("Clock reset")
                    master.update()

        print("Selection")
        for b, v in zip(brains, vehicles):
            compute_fitness(v, b, x_start, x_end, y_start, y_end)

        brains = sorted(brains, key=lambda p: p.performance, reverse=True)
        # Data storage before selection
        best_distance_each_epoch.append(d_start_end - brains[0].performance)
        mean_distance_each_epoch.append(sum([(d_start_end - b.performance) for b in brains]) / len(brains))

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

    plt.plot(best_distance_each_epoch)
    plt.plot(mean_distance_each_epoch)
    plt.show()


if __name__ == '__main__': main()
