
def make_props(pairs):
	return ','.join('"%s":%s' % (key, str(val)) for key,val in pairs if not val is None)

class GraphInstanceBuilder():

	def __init__(self):
		self.lines = []
		
	def start_devices(self):
		self.lines.append(
			'\t<DeviceInstances>\n'
		)
		
	def add_device(self, type, id, props=''):
		self.lines.append(
			'\t\t<DevI id="%s" type="%s">%s</DevI>\n' % (id, type, ('<P>%s</P>' % props) if props!='' else '')
		)

	def end_devices(self):
		self.lines.append(
			'\t</DeviceInstances>\n'
		)

	def start_edges(self):
		self.lines.append(
			'\t<EdgeInstances>\n'
		)
		
	def add_edge(self, dst_id, src_id, dst_port=None, src_port=None, port=None, props=''):
		if dst_port is None:
			dst_port = port+'_in'
		if src_port is None:
			src_port = port+'_out'
		path = '%s:%s-%s:%s' % (dst_id, dst_port, src_id, src_port)
		self.lines.append(
			'\t\t<EdgeI path="%s">%s</EdgeI>\n' % (path, ('<P>%s</P>' % props) if props!='' else '')
		)

	def end_edges(self):
		self.lines.append(
			'\t</EdgeInstances>\n'
		)
