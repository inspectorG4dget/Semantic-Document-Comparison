import re
from nltk.corpus import wordnet as wn
import TreeMaker3 as tm

# start of code from http://marvellouz.pastebin.com/XrwTMrj5
SINGULARS= [
    (r's$', ''),
    (r'(n)ews$', '\1ews'),
    (r'([ti])a$', '\1um'),
    (r'((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$', '\1\2sis'),
    (r'(^analy)ses$', '\1sis'),
    (r'([^f])ves$', '\1fe'),
    (r'(hive)s$', '\1'),
    (r'(tive)s$', '\1'),
    (r'([lr])ves$', '\1f'),
    (r'([^aeiouy]|qu)ies$', '\1y'),
    (r'(s)eries$', '\1eries'),
    (r'(m)ovies$', '\1ovie'),
    (r'(x|ch|ss|sh)es$', '\1'),
    (r'([m|l])ice$', '\1ouse'),
    (r'(bus)es$', '\1'),
    (r'(o)es$', '\1'),
    (r'(shoe)s$', '\1'),
    (r'(cris|ax|test)es$', '\1is'),
    (r'(octop|vir)i$', '\1us'),
    (r'(alias|status)es$', '\1'),
    (r'^(ox)en', '\1'),
    (r'(vert|ind)ices$', '\1ex'),
    (r'(matr)ices$', '\1ix'),
    (r'(quiz)zes$', '\1'),
    ]
 
def singularize(word):
    for pattern,replacement in SINGULARS:
      word, n =  re.subn(pattern, replacement, word)
      if n>0:
        break
    return word

# end of code from http://marvellouz.pastebin.com/XrwTMrj5

def senseRange(word, pos):
    '''Given an english word and its POS tag (as required for wordnet), return the number of senses that it has.'''
    sense = 0
    while True:
        try:
            wn.synset("%s.%s.%02d" %(word, pos, sense))
        except nltk.corpus.reader.wordnet.WordNetError:
            return sense
        else:
            sense += 1
            
