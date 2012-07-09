'''
Created on Nov 24, 2009

@author: Ashwin
'''

#import sys
#pythonLibs = ['C:\\Python26\\Lib\\idlelib', 'C:\\Windows\\system32\\python26.zip', 'C:\\Python26\\DLLs', \
#			  'C:\\Python26\\lib', 'C:\\Python26\\lib\\plat-win', 'C:\\Python26\\lib\\lib-tk', 'C:\\Python26', \
#			  'C:\\Python26\\lib\\site-packages', 'C:\\Python26\\lib\\site-packages\\pygraphics']
#sys.path.extend(pythonLibs)
import nltk, os, shutil#, clr
#clr.AddReference("System.Windows.Forms")
#from System.Windows.Forms import FolderBrowserDialog

#def getDirPath():
#	"""Ask the user for the directory path to the corpus and return tha path"""
#	
#	print "Entering getDirPath"   ## DEBUG ##
#	
#	askFolderPath = FolderBrowserDialog()
#	if askFolderPath.ShowDialog:
#		path = askFolderPath.SelectedPath
#
#	return path

pos_names = ['adj', 'noun', 'verb', 'to', 'det', 'rb', 'md', 'in', '.', ":", "(", ")", '-', "CC", "prp", "invalid_name"]
adj, noun, verb, to, det, rb, md, IN, period, colon, lparen, rparen, hyphen, cc, prp, invalid = pos_names

def run(dirpath):
	print 'running'
	
	subpath = dirpath + "imWorkingHere/"
	os.system("mkdir " +subpath)
	
	parsableParas = []
	
	corpusReader = makeCorpusReader(dirpath)
	paras = corpusReader.paras()
#	print "len(paras):", len(paras)	## DEBUG ##
	
	pn=0
	for para in paras:
#		try:
#			print pn	## DEBUG ##
			words = getWords(para)
			
			subFile = genFile(subpath)
			writeWords(words, subFile)
			
			dirPath = getDirPath(subFile)
			corpusReader = makeCorpusReader(dirPath)
#			print "FILEIDs:", corpusReader.fileids()
#			print "*"*30
			words = [word for word in corpusReader.words()]
			taggedWords = tag(words)
			parsableWords = mash(taggedWords)
			
			parsableParas.append(parsableWords)
			
			pn += 1
#		except Exception, e:
#			print "*"*40; print e; print "*"*40
#			break
		
	os.system("rm -f " +subpath + "/*")
	
	return parsableParas
	
def makeCorpusReader(dirpath):
	"""dirpath is the folder where all the corpus documents are. 
	Take this dirpath as the input paramater. Create a new corpusreader using this parameter and return that corpus"""
	
#	print "Entering makeCorpusReader"   ## DEBUG ##
#	print "dirpath:", dirpath   ## DEBUG ##
	
	folder = nltk.data.find(dirpath)
	corp = nltk.corpus.PlaintextCorpusReader(folder, '.*\.txt')
	
	return corp

def genFile(dirpath):
	"""Generate and return a unique, random filepath. The filepath describes a file in the dirpath"""

#	print "entering genFile"	## DEBUG ##
	filename = "blah.txt"
#	for char in sysTime:
#		filename += str(ord(char))
		
	filepath = dirpath + filename #+ '.txt'
	return filepath

def writeWords(words, filepath):
	"""The input parameter words is a list of words in english, that constitute a paragraph. 
	Write these words to the file described by the input parameter filepath.
	Don't return anything"""
	
#	print "Entering writeWords"	## DEBUG ##
	
	f = open(filepath, 'w')
	
	lastWord = words[-1]
	if '.' in lastWord:
		if len(lastWord) == 1:
			words = words[: -1]
		else:
			lastWord = lastWord[: -1]
			words = words[: -1]
			words.append(lastWord)
		
	for word in words:
		if not word in [',', ';', "!"]:
			f.write(word+" ")

	f.close()
	
def getDirPath(filepath):
	"""The input parameter filepath is the path of a file. 
	Return a string representation of the path of its immediate parent directory."""
	
	return filepath[: filepath.rfind('/') +1]
	

def getParas(corpusReader):
	"""The input parameter corpusReader is a corpus reader. This method returns a list of the paragraphs in the corpus reader. 
	Each paragraph is a list of sentences. Each sentence is a list of words."""
	
#	print "Entering getParas"   ## DEBUG ##

	paras = [para for para in corpusReader.paras()]
	return paras

def getWords(para):
	"""The input parameter paras is a list of paragraphs. Each paragraph is a list of sentences. Each sentence is a list of words.
	This method returns a list of the words in the paragraph"""
	
#	print "Entering getWords"   ## DEBUG ##
	
	words = [word for sentence in para for word in sentence]
	if words[-1] == '.':
		words = words[:-1]
		
	return words

def tag(words):
	"""The input parameter words is a list of words. Tag every word in teh list with its POStag and return the lagged list"""
	
#	print "Entering tag"   ## DEBUG ##
	
	taggedWords = nltk.pos_tag(words)
	return taggedWords

def pos(word):
	"""Return the part of speech of the input parameter word. word is a tuple containing the str word and the POStag."""
	
	pos_tags = ["JJ", "NN", "VB", "TO", "DT", "RB", "MD", "IN", ".", ":", "(", ")", '-', "CC", "PRP", "NOPOSTAGHERE"]
	index = 0

#	print word, pos_tags	## DEBUG ##
	while (index < len(pos_tags) - 1) and (pos_tags[index] not in word[1]):
#		print pos_tags[index], word, index, "<", len(pos_tags)	## DEBUG ##
		index += 1
	return pos_names[index]

def isEnding(word):
	"""Return true if this is a word that is the final word of a sentence"""
	
	return '.' in word[1]

def join(word, nextWord):
	"""The input parameters are tuples of English words and their POStags. 
	Return one such tuple that contains both words and the POStag of the second word"""
	
#	print "Entering join"   ## DEBUG ##
	
	if nextWord[0] in [hyphen]:
		modifiedWord = word[0] + nextWord[0]
		modifiedTag = word[1]
	
	elif word[0] in [hyphen]:
		modifiedWord = word[0] + nextWord[0]
		modifiedTag = nextWord[1]
		
	elif word[0][-1] == '-':
		modifiedWord = word[0] + nextWord[0]
		modifiedTag = nextWord[1]
			
	else:
		modifiedWord = word[0] + " " + nextWord[0]
		modifiedTag = nextWord[1]
	
	return (modifiedWord, modifiedTag)

def end(word, nextWord):
	"""This fucntion is similar to join. 
	The difference is that this function expects a sentence terminator like a period as the nextWord.
	This function will return a word whose POStag = POStag of word + '.'"""
	
	modifiedWord = word[0] + '.'
	modifiedTag = word[1] + '.'
	
	return (modifiedWord, modifiedTag)

def mash(taggedWords, i=0):
	"""The input parameter taggedWords is a list of tuples: (englishWord, POStag)
	Return a list of such tuples where the word incorporates adjectives/DTs/verbs that modify the nouns/verbs"""
	
#	print "Entering mash"   ## DEBUG ##

	seenVerb = False	# have we seen a verb yet? The first verb in a sentence is the edge. The subsequent verbs should modify the nouns that immediately precede them.	
	i=1
	taggedWordsLength=len(taggedWords)
	result = []
	word = taggedWords[0]
	while i<taggedWordsLength:					  # for every word in the list of tagged words
#		print 'i:', i   ## DEBUG ##
#		print 'taggedWordsLength:', taggedWordsLength   ## DEBUG ##
		
#		word = result[result_index]
#		print 'word:', word ## DEBUG  ##

#		print "taggedWords:", taggedWords	## DEBUG ##
		nextWord = taggedWords[i]
		posWord = pos(word)
		posNext = pos(nextWord)
		
		if nextWord[0] in ["("]:
			result.append(word)
			word = nextWord
			i += 1
		
		elif ("(" in word[0]) and \
		     (")" not in nextWord[0]):	# parsing what's inside parentheses
			word = join(word, nextWord)
			i += 1
			
		elif ("(" in word[0]) and (")" in nextWord[0]):	# reached closing parenthesis
			
#			print "word:", word	## DEBUG ##
#			print "word[0]:", word[0]	## DEBUG ##
			tw = nltk.pos_tag(word[0].split()[1:])
#			print "*"*40
#			print "tageedWords:", taggedWords
			parsableWords = mash(tw, i=1)
			
			word = (parsableWords, word[1])
#			print "word:", word	## DEBUG ##
			
			result.append(word)
			i += 1
			if i<taggedWordsLength:
				nextWord = taggedWords[i]
				word = nextWord
				i += 1
			
		elif (seenVerb and posNext in [verb]) or \
			 (posWord in [adj] and posNext in [adj, noun, verb, IN]) or \
			 (posWord in [verb] and posNext in [IN, to, verb, rb]) or \
			 (posWord in [noun] and posNext in [noun]) or \
			 (posWord in [rb] and posNext in [rb, noun, verb, adj]) or \
			 (posWord in [cc]) or \
			 (posNext in [cc]) or \
			 (posWord in [det, IN, to, md] and posNext in [cc, rb, det, noun, verb, adj]):
			
			word = join(word, nextWord)
			i += 1
			
			if not seenVerb and posWord in [verb]:
#				print "YAY"	## DEBUG ##
#				print word	## DEBUG ##
				seenVerb = True
			
		else:
			if posNext == period:
				word = end(word, nextWord)
				i += 1
				seenVerb = False
				
			result.append(word)
			word = taggedWords[i]
			i += 1
		
	result.append(word)
	
#	print "exiting mash"	## DEBUG ##

	return result

if __name__ == "__main__":
	
	print 'starting'
#	import sys
#	sys.path.append("/home/ashwin/workspace/n/")
#	dirPath = "c:\\users\\ashwin\\desktop\\n\\"
#	os.system("rmdir /S/Q C:\\Users\\Ashwin\\Desktop\\n\\imWorkingHere")

#	dirPath = "c:\\users\\ashwin\\desktop\\test\\"
#	os.system("rmdir /S/Q C:\\Users\\Ashwin\\Desktop\\test\\imWorkingHere")

	dirPath = "n/"
	try:
		shutil.rmtree("n/imWorkingHere")
	except:
		print "shutil.rmtree failed"
	
	parsableParas = run(dirPath)
	
#	print "len(parsableWords):", len(parsableWords)	 ## DEBUG ##
	
	for parsableWords in parsableParas:
		for i in parsableWords: 
			if not isinstance(i[0], list):
#				if  i[1]:
#					print "*"*40
#					print "\t\t\t SOMETHING OF INTEREST HERE\t", i[1]
				print i[0], "\t", i[1]
		
			else: 
				for word in i[0]: print '\t', word[0], "\t", i[1]
		
		print "*"*40
	
#		i = parsableWords[0]
#		if not isinstance(i[0], list):
#			print i[0]#, "\t", i[1]
#	
#		else: 
#			for word in i[0]: print '\t', word[0]