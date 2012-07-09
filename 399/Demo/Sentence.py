from TreeMaker3 import *
import Node, Edge, WordNetIntegration as wni

class Sentence:
	def __init__(self, sentenceTokens):
		self.subject = Node.Node()
		self.verb = Edge.Edge()
		self.object = Node.Node()
		self._seenVerb = False	# have we seen a verb yet? If we have, then this next verb is likely part of the OBJECT and not the SUBJECT
		
#		print sentenceTokens
		
		self.process(sentenceTokens)
#		print "S:", self.subject.title
#		print "V:", self.verb.title
#		print "O:",self.object.title
		
	def structure(self):
		'''Return a graph structure of the Subject and Object Nodes being connected by a Verb edge. 
		Return only the subject node. Everything else can be calculated from it'''
		
		self.subject.connect(self.verb, self.object)
		self.verb.linkFrom(self.subject)
		self.verb.linkTo(self.object)
		
		return self.subject
	
	def process(self, tokens):

		descPrev = False	# are the adjectives that I see now describing the previously seen noun  (True) or the one that's coming up (False)
		i = 0
		while i<len(tokens):
			
			token = tokens[i]
			words = token[0]
			words = words.split()
			posTag = pos(token)
			
			if posTag in [noun, prp]:
				if not self._seenVerb:
					self.alterNode(self.subject, words)
				else:
					self.alterNode(self.object, words)
			
			elif posTag in [verb]:	# if we haven't seen a verb before this one, then this is the verb that will form the edge between two nodes
				if not self._seenVerb:	# however, if we have already seen a verb before this, then this verb does not form the edge.
										# but since I haven't dealt with such a sentence yet, I don't know how to handle it.
					self.alterEdge(self.verb, words)
					self.verb.linkFrom(self.subject)
					self.verb.linkTo(self.object)
					self._seenVerb = True
				
			elif posTag in [IN]:
				descPrev = not descPrev
				
			elif posTag in [adj] and descPrev:
				if isinstance(adj, list):
					self.subject.attributes.extend(words)
				else:
					self.subject.attributes.append(words)
					
				descPrev = False
			
			i += 1
					

	def alterNode(self, n, words):
		''' Given a node n and a list of words, use those words to calculate and set the title and label of the node'''

		taggedWords = nltk.pos_tag(words)
		noVerbs = True	# there are no verbs in these words
		for tw in taggedWords:
				if pos(tw) in [verb]:
					noVerbs = False
		
		# if we have seen a verb and both the subject and the object have been populated
		# then, the current tokens are describing the object (current node)
		if n.title: # if this node has already been populated, then WORDS is likely a descriptive phrase to be kept intact 
#			print " ".join([tw[0] for tw in taggedWords])	## DEBUG ##
			n.addAttribute(" ".join([tw[0] for tw in taggedWords]))
			
		else:
			prpFirst = False	# does a PRP or a NOUN come before the other in the node
			
			done = False
			i = 0
			while not done:	# determine if a PRP or a NOUN comes before the other
				if pos(taggedWords[i]) == prp:
					prpFirst = True
					done = True
				elif pos(taggedWords[i]) == noun:
					prpFirst = False
					done = True
				i += 1
					
			nouns = [i[0] for i in taggedWords if pos(i) in [noun, prp]]# and i[1][-1]!='.']	# sometimes a PRP can be the subject
			support = [i[0] for i in taggedWords if pos(i) not in [noun, prp, det]] if prpFirst \
						else [i[0] for i in taggedWords if pos(i) not in [noun, det]]# and i[1][-1]!='.']
						
			# uncomment these lines when ready for WordNetIntegration
#			nouns = [wni.singularize(i[0]) for i in taggedWords if pos(i) in [noun, prp]]# and i[1][-1]!='.']	# sometimes a PRP can be the subject
#			support = [wni.singularize(i[0]) for i in taggedWords if pos(i) not in [noun, prp, det]] if prpFirst \
#						else [i[0] for i in taggedWords if pos(i) not in [noun, det]]# and i[1][-1]!='.']
			for _ in nouns:
				if _ in support:
					support.remove(_)
	#		print "support:", support	## DEBUG ##
	#		print "nouns:", nouns	## DEBUG ##
			if nouns:
				title = nouns[0]	# the first noun is the title of the node
				support = nouns[1:] + support	# the rest of the nouns, adjectives, etc form the descriptor labels
				
				n.title = title
				n.addAttributes(support)
	#			print "n.title:", n.title	## DEBUG ##
	#			print "support:", support	## DEBUG ##
		
	def alterEdge(self, e, words):
		
		taggedWords = nltk.pos_tag(words)
		
		verbs = [i[0] for i in taggedWords if pos(i) in [verb]]
		support = [i[0] for i in taggedWords if pos(i) not in [verb, det]]
		
		if verbs:
			title = verbs[0]	# the first verb is the title of the node
			support = verbs[1:] + support	# the rest of the nouns,adjectives,etc form the descriptor labels
		
			e.title = title
			e.addModifiers(support)