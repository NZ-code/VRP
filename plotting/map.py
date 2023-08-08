from geometry import Point
import matplotlib.pyplot as plt
import random
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        fig, ax = plt.subplots()
        self._ax = ax
        self._fig = fig
    def draw_clients(self, all_clients):
        for client in all_clients:
            self._draw_point(client.get_point(), color='red',label=client.get_demand())

    def draw_depo(self, depo):
        self._draw_point(depo.get_point(), size=50, color='black')

    def draw_vechicals_routes(self, vehicles):
        for vehicle in vehicles:
            self._draw_route(vehicle.get_route(), color=self.get_random_color())

    def generate_random_points(self, number_of_points):
        points = []
        for _ in range(number_of_points):
            point = self.generate_random_point()
            points.append(point)
        return points

    def generate_random_point(self):
        random_x = random.randint(0, self.width)
        random_y = random.randint(0, self.height)
        return Point(random_x, random_y)

    def _draw_route(self, route, color='blue'):
        points = route.get_points()
        for i in range(len(points) - 1):
            self.draw_line_between_points(points[i], points[i + 1], color=color)

    def draw_line_between_points(self, point1, point2, color='blue'):
        self._ax.plot([point1.x, point2.x], [point1.y, point2.y], color=color)

    def _draw_points(self, points, color='blue'):
        x = [p.x for p in points]
        y = [p.y for p in points]
        self._ax.scatter(x, y, color=color)

    def _draw_point(self, point, size=20, color='blue', label=None):
        self._ax.scatter(point.x, point.y, s=size, color=color)
        if label is not None:
            self._ax.annotate(label, (point.x, point.y), textcoords="offset points", xytext=(0, 10), ha='center')

    def get_random_color(self):
        r, g, b = random.random(), random.random(), random.random()
        color = (r, g, b)
        return color

    def show(self):
        plt.show()