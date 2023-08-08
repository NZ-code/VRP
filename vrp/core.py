from pulp import *
import numpy as np
from itertools import combinations

import geometry
from geometry import Point, Route
from plotting import Map
from vrp.Client import Client
from vrp.Place import Place
from vrp.Vehicle import Vehicle


class VRP:
    def __init__(self, number_of_vehicles, number_of_clients):
        self.map = Map(1000, 1000)
        self.depo = Place(Point(500, 500))
        self.START_VEHICLE_CAPACITY = 9
        self.START_CLIENT_DEMAND = 3
        self.total_distance = 0
        self._vehicles = []
        self._all_clients = []
        self._unvisited_clients = []
        self._generate_vehicles(number_of_vehicles)
        self._generate_clients(number_of_clients, self.START_CLIENT_DEMAND)

    def get_distance_map(self, places):
        num_of_places = len(places)
        distance_map = [[places[i].distance_to_place(places[j]) for j in range(num_of_places)] for i in
                        range(num_of_places)]
        return distance_map

    def get_x_var(self, num_of_places):
        x = np.array(
            [[LpVariable(name=f"x_{i}_{j}", cat=LpBinary) for j in range(num_of_places)] for i in range(num_of_places)])
        return x
    def _get_var_f(self, num_of_places,x):
        return np.array([[LpVariable(name=f"f_{i}_{j}", lowBound=0, upBound=x[i][j]*self.START_VEHICLE_CAPACITY, cat=LpInteger)
                          for j in range(num_of_places)] for i in range(num_of_places)])

    def solve_exact(self):
        places = self._get_all_places()
        num_of_places = len(places)
        num_of_vehicles = len(self._vehicles)

        distances = np.array(self.get_distance_map(places))

        problem = LpProblem('Vehicle_flow', LpMinimize)
        x = self.get_x_var(num_of_places)
        f = self._get_var_f(num_of_places, x)

        problem = self._add_objective_function(distances, num_of_places, problem, x)

        problem = self._add_constraints(places, num_of_vehicles, problem, x, f)

        problem.solve()
        print(LpStatus[problem.status])
        if problem.status == 1:
            self._handle_linear_programing_success(places, x, f)
        else:

            self._handle_linear_programing_failure(problem)


    def _get_all_places(self):
        places = [self.depo]
        places.extend(self._all_clients)
        return places

    def _handle_linear_programing_failure(self, problem):
        raise Exception("Linear programing failed! Problem cannot be solved")

    def _handle_linear_programing_success(self, places, x, f):
        print('---------------------'+'f' + '------------------------')
        self.print_2d_array(f)
        print('---------------------' + 'x' + '------------------------')
        self.print_2d_array(x)
        routes = self.create_routes_from_matrix(x)
        for i in range(len(routes)):
            route_places = [places[place_index] for place_index in routes[i]]
            self._vehicles[i].set_places(route_places)

    def _add_objective_function(self, distances, num_of_places, problem, x):
        objective_function = pulp.lpSum(
            [[x[i][j] * distances[i][j] for j in range(num_of_places)] for i in range(num_of_places)])
        problem += objective_function
        return problem

    def _add_constraints(self, places, num_of_vehicles, problem, x, f):
        num_of_places = len(places)
        # 1 constraint and 2
        # exactly one arc enters each vertex associated with a customer
        # exactly one arc leaves each vertex associated with a customer
        for i in range(1, num_of_places):
            problem += (lpSum([x[i][j] for j in range(num_of_places)]) == 1)

        for j in range(1, num_of_places):
            problem += (lpSum([x[i][j] for i in range(num_of_places)]) == 1)
        # 3 constraint and 4 constraint
        # the number of vehicles leaving the depot is the same as the number entering.
        problem += (lpSum([x[i][0] for i in range(1, num_of_places)]) == num_of_vehicles)
        problem += (lpSum([x[0][j] for j in range(1, num_of_places)]) == num_of_vehicles)
        # fifth constraint
        #

        indexes_of_clients = [i for i in range(1, num_of_places)]
        client_combinations = allcombinations(indexes_of_clients, len(indexes_of_clients))
        for comb in client_combinations:
            problem += (lpSum([[x[i][j]
                                for j in range(num_of_places) if (i not in comb) and (j in comb)]
                               for i in range(num_of_places)])
                        >= self.how_many_vehicles_serve_route(comb))

        # DEMAND/ CAPACITY  CONSTRAINTS

        # number of units in a truck going from node i to node j


        # for j in range(1, num_of_places):
        #     problem += f[0][j] == x[0][j]*self.START_VEHICLE_CAPACITY

        row_sums = []
        col_sums = []
        for i in range(num_of_places):
            row_sum = 0
            for j in range(num_of_places):
                row_sum += f[i][j]
            row_sums.append(row_sum)
        for i in range(num_of_places):
            col_sum = 0
            for j in range(num_of_places):
                col_sum += f[j][i]
            col_sums.append(col_sum)
        for i in range(1, len(col_sums)):
            problem += (col_sums[i] - row_sums[i]) == places[i].get_demand()

        # for i in range(1, num_of_places):
        #     sum_1 = 0
        #     sum_2 = 0
        #     for j in range(num_of_places):
        #         sum_1 += f[j][i]
        #         sum_2 += f[i][j]
        #     sum_difference = sum_1 - sum_2
        #     problem += (sum_difference == places[i].get_demand() )

        # for i in range(num_of_places):
        #     for j in range(num_of_places):
        #         problem += f[i][j] - f[j][i] == places[i].get_demand()


        return problem

    def how_many_vehicles_serve_route(self, route):
        return 1

    def create_routes_from_matrix(self, x):
        routes = []
        (width, height) = x.shape
        for i in range(height):
            if value(x[0][i]) == 1:
                route = [0]
                w_to_go = i
                route.append(i)
                while w_to_go != 0:
                    for z in range(height):
                        if value(x[w_to_go][z]) == 1:
                            route.append(z)
                            w_to_go = z
                            break
                routes.append(route)
        return routes

    def print_2d_array(self, x):
        (width, height) = x.shape
        for w in range(width):
            for h in range(height):
                print(value(x[w][h]), end=" ")
            print()

    def solve_greedy(self):
        while (self._unvisited_clients):
            shortest_distance = float('inf')
            best_pair = (None, None)
            for vehicle in self._vehicles:
                last_place_visited_by_vehicle = vehicle.get_last_client()
                for client in self._unvisited_clients:
                    possible_distance = client.distance_to_place(last_place_visited_by_vehicle)
                    if vehicle.get_capacity() >= client.get_demand() and possible_distance < shortest_distance:
                        best_pair = (vehicle, client)
                        shortest_distance = possible_distance
            if best_pair[0] != None:
                best_vehicle = best_pair[0]
                best_client = best_pair[1]
                best_vehicle.visit_place(best_client)
                self._unvisited_clients.remove(best_client)
            else:
                break
        for vehicle in self._vehicles:
            vehicle.visit_place(self.depo)

    def _generate_vehicles(self, number_of_vehicles):
        for _ in range(number_of_vehicles):
            vehicle = Vehicle(capacity=self.START_VEHICLE_CAPACITY)
            vehicle.visit_place(self.depo)
            self._vehicles.append(vehicle)

    def _generate_clients(self, number_of_clients, demand):
        for _ in range(number_of_clients):
            client_coord = self.map.generate_random_point()
            self._unvisited_clients.append(Client(client_coord, demand))
        self._all_clients = self._unvisited_clients.copy()

    def draw(self):
        self.map.draw_depo(self.depo)
        self.map.draw_clients(self._all_clients)
        self.map.draw_vechicals_routes(self._vehicles)
        self.map.show()
