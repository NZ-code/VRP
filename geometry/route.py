from .geometry import distance

class Route:
    def __init__(self):
        self._points = []
    def set_points(self,points):
        self._points = points
    def get_points(self):
        return self._points
    def add_point(self, point):
        return self._points.append(point)
    def get_last_point(self):
        return self._points[len(self._points)-1]
    def calculate_distance(self):
        total_distance = 0
        for i in range(len(self._points) - 1):
            total_distance += distance(self._points[i], self._points[i + 1])
        return total_distance