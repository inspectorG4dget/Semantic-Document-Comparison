import nltk
import pprint

def main():
    global f
    f = open("c:\\users\\ashwin\\desktop\\dump.txt", 'w')
    
    text = """Mr Blobby is a fictional character who featured on Noel
    Edmonds' Saturday night entertainment show Noel's House Party,
    which was often a ratings winner in the 1990s. Mr Blobby also
    appeared on the Jamie Rose show of 1997. He was designed as an
    outrageously over the top parody of a one-dimensional, mute novelty
    character, which ironically made him distinctive, absurd and popular.
    He was a large pink humanoid, covered with yellow spots, sporting a
    permanent toothy grin and jiggling eyes. He communicated by saying
    the word "blobby" in an electronically-altered voice, expressing
    his moods through tone of voice and repetition.
    """
    """
    There was a Mrs. Blobby, seen briefly in the video, and sold as a
    doll.

    However Mr Blobby actually started out as part of the 'Gotcha'
    feature during the show's second series (originally called 'Gotcha
    Oscars' until the threat of legal action from the Academy of Motion
    Picture Arts and Sciences[citation needed]), in which celebrities
    were caught out in a Candid Camera style prank. Celebrities such as
    dancer Wayne Sleep and rugby union player Will Carling would be
    enticed to take part in a fictitious children's programme based around
    their profession. Mr Blobby would clumsily take part in the activity,
    knocking over the set, causing mayhem and saying "blobby blobby
    blobby", until finally when the prank was revealed, the Blobby
    costume would be opened - revealing Noel inside. This was all the more
    surprising for the "victim" as during rehearsals Blobby would be
    played by an actor wearing only the arms and legs of the costume and
    speaking in a normal manner.[citation needed]"""
    
    #see if we can get a LancasterStemmer goijng here...

    sentences = nltk.sent_tokenize(text)
    words = []
    for s in sentences:
        words.extend(nltk.word_tokenize(s))
##    print 'word tokenization complete'
    taggedWords = nltk.pos_tag(words)
##    print 'tagging complete'
    nouns, adjectives, verbs = [], [], [] # list of dictionaries. Keys are words and 
                                          # values are each a list of their occurence (index) in the text
    words = {}  # keys are words and values are lists of their every occurence (index) in the text
    for word, tag in taggedWords:
        if tag[0] == "N":
            d = {}
            d[word] = occurences(text, word, 0, [])
            nouns.append(d)
        elif "JJ" in tag:
            d = {}
            d[word] = occurences(text, word, 0, [])
            adjectives.append(d)
        elif "VB" in tag:
            d = {}
            d[word] = occurences(text, word, 0, [])
            verbs.append(d)

##    print "NAV separation complete"
            
    makeTree(text, nouns, adjectives, verbs)

def occurences(text, word, lastIndex, answer):
##    print 'entering occurences'
    while len(text) != 0:
        try:
##            print "trying"
            i = text.index(word)
            answer.append(lastIndex+i)
            return occurences(text[i+1 :], word, lastIndex+i, answer)
##            print "adding to occurences"
        except ValueError:
##            print "catching"
            return answer
    return answer

def makeTree(text, nouns, adjectives, verbs):
##    print 'entering makeTree'
    nkeys, akeys, vkeys = [], [], []
    nPos = 0
    for n in nouns:
        nkeys.extend(n.keys())
        
    for a in adjectives:
        akeys.extend(a.keys())
        
    for v in verbs:
        vkeys.extend(v.keys())
        
    for noun in nkeys:
        print noun
###        f.write(noun + '\n')
        
        vPos = 0
        for verb in vkeys:
#            print "nouns[nPos][noun]:", nouns[nPos][noun]
            if nvAreClose(noun, nouns[nPos][noun], verb, verbs[vPos][verb]):
                print '\t', verb
###                f.write('\t' + verb)
            vPos += 1
            
            aPos = 0
            for adj in akeys:
                if naAreClose(noun, nouns[nPos][noun], adj, adjectives[aPos][adj]):
                    print '\t\t', adj
###                    f.write('\t\t' + verb)
                aPos += 1
        nPos += 1
###    f.close()
                    
def nvAreClose(noun, nouns, verb, verbs):
#    print 'entering nvAreClose'
    for nPos in nouns:
#        print "nPos:", nPos
        for vPos in verbs:
            if -5 <= nPos-vPos <= 5:
                return True
    return False

def naAreClose(noun, nouns, adj, adjectives):
#    print 'entering naAreClose'
    for nPos in nouns:
        for aPos in adjectives:
            if -5 <= nPos-aPos <= 5:
                return True
    return False
    

if __name__ == '__main__':
    main()
    print 'done!'