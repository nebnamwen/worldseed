from worldseed import *;

my_map = Map([['riv1','riv2','sea'],['land','land','land'],['land']])

rule1 = rule({
	('land', 'land', 'land'): [{'land': 1}, {'land': 1}],
	('land', 'riv1', 'riv1'): [{'riv1': 1, 'riv2': 1}, {'land': 1}],
	('land', 'riv1', 'riv2'): [{'land': 1}, {'riv1': 1, 'riv2': 1}],
	('land', 'riv2', 'riv2'): [{'riv1': 1, 'riv2': 1}, {'land': 1}],
	('land', 'land', 'riv1'): [{'land': 8, 'riv1': 0, 'riv2': 0}, {'land': 1}],
	('land', 'land', 'riv2'): [{'land': 8, 'riv1': 0, 'riv2': 0}, {'land': 1}],
	('riv1', 'riv1', 'riv1'): [{'riv1': 1, 'riv2': 1}, {'land': 1}],
	('riv1', 'riv1', 'riv2'): [{'land': 1}, {'riv1': 1, 'riv2': 1}],
	('riv1', 'riv2', 'riv2'): [{'land': 1}, {'riv1': 1, 'riv2': 1}],
	('riv2', 'riv2', 'riv2'): [{'riv1': 1, 'riv2': 1}, {'land': 1}],
	('land', 'sea', 'sea'): [{'land': 1, 'sea': 2}, {'land': 1, 'sea': 2}],
	('land', 'land', 'sea'): [{'land': 10, 'sea': 5, 'riv1': 0, 'riv2': 0},
				  {'land': 2, 'sea': 1}],
	('riv1', 'riv1', 'sea'): [{'land': 1}, {'land': 1}],
	('riv1', 'riv2', 'sea'): [{'land': 1}, {'land': 1}],
	('riv2', 'riv2', 'sea'): [{'land': 1}, {'land': 1}],
	('riv1', 'sea', 'sea'): [{'land': 1}, {'land': 1}],
	('riv2', 'sea', 'sea'): [{'land': 1}, {'land': 1}],
	('land', 'riv1', 'sea'): [{'riv1': 1, 'riv2': 1, 'sea': 2}, {'riv1': 1, 'riv2': 1, 'sea': 2}],
	('land', 'riv2', 'sea'): [{'riv1': 1, 'riv2': 1, 'sea': 2}, {'riv1': 1, 'riv2': 1, 'sea': 2}],
	('sea', 'sea', 'sea'): [{'sea': 1}, {'sea': 1}]
	})

# wscpal = {'land':'#80ff00', 'sea':'#0000ff','mount':'#808080', 'woods':'#008000', 'riv1':'#0080ff', 'riv2':'#3080ff', 'desert':'#ff8000'}

for i in range(8):
    my_map = my_map.grow(rule1)

pal1 = {'land':(2,2),'sea':(4,4), 'riv1':(6,4), 'riv2':(6,4)}

display(my_map,pal1)
