from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.test import RequestFactory
from django.contrib import messages
from rest_framework.test import APIClient

from .forms import RegistrationForm, AccountAuthenticationForm, UploadFileForm
from algorithm import models as algorithm_models

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
    def read_distances(self, f):
        dists = []
        print(f)
        for line in f:
            if line[0] == '#':
                continue
            print(line)
            dists.append(list(map(int, map(str.strip, line.decode('utf8').split(',')))))
        print(dists)
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




def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            #login(request, user)
            messages.success(request, f'Account created for {email}!')
            return redirect('login')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'users/register.html', {'form': form})


def upload_view(request):
    context = {}
    if request.POST:
        form = UploadFileForm(request.POST, request.FILES)
        print('result, end - start')
        if form.is_valid():
            print('22222')
            form.save()
            factory = RequestFactory()
            content_type = "multipart/form-data"
            arg = request.FILES['file']
            tsp = BruteForceMultiTSP()
            tsp.dist_matrix = tsp.read_distances(arg)

            start = time.time()
            result = tsp.brute_force()
            end = time.time()
            print(result, end - start)
            factory.post('localhost:8000/upload/')

            context = {'data':str(result+"\t"+str(end-start))}
            return render(request, 'home', context)
        else:
            context['file_upload_form'] = form

    else:
        form = UploadFileForm()
        context['file_upload_form'] = form
    return render(request, 'users/upload.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "users/login.html", {'form': form})



