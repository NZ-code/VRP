from vrp import VRP
from linear_programming import test

def vrp_call():
    num_of_vehicles = 2
    num_of_clients = 3
    vrp = VRP(num_of_vehicles, num_of_clients)
    vrp.solve_exact()
    vrp.draw()

def main():
    #test()
    vrp_call()

main()