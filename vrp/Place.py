from geometry import distance

class Place:
    def __init__(self, point, demand=0):
        self._point = point
        self._demand = demand

    def get_point(self):
        return self._point

    def get_demand(self):
        return self._demand

    def distance_to_place(self, other_place):
        return distance(self._point, other_place.get_point())