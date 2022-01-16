from worldseed import *;
from ws_goldberg import ws_goldberg;

my_seed = selector({'land':2, 'sea':2, 'riv':1})

rule1 = rule({
        ('land','land','land'): {'land':1},
        ('land','land','riv'): {'land':1},
        ('land','riv',True,'riv'): {'riv':1},
        ('land','riv',False,'riv'): {'land':1},
        ('riv',True,'riv',True,'riv'): {'riv':1},
        ('riv',False,'riv',False,'riv'): {'land':1},
        ('sea','sea','sea'): {'sea':1},
        ('land','land','sea'): {'land':2, 'sea':1},
        ('land','sea','sea'): {'land':1, 'sea':2},
        ('riv',True,'riv','sea'): {'riv':1},
        ('riv',False,'riv','sea'): {'land':1}, 
        ('riv',False,'sea','sea',False): {'land':1},
        ('riv',True,'sea','sea'): {'sea':1},
        ('land','riv',True,'sea'): {'riv':1, 'sea':1},
        ('land','riv',False,'sea'): {'land':1, 'riv':1}
	})

wscpal = {
    'land':'#80ff00',
    'sea':'#0000ff',
    'riv':'#0080ff'
    }

ws_goldberg(my_seed, rule1, wscpal).run();
