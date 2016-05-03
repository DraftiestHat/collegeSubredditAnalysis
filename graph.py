#!/usr/bin/python3

import argparse
import re
import networkx as nx
import os

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

inFile = open(args.filename)
allcolleges = dict()
keys = list()

for line in inFile:
	splitted = re.split('\W+', line)
	x = list() 
	x.extend(splitted)
	x.remove(splitted[0])
	allcolleges[splitted[0]] = x

inFile.close()

G = nx.Graph()

for key,value in allcolleges.items():
	G.add_node(key)
	keys.append(key)

#print(keys[1])
#print(allcolleges[keys[1]])
numKeys = len(keys)
x = 0

for i in range(1, numKeys):
	looking = keys[0]
	values = allcolleges[looking]
	del allcolleges[looking]
	keys.remove(looking)
	for val in values:
		if val:
			for key in keys:
				if val in allcolleges[key]:
					if (looking, key)  in  G.edges():
						G[looking]
						data = G[looking][key]['weight']
						data = data + 1
						G[looking][key]['weight'] = data
						G[looking]
					else:
						G.add_edge(looking, key, weight=1)
				

#print(G.nodes())
#print(G.edges())
test = 0
fileName = '.graphml'

while True:
	testFileName =  'out_' + str(test) + fileName
	if( not os.path.isfile('./' + testFileName)):
		fileName = testFileName
		break
	test = test + 1	



nx.write_graphml(G, fileName)
