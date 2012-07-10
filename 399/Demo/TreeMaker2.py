'''
 Licensed to Ashwin Panchapakesan under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 Ashwin licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
'''

import nltk
import pprint
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree

def isNoun(word):
    """Determine whether the word in this tuple ('anEnglishWord', 'it'sPOSannotation') is a noun by looking at it's POS tag"""
    return (word[1][0] == 'N' or "PRP" in word[1])

def isDet(word):
    """Determine whether the word in this tuple ('anEnglishWord', 'it'sPOSannotation') is a det by looking at it's POS tag"""
    return word[1] == 'DT'
def isAdj(word):
    """Determine whether the word in this tuple ('anEnglishWord', 'it'sPOSannotation') is an adjective by looking at it's POS tag"""
    return "JJ" in word[1]

def isIN(word):
    """Determine whether the word in this tuple ('anEnglishWord', 'it'sPOSannotation') is an IN by looking at it's POS tag"""
    return word[1] == "IN"

def isVerb(word):
    """Determine whether the word in this tuple ('anEnglishWord', 'it'sPOSannotation') is a verb by looking at it's POS tag"""
    return "VB" in word[1]

def isMD(word):
    """Determine whether the word in this tuple ('anEnglishWord', 'it'sPOSannotation') is an mD by looking at it's POS tag"""
    return word[1] == "MD"

def getTreeIndices(gct):
    """take a gold_chunked_text tree and return a list of the indeces where there are sub trees"""
    answer = []
    i = 0
    for e in gct:
        if type(e) == nltk.tree.Tree:
            answer.append(i)
        i += 1
    return answer

def prettyPrint(gct, treeIndeces, tabs=0):
    """take a GCT and a list of indeces where the trees are in that GCT and print a tree structure"""
    for i in range(len(gct)):
        if not i in treeIndeces:
            print "\t"*tabs + str(gct[i])
        else:
            prettyPrint(gct[i], getTreeIndices(gct[i]), tabs=tabs+1)
            
def main():
    
    text = "By creating an application that can run on relatively inexpensive and \
    completely remote hardware that can clean audio from multiple recordings, \
    the cost of creating clean audio recordings is drastically reduced and the cost of \
    deployment and repairs minimized. This has applications in almost any field that uses audio, \
    such as the recording industry or logging lectures and conferences. For the purposes of tying the groups research together, \
    we could apply this technology to creating a streamlined application \
    for smart phones to record lectures or conferences, upload the audio to a central server \
    and then have a computer with applicable hardware create a single clean audio stream in a minimal amount of time. "
    
    sentences = nltk.sent_tokenize(text)
    words = []
    for s in sentences:
        words.extend(nltk.word_tokenize(s))
#    print 'word tokenization complete'    ##
    taggedWords = nltk.pos_tag(words)
#    for i in taggedWords: print i    ##
#    print 'tagging complete'        ##
    tree = nltk.ne_chunk(taggedWords)
#    print  tree        ##
    trees = []
    for t in tree:
        if type(t) != nltk.tree.Tree:
            t = nltk.tree.Tree(t[0], [t[1]])
        trees.append(t)
    
#    for tr in trees:
#        print tr

    tstring = ''
    i = 0
    while i < len(taggedWords):
        word = taggedWords[i]
        if isDet(word):
            if i != len(taggedWords)-1:
                nextWord = taggedWords[i+1]
                if isNoun(nextWord):
                    tstring += "[ " + word[0] + "/DT " + nextWord[0] + '/' + nextWord[1] + " ] "
                    i += 1
#            print i, word[0], i+1, taggedWords[i+1][0],
        elif isVerb(word):
#            print i, word[0],
            tstring += "[ " + word[0] + '/' + word[1] + " ] "
        elif isIN(word):
#            print i, word[0],
            tstring += "[ " + word[0] + '/' + word[1] + " ] "
        elif isNoun(word):
#            print i, word[0],
            tstring += "[ " + word[0] + '/' + word[1] + " ] "
        elif isMD(word):
            tstring += "[ " + word[0] + '/' + word[1] + " ] "
        elif isAdj(word):
            if i != len(taggedWords)-1:
                nextWord = taggedWords[i+1]
                if isVerb(nextWord):
                    tstring += "[ " + word[0] + " " + nextWord[0] + '/' + nextWord[1] + " ] "
                    i += 1
                elif isNoun(nextWord):
                    tstring += "[ " + word[0] + " " + nextWord[0] + '/' + nextWord[1] + " ] "
                    i += 1
            tstring += "[ " + word[0] + '/' + word[1] + " ] "
        i +=1
    
    gold_chunked_text = tagstr2tree(tstring)
#    print eval('gold_chunked_text')    ##
    
    indeces = getTreeIndices(gold_chunked_text)
    prettyPrint(gold_chunked_text, indeces)
    
if __name__ == "__main__":
    main()
    print "done!"