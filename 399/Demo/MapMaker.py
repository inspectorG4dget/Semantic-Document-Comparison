from TreeMaker3 import *
from Sentence import Sentence
import sys, networkx as nx, matplotlib.pyplot as plt, WordNetIntegration as wni #@UnresolvedImport
from Node import NoSuchNodeException
from WordNetIntegration import senseRange
from nltk.corpus import wordnet as wn
if "c:\\Python26\\networkx\\" not in sys.path: sys.path.append("c:\\Python26\\networkx\\")

def getSentences(parsableWords):
	"""Take a list of parsable words as returned by TreeMaker3.mash.
	   Return a list of lists. Each sublist is a list of (string of words, POStag), each of which is a token in parsableWords.
	   Each sublist is also an entire sentence as represented in the original document."""
	
	sentences = [[]]
	
	for i in range(len(parsableWords)):
		token = parsableWords[i]	# the next set of words that together form a part of speech
		sentences[-1].append(token)	# add this token to the last sentence of this paragraph
		if isEnding(token):			# if these words end the current sentence, then append a new list to the list of sentences
			sentences.append([])	# 	to denote a new sentence
	
	for _ in range(sentences.count([])):
		sentences.remove([])
	return sentences	# remove the last empty list from the list of sentences

def findNode(G, TITLE):
	"""Return the node N in the Graph G with the title TITLE. Raise AttributeError if no such node exists."""
	
	# uncomment these lines when ready for WordNetIntegration
#	titleSenses = range(senseRange(TITLE))
#	answer = ''
#	match = 0.0
#	
	for N in G.nodes():
#		nodeSenses = range(senseRange(N))
#		for t in titleSenses:
#			tsyns = set(wn.synset('%s.n.%02d' %(TITLE, t)).lemma_names)
#			for n in nodeSenses:
#				nsyns = set(wn.synset('%s.n.%02d' %(TITLE, n)).lemma_names)
#				if len(intersection(tsyns, nsyns))/float(len(nsyns)) >= match:
#					match = len(intersection(tsyns, nsyns))/float(len(nsyns))
#					answer = N
#					
#	return N
				
		
		if N.rstrip('.\n') == TITLE.rstrip('.\n'):
			return N
	raise NoSuchNodeException(title=TITLE)
			


def mapMaker(parsableParas):
	
	G = nx.Graph()
	
	nodeLabels = {}
	edgeLabels = {}
	
	for parsablePara in parsableParas:
		parsableWords = parsablePara
		sentences = getSentences(parsableWords)
		
		for sentenceTokens in sentences:	# for each list of set of words in the sentence that forms a POS

			sentence = Sentence(sentenceTokens)	# make a sentence object out of those words
			
			subject = sentence.structure()
			subject.title = subject.title.rstrip(".\n")
			
			# find the node in the graph which has as it's title, the subject of the current sentence
			try:
				s = findNode(G, subject.title)
			
			# if such a node doesn't exist, add it to the graph and add an entry for it in the graph labels 
			except NoSuchNodeException:
				G.add_node(subject.title)
				nodeLabels[subject.title] = [subject.title]
				s = findNode(G, subject.title)

			# add the appropriate labels for this node
			finally:
#				print subject	## DEBUG ##
				if subject.getLabel() not in nodeLabels[subject.title]:
					nodeLabels[subject.title].append(subject.getLabel())
				

			for verb in subject.paths.keys():
				
				dest = subject.paths[verb]
				dest.title = dest.title.rstrip('.\n')
				
				# find the node in the graph which has as it's title, the object of the current sentence
				try:
					d = findNode(G, dest.title)
				
				# if such a node doesn't exist, add it to the graph and add an entry for it in the graph labels	
				except NoSuchNodeException:
					G.add_node(dest.title)
					nodeLabels[dest.title] = [dest.title]
					
				# add the appropriate labels for this node
				finally:
#					print dest	## DEBUG ##
					d = findNode(G, dest.title)
					if dest.getLabel() not in nodeLabels[dest.title]:
						nodeLabels[dest.title].append(dest.getLabel())
		
				# add the edge label in the graph for this verb
				edgeLabels[verb.getIdentifier()] = verb.getLabel()
				
				# add an edge between the subject and the object
				G.add_edge(s,d)

	# nltk requires that the node labels be strings and not lists.
	# this for loop takes the nodeLabels dict and turns the list of descriptors into a newline-separated string of descriptors
	# the next loop does the same for edge labels
	for node in nodeLabels.keys():
		nodeLabels[node] = ''.join(['\n'+label for label in nodeLabels[node]])
		nodeLabels[node] = nodeLabels[node].strip("\n")
		
	for e in edgeLabels.keys():
		edgeLabels[e] = edgeLabels[e].rstrip('\n')
		
	# draw the graph to the following specs:
	# use the generated node labels: nouns and attributes
	# the size of the node needs to be 1000 * (number of '\n' +1). The reason for the +1 is to accomodate single-line labels
	# node_shape='s' describes that each node should be a square
	# spectral layout is the one layout that makes the most sense to display the graph. Many layouts were tried in a trial-and-error fashion
	nx.draw(G, labels=nodeLabels, node_size=[(nodeLabels[node].count('\n') +1)*1000 for node in G.nodes()], node_shape='s', pos=nx.spectral_layout(G)) 
	pos = nx.layout.spectral_layout(G)
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edgeLabels)
#	nx.write_dot(G, '/home/ashwin/Desktop/sample')
	plt.show()
	
	
if __name__ == "__main__":
	import os
#	os.system("C:\\Python26\\python C:\\Users\\Ashwin\\workspace\\399\\src\\Demo\\")
	
#	dirPath = "c:\\users\\ashwin\\desktop\\test\\"
#	os.system("rd /S/Q C:\\Users\\Ashwin\\Desktop\\test\\imWorkingHere")
	dirPath = "n/"
#	os.system("rd /S/Q C:\\Users\\Ashwin\\Desktop\\blarpf\\imWorkingHere")
	parsableParas = run(dirPath)
	
	mapMaker(parsableParas)
	