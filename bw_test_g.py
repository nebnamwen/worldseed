# Accepts a black/white rule defined by an integer 0 <= n <= 99999999
# interpreted as a vector of digits specifying each of the rule clauses.
# If no command-line argument given, picks a random integer in this range.

from worldseed import *
from ws_goldberg import ws_goldberg
from random import randrange
import sys

seed = selector({'b':1, 'w':1})

rulecode = randrange(100000000)
if len(sys.argv) > 1:
    rulecode = int(sys.argv[1])

print(str(rulecode).zfill(8))
    
rb = []
rw = []
for i in range(8):
    val = (rulecode % 10) / 9.0
    rb.append(val)
    rw.append(1.0 - val)
    rulecode = rulecode // 10
    
rule = rule({
    ('b',True,'b','b'): {'b':rb[0], 'w':rw[0]},
    ('b',False,'b','b'): {'b':rb[1], 'w':rw[1]},
    ('b',True,'b','w'): {'b':rb[2], 'w':rw[2]},
    ('b',False,'b','w'): {'b':rb[3], 'w':rw[3]},
    ('b','w',True,'w'): {'b':rb[4], 'w':rw[4]},
    ('b','w',False,'w'): {'b':rb[5], 'w':rw[5]},
    ('w',True,'w','w'): {'b':rb[6], 'w':rw[6]},
    ('w',False,'w','w'): {'b':rb[7], 'w':rw[7]},
})

pal = {
    'b':'#000000',
    'w':'#ffffff'
    }

ws_goldberg(seed, rule, pal).run();
