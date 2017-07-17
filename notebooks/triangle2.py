class Triangle2(object):
    def __init__(self, oid, vertices=[]):
        if not vertices:
            raise ValueError("Creation of Triangle2 requires vertices.")
        self._sides = 3  # Triangles have three sides.
        self._oid = oid
        self._vertices = vertices
        self._edges = None
        self._inverted = False
        self._centroid = None
        self._area = None
        self._edge_length = None
        self._radius = None
        self._apothem = None

    def __invert__(self):
        self._inverted = not self._inverted
        return self

    @property
    def inverted(self):
        return self._inverted

    @property
    def centroid(self):
        x = sum([vertex[0] for vertex in self.vertices])/3
        y = sum([vertex[1] for vertex in self.vertices])/3
        return x, y

    @property
    def area(self):
        if not self._area:
            from math import radians, sin
            self._area = ((self.radius * self._sides * sin(radians(360/self._sides))) / 2)
        return self._area

    @property
    def edge_length(self):
        if not self._edge_length:
            from math import sqrt
            x_diff = self.vertices[1][0] - self.vertices[0][0]
            y_diff = self.vertices[1][1] - self.vertices[0][1]
            self._edge_length = sqrt(x_diff**2 + y_diff**2)
        return self._edge_length

    @property
    def radius(self):
        if not self._radius:
            from math import sqrt
            self._radius = self.edge_length / sqrt(3)
        return self._radius

    @property
    def apothem(self):
        if not self._apothem:
            from math import cos, radians
            self._apothem = self.radius * cos(radians(180/self._sides))
        return self._apothem

    @property
    def vertices(self):
        for vertex in self._vertices:
            yield vertex

    def tessellate(self):
        raise NotImplementedError
