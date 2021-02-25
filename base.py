import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass

from frequentation import compute_frequentation

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
    importance: float = 0.

    def update_importance(self, importance_increment):
        self.importance += importance_increment

class Car():
    def __init__(self, streets_taken, importance = 0):
        self.streets_taken = streets_taken
        self.importance = importance

        
# For txt
def make_out(instance_name, lib_list):
    '''Instance name is the csv file name (with .txt)
    lib_list is simply the list of libraries'''

    with open(instance_name[:-4] +'_output.txt', 'w') as res_file:

        open_libs_list = np.array([1 if lib.isOpen==True and len(lib.scannedBooks)>0 else 0 for lib in lib_list])
        open_libs = np.sum(open_libs_list)
        # print(open_libs)

        res_file.write(str(open_libs) + '\n')

        lib_list.sort(key = lambda x: x.openNumber)

        for i, lib in enumerate(lib_list):
            if lib.isOpen and len(lib.scannedBooks)>0:
                # print("scannedBooks",lib.scannedBooks)
                nb_books = len(lib.scannedBooks)
                res_file.write(str(lib.id) + ' ' + str(nb_books) + '\n')
                books_str = ''
                for i, idx in enumerate(lib.scannedBooks):
                    books_str += str(idx) + ' '
                res_file.write(books_str[:-1] + '\n')


def parse_input(filename):
    with open(filename, 'r') as f :
        streets = {}
        cars = []
        line = f.readline()

        total_time, total_intersections, total_streets, total_cars, car_score = list(map(int, line.split(" ")))

        intersections = [Intersection() for i in range(total_intersections)]


        for i in range(total_streets):
            intersection_in, intersection_out, name, travel_time = f.readline().split(" ")
            intersection_in = int(intersection_in)
            intersection_out = int(intersection_out)
            travel_time = int(travel_time)

            streets[name]=Street(intersection_in, intersection_out, name, travel_time)
            intersections[intersection_out].add_in_street(name)


        for i in range(total_cars):
            line_split = f.readline().split(" ")
            total_streets_travel = int(line_split[0])
            streets_taken = line_split[1:]
            cars.append(Car(streets_taken))

    return streets, cars, intersections



if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str)
    args = parser.parse_args()
    streets, cars, intersections = parse_input(args.filename)
    print(intersections[0].in_streets)
    compute_frequentation(streets, cars)
    print(streets)
    # expectation_heuristic(libraries,days, book_to_value)
    # for i in range(len(libraries)):
    #     print(i,libraries[i].scannedBooks)
    # make_out(args.filename,libraries)

