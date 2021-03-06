import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
import math

from frequentation import compute_streets_frequentation, compute_inters_importance
from order import compute_starting_points, compute_starting_orders
from importance import update_cars_importance

class Intersection():
    def __init__(self):
        self.in_streets = {}

    def add_in_street(self, street_name):
        self.in_streets[street_name]=0

    def update_street_importance(self, street_name, importance):
        self.in_streets[street_name]=importance


@dataclass
class Street():
    intersection_in: int
    intersection_out: int
    name: str
    travel_time: int
    frequentation: float = 0.
    init_frequentation: float = 0.

    def update_frequentation(self, frequentation_increment):
        self.frequentation += frequentation_increment

    def update_init_frequentation(self, frequentation_increment):
        self.init_frequentation += frequentation_increment

class Car():
    def __init__(self, streets_taken, importance = 0):
        self.streets_taken = streets_taken
        self.importance = importance

    def update_importance(self, importance):
        self.importance = importance

        
# For txt
def make_out(instance_name, intersections):
    '''Instance name is the csv file name (with .txt)
    lib_list is simply the list of libraries'''
    print(instance_name[:-4] +'_output.txt')
    with open(instance_name[:-4] +'_output.txt', 'w') as res_file:
        res_file.write(f"{len(intersections)}\n")
        for i,intersection in enumerate(intersections):
            res_file.write(f"{i}\n")
            list_importance = np.array(list(intersection.in_streets.values()))
            nb_frequented_streets = np.count_nonzero(list_importance)
            
            if nb_frequented_streets==0:
                res_file.write("1\n")
                res_file.write(f"{list(intersection.in_streets.keys())[0]} 1\n")
            else:
                res_file.write(f"{nb_frequented_streets}\n")
                min_importance = np.min(list_importance[np.nonzero(list_importance)])
                THRESHOLD = 20.
                max_importance = max(list_importance)/min_importance
                for street in intersection.in_streets.keys():
                    if intersection.in_streets[street] >0:
                        if max_importance > THRESHOLD:
                            importance = int(math.ceil(intersection.in_streets[street]/min_importance/max_importance * THRESHOLD))
                        else:
                            importance = int(round(intersection.in_streets[street]/min_importance))
                        res_file.write(f"{street} {importance}\n")


def parse_input(filename):
    with open(filename, 'r') as f :
        streets = {}
        cars = []
        line = f.readline()

        total_time, total_intersections, total_streets, total_cars, car_base_score = list(map(int, line.split(" ")))

        intersections = [Intersection() for i in range(total_intersections)]


        for i in range(total_streets):
            intersection_in, intersection_out, name, travel_time = f.readline().split(" ")
            intersection_in = int(intersection_in)
            intersection_out = int(intersection_out)
            travel_time = int(travel_time)

            streets[name]=Street(intersection_in, intersection_out, name, travel_time)
            intersections[intersection_out].add_in_street(name)


        for i in range(total_cars):
            line_split = f.readline().split("\n")[0].split(" ")
            total_streets_travel = int(line_split[0])
            streets_taken = line_split[1:]
            cars.append(Car(streets_taken))

    return streets, cars, intersections, total_time, car_base_score



if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str)
    args = parser.parse_args()
    streets, cars, intersections, total_time, car_base_score = parse_input(args.filename)
    update_cars_importance(cars, streets, total_time, car_base_score)
    # print(intersections[0].in_streets)
    compute_streets_frequentation(streets, cars, mode="car_importance")  # car_importance
    # print(streets)
    compute_inters_importance(streets, intersections)

    compute_starting_points(streets, cars, mode="car_importance")
    compute_starting_orders(streets, intersections)
    # for i in range(len(intersections)):
    #     print("---")
    #     for street_name in intersections[i].in_streets.keys():
    #         print(intersections[i].in_streets[street_name])
    make_out(args.filename,intersections)

