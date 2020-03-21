#!/usr/bin/env python
from docopt import docopt

from poeml.graph import Graph
from poeml.ginst_builder import GraphInstanceBuilder
from poeml.ginst_builder import make_props
from poeml.template import apply_template

usage = """ASP XML generator
Usage:
	aspo.py <graphml> <roots>
"""

def d_print(s):
	print(s)

def aspo(graph, roots):
	d_print('Started')
	nodes = len(graph.nodes)
	tiles = nodes // roots
	assert tiles*roots==nodes, 'Node count is not divisible by root count'

	def node_id(tile, id):
		return 'node_%d_%s' % (tile, graph.nodes[id] if type(id) is int else id)
	
	inst = GraphInstanceBuilder()
	
	d_print('Generating devices...')
	inst.start_devices()
	
	for tile in range(tiles):
		base_id = tile*roots
		for id in range(nodes):
			root_idx = (id - base_id) if (id>=base_id and id<base_id+roots) else None
			props = make_props( [ ('rootIdx', root_idx), ('graphInst', tile), ('id', id) ] )
			inst.add_device('node', node_id(tile, id), props)

	inst.end_devices()
	
	d_print('Generating edges...')
	inst.start_edges()
	
	for tile in range(tiles):
		for id in range(nodes):
			inst.add_edge('', node_id(tile, id), port='finished')

	for tile in range(tiles):
		for id in range(nodes):
			node = node_id(tile, id)
			inst.add_edge(node, node, port='heartbeat')

	for tile in range(tiles):
		d_print('Generating node edges... tile %d' % tile)
		for dst,src in graph.edges:
			inst.add_edge(node_id(tile, dst), node_id(tile, src), port='update')
		
	inst.end_edges()
	
	vars = {
		'nodeCount': nodes,
		'totalNodeCount': nodes*tiles,
		'tileCount': tiles,
		'rootCount': roots,
		'graphInstance': ''.join(inst.lines)
	}
	
	return apply_template('aspo_template.xml', vars)

def main():
	args = docopt(usage, version='1.0')
	xml = aspo(
		graph=Graph.load(args['<graphml>']),
		roots=int(args['<roots>'])
	)
	d_print('Done')
	print(xml)


if __name__ == "__main__":
	main()
