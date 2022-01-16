"""WorldSeed: a system for generating fractal hex maps"""

from random import random, randrange

class Map(list):

    """Map grid representation (as a list)

    Map(sequence) -> map from sequence having (X+Y)*Y+X*X structure.
    Map.new(X,Y[,s]) -> map of size X,Y seeded by selector s, or with None.
    """

    def __init__(self,L=[], useAB=True):
        """Initialize map with contents of sequence having (X+Y)*Y+X*X structure."""
        list.__init__(self,L)
        X = len(self[-1])
        Y = len(self) - X
        for y in range(Y):
            assert len(self[y]) == X+Y
        for y in range(Y, X+Y):
            assert len(self[y]) == X
        self.X, self.Y = X, Y
        self.useAB = useAB
        self.parent = None

    def coordinates(self):
        """Return valid coordinates in map grid as a list of tuples."""
        L = []
        for y in range(len(self)):
            for x in range(len(self[y])):
                L.append((x,y))
        return L

    def modfix(self,x,y):
        """Translate a pair of integers into valid coordinates in map grid."""
        X, Y = self.X, self.Y
        R = X + Y
        if (x < 0 or y < 0 or x >= R or y >= R or (x >= X and y >= Y)):
            d = (X*x+X*y+Y*y)/(X*X+X*Y+Y*Y)
            x, y = x - d*X, y - d*Y
            d = x/R
            x, y = x - R*d, y + X*d
            if y < 0: x, y = x+X, y+Y
            if x >= R: x, y = x-R, y+X
        return x, y

    def colors(self):
        """Return a list of the colors (cell contents) that occur in this map."""
        D = {}
        for x, y in self.coordinates():
            D[self[y][x]] = 1
        return D.keys()

    @staticmethod
    def growfix(x, y):
        return (x - y), (x + 2*y)

    @staticmethod
    def XYfix(X, Y):
        """Rotate X,Y into first sextant."""
        while (X < 0 or Y <= 0):
            X, Y = X+Y, -X
        return X, Y

    def grow(self, r, ni=1):
        """Apply growth rule to map and return a new map."""
        if ni == 0: return self

        M = self.new(*self.XYfix(*self.growfix(self.X, self.Y)))
        M.useAB = self.useAB
        M.parent = self

        AB = {}

        for x, y in self.coordinates():
            a = self[y][x]
            x, y = M.modfix(*self.growfix(x,y))
            M[y][x] = a
            AB[(x,y)] = randrange(self.useAB + 1)

        o = ((-1,0),(1,-1),(0,1))
        for x, y in M.coordinates():
            p = (x-y)%3
            if p:
                k = 3 - p*2
                nxy = [ M.modfix(x+k*o[n][0],y+k*o[n][1]) for n in range(3) ]
                abc = []
                for n in range(3):
                    x_, y_ = nxy[n]
                    abc.append(M[y_][x_])
                    abc.append(AB[(x_,y_)] ^ AB[nxy[(n+1)%3]] ^ (p-1))
                M[y][x] = r.apply(abc)

        return M.grow(r,ni-1)

    @classmethod
    def new(cls, X, Y, sel = {None: 1}):
        """Return a new map of size X,Y seeded by a selector, or with None."""
        sel = selector(sel)
        L = []
        for y in range(Y):
            L.append([])
            for x in range(X+Y):
                L[-1].append(sel.pick())
        for y in range(X):
            L.append([])
            for x in range(X):
                L[-1].append(sel.pick())
        return cls(L)

class rule(dict):

    """Map growth rule representation (as a dict)"""

    def __init__(self,D):
        dict.__init__(self,{})
        for key in D:
            index = 0
            colors = [None] * 3
            connections = [None] * 3

            for term in key:
                if term in (True, False):
                    connections[index-1] = term
                else:
                    colors[index] = term
                    index += 1

            rows = []
            for i in range(2):
                if connections[0] in (None, i):
                    for j in range(2):
                        if connections[1] in (None, j):
                            for k in range(2):
                                if connections[2] in (None, k):
                                    rows.append([colors[0],i,colors[1],j,colors[2],k])

            sel = selector(D[key])

            for r in rows:
                rkey = self._fix_key(r)
                self[rkey] = sel

    def apply(self,key):
        """Use rule to choose color for cell at vertex with given neighbors and parity."""
        key = self._fix_key(key)
        if self.has_key(key):
            return self[key].pick()
        else:
            print None, key
            return None

    @staticmethod
    def _fix_key(key):
        permutations = [
            [0,1,2,3,4,5],
            [2,3,4,5,0,1],
            [4,5,0,1,2,3],
            [0,5,4,3,2,1],
            [2,1,0,5,4,3],
            [4,3,2,1,0,5]
            ]

        return tuple(min([ [key[i] for i in p] for p in permutations ]))

class selector(dict):

    """Representation of the distribution of a random variable (as a dict).

    selector(mapping) -> selector from mapping.
    (Mapping is non-empty, values are positive numbers.)
    """

    def __init__(self, D):
        """Initialize selector from non-empty mapping whose values are positive numbers."""
        dict.__init__(self, D)
        self.normalize()

    def normalize(self):
        """Scale values so they sum to 1.0."""
        S = sum(self.values())
        for k in self.keys():
            self[k] = float(self[k])/S
            if self[k] == 0: del self[k]

    def pick(self):
        """Chose a key from selector with probability self[key]."""
        s = 0
        r = random()
        for k in self.keys():
            s = s + self[k]
            if s > r: return k
        return None
