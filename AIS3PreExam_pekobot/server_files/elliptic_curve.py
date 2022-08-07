class Curve:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

    def __eq__(self, other):
        if isinstance(other, Curve):
            return self.p == other.p and self.a == other.a and self.b == other.b
        return None

    def __str__(self):
        return "y^2 = x^3 + %dx + %d over F_%d" % (self.a, self.b, self.p)


class Point:
    def __init__(self, curve, x, y):
        if curve == None:
            self.curve = self.x = self.y = None
            return
        self.curve = curve
        self.x = x % curve.p
        self.y = y % curve.p

    def __str__(self):
        if self == INFINITY:
            return "INF"
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.curve == other.curve and self.x == other.x and self.y == other.y
        return None

    def __add__(self, other):
        if not isinstance(other, Point):
            return None
        if other == INFINITY:
            return self
        if self == INFINITY:
            return other
        p = self.curve.p
        if self.x == other.x:
            if (self.y + other.y) % p == 0:
                return INFINITY
            else:
                return self.double()
        p = self.curve.p
        l = ((other.y - self.y) * pow(other.x - self.x, -1, p)) % p
        x3 = (l * l - self.x - other.x) % p
        y3 = (l * (self.x - x3) - self.y) % p
        return Point(self.curve, x3, y3)

    def __neg__(self):
        return Point(self.curve, self.x, self.curve.p - self.y)

    def __mul__(self, e):
        if e == 0:
            return INFINITY
        if self == INFINITY:
            return INFINITY
        if e < 0:
            return (-self) * (-e)
        ret = self * (e // 2)
        ret = ret.double()
        if e % 2 == 1:
            ret = ret + self
        return ret

    def __rmul__(self, other):
        return self * other

    def double(self):
        if self == INFINITY:
            return INFINITY
        p = self.curve.p
        a = self.curve.a
        l = ((3 * self.x * self.x + a) * pow(2 * self.y, -1, p)) % p
        x3 = (l * l - 2 * self.x) % p
        y3 = (l * (self.x - x3) - self.y) % p
        return Point(self.curve, x3, y3)


INFINITY = Point(None, None, None)
