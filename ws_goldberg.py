from worldseed import Map
from goldberg import *
from random import choice

class ws_goldberg(game):
    def __init__(self, seed, rule, pal):
        self.M = 1
        self.N = 0
        game.__init__(self, self.M, self.N)
        self.players = ["worldseed"]
        self.verbs = [verb('grow', 'face', self.grow)]

        self.seed = seed
        self.rule = rule
        self.pal = pal

        for p in self.gn:
            t = seed.pick()
            self.add_thing(filled_hex(location=p, layer=0, type=t, color=self.pal[t]))

    def run(self):
        gcanvas(self, zoom=0.875).run()

    def grow(self, f, c):
        M_, N_ = Map.XYfix(*Map.growfix(self.M,self.N))
        gn_ = gnet(M_, N_)

        L = gvector.decode([ p for p in self.gn if gvector.decode(p).keys() == ['A'] ][0])['A']
        L_ = gvector.decode([ p for p in gn_ if gvector.decode(p).keys() == ['A'] ][0])['A']

        for p in self.gn:
            for t in self.things[p]:
                self.update_thing(t, location = (gvector.decode(p) * (L_/L)).encode())

        connect = {}
        for e in gn_.edges():
            if not [ f for f in gn_.faces_for_edge(e) if self.things[f] ]:
                connect[e] = choice(gn_.faces_for_edge(e))

        new_hexes = []
        for p in gn_:
            if not self.things[p]:
                key = []
                i0 = 0 if self.things[gn_[p][0]] else -1
                for i in range(i0, i0+len(gn_[p])):
                    if self.things[gn_[p][i]]:
                        key.append(self.things[gn_[p][i]][0].type)
                    else:
                        key.append(connect[gvector.sum(p,gn_[p][i])] == p)
                t = self.rule.apply(key)
                new_hexes.append(filled_hex(location=p, layer=0, type=t, color=self.pal[t]))

        for h in new_hexes:
            self.add_thing(h)

        self.update_thing(self, gn = gn_)
        self.update_thing(self, M = M_)
        self.update_thing(self, N = N_)
