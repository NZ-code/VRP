class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def equal(self, point):
        if self.x == point.x and self.y == point.y:
            return True
        return False
