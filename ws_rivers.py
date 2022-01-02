from worldseed import *

my_map = Map.new(2,2,selector({'land':1, 'sea':1}))

rule1 = rule({
	('land', 'land', 'land'): [{'land': 1}, {'land': 1}],
	('land', 'river', 'river'): [{'river': 1}, {'land': 1}],
	('land', 'land', 'river'): [{'land': 1}, {'land': 1}],
	('river', 'river', 'river'): [{'river': 1}, {'land':1, 'river': 2}],
	('land', 'sea', 'sea'): [{'sea': 1}, {'land': 1, 'sea': 2}],
	('land', 'land', 'sea'): [{'land': 2, 'sea': 1}, {'land': 1}],
	('river', 'river', 'sea'): [{'river': 0, 'sea': 1}, {'sea': 1}],
	('river', 'sea', 'sea'): [{'sea': 1}, {'sea': 1}],
	('land', 'river', 'sea'): [{'river':1}, {'land': 1}],
	('sea', 'sea', 'sea'): [{'sea': 1}, {'sea': 1}]})

schedule = {
	(('land','land','land'),(0,1),'sea'): [ 0.3, 0.3, 0.3, 0., 0, 0, 0 ],
	(('sea','sea','sea'),(0,1),'land'): [ 0.45, 0.39, 0.3, 0, 0, 0, 0 ],
	(('land','land','sea'),(0,),'river'): [ 0.9, 0.9, 0.9, 0.5, 0, 0, 0 ],
	(('land','land','river'),(0,),'river'): [ 0.9, 0.9, 0.7, 0.5, 0.2, 0, 0 ],
	(('land','river','river'),(1,),'river'): [ 0, 0, 0, 0, 0.02, 0.04, 0.1 ],
	(('land','river','sea'),(1,),'river'): [ 0, 0, 0, 0, 0.1, 0.4, 0.7 ],
	(('river','river','sea'),(1,),'land'): [ 0, 0, 0, 0, 0.1, 0.2, 0.4 ],
	(None,(),None): None }

for i in range(7):
	for (key,ps,ter) in schedule.keys():
		for p in ps:
			rule1[key][p].set(ter,schedule[(key,ps,ter)][i])
	my_map = my_map.grow(rule1)

pal1 = {'land':(2,3),'sea':(4,4),'mount':(2,5), 'woods':(2,0), 'river':(4,6), 'desert':(3,7)}

# wscpal = {'land':'#80ff00', 'sea':'#0000ff','mount':'#808080', 'woods':'#008000', 'river':'#0080ff', 'desert':'#ff8000'}

display(my_map,pal1)
