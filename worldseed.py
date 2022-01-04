"""WorldSeed: a system for generating fractal hex maps"""

from random import random, randrange

class Map(list):

    """Map grid representation (as a list)

    Map(sequence) -> map from sequence having (X+Y)*Y+X*X structure.
    Map.new(X,Y[,s]) -> map of size X,Y seeded by selector s, or with None.
    """

    def __init__(self,L=[]):
        """Initialize map with contents of sequence having (X+Y)*Y+X*X structure."""
        list.__init__(self,L)
        X = len(self[-1])
        Y = len(self) - X
        for y in range(Y):
            assert len(self[y]) == X+Y
        for y in range(Y, X+Y):
            assert len(self[y]) == X
        self.X, self.Y = X, Y
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

    def grow(self, r, ni=1):
        """Apply growth rule to map and return a new map."""
        if ni == 0: return self
        def growfix(x, y):
            return (x - y), (x + 2*y)
        M = self.new(*self.XYfix(*growfix(self.X, self.Y)))
        M.parent = self
        AB = {}
        for x, y in self.coordinates():
            a = self[y][x]
            x, y = M.modfix(*growfix(x,y))
            M[y][x] = a
            AB[(y,x)] = randrange(2)
        o = ((-1,0),(1,-1),(0,1))
        for x, y in M.coordinates():
            p = (x-y)%3
            if p:
                k = 3 - p*2
                abc = []
                for n in range(3):
                    x_, y_ = M.modfix(x+k*o[n][0],y+k*o[n][1])
                    abc.append((M[y_][x_],AB[(y_,x_)])) 
                M[y][x] = r.apply(abc,p-1)
        return M.grow(r,ni-1)

    @staticmethod
    def XYfix(X, Y):
        """Rotate X,Y into first sextant."""
        while (X < 0 or Y <= 0):
            X, Y = X+Y, -X
        return X, Y

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
            parity = None

            for term in key:
                if term in (True, False):
                    connections[index-1] = term
                elif term in (0,1):
                    parity = term
                else:
                    colors[index] = term
                    index += 1

            rows = []
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        for p in range(2):
                            rows.append([(colors[0],i),(colors[1],j),(colors[2],k),p])

            for i in range(3):
                if connections[i] is not None:
                    rows = [
                        r for r in rows
                        if (r[i][1] ^ r[(i+1) % 3][1] ^ r[3] == 0) is connections[i]
                        ]

            if parity is not None:
                rows = [ r for r in rows if r[3] == parity ]

            sel = selector(D[key])

            for r in rows:
                rkey = tuple(sorted(r[0:3]) + [r[3]])
                self[rkey] = sel

    def apply(self,key,par):
        """Use rule to choose color for cell at vertex with given neighbors and parity."""
        key = tuple(sorted(key) + [par])
        if self.has_key(key):
            return self[key].pick()
        else:
            print None, key
            return None

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
