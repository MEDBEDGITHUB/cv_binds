import math
class Point:
    def __init__(self, x, y=None, polar=False):
        if not polar:
            self.x = x
            self.y = y
        else:
            self.x = x * math.cos(y)
            self.y = x * math.sin(y)
        self.polar = polar

    def __abs__(self):
        return math.hypot(self.y, self.x)

    def __str__(self):
        return str((self.x, self.y))

    def dist(self, x=0, y=0):
        if isinstance(x, Point):
            y = x.y
            x = x.x
        return math.hypot(y - self.y, x - self.x)


class Vector(Point):
    def __init__(self, x1, y1=0, x2=None, y2=None):
        if isinstance(x2, int):
            super().__init__(x2 - x1, y2 - y1)
        elif not isinstance(x2, int):
            super().__init__(x1, y1)
        if isinstance(x1, Point):
            super().__init__(x1.x, x1.y)
        if isinstance(y1, Point):
            super().__init__(y1.x - x1.x, y1.y - x1.y)


    def __mul__(self, other):
        try:
            return self.dot_product(other)
        except:
            self.x, self.y = self.x * other, self.y * other
            return self

    def dot_product(self, other: "Vector"):
        return self.x * other.x + self.y * other.y

    def cross_product(self, other):
        return self.x * other.y - self.y * other.x

    __xor__ = cross_product
    __rmul__ = __mul__