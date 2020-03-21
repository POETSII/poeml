from xml.etree import cElementTree as ET

class Graph():
	def __init__(self, nodes, edges):
		self.nodes = nodes
		self.edges = edges

	@classmethod
	def load(cls, path):
		with open(path, "r") as file:
			graphml = file.read()
		tree = ET.ElementTree(ET.fromstring(graphml))
		root_elems = [ elem for elem in tree.getroot() if elem.tag.endswith("graph") ]
		assert root_elems, "Could not find <graph> element"
		root = root_elems[0]
		namespaces = {"graphml": "http://graphml.graphdrawing.org/xmlns"}
		edge_default = root.attrib.get("edgedefault", "directed")

		nodes = [ n.attrib["id"]
			for n in root.findall("graphml:node", namespaces)
		]

		edges = [ (e.attrib["source"], e.attrib["target"])
			for e in root.findall("graphml:edge", namespaces)
		]

		if edge_default == "undirected":
			reversed_edges = [ (dst, src) for src, dst in edges ]
			edges += reversed_edges

		return cls(nodes, edges)
