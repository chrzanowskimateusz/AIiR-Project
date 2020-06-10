import sys
import itertools
import time
import random
import math
from multiprocessing import Pool
from functools import partial


class BruteForceMultiTSP:
    def BruteForceTSP(self, dist_matrix):
        self.dist_matrix = dist_matrix

    # wczytywanie danych z pliku
    def read_distances(self, filename):
        dists = []
        with open(filename, 'r') as f:
            for line in f:
                if line[0] == '#':
                    continue
                dists.append(list(map(int, map(str.strip, line.split(',')))))
        return dists

    # liczenie wartosci przejscia
    def value(self, current_permutation):
        value = 0
        for city, next_city in zip(current_permutation, current_permutation[1:]):
            if city == current_permutation[-1]:
                break
            else:
                value += self.dist_matrix[city][next_city]
        value += self.dist_matrix[current_permutation[-1]][current_permutation[0]]
        return value

    def print_matrix(self):
        for row in self.dist_matrix:
            print(row)

    def get_best_route(self, args):
        best_value = sys.maxsize
        start, end, route_list = args[0], args[1], args[2]
        for x in range(start, end):
            if self.value(route_list[x]) < best_value:
                best_value = self.value(route_list[x])
                best_route = route_list[x]
        return best_route

    def brute_force(self):
        """
        przygotowanie zmiennych potrzebnych do wykonania
        w tym liczba miast, permutacja poczatkowa, liczba
        procesow, interwaly, permutacja koncowa
        """
        n = len(self.dist_matrix[0])
        start = 0
        perm_num = math.factorial(n)
        proc = 10
        interval = int(perm_num / proc)
        end = interval
        # oznaczamy najlepsza wartosc jako najwieksza mozliwa
        best_value = sys.maxsize
        # tworzymy pusta tablice rozwiazan
        best_route = []
        # odpowiedz koncowa
        best_answer = []
        # wypisujemy wszystkie mozliwe permutacje n-elementowe korzystajac z pakietu itertools
        route_list = list(itertools.permutations(range(n), n))
        # przygotowanie listy dwoch argumentow (poczatek i koniec iteracji
        arg1 = []
        arg2 = []

        # wypelnienie listy argumentow
        for x in range(proc-1):
            arg1.append(start)
            arg2.append(end)
            start+=interval
            end+=interval
        arg1.append(start)
        arg2.append(perm_num-1)

        new_iterable = ([x,y, route_list] for x,y in zip(arg1, arg2))
        p = Pool(proc)
        for part in p.imap_unordered(self.get_best_route, new_iterable):
            best_route.append(part)
        p.close()
        p.join()

        for result in best_route:
            x = self.value(result)
            if x < best_value:
                best_value = x
                best_answer = part

        return best_value, best_answer

    def generate_sync_distances(self, n):
        dists = [[0] * n for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                dists[i][j] = dists[j][i] = random.randint(1, 1000)
        return dists

    def generate_async_distances(self, n):
        dists = [[0] * n for i in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dists[i][j] = random.randint(1, 1000)
        return dists


if __name__ == '__main__':
    arg = sys.argv[1]
    tsp = BruteForceMultiTSP()

    if arg.endswith('.csv'):
        tsp.dist_matrix = tsp.read_distances(arg)
        start = time.time()
        result = tsp.brute_force()
        end = time.time()
        print(result, end - start)
    else:
        print("Nie podano pliku do odczytu.")
        
