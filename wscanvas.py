from Tkinter import *
from math import *

sextant = 0.5*(1+sqrt(3)*1j)

class wscanvas(Canvas):

    def __init__(self, map, rule, pal, **kw):
        Canvas.__init__(self, **kw)
        self.width = int(self['width'])
        self.height = int(self['height'])

        self.map = map
        self.rule = rule
        self.pal = pal

        self.dx = self.width/(map.X + sextant*map.Y)
        self.x0 = self.dx*(1+sextant)/2

        W = self.master

        W.bind("w", lambda e: self.pan(-0.2j))
        W.bind("a", lambda e: self.pan(-0.2))
        W.bind("s", lambda e: self.pan(0.2j))
        W.bind("d", lambda e: self.pan(0.2))

        W.bind("W", lambda e: self.pan(-0.05j))
        W.bind("A", lambda e: self.pan(-0.05))
        W.bind("S", lambda e: self.pan(0.05j))
        W.bind("D", lambda e: self.pan(0.05))

        W.bind("=", lambda e: self.zoom(2))
        W.bind("-", lambda e: self.zoom(0.5))

        W.bind("+", lambda e: self.zoom(1.25))
        W.bind("_", lambda e: self.zoom(0.8))

        W.bind("q", lambda e: self.zoom(1j**(-1.0/3)))
        W.bind("e", lambda e: self.zoom(1j**(1.0/3)))

        W.bind("<space>", lambda e: self.grow())
        W.bind("<BackSpace>", lambda e: self.revert())

        W.bind("<Escape>", lambda e: self.quit())

        self.grid()

    def pan(self, delta):
        self.x0 += delta * self.width
        self.draw_map()

    def zoom(self, delta):
        self.dx *= delta
        self.x0 = (self.x0 - self._window_center()) * delta + self._window_center()
        self.draw_map()

    def grow(self):
        self.map = self.map.grow(self.rule)
        self.dx /= (1 + sextant)
        self.draw_map()

    def revert(self):
        if self.map.parent is not None:
            self.map = self.map.parent
            self.dx *= (1 + sextant)
            self.draw_map()

    def run(self):
        self.draw_map()
        self.mainloop()

    def draw_map(self):
        self.addtag_all('remove')
        self.delete('remove')
        for (x, y) in self._get_display_coords():
            (mx, my) = self.map.modfix(x,y)
            label = self.map[my][mx]
            self.draw_hex(x,y,label,self.pal[label])

    def locate_hex(self,x,y): return self.x0 + self.dx*(x+sextant*y)

    def draw_hex(self,x,y,label,color):
        xy = self.locate_hex(x,y)
        (a,b,c,d,e,f) = [xy+self.dx*(1.0+sextant)*(sextant**k)/3 for k in range(6)]
        line = "black" if abs(self.dx) >= 10 else ""
        id = self.create_polygon(a.real, a.imag,
                                 b.real, b.imag,
                                 c.real, c.imag,
                                 d.real, d.imag,
                                 e.real, e.imag,
                                 f.real, f.imag,
                                 outline=line, fill=color, tags=[label])
        return id

    def _in_view(self,x,y):
        xy = self.locate_hex(x,y)
        (x, y) = xy.real, xy.imag
        return x >= 0 and y >= 0 and x <= self.width and y <= self.height

    def _window_center(self):
        return 0.5*(self.width+self.height*1j)
 
    def _find_center(self):
        xy = (self._window_center() - self.x0) / self.dx
        y = xy.imag / sextant.imag
        x = (xy - y*sextant).real
        return (x,y)
        
    def _get_display_coords(self):
        (xc, yc) = map(int, self._find_center())
        for dir in (1, -1):
            (x, y0, y1) = (xc, yc - dir, yc + dir)
            while 1:
                while self._in_view(x,y0): y0 = y0 - dir
                while self._in_view(x,y1): y1 = y1 + dir
                if (x != xc or dir == 1):
                    for y in range(y0, y1+dir, dir): yield x, y
                while not (self._in_view(x,y0) or y0 == y1): y0 = y0 + dir
                if (y0 == y1):
                    if x == xc: (y0, y1) = (yc, yc)
                    else: break
                else:
                    while not self._in_view(x,y1): y1 = y1 - dir
                x = x + dir
                y0 = y0 - dir
