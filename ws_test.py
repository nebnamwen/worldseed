from worldseed import *

my_map = Map.new(3,0,selector({'l':1, 's':1}))

(llsl, llss, lssl, lsss) = 0.5,0.5, 0.5,0.5

lll = {'l': 1}
lls = {'l': llsl, 's': llss}
lss = {'l': lssl, 's': lsss}
sss = {'s': 1}

rule1 = rule({
	('l', 'l', 'l'): [lll, lll],
	('l', 'l', 's'): [lls, lll],
	('l', 's', 's'): [lss, sss],
	('s', 's', 's'): [sss, sss]})

for i in range(8):
	my_map = my_map.grow(rule1)

pal1 = {'l':(2,2),'s':(4,4)}
display(my_map,pal1)
