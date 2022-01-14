from worldseed import *;
from wscanvas import wscanvas;

my_map = Map([['riv','riv','sea'],['land','land','land'],['land']])

rule1 = rule({
        ('land','land','land'): {'land':1},
        ('land','land','riv'): {'land':1},
        ('land','riv','riv',0): {'riv':1},
        ('land','riv','riv',1): {'land':1},
        ('riv','riv','riv',0): {'riv':1},
        ('riv','riv','riv',1): {'land':1},
        ('sea','sea','sea'): {'sea':1},
        ('land','land','sea'): {'land':2, 'sea':1},
        ('land','sea','sea'): {'land':1, 'sea':2},
        ('riv','riv','sea'): {'land':1},
        ('riv','sea','sea'): {'land':1},
        ('land','riv','sea'): {'riv':1, 'sea':1}
	})

wscpal = {
    'land':'#80ff00',
    'sea':'#0000ff',
    'riv':'#0080ff'
    }

wscanvas(my_map, rule1, wscpal, width=800,height=700).run();
