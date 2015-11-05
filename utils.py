import itertools
import nltk
import os
import re
from twokenize import tokenize

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def is_url(s):
    return s.startswith('http://') or s.startswith('https://') or s.startswith('ftp://') \
            or s.startswith('ftps://') or s.startswith('smb://')

def clean_str(string, TREC=False):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Every dataset is lower cased except for TREC
    """
    string = re.sub(r"\'m", " \'m", string) 
    string = re.sub(r"\'s", " \'s", string) 
    string = re.sub(r"\'ve", " \'ve", string) 
    string = re.sub(r"n\'t", " n\'t", string) 
    string = re.sub(r"\'re", " \'re", string) 
    string = re.sub(r"\'d", " \'d", string) 
    string = re.sub(r"\'ll", " \'ll", string) 
    string = re.sub(r"`", " ` ", string)
    string = re.sub(r",", " , ", string) 
    return string.strip() 

def process_token(c):
    """
    Use NLTK to replace named entities with generic tags.
    Also replace URLs, numbers, and paths.
    """
    nodelist = ['PERSON', 'ORGANIZATION', 'GPE', 'LOCATION', 'FACILITY', 'GSP']
    if hasattr(c, 'label'):
        if c.label() in nodelist:
            return "__%s__" % c.label()
    word = c[0]
    if is_url(word):
        return "__URL__"
    elif is_number(word):
        return "__NUMBER__"
    elif os.path.isabs(word):
        return "__PATH__"
    return word

def process_line(s, clean_string=True):
    """
    Processes a line by iteratively calling process_token.
    """
    if clean_string:
        s = clean_str(s)
    tokens = tokenize(s)
    sent = nltk.pos_tag(tokens)
    chunks = nltk.ne_chunk(sent, binary=False)
    return [process_token(c).lower().encode('UTF-8') for c in chunks]

def test():
    s='''
    hi, please some1 can help me with my driver in ubuntu :( its a intel GM965 i tried compiz, but give me the error, Checking for Xgl: not present. Blacklisted PCIID '8086:2a02' found aborting and using fallback: /usr/bin/metacity some1 can help me please :( what kind of video card are you running? if you're not sure exactly, lspci | grep -i vga will tell you nickrud 00:02.0 VGA compatible controller: Intel Corporation Mobile GM965/GL960 Integrated Graphics Controller (rev 03) http://wiki.compiz-fusion.org/Hardware/Blacklist nickrud ty i go try it
    '''

    print process_line(s)

if __name__ == '__main__':
    test()

