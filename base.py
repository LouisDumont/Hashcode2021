import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass

class Intersection():
    def __init__(self):
        self.a = 0

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
        # book_to_value = {}
        # libraries = []
        # compteur = 0
        streets = {}
        cars = []
        line = f.readline()

        total_time, total_intersections, total_streets, total_cars, car_score = list(map(int, line.split(" ")))

        for i in range(total_streets):
            intersection_in, intersection_out, name, travel_time = f.readline().split(" ")
            intersection_in = int(intersection_in)
            intersection_out = int(intersection_out)
            travel_time = int(travel_time)

            streets[name]=Street(intersection_in, intersection_out, name, travel_time)

        for i in range(total_cars):
            line_split = f.readline().split(" ")
            total_streets_travel = int(line_split[0])
            streets_taken = line_split[1:]
            cars.append(Car(streets_taken))

    return streets, cars



        # book_number = int(book_number)
        # libraries_number = int(libraries_number)
        # days = int(days)
        # scores  = f.readline().split(" ")
        # for i,score in  enumerate(scores):
        #     book_to_value[i]=int(score)

        # compteur = 0
        # while compteur < libraries_number :
        #     line = f.readline()
        #     N,T,M = line.split(" ")
        #     N = int(N)
        #     T = int(T)
        #     M = int(M)
        #     libraries.append(Library(compteur,T,M,N))
        #     list_books = f.readline().split(" ")
        #     list_books = list(map(int,list_books))
        #     libraries[-1].add_books(list_books,book_to_value)
        #     compteur+=1
        
        # return book_to_value, libraries, days


if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str)
    args = parser.parse_args()
    streets, cars = parse_input(args.filename)
    print(cars)
    # expectation_heuristic(libraries,days, book_to_value)
    # for i in range(len(libraries)):
    #     print(i,libraries[i].scannedBooks)
    # make_out(args.filename,libraries)

