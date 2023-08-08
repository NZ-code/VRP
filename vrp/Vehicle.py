from geometry import Route


class Vehicle:
    def __init__(self, capacity=0):
        self._route = Route()
        self._places = []
        self._capacity = capacity

    def get_route(self):
        return self._route

    def visit_place(self, place):
        self._route.add_point(place.get_point())
        self._places.append(place)
        self._capacity -= place.get_demand()

    def get_capacity(self):
        return self._capacity

    def set_places(self, places):
        for place in places:
            self.visit_place(place)

    def get_last_client(self):
        if self._places:
            return self._places[-1]
        else:
            return None
