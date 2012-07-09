class Edge:
	def __init__(self, title='', atts=[], source='', dest=''):
		self.title = title
#		if atts:
#			self.modifiers = atts
#		else:
#			self.modifiers = []
#		
#		if source:
#			self.source = source
#		else:
#			self.source = ''
#		if dest:
#			self.destination = dest
#		else:
#			self.destination = ''
		self.modifiers = atts
		self.source = source
		self.destination = dest
		
	def linkTo(self, N):
		"""Define that this edge points to node N"""
		
		self.destination = N
		
	def linkFrom(self, N):
		"""Define that this edge points from node N"""
		
		self.source = N
		
	def setTitle(self, t):
		"""Define the title of this edge"""
		
		self.title = t
		
	def addModifier(self, m):
		"""Add modifiers to this edge"""
		
		self.modifiers.append(m)
		
	def addModifiers(self, M):
		"""Add the list of modifiers (M) to this edge"""
		
		self.modifiers.extend(M)
		
	def getIdentifier(self):
		"""Return a tuple that identifies this edge based on what it links from and to"""
		
		return (self.source.title, self.destination.title)
	
	def getLabel(self):
		"""Return the label associates with this edge in the format that it should be displayed in the graph"""
		
		label = self.title + '\n'
		
		modSet = set([i.lower() for i in self.modifiers])
		for m in modSet:
			label += m + '\n'
			
		return label