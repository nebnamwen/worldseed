#!/usr/bin/python -i

"""WorldSeed: a system for generating fractal hex maps"""

import sys, random, curses

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
        for x, y in self.coordinates():
            a = self[y][x]
            x, y = M.modfix(*growfix(x,y))
            M[y][x] = a
        o = ((-1,0),(1,-1),(0,1))
        for x, y in M.coordinates():
            p = (x-y)%3
            if p:
                k = 3 - p*2
                abc = []
                for n in range(3):
                    x_, y_ = M.modfix(x+k*o[n][0],y+k*o[n][1])
                    abc.append(M[y_][x_]) 
                abc = tuple(abc)
                
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

    """Map growth rule representation (as a dict)

    rule(mapping) -> rule from mapping having the following structure:
    - Each key in mapping is a sorted 3-tuple.
    - Every sorted 3-tuple of values that occur in keys occurs as a key.
    - Each value in mapping is a 2-list.
    - Each element of this 2-list is a non-empty mapping.
    - The values in this mapping are positive numbers.

    rule.new(colors) -> rule giving a default distribution over a list of colors.
    """

    def __init__(self,D):
        """Initialize rule from mapping having appropriate structure."""
        dict.__init__(self,D)
        colors = {}
        for k in self.keys():
            assert isinstance(k, tuple)
            assert len(k) == 3
            for c in k:
                colors[c] = 1
        colors = colors.keys()
        colors.sort()
        for a in colors:
            for b in [x for x in colors if x >= a]:
                for c in [x for x in colors if x >= b]:
                    abc = (a,b,c)
                    assert self.has_key(abc)
                    assert len(self[abc]) == 2
                    for p in range(2):
                        self[abc][p] = selector(self[abc][p])
        self.colors = colors

    def apply(self,key,par):
        """Use rule to choose color for cell at vertex with given neighbors and parity."""
        L = list(key)
        L.sort()
        key = tuple(L)
        assert self.has_key(key)
        return self[key][par].pick()

    @classmethod
    def new(cls,colors):
        """Return a rule giving the default distribution over a sequence of colors."""
        D = {}
        for a in colors:
            D[(a,a,a)] = [{},{}]
            for p in range(2):
                D[(a,a,a)][p][a] = 1
            for b in [x for x in colors if x > a]:
                for x in [a,b]: D[(a,x,b)] = [{},{}]
                for p in range(2):
                    D[(a,a,b)][p][a] = D[(a,b,b)][p][b] = 2
                    D[(a,a,b)][p][b] = D[(a,b,b)][p][a] = 1
                for c in [x for x in colors if x > b]:
                    D[(a,b,c)] = [{},{}]
                    for p in range(2):
                        for x in [a,b,c]:
                            D[(a,b,c)][p][x] = 1
        return cls(D)

    def addcolors(self,colors):
        newrule = self.__class__.new(self.colors+colors)
        for key in self.keys():
            newrule[key] = self[key]
        self.__init__(newrule)

    def addcolor(self,color):
        self.addcolors([color])

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

    def pick(self, source = random.random):
        """Chose a key from selector with probability self[key].

        Uses random.random, or supply another 0-argument function
        that returns a random number in [0, 1).
        """
        self.normalize()
        s = 0
        r = source()
        for k in self.keys():
            s = s + self[k]
            if s > r: return k
        return None

    def set(self, key, val):
        """Set probability of key to value, adjust other values so total remains 1.0."""
        s = sum([self[k] for k in self.keys() if k != key])
        if val < 0 or val > 1 or s == 0: return None
        s = (1.0 - val)/s
        for k in self.keys():
            self[k] = self[k] * s
        self[key] = val

    def adjust(self, D):
        """Adjust relative probabilities of given keys while maintaining their total."""
        s = sum(D.values())
        r = sum([self[k] for k in self.keys() if k not in D.keys()])
        for k in D.keys():
            self[k] = D[k]*(1.0-r)/s

def display(M, pal):
    """Display map using palette.

    Palette is a mapping whose keys are map colors and whose values are 2-tuples
    of ANSI colors: (black, red, green, yellow, blue, magenta, cyan, white).
    """
    sys.stdout.write(chr(27)+")0"+chr(14))
    for y in range(len(M)):
        sys.stdout.write(" " * y)
        for a in M[y]:
            if pal.has_key(a):
                fg, bg = pal[a]
                sys.stdout.write(chr(27)+"[3"+str(fg)+";4"+str(bg)+"maa")
            else:
                sys.stdout.write(chr(27)+"[30;47mvw")
        sys.stdout.write(chr(27)+"[0m\n")
    sys.stdout.write(chr(15))
    sys.stdout.flush()
