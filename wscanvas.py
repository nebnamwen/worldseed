from Tkinter import *
from math import *

sextant = 0.5*(1+sqrt(3)*1j)

class WS_Canvas(Canvas):

    def __init__(self, master=None, **kw):
        Canvas.__init__(self, master, **kw)
        self.width = int(self['width'])
        self.height = int(self['height'])
        self.dx = None
        self.x0 = None
        self.grid()

    def fit_map(self, m):
        self.dx = self.width/(m.X + sextant*m.Y)
        self.x0 = self.dx*(1+sextant)/2

    def locate_hex(self,x,y): return self.x0 + self.dx*(x+sextant*y)

    def draw_hex(self,x,y,label,color):
        line = "black"
        if abs(self.dx) <= 10: line = ""
        xy = self.locate_hex(x,y)
        (a,b,c,d,e,f) = [xy+self.dx*(1.0+sextant)*(sextant**k)/3 for k in range(6)]
        id = self.create_polygon(a.real, a.imag,
                                 b.real, b.imag,
                                 c.real, c.imag,
                                 d.real, d.imag,
                                 e.real, e.imag,
                                 f.real, f.imag,
                                 outline=line, fill=color, tags=[label])
        return id

    def draw_map(self, m, palette):
        self.addtag_all('remove')
        self.delete('remove')
        if self.dx is None: self.fit_map(m)
        for (x, y) in self._get_display_coords():
            (mx, my) = m.modfix(x,y)
            label = m[my][mx]
            self.draw_hex(x,y,label,palette[label])

    def _in_view(self,x,y):
        xy = self.locate_hex(x,y)
        (x, y) = xy.real, xy.imag
        return x >= 0 and y >= 0 and x <= self.width and y <= self.height
 
    def _find_center(self):
        xy = (0.5*(self.width+self.height*1j) - self.x0) / self.dx
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

