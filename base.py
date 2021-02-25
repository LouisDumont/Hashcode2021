import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np

class Library():
    def __init__(self,id, signupDelay, flow, nbBooks):
        self.id = id
        self.books_id = []
        self.signupDelay= signupDelay
        self.flow = flow # nb books shippable per day
        self.nbBooks = nbBooks
        self.scannedBooks = []
        self.isOpen = False
        self.openNumber=float("inf")

    def add_book(self,book_id, dic):
        self.books_id.append(book_id)
        self.books_id.sort(key = lambda x : dic[x])
    
    def add_books(self,books_ids,dic):
        self.books_id.extend(books_ids)
        self.books_id.sort(key = lambda x : dic[x])

    def average_returns(self,days,book_to_value):
        profitDays=days-self.signupDelay
        self.books_id.sort(key = lambda x : book_to_value[x])
        bestbooks=self.books_id[-profitDays*self.flow:]
        score=0
        for book in bestbooks:
            score+=book_to_value[book]
        return score/days


    def scan_books(self, books):
        self.scannedBooks.extend(books)
        self.scannedBooks=list(dict.fromkeys(self.scannedBooks))
    
    def scan_n_best_books(self,n,book_to_value):
        self.books_id.sort(key = lambda x : book_to_value[x])
        if len(self.scannedBooks)<len(self.books_id):
            if n>0:
                self.scan_books(self.books_id[-n:])
                return self.books_id[-n:]
        return []

    def openLibrary(self, number): #number indique c'est la combientieme librairie qu'on ouvre
        self.isOpen = True
        self.openNumber = number

        
    return None #library_signup_order


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
        book_to_value = {}
        libraries = []
        compteur = 0
        line = f.readline()

        book_number, libraries_number, days =line.split(" ")
        book_number = int(book_number)
        libraries_number = int(libraries_number)
        days = int(days)
        scores  = f.readline().split(" ")
        for i,score in  enumerate(scores):
            book_to_value[i]=int(score)

        compteur = 0
        while compteur < libraries_number :
            line = f.readline()
            N,T,M = line.split(" ")
            N = int(N)
            T = int(T)
            M = int(M)
            libraries.append(Library(compteur,T,M,N))
            list_books = f.readline().split(" ")
            list_books = list(map(int,list_books))
            libraries[-1].add_books(list_books,book_to_value)
            compteur+=1
        
        return book_to_value, libraries, days


if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", type=str)
    args = parser.parse_args()
    book_to_value, libraries, days = parse_input(args.filename)
    expectation_heuristic(libraries,days, book_to_value)
    # for i in range(len(libraries)):
    #     print(i,libraries[i].scannedBooks)
    make_out(args.filename,libraries)

