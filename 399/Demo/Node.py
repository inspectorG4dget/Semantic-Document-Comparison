class Node:
	def __init__(self, title='', atts=None, edges=None, dests=None):
		self.title = title.upper()		# The text with which this node is referred to
		
		if atts:
			self.attributes = atts		# attributes of this nodes (typically adjectives)
		else: 
			self.attributes = []
			
		if edges:
			self.edges = edges			# edges that come out of this node
		else:
			self.edges = []
			
		if dests:
			self.destinations = dests	# other nodes that can be reached from this node
		else:
			self.destinations = []
			
		self.paths = {}				# a dictionary that maps edge to destination node from this node
		
	def __str__(self):
		edgy = ''
		for e in self.edges:
			edgy += "EDGE: " + e.title + '\n'
			for m in e.modifiers:
				edgy += '\t' + m + '\n'
		s = ''.join(['Title: ']+[self.title+'\nAttributes:\n']+['\t' + a +'\n' for a in self.attributes]+['\n']+[ edgy[:-1] ])
		return s
		
	def addAttribute(self, att):
		"""Add the attribute att to this node. 
		   Typical attributes are adjectives"""
		
		self.attributes.append(att)
		
	def addAttributes(self, atts):
		"""Add the list of attributes atts to this node. 
		   Typical attributes are adjectives"""
		
		self.attributes.extend(atts)
		
	def connect(self, E, N):
		"""Connect this node to node N by edge E.
		   Add E to the list of edges that connect to this node"""

		self.edges.append(E)
		self.destinations.append(N)
		self.paths[E] = N
		
	def getLabel(self):
		"""Return the label associates with this edge in the format that it should be displayed in the graph"""
		
		label = ""
		
		attSet = set([i.rstrip(".\n").lower() for i in self.attributes])
		for a in attSet:
			label += a + '\n'
			
		return label
	
class NoSuchNodeException:
	def __init__(self, msg='', title=''):
		pass
#		if not msg and not title:
#			print "No node exists with such a title."
#		elif msg:
#			print msg
#		elif title:
#			print "No node exists with Title:", title
