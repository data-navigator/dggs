class Triangle(object):
    """A RegularPolygon is the abstract concept defining a polygon which can be tessellated.

        :param size: The distance from centroid to a vertex (radius of circumcircle)
        :param shape_type: The name of the shape being created.
        :param x: The x value of the origin shape's centroid.
        :param y: The y value of the origin shape's centroid.
        :param oid: The Object ID for this shape.
        :return: RegularPolygon
        """
    def __init__(self, oid, x=None, y=None, radius=None, area=None):
        from math import pi
        self.oid = str(oid)
        self._radius = radius
        self._area = area
        self._angle_func = lambda i: 0
        self._sides = 3
        self._side_length = 0
        self._apothem = 0
        self._x = x
        self._y = y
        self._inverted = False
        self._vertices = []
        self._edges = []
        self._angle_func = lambda i: (pi/6)*(3*(i+1)+i)+(pi/3) if self._inverted else (pi/6)*(3*(i+1)+i)

    def __repr__(self):
        """Machine readable representation of the shape."""
        return u"ID={0.oid}".format(self)

    def __invert__(self):
        self._inverted = not self._inverted
        return self

    @property
    def centroid(self):
        if not self._x:
            self._x = sum([vertex[0] for vertex in self.vertices])/3
        if not self._y:
            self._y = sum([vertex[1] for vertex in self.vertices])/3
        return self._x, self._y

    @property
    def inverted(self):
        return self._inverted

    @property
    def area(self):
        from math import radians, sin
        if not self._area:
            self._area = ((self.radius * self._sides * sin(radians(360/self._sides))) / 2)
        return self._area

    @property
    def side_length(self):
        from math import radians, sin
        if not self._side_length:
            self._side_length = 2 * self.radius * sin(radians(180/self._sides))
        return self._side_length

    @property
    def radius(self):
        from math import sqrt
        if not self._radius:
            self._radius = sqrt((4*(self._area/self._sides)) / sqrt(3))
        return self._radius

    @property
    def apothem(self):
        from math import radians, cos
        if not self._apothem:
            self._apothem = self._radius * cos(radians(180/self._sides))
        return self._apothem

    @property
    def vertices(self):
        """Generator to return the vertices of the shape.
        1.3589838486224 = The 'shift value' for points so the icosahedron points fits on WGS84 ellipsoid
        :return: Generator containing shape's vertexes.
        """
        from math import cos, sin
        if not self._vertices:
            for i in range(self._sides):
                x = float(self.radius)*cos(self._angle_func(i))+self._x
                y = float(self.radius)*sin(self._angle_func(i))+self._y
                if i == 1 and self.inverted:
                    self._vertices.append((round(x, 1), round(y, 1)))
                elif ((i == 0) or (i == 3)) and self.inverted:
                    self._vertices.append((round(x - 1.3589838486224, 1), round(y, 1)))
                elif i == 2 and self.inverted:
                    self._vertices.append((round(x + 1.3589838486224), round(y, 1)))
                elif (i == 0 or i == 3) and not self.inverted:
                    self._vertices.append((round(x, 1), round(y, 1)))
                elif i == 1 and not self.inverted:
                    self._vertices.append((round(x - 1.3589838486224, 1), round(y, 1)))
                elif i == 2 and not self.inverted:
                    self._vertices.append((round(x + 1.3589838486224), round(y, 1)))
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        if not type(value) is list and not len(value) == 4:
            return
        self._vertices = value

    def tessellate_class_one(self):
        # for each line that comprises the polygon, create a point at the mid-point.
        # Create 4 triangles from the initial triangles vertices and the newly created midpoints
        apothem_a = ((self.vertices[0][0] + self.vertices[1][0])/2, (self.vertices[0][1] + self.vertices[1][1])/2)
        apothem_b = ((self.vertices[1][0] + self.vertices[2][0])/2, (self.vertices[1][1] + self.vertices[2][1])/2)
        apothem_c = ((self.vertices[0][0] + self.vertices[2][0])/2, (self.vertices[0][1] + self.vertices[2][1])/2)
        t0 = Triangle(self.oid + '_0')
        t0.vertices = [apothem_a, apothem_b, apothem_c, apothem_a] if not self._inverted else [apothem_c, apothem_a, apothem_b, apothem_c]
        yield t0
        t1 = Triangle(self.oid + '_1')
        t1.vertices = [self.vertices[0], apothem_a, apothem_c, self.vertices[0]]
        yield t1
        t2 = Triangle(self.oid + '_2')
        t2.vertices = [apothem_a, self.vertices[1], apothem_b, apothem_a]
        yield t2
        t3 = Triangle(self.oid + '_3')
        t3.vertices = [apothem_c, apothem_b, self.vertices[2], apothem_c]
        yield t3

    def tessellate_class_two(self):
        # for each line that comprises the polygon, create a point at the mid-point.
        # Create 4 triangles from the initial triangles vertices and the newly created midpoints
        print(self.vertices)
        apothem_a = ((self.vertices[0][0] + self.vertices[1][0])/2, (self.vertices[0][1] + self.vertices[1][1])/2)
        apothem_b = ((self.vertices[1][0] + self.vertices[2][0])/2, (self.vertices[1][1] + self.vertices[2][1])/2)
        apothem_c = ((self.vertices[0][0] + self.vertices[2][0])/2, (self.vertices[0][1] + self.vertices[2][1])/2)
        t0 = Triangle(self.oid + '_0')
        t0.vertices = [apothem_a, apothem_b, apothem_c, apothem_a] if not self._inverted else [apothem_c, apothem_a, apothem_b, apothem_c]
        yield t0
        t1 = Triangle(self.oid + '_1')
        t1.vertices = [self.vertices[0], apothem_a, apothem_c, self.vertices[0]]
        yield t1
        t2 = Triangle(self.oid + '_2')
        t2.vertices = [apothem_a, self.vertices[1], apothem_b, apothem_a]
        yield t2
        t3 = Triangle(self.oid + '_3')
        t3.vertices = [apothem_c, apothem_b, self.vertices[2], apothem_c]
        yield t3

    def rotate(self, degrees):
        from math import cos, sin, radians
        theta = radians(degrees)
        for i in range(len(self.vertices)):
            v = self.vertices[i]
            self.vertices[i] = v[0]*cos(theta)-v[1]*sin(theta), v[0]*sin(theta)+v[1]*cos(theta)
